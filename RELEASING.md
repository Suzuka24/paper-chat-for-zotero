# Release process

This document is for maintainers.

1. Update `plugin/manifest.json` and `CHANGELOG.md` with the release version.
2. Run `scripts/Test.ps1` twice and confirm the XPI SHA-256 is identical.
3. Run `scripts/Update-Manifest.ps1`; it rebuilds the XPI and writes its hash to `updates.json`.
4. Review `git diff`, commit the release, and push `main`.
5. Create and push an annotated tag matching the manifest version, for example `v0.5.0`.
6. The `release.yml` workflow rebuilds the deterministic XPI, verifies `updates.json`, and creates a GitHub Release with the XPI and checksum file.
7. Mark early public versions as pre-release in GitHub if additional testing is still needed.

Never release a package containing `token.txt`, `bridge.log`, `codex-app-server.exe`, Codex authentication data, or local paper/conversation files.
