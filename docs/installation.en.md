# Installation, upgrades, and troubleshooting

## Prerequisites

1. Install Zotero 9.0.x and Python 3.10+; verify `python --version` in PowerShell.
2. Sign in to the official Codex desktop app under the same Windows account, or sign in with the Codex CLI using `codex login`.
3. Make sure the ChatGPT account or workspace is eligible to use Codex. The plugin does not grant access and does not use an API key.

The Codex app does not need to remain open. A previous sign-in must still be valid; sign out, credential expiry, or workspace policy changes can require signing in again.

## Install

Extract the Release source archive and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install.ps1
```

The installer downloads a pinned OpenAI Codex App Server release, requires its published SHA-256 digest to match, installs the bridge under `%LOCALAPPDATA%\PaperChatForZotero`, creates a per-installation token and builds `dist\paper-chat-for-zotero.xpi`.

In Zotero, choose `Tools → Plugins → gear menu → Install Plugin From File`, select the XPI, and fully restart Zotero. Use `Install.ps1 -NoAutoStart` to skip the login startup shortcut.

## Upgrade

Close Zotero, run the new `Install.ps1`, install the newly built XPI over the existing public version, and restart Zotero. When moving from a `0.4.x` development build to `0.5.0`, remove the old development plugin first because the permanent public plugin ID changed.

## Bridge controls

```powershell
& "$env:LOCALAPPDATA\PaperChatForZotero\Start-Bridge.ps1"
& "$env:LOCALAPPDATA\PaperChatForZotero\Stop-Bridge.ps1"
& "$env:LOCALAPPDATA\PaperChatForZotero\Start-Bridge.ps1" -Foreground
```

Diagnostics are written to `%LOCALAPPDATA%\PaperChatForZotero\bridge.log`.

## Troubleshooting

- Not connected: start the bridge, inspect the log, and rerun `Install.ps1` if the local token is out of sync.
- Empty account or model list: sign in again through the official Codex app or `codex login`.
- Missing paper content: make sure the PDF is local and has a text layer; OCR scanned documents first.
- Missing sidebar section: verify Zotero 9.0.x, enable the plugin, and fully restart Zotero.

See [SUPPORT.md](../SUPPORT.md) when filing a bug.
