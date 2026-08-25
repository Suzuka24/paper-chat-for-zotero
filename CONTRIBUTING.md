# Contributing

Issues and pull requests are welcome.

## Development setup

Requirements: Windows 10/11, Zotero 9.0.x, Python 3.10+, and a valid local Codex sign-in.

1. Fork and clone the repository.
2. Run `Install.ps1` to install the local bridge and build a development XPI.
3. Install `dist/paper-chat-for-zotero.xpi` in a test Zotero profile.
4. Keep changes focused and avoid committing local tokens, logs, binaries, paper files, or Zotero profile data.

## Checks

Run before opening a pull request:

```powershell
.\scripts\Test.ps1
```

The script checks JavaScript, Python, JSON/XML, PowerShell syntax, reproducible packaging, required XPI contents, and update metadata.

## Pull requests

- Explain the user-visible behavior and testing performed.
- Include screenshots for UI changes.
- Add an entry under `Unreleased` in `CHANGELOG.md` for user-facing changes.
- Do not change the permanent plugin ID.
- Avoid new runtime dependencies unless they are necessary and their licenses are documented.
