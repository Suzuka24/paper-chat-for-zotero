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
    main_script = (PROJECT_ROOT / "plugin" / "content" / "main.js").read_text(encoding="utf-8")
    if not re.search(r"sidenav:\s*\{[^}]*orderable:\s*false", main_script, re.DOTALL):
        raise RuntimeError("The Paper Chat sidenav button must remain fixed after orderable panes.")
    if "applyItemPaneOrder" in main_script or "movePaperChatSectionLast" in main_script:
        raise RuntimeError("Paper Chat must not patch Zotero's global item-pane ordering.")
    if not re.search(r"\.zcc-panel\{[^}]*border:0;[^}]*border-radius:0", main_script):
        raise RuntimeError("Paper Chat must use the native frameless item-pane layout.")
    if not re.search(r"\.zcc-actions\{[^}]*flex-wrap:nowrap", main_script):
        raise RuntimeError("Paper Chat action controls must remain on one row in narrow panes.")
    if not re.search(r'registerObserver\(PREF_PREFIX \+ "fontSize",[^;]+, true\)', main_script):
        raise RuntimeError("The Paper Chat font-size preference must be observed by open panels.")
    if 'webSearchMode: pref("webSearchMode", "live")' not in main_script:
        raise RuntimeError("The selected web-search mode must be sent to the local bridge.")

    for script in ("plugin/content/main.js", "plugin/content/preferences.js"):
        run("node", "--check", script)

    run("node", str(PROJECT_ROOT / "scripts" / "test_markdown_renderer.js"))

    for script in (
        "bridge/server.py",
        "scripts/build_xpi.py",
        "scripts/test.py",
        "scripts/test_bridge_lifecycle.py",
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

    run(sys.executable, str(PROJECT_ROOT / "scripts" / "test_bridge_lifecycle.py"))

    manifest = json.loads((PROJECT_ROOT / "plugin" / "manifest.json").read_text(encoding="utf-8"))
    updates = json.loads((PROJECT_ROOT / "updates.json").read_text(encoding="utf-8"))
    ET.parse(PROJECT_ROOT / "plugin" / "content" / "preferences.xhtml")

    zotero_compatibility = manifest["applications"]["zotero"]
    if zotero_compatibility["strict_min_version"] != "9.0.0":
        raise RuntimeError("The plugin must retain Zotero 9 compatibility.")
    if zotero_compatibility["strict_max_version"] != "10.0.*":
        raise RuntimeError("The plugin must declare Zotero 10.0.x compatibility.")

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
        forbidden = re.compile(r"(^|/)(token\.txt|bridge\.log|bridge\.pid|codex-(?:app-server|code-mode-host)(?:\.exe)?)$")
        leaked = sorted(entry for entry in entries if forbidden.search(entry))
        if leaked:
            raise RuntimeError(f"The XPI contains forbidden local files: {', '.join(leaked)}")

    plugin_id = manifest["applications"]["zotero"]["id"]
    update = updates["addons"][plugin_id]["updates"][0]
    if update["version"] != manifest["version"]:
        raise RuntimeError("updates.json version does not match manifest.json.")
    built_hash = f"sha256:{second_hash}"
    if update["update_hash"] != built_hash:
        raise RuntimeError(
            f"updates.json hash {update['update_hash']} does not match the XPI {built_hash}."
        )

    print(f"All checks passed for {plugin_id} {manifest['version']}.")
    print(f"SHA-256: {second_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
