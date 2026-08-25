# Installation, upgrades, and troubleshooting

## Prerequisites

1. Install Zotero 9.0.x and Python 3.10+ on Windows 10/11 or macOS.
2. Sign in to the official Codex desktop app under the same OS account, or sign in with the Codex CLI using `codex login`.
3. Make sure the ChatGPT account or workspace is eligible to use Codex. The plugin does not grant access and does not use an API key.

The Codex app does not need to remain open. A previous sign-in must still be valid; sign out, credential expiry, or workspace policy changes can require signing in again.

## Install

Extract the Release source archive and run the installer for your platform.

### Windows

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install.ps1
```

### macOS

```bash
python3 Install-macOS.py
```

The installer downloads a pinned OpenAI Codex App Server release, requires its published SHA-256 digest to match, installs the bridge under `%LOCALAPPDATA%\PaperChatForZotero` on Windows or `~/Library/Application Support/PaperChatForZotero` on macOS, creates a per-installation token, configures login startup, and builds `dist/paper-chat-for-zotero.xpi`.

In Zotero, choose `Tools → Plugins → gear menu → Install Plugin From File`, select the XPI, and fully restart Zotero. Use `Install.ps1 -NoAutoStart` on Windows or `python3 Install-macOS.py --no-auto-start` on macOS to skip login startup.

## Upgrade

Close Zotero, rerun the installer for your platform, install the newly built XPI over the existing public version, and restart Zotero. When moving from a `0.4.x` development build to `0.5.0` or newer, remove the old development plugin first because the permanent public plugin ID changed.

On first bridge connection after upgrading to `0.6.1`, existing plugin-managed Codex tasks are archived so they no longer occupy Codex **Recent**. Zotero messages and resumable context are retained. If the local history contains Codex thread IDs, it is first backed up once as `<Zotero data directory>/zotero-codex-chat/conversations.pre-thread-lifecycle-v1.json`.

## Bridge controls

```powershell
& "$env:LOCALAPPDATA\PaperChatForZotero\Start-Bridge.ps1"
& "$env:LOCALAPPDATA\PaperChatForZotero\Stop-Bridge.ps1"
& "$env:LOCALAPPDATA\PaperChatForZotero\Start-Bridge.ps1" -Foreground
```

Diagnostics are written to `%LOCALAPPDATA%\PaperChatForZotero\bridge.log`.

On macOS:

```bash
"$HOME/Library/Application Support/PaperChatForZotero/Start-Bridge.sh"
"$HOME/Library/Application Support/PaperChatForZotero/Stop-Bridge.sh"
"$HOME/Library/Application Support/PaperChatForZotero/Start-Bridge.sh" --foreground
```

Diagnostics are written to `~/Library/Application Support/PaperChatForZotero/bridge.log`.

## Troubleshooting

- Not connected: start the bridge, inspect the log, and rerun the platform installer if the local token is out of sync.
- Empty account or model list: sign in again through the official Codex app or `codex login`.
- Missing paper content: make sure the PDF is local and has a text layer; OCR scanned documents first.
- Missing sidebar section: verify Zotero 9.0.x, enable the plugin, and fully restart Zotero.

See [SUPPORT.md](../SUPPORT.md) when filing a bug.

## Uninstall

After removing the plugin from Zotero, run `Uninstall-Bridge.ps1` on Windows or `./Uninstall-Bridge.sh` on macOS. This does not delete Zotero items, notes, or saved conversation metadata.
