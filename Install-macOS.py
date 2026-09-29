#!/usr/bin/env python3
"""Install the Paper Chat bridge for the current macOS user."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import platform
import secrets
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path


DEFAULT_CODEX_VERSION = "rust-v0.157.1"
LAUNCH_LABEL = "io.github.suzuka24.paper-chat-for-zotero-bridge"


def require_macos() -> None:
    if sys.platform != "darwin":
        raise SystemExit("Install-macOS.py can only run on macOS.")


def find_python_runtime() -> Path:
    candidates = [sys.executable]
    candidates.extend(
        executable
        for name in ("python3.13", "python3.12", "python3.11", "python3.10", "python3")
        if (executable := shutil.which(name))
    )
    for candidate in dict.fromkeys(candidates):
        result = subprocess.run(
            [candidate, "-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return Path(candidate).resolve()
    raise SystemExit("Python 3.10 or newer is required. Install it and rerun this installer.")


def stop_existing_bridge(launch_agent: Path, installed_stop: Path) -> None:
    if installed_stop.is_file():
        subprocess.run([str(installed_stop)], check=False)
        return
    subprocess.run(
        ["launchctl", "bootout", f"gui/{os.getuid()}", str(launch_agent)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def copy_bridge(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("server.py", "requirements.txt", "Start-Bridge.sh", "Stop-Bridge.sh"):
        shutil.copy2(source / name, destination / name)
    vendor_destination = destination / "vendor"
    if vendor_destination.exists():
        shutil.rmtree(vendor_destination)
    shutil.copytree(source / "vendor", vendor_destination)
    for name in ("Start-Bridge.sh", "Stop-Bridge.sh"):
        (destination / name).chmod(0o755)


def ensure_token(token_file: Path) -> None:
    token = ""
    if token_file.is_file():
        token = token_file.read_text(encoding="utf-8").strip()
    if len(token) != 64 or any(character not in "0123456789abcdefABCDEF" for character in token):
        token = secrets.token_hex(32)
        token_file.write_text(token, encoding="utf-8")
    token_file.chmod(0o600)


def codex_target() -> str:
    machine = platform.machine().lower()
    if machine in {"arm64", "aarch64"}:
        architecture = "aarch64"
    elif machine in {"x86_64", "amd64"}:
        architecture = "x86_64"
    else:
        raise RuntimeError(f"Unsupported macOS architecture: {machine}")
    return f"{architecture}-apple-darwin"


def component_asset_name(component: str) -> str:
    return f"{component}-{codex_target()}.tar.gz"


def release_asset(version: str, asset_name: str) -> tuple[str, str]:
    request = urllib.request.Request(
        f"https://api.github.com/repos/openai/codex/releases/tags/{version}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Paper-Chat-for-Zotero-Installer",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        release = json.load(response)
    asset = next((item for item in release.get("assets", []) if item.get("name") == asset_name), None)
    if not asset:
        raise RuntimeError(f"Asset not found in the OpenAI release: {asset_name}")
    digest = str(asset.get("digest", ""))
    if not digest.startswith("sha256:") or len(digest) != 71:
        raise RuntimeError("The official release did not provide a valid SHA-256 digest.")
    return str(asset["browser_download_url"]), digest.removeprefix("sha256:").lower()


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Paper-Chat-for-Zotero-Installer"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def install_codex_component(version: str, component: str, destination: Path) -> None:
    asset_name = component_asset_name(component)
    url, expected_hash = release_asset(version, asset_name)
    print(f"Downloading {component} {version} ({asset_name})...")
    with tempfile.TemporaryDirectory(prefix="paper-chat-codex-") as temporary_directory:
        archive_path = Path(temporary_directory) / asset_name
        download(url, archive_path)
        actual_hash = sha256(archive_path)
        if actual_hash != expected_hash:
            raise RuntimeError("Codex App Server SHA-256 verification failed.")
        with tarfile.open(archive_path, "r:gz") as archive:
            members = [
                member
                for member in archive.getmembers()
                if member.isfile() and Path(member.name).name.startswith(component)
            ]
            if len(members) != 1:
                raise RuntimeError(f"The {component} archive has an unexpected layout.")
            extracted = archive.extractfile(members[0])
            if extracted is None:
                raise RuntimeError(f"Unable to extract the {component} binary.")
            temporary_binary = Path(temporary_directory) / component
            with temporary_binary.open("wb") as output:
                shutil.copyfileobj(extracted, output)
            temporary_binary.chmod(0o755)
            os.replace(temporary_binary, destination)
    print(f"Installed {component} {version}.")


def component_matches_version(destination: Path, version: str) -> bool:
    if not destination.is_file():
        return False
    try:
        result = subprocess.run(
            [str(destination), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    expected = version.removeprefix("rust-v")
    output = f"{result.stdout}\n{result.stderr}"
    return result.returncode == 0 and expected in output.split()


def write_launch_agent(
    launch_agent: Path,
    python_binary: Path,
    install_root: Path,
) -> None:
    launch_agent.parent.mkdir(parents=True, exist_ok=True)
    arguments = [
        str(python_binary),
        str(install_root / "server.py"),
        "--codex-app-server",
        str(install_root / "codex-app-server"),
        "--token-file",
        str(install_root / "token.txt"),
        "--log-file",
        str(install_root / "bridge.log"),
    ]
    configuration = {
        "Label": LAUNCH_LABEL,
        "ProgramArguments": arguments,
        "WorkingDirectory": str(install_root),
        "RunAtLoad": True,
        "KeepAlive": True,
        "ThrottleInterval": 10,
        "StandardOutPath": "/dev/null",
        "StandardErrorPath": "/dev/null",
    }
    with launch_agent.open("wb") as output:
        plistlib.dump(configuration, output, sort_keys=False)
    launch_agent.chmod(0o600)


def build_xpi(project_root: Path, python_binary: Path) -> Path:
    output = project_root / "dist" / "paper-chat-for-zotero.xpi"
    subprocess.run(
        [
            str(python_binary),
            str(project_root / "scripts" / "build_xpi.py"),
            str(project_root / "plugin"),
            str(output),
        ],
        check=True,
    )
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-auto-start", action="store_true")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--codex-version", default=DEFAULT_CODEX_VERSION)
    return parser.parse_args()


def main() -> int:
    require_macos()
    args = parse_args()
    python_binary = find_python_runtime()
    project_root = Path(__file__).resolve().parent
    install_root = Path.home() / "Library" / "Application Support" / "PaperChatForZotero"
    launch_agent = Path.home() / "Library" / "LaunchAgents" / f"{LAUNCH_LABEL}.plist"
    app_server = install_root / "codex-app-server"
    code_mode_host = install_root / "codex-code-mode-host"

    stop_existing_bridge(launch_agent, install_root / "Stop-Bridge.sh")
    copy_bridge(project_root / "bridge", install_root)
    (install_root / "python-bin.txt").write_text(str(python_binary), encoding="utf-8")
    (install_root / "python-bin.txt").chmod(0o600)
    ensure_token(install_root / "token.txt")

    if not component_matches_version(app_server, args.codex_version):
        if args.skip_download:
            raise RuntimeError("The installed Codex App Server does not match --codex-version; --skip-download cannot be used.")
        install_codex_component(args.codex_version, "codex-app-server", app_server)
    if not code_mode_host.is_file():
        if args.skip_download:
            raise RuntimeError("Codex Code Mode Host is not installed; --skip-download cannot be used.")
        install_codex_component(args.codex_version, "codex-code-mode-host", code_mode_host)
    for executable in (app_server, code_mode_host):
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    if args.no_auto_start:
        launch_agent.unlink(missing_ok=True)
    else:
        write_launch_agent(launch_agent, python_binary, install_root)

    xpi_path = build_xpi(project_root, python_binary)
    subprocess.run([str(install_root / "Start-Bridge.sh")], check=True)
    print("\nInstallation preparation is complete.")
    print(f"In Zotero, open Tools -> Plugins and install this file: {xpi_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
