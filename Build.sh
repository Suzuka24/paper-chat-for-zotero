#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON:-python3}

"$python_bin" "$project_root/scripts/build_xpi.py" \
    "$project_root/plugin" \
    "$project_root/dist/paper-chat-for-zotero.xpi"

printf 'Built: %s\n' "$project_root/dist/paper-chat-for-zotero.xpi"
