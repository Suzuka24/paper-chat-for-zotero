# Changelog

All notable changes to this project are documented here.

## [0.6.3] - 2026-08-26

### Fixed

- Preserved LaTeX norm delimiters and other inline pipes when parsing Markdown table cells.
- Preserved explicit ordered-list numbering when explanatory paragraphs split a list into separate HTML blocks.

## [0.6.2] - 2026-08-25

### Fixed

- Prevented the **Back up note** and **Attach** button borders from being clipped in the macOS Zotero compose toolbar.

## [0.6.1] - 2026-08-25

### Changed

- Paper conversations are archived in Codex after each completed response, keeping them out of the default **Recent** list while preserving resumable context.
- Existing plugin-managed Codex threads are archived once during upgrade after an automatic local conversation-history backup.
- Deleting a Zotero conversation now also deletes its corresponding Codex thread after confirmation; a bridge failure leaves the Zotero conversation untouched.

### Fixed

- New plugin threads now use the non-interactive App Server source instead of being identified as VS Code tasks.

## [0.6.0] - 2026-08-25

### Added

- Native macOS installation for Apple Silicon and Intel Macs using SHA-256-verified official Codex App Server builds.
- User-level `launchd` startup, macOS bridge control scripts, and automatic token discovery in Zotero.
- Cross-platform build, validation, release metadata tooling, and macOS CI coverage.

### Changed

- Shared package validation now runs from Python while retaining Windows PowerShell syntax checks.
- Installation, privacy, support, and contribution documentation now covers Windows and macOS.

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
