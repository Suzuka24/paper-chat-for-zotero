$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pluginRoot = Join-Path $projectRoot 'plugin'
$distRoot = Join-Path $projectRoot 'dist'
$xpiPath = Join-Path $distRoot 'paper-chat-for-zotero.xpi'

New-Item -ItemType Directory -Force -Path $distRoot | Out-Null
Remove-Item -LiteralPath $xpiPath -Force -ErrorAction SilentlyContinue
$python = (Get-Command python -ErrorAction Stop).Source
& $python (Join-Path $projectRoot 'scripts\build_xpi.py') $pluginRoot $xpiPath
if ($LASTEXITCODE -ne 0) {
    throw 'The deterministic XPI build failed.'
}
Write-Output "Built: $xpiPath"
