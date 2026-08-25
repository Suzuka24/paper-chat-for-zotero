#!/usr/bin/env python3
"""Build a reproducible Zotero XPI from the plugin source tree."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_xpi.py PLUGIN_ROOT OUTPUT_XPI")
    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_STORED)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
