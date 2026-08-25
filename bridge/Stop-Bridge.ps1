$ErrorActionPreference = 'Stop'
$bridgeRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = (Join-Path $bridgeRoot 'server.py').ToLowerInvariant()
$processes = Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.ToLowerInvariant().Contains($serverPath)
}
foreach ($process in $processes) {
    Stop-Process -Id $process.ProcessId
}
Write-Output "Stopped $($processes.Count) Paper Chat for Zotero Bridge process(es)."
