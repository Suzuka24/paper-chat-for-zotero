# Privacy

Paper Chat for Zotero runs a Zotero extension and a local Windows bridge. It does not operate a project-owned cloud service.

## Data sent for model processing

When you send a message, the plugin can provide the following to OpenAI through the official Codex App Server:

- your question and the conversation history managed by Codex;
- text extracted from the current local PDF;
- selected PDF text, annotations, and Zotero notes you explicitly add as context;
- local files you explicitly attach.

This processing is governed by the policies and controls of the ChatGPT/Codex account or workspace used to sign in.

## Local storage

- Zotero conversation metadata: `<Zotero data directory>/zotero-codex-chat/conversations.json`.
- Clipboard-created temporary attachments: `<Zotero data directory>/zotero-codex-chat/clipboard-files/`.
- Codex project working directory: `<Zotero data directory>/Paper Chat for Zotero/`.
- Bridge program, log, App Server binary, and local token: `%LOCALAPPDATA%\PaperChatForZotero\`.
- Plugin preferences: the current Zotero profile under the legacy-compatible prefix `extensions.zotero-codex-chat.*`.

The local bridge token is not an OpenAI credential. It is a random per-installation secret used only to reject unauthorized requests to the loopback bridge.

## Deletion

Removing the plugin and running `Uninstall-Bridge.ps1` deletes the bridge installation, log, App Server binary, and bridge token. It does not delete Zotero notes, Zotero items, conversation metadata, clipboard cache, or Codex task history. Delete those separately if required.

## Network scope

The bridge listens only on `127.0.0.1:23120`. Model requests are made by the official Codex App Server to OpenAI. The installer downloads the pinned App Server from the official `openai/codex` GitHub release and verifies its published SHA-256 digest.
