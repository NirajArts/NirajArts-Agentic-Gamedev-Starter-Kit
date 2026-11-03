# Shared, side-effect-free helpers. PowerShell 7 required by the launcher.
Set-StrictMode -Version Latest

function Assert-PlainPath {
    param([string] $Root, [string] $Relative)
    $cursor = $Root
    foreach ($part in ($Relative -split '[/\\]')) {
        if (-not $part -or $part -in @('.', '..')) { throw 'Unsafe relative tool/runtime path.' }
        $cursor = Join-Path $cursor $part
        # Get-Item also identifies a dangling link, which Test-Path may report absent.
        $item = Get-Item -LiteralPath $cursor -Force -ErrorAction SilentlyContinue
        if ($null -ne $item) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw 'Linked tool/runtime paths are not supported.'
            }
        }
    }
    return $cursor
}

function Assert-PhotoCraftBinaries {
    param([string] $Root)
    foreach ($name in @('photocraft.exe', 'photocraft-cli.exe')) {
        $path = Assert-PlainPath $Root "tools/photocraft/$name"
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Missing tools/photocraft/$name. Follow docs/photocraft.md; no download was performed."
        }
    }
}

function Assert-PortFree {
    param([int] $Port = 9880)
    $connections = [Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
    if (@($connections | Where-Object Port -eq $Port).Count -gt 0) {
        throw "Port $Port is occupied. Inspect the existing instance; never kill it automatically."
    }
}

function Assert-PrivateAcl {
    param([string] $Path)
    $me = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $acl = Get-Acl -LiteralPath $Path
    $owner = $acl.GetOwner([Security.Principal.SecurityIdentifier]).Value
    if ($owner -ne $me) { throw 'Runtime credential location must be owned by the current user.' }
    foreach ($rule in $acl.GetAccessRules($true, $true, [Security.Principal.SecurityIdentifier])) {
        if ($rule.AccessControlType -eq 'Allow' -and $rule.IdentityReference.Value -ne $me) {
            throw 'Runtime credential location grants another principal access. Review its ACL deliberately.'
        }
    }
}

function New-PhotoCraftStartInfo {
    param([string] $Root, [string] $TokenFile)
    $info = [Diagnostics.ProcessStartInfo]::new()
    $info.FileName = Join-Path $Root 'tools/photocraft/photocraft.exe'
    $info.WorkingDirectory = $Root
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    foreach ($value in @('--control', '9880', '--control-token-file', $TokenFile,
                         '--automation-read-root', $Root, '--automation-write-root', $Root)) {
        $info.ArgumentList.Add($value)
    }
    foreach ($key in @($info.Environment.Keys)) {
        if ($key -like 'PHOTOCRAFT_CONTROL_*' -or $key -like 'PHOTOCRAFT_AUTOMATION_*') {
            [void] $info.Environment.Remove($key)
        }
    }
    return $info
}
