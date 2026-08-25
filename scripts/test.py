#!/usr/bin/env python3
"""Run platform-neutral validation and reproducible packaging checks."""

from __future__ import annotations

import hashlib
import json
import os
import py_compile
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
XPI_PATH = PROJECT_ROOT / "dist" / "paper-chat-for-zotero.xpi"


def run(*arguments: str) -> None:
    subprocess.run(arguments, cwd=PROJECT_ROOT, check=True)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build() -> str:
    run(
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "build_xpi.py"),
        str(PROJECT_ROOT / "plugin"),
        str(XPI_PATH),
    )
    return file_hash(XPI_PATH)


def main() -> int:
    for script in ("plugin/content/main.js", "plugin/content/preferences.js"):
        run("node", "--check", script)

    for script in (
        "bridge/server.py",
        "scripts/build_xpi.py",
        "scripts/test.py",
        "Install-macOS.py",
    ):
        py_compile.compile(str(PROJECT_ROOT / script), doraise=True)

    if os.name != "nt":
        for script in (
            "Build.sh",
            "Uninstall-Bridge.sh",
            "bridge/Start-Bridge.sh",
            "bridge/Stop-Bridge.sh",
        ):
            run("sh", "-n", script)

    manifest = json.loads((PROJECT_ROOT / "plugin" / "manifest.json").read_text(encoding="utf-8"))
    updates = json.loads((PROJECT_ROOT / "updates.json").read_text(encoding="utf-8"))
    ET.parse(PROJECT_ROOT / "plugin" / "content" / "preferences.xhtml")

    first_hash = build()
    second_hash = build()
    if first_hash != second_hash:
        raise RuntimeError("The XPI build is not reproducible.")

    with zipfile.ZipFile(XPI_PATH) as archive:
        entries = set(archive.namelist())
        required = {"manifest.json", "bootstrap.js", "prefs.js", "content/main.js", "content/codex.svg"}
        missing = sorted(required - entries)
        if missing:
            raise RuntimeError(f"The XPI is missing: {', '.join(missing)}")
        forbidden = re.compile(r"(^|/)(token\.txt|bridge\.log|bridge\.pid|codex-app-server(?:\.exe)?)$")
        leaked = sorted(entry for entry in entries if forbidden.search(entry))
        if leaked:
            raise RuntimeError(f"The XPI contains forbidden local files: {', '.join(leaked)}")

    plugin_id = manifest["applications"]["zotero"]["id"]
    update = updates["addons"][plugin_id]["updates"][0]
    if update["version"] != manifest["version"]:
        raise RuntimeError("updates.json version does not match manifest.json.")
    if update["update_hash"] != f"sha256:{second_hash}":
        raise RuntimeError("updates.json hash does not match the XPI.")

    print(f"All checks passed for {plugin_id} {manifest['version']}.")
    print(f"SHA-256: {second_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
