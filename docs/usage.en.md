# Usage guide

## Start a paper conversation

1. Open a locally available PDF in Zotero.
2. Select the Paper Chat icon in the right-side navigation.
3. Choose a model and reasoning effort, then enter a question.
4. Use **New conversation** to start an independent thread for the current paper. Conversations can be switched, renamed, or deleted from the second row.

The current PDF is parsed locally and supplied to Codex when a conversation starts. A scanned PDF without a text layer may require OCR first.

After each completed response, the corresponding Codex task is archived so it does not remain in Codex **Recent**. Continuing the conversation in Zotero automatically restores its context and archives it again afterward. Deleting a Zotero conversation also permanently deletes the corresponding Codex thread after confirmation.

## Add context

- Select text in the PDF and choose **Ask Codex**.
- Use an annotation's context menu to add a highlight, region, or ink annotation.
- Select one or more item notes from **Add item notes as context**; use **Refresh** after notes change.
- Choose **Attach** for local files.
- Paste clipboard images, PDFs, Office documents, text files, or files copied in Windows Explorer or macOS Finder directly into the input box.

Only items explicitly selected or attached are added beyond the current paper.

## Work with responses

- Markdown, tables, code blocks, inline math, and display math are rendered in the sidebar.
- Page references such as “page 3” can be selected to navigate to the physical PDF page.
- The icons below a message copy that message or save it to the selected Zotero note.
- **Back up note** saves the complete conversation to a new or selected item note.
- Drag the handle above the input area to resize the conversation history.

## Preferences

Open `Edit → Settings → Paper Chat for Zotero` to configure the default answer language, response style, interface font size, persistent general prompt, and web-search mode. **Live web search** is the default and can retrieve sources beyond the current paper. **Cached search index only** avoids live page retrieval, while **Disable web search** removes the search tool. Changes apply from the next question, and local files remain read-only in every mode.

## Authentication and bridge

The plugin starts a separate official Codex App Server through a local bridge. It reuses a valid Codex sign-in for the current OS user; the Codex desktop app does not need to stay open. If the account or model list is unavailable, sign in again through the official Codex app or run `codex login`.

For bridge controls, upgrades, logs, and troubleshooting, see the [installation guide](installation.en.md).
