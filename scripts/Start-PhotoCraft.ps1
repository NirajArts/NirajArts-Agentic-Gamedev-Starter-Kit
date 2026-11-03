#requires -Version 7.0
[CmdletBinding()]
param([switch] $CheckOnly, [switch] $AllowTokenCreation)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'PhotoCraft.Common.ps1')

try {
    if (-not $IsWindows) { throw 'This launcher targets Windows. See docs/photocraft.md for other platforms.' }
    $repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
    Assert-PhotoCraftBinaries $repoRoot
    $runtimePath = Assert-PlainPath $repoRoot '.local'
    $tokenPath = Assert-PlainPath $repoRoot '.local/photocraft-control.token'
    Assert-PortFree 9880
    if (Test-Path -LiteralPath $runtimePath) {
        if (-not (Test-Path -LiteralPath $runtimePath -PathType Container)) { throw '.local must be a directory.' }
        Assert-PrivateAcl $runtimePath
    }
    if (Test-Path -LiteralPath $tokenPath) {
        if (-not (Test-Path -LiteralPath $tokenPath -PathType Leaf)) { throw 'Credential path must be a regular file.' }
        Assert-PrivateAcl $tokenPath
    }
    if ($CheckOnly) {
        Write-Output 'Preflight passed. No application launched and no directories or credentials created.'
        exit 0
    }
    if (-not (Test-Path -LiteralPath $tokenPath) -and -not $AllowTokenCreation) {
        throw 'First launch needs authorization to create the repo-local credential. Review docs/photocraft.md and use -AllowTokenCreation.'
    }
    if (-not (Test-Path -LiteralPath $runtimePath)) {
        # Supply a restrictive ACL at directory creation; do not alter an existing directory.
        $sid = [Security.Principal.WindowsIdentity]::GetCurrent().User
        $acl = [Security.AccessControl.DirectorySecurity]::new()
        $acl.SetOwner($sid)
        $acl.SetAccessRuleProtection($true, $false)
        $rule = [Security.AccessControl.FileSystemAccessRule]::new($sid, 'FullControl',
                    'ContainerInherit,ObjectInherit', 'None', 'Allow')
        $acl.AddAccessRule($rule)
        $directory = [IO.DirectoryInfo]::new($runtimePath)
        [IO.FileSystemAclExtensions]::Create($directory, $acl)
        Assert-PrivateAcl $runtimePath
    }
    # Recheck immediately before launch; another process can still win the subsequent bind race.
    Assert-PortFree 9880
    $startInfo = New-PhotoCraftStartInfo $repoRoot $tokenPath
    $process = [Diagnostics.Process]::Start($startInfo)
    if ($null -eq $process) { throw 'PhotoCraft process did not start.' }
    Write-Output "PhotoCraft launch attempted (PID $($process.Id)). Verify its UI and authenticated connection."
    $process.Dispose()
    exit 0
} catch {
    Write-Error $_.Exception.Message
    exit 1
}
