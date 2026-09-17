[CmdletBinding()]
param(
    [string]$ValidatorPath = "",
    [string]$InstalledSkillPath = ""
)

# Compatibility entry; product checks no longer inspect host skill source.
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
if ([string]::IsNullOrWhiteSpace($InstalledSkillPath) -and $env:CODEX_HOME) {
    $candidate = Join-Path $env:CODEX_HOME "skills\claim"
    if (Test-Path -LiteralPath $candidate -PathType Container) { $InstalledSkillPath = $candidate }
}
$arguments = @("-3", "-B", (Join-Path $PSScriptRoot "validate.py"))
if (-not [string]::IsNullOrWhiteSpace($InstalledSkillPath)) {
    $arguments += @("--installed", $InstalledSkillPath)
}
& py @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if (-not [string]::IsNullOrWhiteSpace($ValidatorPath)) {
    if (-not (Test-Path -LiteralPath $ValidatorPath -PathType Leaf)) { throw "Explicit host validator not found: $ValidatorPath" }
    Write-Output "Optional host validation uses explicit Python UTF-8 mode; this does not repair its source."
    & py -3 -X utf8 $ValidatorPath (Join-Path $repoRoot "claim")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
exit 0
