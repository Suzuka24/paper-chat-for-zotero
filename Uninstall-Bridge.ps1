$ErrorActionPreference = 'Stop'
$startupFolder = [Environment]::GetFolderPath('Startup')
$roots = @(
    (Join-Path $env:LOCALAPPDATA 'PaperChatForZotero'),
    (Join-Path $env:LOCALAPPDATA 'ZoteroCodexChat')
)
$links = @(
    (Join-Path $startupFolder 'Paper Chat for Zotero Bridge.lnk'),
    (Join-Path $startupFolder 'Zotero Codex Chat Bridge.lnk')
)

foreach ($root in $roots) {
    $stopScript = Join-Path $root 'Stop-Bridge.ps1'
    if (Test-Path -LiteralPath $stopScript -PathType Leaf) {
        & $stopScript
    }
}
foreach ($link in $links) {
    Remove-Item -LiteralPath $link -Force -ErrorAction SilentlyContinue
}
foreach ($root in $roots) {
    if (Test-Path -LiteralPath $root) {
        $resolved = (Resolve-Path -LiteralPath $root).Path
        $expected = [IO.Path]::GetFullPath($root)
        if ($resolved -ne $expected -or $expected -notlike "$env:LOCALAPPDATA\*") {
            throw "Refusing to delete an unexpected path: $resolved"
        }
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
Write-Output 'The Paper Chat for Zotero bridge was removed. Remove the Zotero plugin separately in Tools -> Plugins.'
