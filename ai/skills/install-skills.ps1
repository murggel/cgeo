# Links the interactive c:geo skills of this checkout into the personal skill folder
# of Claude Code (%USERPROFILE%\.claude\skills), so they are available in every
# local session, whatever branch or project it works on.
#
# Run it from a checkout of dev/ai-workflows, ideally a separate git worktree:
#   powershell -ExecutionPolicy Bypass -File <worktree>\ai\skills\install-skills.ps1
#
# It creates directory junctions, which need no administrator rights and no
# developer mode. Run it again after a skill has been added to
# interactive-skills.txt; a "git pull" in the worktree is enough for changes
# to existing skills.

[CmdletBinding()]
param(
    # Replace an existing real folder of the same name (it is renamed to <name>.bak first).
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

$skillsSource = $PSScriptRoot
$listFile = Join-Path $skillsSource 'interactive-skills.txt'
$target = Join-Path $env:USERPROFILE '.claude\skills'

if (-not (Test-Path $listFile)) {
    throw "List of skills not found: $listFile"
}
New-Item -ItemType Directory -Force -Path $target | Out-Null

$names = Get-Content $listFile |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith('#') }

foreach ($name in $names) {
    $source = Join-Path $skillsSource $name
    $link = Join-Path $target $name

    if (-not (Test-Path (Join-Path $source 'SKILL.md'))) {
        Write-Warning "Skipped ${name}: no SKILL.md in $source"
        continue
    }

    if (Test-Path $link) {
        $item = Get-Item $link -Force
        if ($item.LinkType -in @('Junction', 'SymbolicLink')) {
            # Remove only the link, never the content it points to.
            $item.Delete()
        } elseif ($Force) {
            $backup = "$link.bak"
            if (Test-Path $backup) { Remove-Item -Recurse -Force $backup }
            Rename-Item $link $backup
            Write-Host "Renamed existing folder to $backup"
        } else {
            Write-Warning "Skipped ${name}: $link is a real folder. Run again with -Force to replace it."
            continue
        }
    }

    New-Item -ItemType Junction -Path $link -Target $source | Out-Null
    Write-Host "Linked $link -> $source"
}

Write-Host ''
Write-Host 'Done. Start a new Claude Code session to load the skills.'
Write-Host 'Delete copies of these skills in your claude.ai account, so there is only one version.'
