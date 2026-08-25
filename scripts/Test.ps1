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

$node = (Get-Command node -ErrorAction Stop).Source
& $node --check (Join-Path $projectRoot 'plugin\content\main.js')
& $node --check (Join-Path $projectRoot 'plugin\content\preferences.js')
$python = (Get-Command python -ErrorAction Stop).Source
& $python -m py_compile (Join-Path $projectRoot 'bridge\server.py') (Join-Path $projectRoot 'scripts\build_xpi.py')

$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'plugin\manifest.json') -Raw | ConvertFrom-Json
[xml](Get-Content -LiteralPath (Join-Path $projectRoot 'plugin\content\preferences.xhtml') -Raw) | Out-Null
$updates = Get-Content -LiteralPath (Join-Path $projectRoot 'updates.json') -Raw | ConvertFrom-Json

& (Join-Path $projectRoot 'Build.ps1')
$xpiPath = Join-Path $projectRoot 'dist\paper-chat-for-zotero.xpi'
$firstHash = (Get-FileHash -LiteralPath $xpiPath -Algorithm SHA256).Hash.ToLowerInvariant()
& (Join-Path $projectRoot 'Build.ps1')
$secondHash = (Get-FileHash -LiteralPath $xpiPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($firstHash -ne $secondHash) {
    throw 'The XPI build is not reproducible.'
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::OpenRead($xpiPath)
try {
    $entries = @($archive.Entries | ForEach-Object FullName)
    foreach ($required in @('manifest.json', 'bootstrap.js', 'prefs.js', 'content/main.js', 'content/codex.svg')) {
        if ($required -notin $entries) { throw "The XPI is missing $required." }
    }
    if ($entries | Where-Object { $_ -match '(^|/)(token\.txt|bridge\.log|codex-app-server\.exe)$' }) {
        throw 'The XPI contains a forbidden local secret, log, or binary.'
    }
} finally {
    $archive.Dispose()
}

$pluginID = $manifest.applications.zotero.id
$update = $updates.addons.$pluginID.updates | Select-Object -First 1
if ($update.version -ne $manifest.version) { throw 'updates.json version does not match manifest.json.' }
if ($update.update_hash -ne "sha256:$secondHash") { throw 'updates.json hash does not match the XPI.' }

Write-Output "All checks passed for $pluginID $($manifest.version)."
Write-Output "SHA-256: $secondHash"
