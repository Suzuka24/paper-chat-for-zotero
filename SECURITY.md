# Security policy

## Supported versions

Security fixes are provided for the latest public release.

## Reporting a vulnerability

Do not open a public issue for a vulnerability that could expose account data, local files, or bridge access. Contact the maintainer through GitHub's private vulnerability reporting feature for this repository. If private reporting is unavailable, open a minimal issue requesting a private contact channel without including exploit details.

Include the affected version, Zotero version, operating system, impact, reproduction outline, and any suggested mitigation. Do not include Codex authentication files, bridge tokens, paper contents, or personal Zotero data.

## Design boundaries

- The bridge binds to loopback and rejects requests without a per-installation token.
- Codex turns run with `approvalPolicy: never` and a read-only sandbox.
- Interactive App Server tool requests are rejected.
- The installer downloads a pinned official App Server release and requires SHA-256 verification.

These controls reduce risk but do not make untrusted attachments or prompts harmless. Review sensitive papers and workspace policies before sending content for model processing.
