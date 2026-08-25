# Changelog

All notable changes to this project are documented here.

## [0.5.0] - 2026-08-25

First public beta under the name **Paper Chat for Zotero**.

### Added

- Native Zotero 9 sidebar paper chat powered by the official Codex App Server.
- Current PDF, selections, annotations, item notes, local files, and clipboard files as context.
- Persistent per-paper conversations, model and reasoning controls, streaming, stop, rename, and delete.
- Markdown, KaTeX math, tables, code blocks, clickable page references, and resizable chat area.
- Copy and save-to-note actions for individual messages and complete conversations.
- Chinese and English UI following the Zotero locale.
- Reproducible XPI builds, CI checks, release automation, and Zotero update metadata.

### Security

- Removed the development bridge token from source and packages.
- Added a random per-installation bridge token loaded from the local bridge directory.
- Pinned and SHA-256-verified the downloaded official Codex App Server.

### Changed

- Permanent public plugin ID: `paper-chat-for-zotero@suzuka24.github.io`.
- Public package name: `paper-chat-for-zotero.xpi`.
- Bridge install directory: `%LOCALAPPDATA%\PaperChatForZotero`.

### Upgrade note

The public plugin ID differs from `0.4.x` development builds. Remove the development plugin once before installing `0.5.0`; legacy preferences and conversation storage remain readable.
