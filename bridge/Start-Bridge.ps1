param(
    [switch]$Foreground
)

$ErrorActionPreference = 'Stop'
$bridgeRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = (Get-Command python -ErrorAction Stop).Source
$server = Join-Path $bridgeRoot 'server.py'
$appServer = Join-Path $bridgeRoot 'codex-app-server.exe'
$token = Join-Path $bridgeRoot 'token.txt'
$log = Join-Path $bridgeRoot 'bridge.log'
$arguments = @(
    $server,
    '--codex-app-server', $appServer,
    '--token-file', $token,
    '--log-file', $log
)

try {
    $headers = @{ 'X-Zotero-Codex-Token' = (Get-Content -LiteralPath $token -Raw).Trim() }
    $health = Invoke-RestMethod -Uri 'http://127.0.0.1:23120/health' -Headers $headers -TimeoutSec 2
    if ($health.ok) {
        Write-Output 'Paper Chat for Zotero Bridge is already running.'
        exit 0
    }
} catch {
    # Expected when the bridge has not started yet.
}

if (-not (Test-Path -LiteralPath $appServer -PathType Leaf)) {
    throw "Missing $appServer. Run Install.ps1 first."
}

if ($Foreground) {
    & $python @arguments
} else {
    $quotedArguments = $arguments | ForEach-Object { '"{0}"' -f $_ }
    Start-Process -FilePath $python -ArgumentList $quotedArguments -WorkingDirectory $bridgeRoot -WindowStyle Hidden
    Write-Output 'Paper Chat for Zotero Bridge started.'
}
