$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$python = (Get-Command python -ErrorAction Stop).Source
& $python (Join-Path $projectRoot 'scripts\update_manifest.py')
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to update release metadata.'
}
