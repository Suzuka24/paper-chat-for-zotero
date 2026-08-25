#!/usr/bin/env python3
"""Build the XPI and update Zotero release metadata."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent.parent
    manifest = json.loads((project_root / "plugin" / "manifest.json").read_text(encoding="utf-8"))
    xpi_path = project_root / "dist" / "paper-chat-for-zotero.xpi"
    subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "build_xpi.py"),
            str(project_root / "plugin"),
            str(xpi_path),
        ],
        check=True,
    )
    digest = hashlib.sha256(xpi_path.read_bytes()).hexdigest()
    plugin_id = manifest["applications"]["zotero"]["id"]
    version = manifest["version"]
    updates = {
        "addons": {
            plugin_id: {
                "updates": [
                    {
                        "version": version,
                        "update_link": (
                            "https://github.com/Suzuka24/paper-chat-for-zotero/"
                            f"releases/download/v{version}/paper-chat-for-zotero.xpi"
                        ),
                        "update_hash": f"sha256:{digest}",
                        "applications": {
                            "zotero": {
                                "strict_min_version": manifest["applications"]["zotero"]["strict_min_version"],
                                "strict_max_version": manifest["applications"]["zotero"]["strict_max_version"],
                            }
                        },
                    }
                ]
            }
        }
    }
    (project_root / "updates.json").write_text(
        json.dumps(updates, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated updates.json for {plugin_id} {version} ({digest}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
