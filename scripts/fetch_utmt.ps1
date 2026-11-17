# Download the latest UndertaleModTool CLI into .\tools\
# Works without the GitHub API (which rate-limits shared IPs): resolves the
# latest tag from the releases redirect, then scrapes expanded_assets.
$ErrorActionPreference = "Stop"
$repo = "UnderminersTeam/UndertaleModTool"

$resp = Invoke-WebRequest "https://github.com/$repo/releases/latest" -MaximumRedirection 0 -ErrorAction SilentlyContinue
$tag = ($resp.Headers.Location -split "/")[-1]
if (-not $tag) { throw "could not resolve latest release tag" }

$assets = Invoke-WebRequest "https://github.com/$repo/releases/expanded_assets/$tag" -UseBasicParsing
$link = ($assets.Links | Where-Object { $_.href -match "UTMT_CLI.*Windows\.zip$" } | Select-Object -First 1).href
if (-not $link) {
  $link = ($assets.Links | Where-Object { $_.href -match "UndertaleModTool.*Windows\.zip$" } | Select-Object -First 1).href
}
if (-not $link) { throw "no Windows zip asset in release $tag" }

New-Item -ItemType Directory -Force "$PSScriptRoot\..\tools" | Out-Null
$zip = "$PSScriptRoot\..\tools\utmt.zip"
Invoke-WebRequest "https://github.com$link" -OutFile $zip
Expand-Archive -Force $zip "$PSScriptRoot\..\tools\utmt"
Remove-Item $zip
Write-Output "UTMT $tag -> tools\utmt"
