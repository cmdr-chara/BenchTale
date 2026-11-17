# Patch a data.win with the bench bridge -> data_bench.win
# Usage: .\patch_datawin.ps1 -GameDir "C:\...\steamapps\common\Undertale"
param(
  [Parameter(Mandatory)] [string] $GameDir,
  [string] $UtmtDir = ""
)
$ErrorActionPreference = "Stop"
if (-not $UtmtDir) { $UtmtDir = Join-Path $PSScriptRoot "..\tools\utmt" }
$UtmtDir = (Resolve-Path $UtmtDir -ErrorAction SilentlyContinue).Path
if (-not $UtmtDir) { throw "UTMT dir not found - run fetch_utmt.ps1 first" }
$cli = Get-ChildItem $UtmtDir -Recurse -Filter "UndertaleModCli*.exe" | Select-Object -First 1
if (-not $cli) { throw "UndertaleModCli not found under $UtmtDir - run fetch_utmt.ps1 first" }
$data = Join-Path $GameDir "data.win"
$out  = Join-Path $GameDir "data_bench.win"
if (-not (Test-Path $data)) { throw "data.win not found at $data" }
& $cli.FullName load $data -s (Join-Path $PSScriptRoot "..\patches\bench_bridge.csx") -o $out -f
if (-not (Test-Path $out)) { throw "patch produced no output" }
Write-Output "patched -> $out"
Write-Output "launch with: `"$GameDir\UNDERTALE.exe`" -game `"$out`""
