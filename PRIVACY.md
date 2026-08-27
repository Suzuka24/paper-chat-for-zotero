# Privacy

Paper Chat for Zotero runs a Zotero extension and a local Windows or macOS bridge. It does not operate a project-owned cloud service.

## Data sent for model processing

When you send a message, the plugin can provide the following to OpenAI through the official Codex App Server:

- your question and the conversation history managed by Codex;
- text extracted from the current local PDF;
- selected PDF text, annotations, and Zotero notes you explicitly add as context;
- local files you explicitly attach.

This processing is governed by the policies and controls of the ChatGPT/Codex account or workspace used to sign in.

When **Live web search** is enabled in the plugin preferences, Codex may send search queries derived from your question and conversation context to OpenAI's web-search service and retrieve external pages. Choose **Cached search index only** to avoid live page retrieval, or **Disable web search** to remove the web-search tool from Paper Chat conversations. This setting does not grant write access to local files.

## Local storage

- Zotero conversation metadata: `<Zotero data directory>/zotero-codex-chat/conversations.json`.
- Before the first thread-lifecycle migration, the plugin creates `<Zotero data directory>/zotero-codex-chat/conversations.pre-thread-lifecycle-v1.json` once as a safety backup when existing Codex thread IDs are present.
- Clipboard-created temporary attachments: `<Zotero data directory>/zotero-codex-chat/clipboard-files/`.
- Codex project working directory: `<Zotero data directory>/Paper Chat for Zotero/`.
- Bridge program, log, App Server and Code Mode Host binaries, and local token: `%LOCALAPPDATA%\PaperChatForZotero\` on Windows or `~/Library/Application Support/PaperChatForZotero/` on macOS.
- Plugin preferences: the current Zotero profile under the legacy-compatible prefix `extensions.zotero-codex-chat.*`.

The local bridge token is not an OpenAI credential. It is a random per-installation secret used only to reject unauthorized requests to the loopback bridge.

## Deletion

Completed plugin conversations are archived by the Codex App Server. Archiving removes them from the default Codex **Recent** list but preserves their server-side context so that Zotero can resume them. Deleting a conversation in Zotero, after confirmation, permanently deletes its corresponding Codex thread; if that request fails, the Zotero conversation is kept.

Removing the plugin and running `Uninstall-Bridge.ps1` on Windows or `Uninstall-Bridge.sh` on macOS deletes the bridge installation, log, App Server and Code Mode Host binaries, and bridge token. It does not delete Zotero notes, Zotero items, conversation metadata, clipboard cache, or Codex task history. Delete those separately if required.

## Network scope

The bridge listens only on `127.0.0.1:23120`. Model and enabled web-search requests are made by the official Codex App Server and Code Mode Host to OpenAI. The installer downloads both pinned components from the official `openai/codex` GitHub release and verifies their published SHA-256 digests.
