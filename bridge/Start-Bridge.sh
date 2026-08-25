#!/bin/sh
set -eu

bridge_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
app_server="$bridge_root/codex-app-server"
token_file="$bridge_root/token.txt"
log_file="$bridge_root/bridge.log"
pid_file="$bridge_root/bridge.pid"
launch_label=io.github.suzuka24.paper-chat-for-zotero-bridge
launch_agent="${HOME}/Library/LaunchAgents/${launch_label}.plist"
foreground=false

if [ "${1:-}" = "--foreground" ]; then
    foreground=true
elif [ "$#" -gt 0 ]; then
    printf 'Usage: %s [--foreground]\n' "$0" >&2
    exit 2
fi

if [ -f "$bridge_root/python-bin.txt" ]; then
    python_bin=$(cat "$bridge_root/python-bin.txt")
else
    python_bin=$(command -v python3)
fi

if curl --fail --silent --max-time 2 \
    -H "X-Zotero-Codex-Token: $(cat "$token_file" 2>/dev/null || true)" \
    http://127.0.0.1:23120/health >/dev/null 2>&1; then
    printf 'Paper Chat for Zotero Bridge is already running.\n'
    exit 0
fi

if [ ! -x "$app_server" ]; then
    printf 'Missing %s. Run Install-macOS.py first.\n' "$app_server" >&2
    exit 1
fi

set -- \
    "$bridge_root/server.py" \
    --codex-app-server "$app_server" \
    --token-file "$token_file" \
    --log-file "$log_file"

if [ "$foreground" = true ]; then
    exec "$python_bin" "$@"
fi

service_target="gui/$(id -u)/$launch_label"
if [ -f "$launch_agent" ]; then
    if ! launchctl print "$service_target" >/dev/null 2>&1; then
        launchctl bootstrap "gui/$(id -u)" "$launch_agent"
    fi
    launchctl kickstart -k "$service_target"
else
    nohup "$python_bin" "$@" >/dev/null 2>&1 &
    bridge_pid=$!
    printf '%s\n' "$bridge_pid" > "$pid_file"
    chmod 600 "$pid_file"
fi

printf 'Paper Chat for Zotero Bridge started.\n'
