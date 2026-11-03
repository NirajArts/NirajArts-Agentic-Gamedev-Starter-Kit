#requires -Version 7.0
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$count = 0
foreach ($file in Get-ChildItem -LiteralPath $repoRoot -Filter '*.ps1' -Recurse) {
    $parseErrors = $null
    $tokens = $null
    [void] [Management.Automation.Language.Parser]::ParseFile($file.FullName, [ref] $tokens, [ref] $parseErrors)
    if ($parseErrors.Count -ne 0) { throw "Parse errors in $($file.Name): $parseErrors" }
    $count++
}
. (Join-Path $repoRoot 'scripts/PhotoCraft.Common.ps1')
$fictionalRoot = 'C:\Fictional Path With Spaces\Starter'
$fictionalToken = Join-Path $fictionalRoot '.local/photocraft-control.token'
$info = New-PhotoCraftStartInfo $fictionalRoot $fictionalToken
if ($info.ArgumentList.Count -ne 8) { throw 'Expected eight argument entries.' }
if ($info.ArgumentList[3] -ne $fictionalToken -or $info.ArgumentList[5] -ne $fictionalRoot -or $info.ArgumentList[7] -ne $fictionalRoot) {
    throw 'Paths were not preserved as separate argument values.'
}
if ($info.UseShellExecute -or -not $info.CreateNoWindow) { throw 'Unexpected process settings.' }
$count++
$previousControlToken = [Environment]::GetEnvironmentVariable('PHOTOCRAFT_CONTROL_TOKEN', 'Process')
$env:PHOTOCRAFT_CONTROL_TOKEN = 'SYNTHETIC-NON-CREDENTIAL'
try {
    $info = New-PhotoCraftStartInfo $fictionalRoot $fictionalToken
    if ($info.Environment.ContainsKey('PHOTOCRAFT_CONTROL_TOKEN')) { throw 'Inherited override was not cleared.' }
    $count++
} finally { [Environment]::SetEnvironmentVariable('PHOTOCRAFT_CONTROL_TOKEN', $previousControlToken, 'Process') }

# Test doubles exercise failure branches without binaries, listeners or credentials.
function Test-Path { return $false }
function Get-Item { return $null }
$failed = $false
try { Assert-PhotoCraftBinaries $fictionalRoot } catch { $failed = $_.Exception.Message -like '*Missing tools/photocraft/*' }
if (-not $failed) { throw 'Missing binary was not rejected.' }
Remove-Item Function:Test-Path
Remove-Item Function:Get-Item
$count++

function Get-Item { return [pscustomobject]@{Attributes=[IO.FileAttributes]::ReparsePoint} }
$failed = $false
try { Assert-PlainPath $fictionalRoot '.local/photocraft-control.token' } catch { $failed = $_.Exception.Message -like '*Linked tool/runtime*' }
if (-not $failed) { throw 'Dangling link/reparse point was not rejected.' }
Remove-Item Function:Get-Item
$count++

# Extract the port comparison into a controlled substitute for the system enumeration.
$portFunction = (Get-Command Assert-PortFree).ScriptBlock.ToString()
$portFunction = $portFunction.Replace('[Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()', '@([pscustomobject]@{Port=9880})')
$occupied = [scriptblock]::Create($portFunction)
$failed = $false
try { & $occupied 9880 } catch { $failed = $_.Exception.Message -like '*occupied*' }
if (-not $failed) { throw 'Occupied-port branch failed.' }
$count++

# The real launcher preflight stops at the absent binary without making .local/.
if (Test-Path -LiteralPath (Join-Path $repoRoot 'tools/photocraft/photocraft.exe')) {
    Write-Output 'Real missing-binary preflight skipped: locally installed binary is present.'
} else {
    $before = Test-Path -LiteralPath (Join-Path $repoRoot '.local')
    & (Join-Path $PSHOME 'pwsh.exe') -NoProfile -File (Join-Path $repoRoot 'scripts/Start-PhotoCraft.ps1') -CheckOnly 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { throw 'Missing-binary preflight unexpectedly succeeded.' }
    if ((Test-Path -LiteralPath (Join-Path $repoRoot '.local')) -ne $before) { throw 'Preflight created runtime directory.' }
    $count++
}
Write-Output "PASS: $count PowerShell checks; no GUI launched, credentials created or ACLs changed."
