# Contributing

Issues and pull requests are welcome.

## Development setup

Requirements: Windows 10/11 or macOS, Zotero 9.0.x or 10.0.x, Python 3.10+, Node.js, and a valid local Codex sign-in.

1. Fork and clone the repository.
2. Run `Install.ps1` on Windows or `python3 Install-macOS.py` on macOS to install the local bridge and build a development XPI.
3. Install `dist/paper-chat-for-zotero.xpi` in a test Zotero profile.
4. Keep changes focused and avoid committing local tokens, logs, binaries, paper files, or Zotero profile data.

## Checks

Run before opening a pull request:

```powershell
.\scripts\Test.ps1
```

On macOS or another POSIX development environment:

```bash
python3 scripts/test.py
```

The checks cover JavaScript, Python, JSON/XML, platform scripts, reproducible packaging, required XPI contents, and update metadata. The Windows wrapper additionally validates PowerShell syntax.

## Pull requests

- Explain the user-visible behavior and testing performed.
- Include screenshots for UI changes.
- Add an entry under `Unreleased` in `CHANGELOG.md` for user-facing changes.
- Do not change the permanent plugin ID.
- Avoid new runtime dependencies unless they are necessary and their licenses are documented.
