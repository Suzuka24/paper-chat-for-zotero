# Paper Chat for Zotero

[中文](README.md) · [Installation](docs/installation.en.md) · [Privacy](PRIVACY.md) · [Changelog](CHANGELOG.md)

Chat with the paper currently open in Zotero, directly from the native right sidebar. The plugin reuses your local Codex sign-in; it does not require an OpenAI API key or API credit balance.

> This is an independent project and is not affiliated with or endorsed by OpenAI or Zotero. It does not grant Codex access or bypass subscription limits. Usage remains subject to your ChatGPT/Codex plan, workspace policy, and model availability.

## Requirements

- Windows 10/11, Zotero 9.0.x, and Python 3.10+.
- You have signed in to the official Codex desktop app or Codex CLI under the same Windows account, and that sign-in is still valid.
- The Codex app does not need to remain open. The plugin starts a separate official Codex App Server and reuses its local authentication state.
- If you have never signed in, signed out, or the credentials expired, open Codex and sign in once, or run `codex login` in the Codex CLI.

## Highlights

- Native Zotero sidebar UI with automatic Chinese/English localization.
- Current PDF, selected text, annotations, item notes, and local files as context.
- Clipboard paste for images, PDFs, Office documents, text files, and Explorer-copied files.
- Account-aware model list, reasoning effort, streaming responses, and stop control.
- Multiple persistent conversations per paper.
- Markdown, tables, code, KaTeX math, and clickable PDF page references.
- Copy or save one message or a full conversation to Zotero notes.
- Resizable message area and defensive wrapping for long math, tables, and links.
- Read-only Codex sandbox and a loopback bridge protected by a per-installation token.

## Installation

Download the source or a Release source archive, then run in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install.ps1
```

Install the generated `dist/paper-chat-for-zotero.xpi` from Zotero's `Tools → Plugins → gear menu → Install Plugin From File`, then fully restart Zotero. See the [installation guide](docs/installation.en.md) for upgrades and troubleshooting.

## Authentication model

The plugin does not read or transmit account credentials itself. Its local bridge starts OpenAI's official `codex-app-server`, which owns the existing Codex authentication state for the current Windows user. If that account cannot use Codex, has signed out, or is restricted by an organization policy, the plugin cannot connect either.

## Build

```powershell
.\Build.ps1
```

The reproducible XPI is written to `dist/paper-chat-for-zotero.xpi`. See [CONTRIBUTING.md](CONTRIBUTING.md) and [RELEASING.md](RELEASING.md) for development and release details.

## License

MIT. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for bundled dependencies. OpenAI, ChatGPT, Codex, and Zotero are trademarks of their respective owners.
