param(
    [switch]$NoAutoStart,
    [switch]$SkipDownload,
    [string]$CodexVersion = 'rust-v0.157.1'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceBridge = Join-Path $projectRoot 'bridge'
$installRoot = Join-Path $env:LOCALAPPDATA 'PaperChatForZotero'
$legacyRoot = Join-Path $env:LOCALAPPDATA 'ZoteroCodexChat'
$appServer = Join-Path $installRoot 'codex-app-server.exe'
$codeModeHost = Join-Path $installRoot 'codex-code-mode-host.exe'
$startupFolder = [Environment]::GetFolderPath('Startup')
$startupLink = Join-Path $startupFolder 'Paper Chat for Zotero Bridge.lnk'
$legacyStartupLink = Join-Path $startupFolder 'Zotero Codex Chat Bridge.lnk'

$python = (Get-Command python -ErrorAction Stop).Source
Write-Output "Python: $python"

New-Item -ItemType Directory -Force -Path $installRoot | Out-Null
foreach ($root in @($installRoot, $legacyRoot)) {
    $installedStopBridge = Join-Path $root 'Stop-Bridge.ps1'
    if (Test-Path -LiteralPath $installedStopBridge -PathType Leaf) {
        & $installedStopBridge
    }
}
$files = @('server.py', 'requirements.txt', 'Start-Bridge.ps1', 'Stop-Bridge.ps1')
foreach ($file in $files) {
    Copy-Item -LiteralPath (Join-Path $sourceBridge $file) -Destination (Join-Path $installRoot $file) -Force
}
$installedVendor = Join-Path $installRoot 'vendor'
if (Test-Path -LiteralPath $installedVendor) {
    Remove-Item -LiteralPath $installedVendor -Recurse -Force
}
Copy-Item -LiteralPath (Join-Path $sourceBridge 'vendor') -Destination $installedVendor -Recurse -Force
Write-Output 'Installed the bundled local PDF text extractor.'

$tokenFile = Join-Path $installRoot 'token.txt'
$token = if (Test-Path -LiteralPath $tokenFile -PathType Leaf) {
    (Get-Content -LiteralPath $tokenFile -Raw).Trim()
} elseif (Test-Path -LiteralPath (Join-Path $legacyRoot 'token.txt') -PathType Leaf) {
    (Get-Content -LiteralPath (Join-Path $legacyRoot 'token.txt') -Raw).Trim()
} else {
    ''
}
if ($token -notmatch '^[a-fA-F0-9]{64}$') {
    $bytes = [byte[]]::new(32)
    [Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
    $token = [Convert]::ToHexString($bytes).ToLowerInvariant()
}
[IO.File]::WriteAllText($tokenFile, $token, [Text.UTF8Encoding]::new($false))
Write-Output 'Created a per-installation loopback bridge token.'

$expectedCodexVersion = $CodexVersion -replace '^rust-v', ''
$appServerVersionMatches = $false
if (Test-Path -LiteralPath $appServer -PathType Leaf) {
    $installedAppServerVersion = (& $appServer --version 2>$null | Out-String).Trim()
    $appServerVersionMatches = $LASTEXITCODE -eq 0 -and $installedAppServerVersion -match "(^|\s)$([regex]::Escape($expectedCodexVersion))(\s|$)"
}
if (-not $appServerVersionMatches -or -not (Test-Path -LiteralPath $codeModeHost -PathType Leaf)) {
    if ($SkipDownload) {
        throw 'Codex App Server or Code Mode Host is not installed; -SkipDownload cannot be used.'
    }
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/openai/codex/releases/tags/$CodexVersion" -Headers @{
        'User-Agent' = 'Paper-Chat-for-Zotero-Installer'
    }
    $architecture = if ([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture -eq 'Arm64') {
        'aarch64'
    } else {
        'x86_64'
    }
    foreach ($component in @(
        @{ Name = 'codex-app-server'; Destination = $appServer },
        @{ Name = 'codex-code-mode-host'; Destination = $codeModeHost }
    )) {
        if ($component.Name -eq 'codex-app-server' -and $appServerVersionMatches) {
            continue
        }
        if ($component.Name -eq 'codex-code-mode-host' -and (Test-Path -LiteralPath $component.Destination -PathType Leaf)) {
            continue
        }
        $assetName = "$($component.Name)-$architecture-pc-windows-msvc.exe"
        $asset = $release.assets | Where-Object { $_.name -eq $assetName } | Select-Object -First 1
        if (-not $asset) {
            throw "Asset not found in the OpenAI release: $assetName"
        }
        Write-Output "Downloading $($component.Name) $CodexVersion from the official OpenAI GitHub release..."
        $temporaryDownload = "$($component.Destination).download"
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $temporaryDownload
        if ($asset.digest -notmatch '^sha256:([a-fA-F0-9]{64})$') {
            [IO.File]::Delete($temporaryDownload)
            throw 'The official release did not provide a valid SHA-256 digest.'
        }
        $expectedHash = $Matches[1].ToLowerInvariant()
        $actualHash = (Get-FileHash -LiteralPath $temporaryDownload -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualHash -ne $expectedHash) {
            [IO.File]::Delete($temporaryDownload)
            throw "$($component.Name) SHA-256 verification failed."
        }
        Move-Item -LiteralPath $temporaryDownload -Destination $component.Destination -Force
        Write-Output "Installed $($component.Name) $($release.tag_name)."
    }
}

& (Join-Path $projectRoot 'Build.ps1')

if (-not $NoAutoStart) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($startupLink)
    $shortcut.TargetPath = (Get-Command powershell.exe -ErrorAction Stop).Source
    $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $installRoot 'Start-Bridge.ps1')`""
    $shortcut.WorkingDirectory = $installRoot
    $shortcut.WindowStyle = 7
    $shortcut.Description = 'Start the local Paper Chat for Zotero bridge'
    $shortcut.Save()
    Write-Output "Added login autostart shortcut: $startupLink"
} else {
    Remove-Item -LiteralPath $startupLink -Force -ErrorAction SilentlyContinue
}
Remove-Item -LiteralPath $legacyStartupLink -Force -ErrorAction SilentlyContinue

& (Join-Path $installRoot 'Start-Bridge.ps1')
$xpiPath = Join-Path $projectRoot 'dist\paper-chat-for-zotero.xpi'
Write-Output ''
Write-Output 'Installation preparation is complete.'
Write-Output "In Zotero, open Tools -> Plugins and install this file: $xpiPath"
