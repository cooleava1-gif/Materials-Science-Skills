$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkillsDir = Join-Path $repoRoot "skills"

if ($env:CODEX_HOME) {
    $targetSkillsDir = Join-Path $env:CODEX_HOME "skills"
} else {
    $targetSkillsDir = Join-Path $HOME ".codex\skills"
}

if (-not (Test-Path -LiteralPath $sourceSkillsDir -PathType Container)) {
    Write-Error "Source skills directory not found: $sourceSkillsDir"
    exit 1
}

$civilSkillDirs = Get-ChildItem -LiteralPath $sourceSkillsDir -Directory -Filter "civil-materials-*"
if (-not $civilSkillDirs) {
    Write-Error "No civil-materials-* skill directories found in: $sourceSkillsDir"
    exit 1
}

$sharedDir = Join-Path $sourceSkillsDir "_shared"
if (-not (Test-Path -LiteralPath $sharedDir -PathType Container)) {
    Write-Error "Required shared skill directory not found: $sharedDir"
    exit 1
}

New-Item -ItemType Directory -Force -Path $targetSkillsDir | Out-Null

$resolvedTargetSkillsDir = (Resolve-Path -LiteralPath $targetSkillsDir).Path

function Remove-ExistingInstallDir {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $targetDir = Join-Path $targetSkillsDir $Name
    if (-not (Test-Path -LiteralPath $targetDir)) {
        return
    }

    $resolvedTargetDir = (Resolve-Path -LiteralPath $targetDir).Path
    if (-not $resolvedTargetDir.StartsWith($resolvedTargetSkillsDir, [System.StringComparison]::OrdinalIgnoreCase)) {
        Write-Error "Refusing to remove install directory outside target skills dir: $resolvedTargetDir"
        exit 1
    }
    if ($resolvedTargetDir -eq $resolvedTargetSkillsDir) {
        Write-Error "Refusing to remove target skills root: $resolvedTargetDir"
        exit 1
    }

    Remove-Item -LiteralPath $resolvedTargetDir -Recurse -Force
}

foreach ($skillDir in $civilSkillDirs) {
    Remove-ExistingInstallDir -Name $skillDir.Name
    Copy-Item -LiteralPath $skillDir.FullName -Destination $targetSkillsDir -Recurse -Force
}
Remove-ExistingInstallDir -Name "_shared"
Copy-Item -LiteralPath $sharedDir -Destination $targetSkillsDir -Recurse -Force

Write-Output "Installed civil materials skills to: $targetSkillsDir"
Write-Output "Installed directories:"
Get-ChildItem -LiteralPath $targetSkillsDir -Directory |
    Where-Object { $_.Name -like "civil-materials-*" -or $_.Name -eq "_shared" } |
    Sort-Object Name |
    ForEach-Object { Write-Output ("- " + $_.Name) }
