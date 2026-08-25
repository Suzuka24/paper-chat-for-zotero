$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$parseErrors = @()
Get-ChildItem -LiteralPath $projectRoot -Filter '*.ps1' -Recurse | ForEach-Object {
    $tokens = $null
    $errors = $null
    [Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$errors) | Out-Null
    $parseErrors += $errors
}
if ($parseErrors.Count) {
    $parseErrors | Format-List | Out-String | Write-Error
}

$python = (Get-Command python -ErrorAction Stop).Source
& $python (Join-Path $projectRoot 'scripts\test.py')
if ($LASTEXITCODE -ne 0) {
    throw 'Cross-platform validation failed.'
}
