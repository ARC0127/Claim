param([string]$SkillPath = (Join-Path $PSScriptRoot '..\claim'))
$ErrorActionPreference = 'Stop'
$claimRef = (Resolve-Path -LiteralPath (Join-Path $SkillPath 'references\theory-coach.md')).Path
$claimBytes = [System.IO.File]::ReadAllBytes($claimRef)
if ($claimBytes[0] -ne 239 -or $claimBytes[1] -ne 187 -or $claimBytes[2] -ne 191) { throw 'Expected UTF-8 BOM' }
$claimStage = ([string][char]0x9636) + [char]0x6BB5
$claimDefault = Get-Content -LiteralPath $claimRef -Raw
$claimExplicit = Get-Content -LiteralPath $claimRef -Raw -Encoding UTF8
if ($claimDefault -cne $claimExplicit -or -not $claimExplicit.Contains($claimStage)) { throw 'Default/UTF-8 Chinese read mismatch' }
if ($claimExplicit -match '[\uFFFD\uE000-\uF8FF]') { throw 'Damaged decoded text' }
# Negative control: emulate the historical UTF-8 bytes decoded as CP936.
$claimWrong = [System.Text.Encoding]::GetEncoding(936).GetString($claimBytes, 3, $claimBytes.Length - 3)
if ($claimWrong.Contains($claimStage)) { throw 'Negative control failed to distinguish the stage label' }
Write-Output ('PASS: PowerShell ' + $PSVersionTable.PSVersion + ' default and explicit UTF-8 match; CP936 negative control differs')
