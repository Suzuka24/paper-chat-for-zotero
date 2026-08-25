#!/bin/sh
set -eu

bridge_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
pid_file="$bridge_root/bridge.pid"
launch_label=io.github.suzuka24.paper-chat-for-zotero-bridge
launch_agent="${HOME}/Library/LaunchAgents/${launch_label}.plist"
stopped=0

if launchctl print "gui/$(id -u)/$launch_label" >/dev/null 2>&1; then
    launchctl bootout "gui/$(id -u)" "$launch_agent"
    stopped=1
fi

if [ -f "$pid_file" ]; then
    bridge_pid=$(cat "$pid_file")
    case "$bridge_pid" in
        ''|*[!0-9]*) ;;
        *)
            command_line=$(ps -p "$bridge_pid" -o command= 2>/dev/null || true)
            case "$command_line" in
                *"$bridge_root/server.py"*)
                    kill "$bridge_pid" 2>/dev/null || true
                    stopped=1
                    ;;
            esac
            ;;
    esac
    rm -f -- "$pid_file"
fi

printf 'Stopped %s Paper Chat for Zotero Bridge service(s).\n' "$stopped"
