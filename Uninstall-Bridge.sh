#!/bin/sh
set -eu

install_root="${HOME}/Library/Application Support/PaperChatForZotero"
launch_agent="${HOME}/Library/LaunchAgents/io.github.suzuka24.paper-chat-for-zotero-bridge.plist"

case "$install_root" in
    "${HOME}/Library/Application Support/PaperChatForZotero") ;;
    *)
        printf 'Refusing to remove unexpected path: %s\n' "$install_root" >&2
        exit 1
        ;;
esac

if [ -x "$install_root/Stop-Bridge.sh" ]; then
    "$install_root/Stop-Bridge.sh"
else
    launchctl bootout "gui/$(id -u)" "$launch_agent" >/dev/null 2>&1 || true
fi

rm -f -- "$launch_agent"
rm -rf -- "$install_root"
printf 'Removed the Paper Chat for Zotero bridge. Zotero data was not changed.\n'
