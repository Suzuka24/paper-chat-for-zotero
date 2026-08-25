$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
& (Join-Path $projectRoot 'Build.ps1')

$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'plugin\manifest.json') -Raw | ConvertFrom-Json
$xpiPath = Join-Path $projectRoot 'dist\paper-chat-for-zotero.xpi'
$hash = (Get-FileHash -LiteralPath $xpiPath -Algorithm SHA256).Hash.ToLowerInvariant()
$pluginID = $manifest.applications.zotero.id
$version = $manifest.version
$entry = [ordered]@{
    version = $version
    update_link = "https://github.com/Suzuka24/paper-chat-for-zotero/releases/download/v$version/paper-chat-for-zotero.xpi"
    update_hash = "sha256:$hash"
    applications = [ordered]@{
        zotero = [ordered]@{
            strict_min_version = $manifest.applications.zotero.strict_min_version
            strict_max_version = $manifest.applications.zotero.strict_max_version
        }
    }
}
$updates = [ordered]@{ addons = [ordered]@{ $pluginID = [ordered]@{ updates = @($entry) } } }
$json = $updates | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText((Join-Path $projectRoot 'updates.json'), $json + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "Updated updates.json for $pluginID $version ($hash)."
