# Installs the commit-msg hook of ai/hooks into the hooks folder of the clone
# that contains this script. The hooks folder is shared by all worktrees of a
# clone; the hook itself acts only on the branch dev/ai-workflows.
#
# Run it from a checkout of dev/ai-workflows:
#   powershell -ExecutionPolicy Bypass -File <worktree>\ai\hooks\install-hooks.ps1
#
# The hook calls ai/scripts/check_commit_message.py of the checkout, so a
# "git pull" is enough for changes to the check. Run the script again only when
# ai/hooks/commit-msg itself changes.

[CmdletBinding()]
param(
    # Replace an existing, different commit-msg hook (it is saved as commit-msg.bak first).
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

$source = Join-Path $PSScriptRoot 'commit-msg'
if (-not (Test-Path $source)) {
    throw "Hook not found: $source"
}
$hooks = git -C $PSScriptRoot rev-parse --path-format=absolute --git-path hooks
if ($LASTEXITCODE -ne 0 -or -not $hooks) {
    throw "$PSScriptRoot is not inside a git checkout."
}
New-Item -ItemType Directory -Force -Path $hooks | Out-Null
$target = Join-Path $hooks 'commit-msg'

# Git for Windows runs hooks with its own sh, which needs LF line endings.
$content = [IO.File]::ReadAllText($source) -replace "`r`n", "`n"

if (Test-Path $target) {
    $existing = [IO.File]::ReadAllText($target) -replace "`r`n", "`n"
    if ($existing -eq $content) {
        Write-Host "Already installed: $target"
        return
    }
    if (-not $Force) {
        Write-Warning "$target already exists and differs. Run again with -Force to replace it (the old hook is saved as commit-msg.bak)."
        exit 1
    }
    Copy-Item $target "$target.bak" -Force
    Write-Host "Saved the existing hook as $target.bak"
}

[IO.File]::WriteAllText($target, $content, (New-Object Text.UTF8Encoding $false))
Write-Host "Installed $target"
