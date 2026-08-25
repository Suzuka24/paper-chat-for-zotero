# Release process

This document is for maintainers.

1. Update `plugin/manifest.json` and `CHANGELOG.md` with the release version.
2. Run `scripts/Test.ps1` on Windows or `python3 scripts/test.py` on macOS and confirm the checks pass.
3. Run `scripts/Update-Manifest.ps1` or `python3 scripts/update_manifest.py`; it rebuilds the XPI and writes its hash to `updates.json`.
4. Review `git diff`, commit the release, and push `main`.
5. Create and push an annotated tag matching the manifest version, for example `v0.5.0`.
6. The `release.yml` workflow rebuilds the deterministic XPI, verifies `updates.json`, and creates a GitHub Release with the XPI and checksum file.
7. Mark early public versions as pre-release in GitHub if additional testing is still needed.

Never release a package containing `token.txt`, `bridge.log`, `bridge.pid`, a Codex App Server binary, Codex authentication data, or local paper/conversation files.
