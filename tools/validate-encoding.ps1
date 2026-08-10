[CmdletBinding()]
param(
    [string]$ValidatorPath = "",
    [string]$InstalledSkillPath = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)
$failureCount = 0

function Write-Pass {
    param([string]$Message)
    Write-Host "[PASS] $Message"
}

function Write-Skip {
    param([string]$Message)
    Write-Host "[SKIP] $Message"
}

function Write-Fail {
    param([string]$Message)
    $script:failureCount += 1
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function ConvertFrom-Utf8Base64 {
    param([string]$Value)
    return [System.Text.Encoding]::UTF8.GetString(
        [System.Convert]::FromBase64String($Value)
    )
}

function Read-StrictUtf8 {
    param([string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if (
        $bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF
    ) {
        throw "UTF-8 BOM is not allowed"
    }

    $text = $utf8Strict.GetString($bytes)
    if ($text.IndexOf([char]0xFFFD) -ge 0) {
        throw "replacement character U+FFFD is present"
    }
    if ($text.IndexOf([char]0x0000) -ge 0) {
        throw "NUL character is present"
    }
    if ([System.Text.RegularExpressions.Regex]::IsMatch($text, "[\uE000-\uF8FF]")) {
        throw "private-use characters associated with mojibake are present"
    }

    return [pscustomobject]@{
        Bytes = $bytes
        Text = $text
    }
}

function Get-BytesSha256 {
    param([byte[]]$Bytes)

    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha256.ComputeHash($Bytes)
        return (($hash | ForEach-Object { $_.ToString("x2") }) -join "")
    }
    finally {
        $sha256.Dispose()
    }
}

function Test-MojibakeMarkers {
    param(
        [string]$Label,
        [string]$Text
    )

    $badMarkerBase64 = @(
        "6Yil",
        "57uX77mA5b2/",
        "5raT7oWf5p6D",
        "6Y605oiU",
        "6Y+N54WO57Sh",
        "6Y2Z5qmA5Zm6",
        "6ZCo5Yur5oOI5raU"
    )

    foreach ($encoded in $badMarkerBase64) {
        $marker = ConvertFrom-Utf8Base64 $encoded
        if ($Text.Contains($marker)) {
            throw "$Label contains a known mojibake marker"
        }
    }
}

function Test-RequiredMarkers {
    param(
        [string]$RelativePath,
        [string]$Text
    )

    $markersByPath = @{
        "claim/SKILL.md" = @(
            "4oCc5pWZ5oiR4oCd",
            "4oCc5byV5a+85oiR4oCd",
            "4oCc6YCQ6L2u4oCd",
            "4oCc6K6t57uD5Yik5pat4oCd",
            "4oCc5LiN6KaB5pu/5oiR5YGa5a6M4oCd",
            "56ym5Y+3",
            "5Lit5paH5ZCr5LmJ",
            "57G75Z6L5oiW5Y+W5YC85Z+f",
            "5b2i54q2L+e7tOW6pi/ljZXkvY0=",
            "6KeS6Imy5LiO5L6d6LWW5YWz57O7"
        )
        "claim/references/theory-coach.md" = @(
            "5L2g5Yia5omN6KGo6L6+5LqG5LuA5LmI",
            "5oiR5aaC5L2V5b2i5byP5YyW",
            "5b2T5YmN5pyA5aSn5q2n5LmJ",
            "5LiA5Liq6ZyA6KaB5L2g5Lqy6Ieq5Zue562U55qE6Zeu6aKY"
        )
    }

    if (-not $markersByPath.ContainsKey($RelativePath)) {
        return
    }

    foreach ($encoded in $markersByPath[$RelativePath]) {
        $marker = ConvertFrom-Utf8Base64 $encoded
        if (-not $Text.Contains($marker)) {
            throw "$RelativePath is missing a required Chinese protocol marker"
        }
    }
}

function Get-ZipEntryBytes {
    param([System.IO.Compression.ZipArchiveEntry]$Entry)

    $entryStream = $Entry.Open()
    $memoryStream = New-Object System.IO.MemoryStream
    try {
        $entryStream.CopyTo($memoryStream)
        return ,$memoryStream.ToArray()
    }
    finally {
        $entryStream.Dispose()
        $memoryStream.Dispose()
    }
}

Push-Location -LiteralPath $repoRoot
try {
    $trackedFiles = @(& git ls-files --cached --others --exclude-standard)
    if ($LASTEXITCODE -ne 0) {
        throw "git ls-files failed"
    }

    $textFiles = @(
        $trackedFiles | Where-Object {
            $_ -eq ".gitattributes" -or
            $_ -eq "VERSION" -or
            [System.IO.Path]::GetExtension($_) -in @(
                ".md", ".yaml", ".yml", ".json", ".txt", ".ps1"
            )
        }
    )

    foreach ($relativePath in $textFiles) {
        $fullPath = Join-Path $repoRoot $relativePath
        try {
            $record = Read-StrictUtf8 $fullPath
            Test-MojibakeMarkers -Label $relativePath -Text $record.Text
            Test-RequiredMarkers -RelativePath ($relativePath -replace "\\", "/") -Text $record.Text
        }
        catch {
            Write-Fail "${relativePath}: $($_.Exception.Message)"
        }
    }

    if ($failureCount -eq 0) {
        Write-Pass "$($textFiles.Count) tracked text files are strict UTF-8 without BOM"
        Write-Pass "required Chinese protocol markers are intact"
    }

    $manifestPath = Join-Path $repoRoot "manifest.json"
    $manifestRecord = Read-StrictUtf8 $manifestPath
    $manifest = $manifestRecord.Text | ConvertFrom-Json

    $checksumPath = Join-Path $repoRoot "dist\SHA256SUMS.txt"
    $checksumRecord = Read-StrictUtf8 $checksumPath
    foreach ($line in ($checksumRecord.Text -split "`r?`n")) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }
        if ($line -notmatch "^([0-9a-fA-F]{64})\s+(.+)$") {
            Write-Fail "invalid SHA256SUMS row: $line"
            continue
        }

        $expectedHash = $Matches[1].ToLowerInvariant()
        $relativePath = $Matches[2].Trim()
        $targetPath = Join-Path $repoRoot ($relativePath -replace "/", "\")
        if (-not (Test-Path -LiteralPath $targetPath -PathType Leaf)) {
            Write-Fail "checksum target is missing: $relativePath"
            continue
        }

        $actualHash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualHash -ne $expectedHash) {
            Write-Fail "checksum mismatch: $relativePath"
        }
    }
    if ($failureCount -eq 0) {
        Write-Pass "dist/SHA256SUMS.txt matches repository artifacts"
    }

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archivePath = Join-Path $repoRoot ($manifest.archive -replace "/", "\")
    if (-not (Test-Path -LiteralPath $archivePath -PathType Leaf)) {
        Write-Fail "manifest archive is missing: $($manifest.archive)"
    }
    else {
        $archive = [System.IO.Compression.ZipFile]::OpenRead($archivePath)
        try {
            foreach ($coreFile in $manifest.core_files) {
                $entryName = $coreFile -replace "\\", "/"
                $entry = $archive.Entries | Where-Object {
                    ($_.FullName -replace "\\", "/") -eq $entryName
                } | Select-Object -First 1
                if ($null -eq $entry) {
                    Write-Fail "archive entry is missing: $entryName"
                    continue
                }

                try {
                    $entryBytes = Get-ZipEntryBytes $entry
                    $entryText = $utf8Strict.GetString($entryBytes)
                    if (
                        $entryBytes.Length -ge 3 -and
                        $entryBytes[0] -eq 0xEF -and
                        $entryBytes[1] -eq 0xBB -and
                        $entryBytes[2] -eq 0xBF
                    ) {
                        throw "UTF-8 BOM is not allowed"
                    }
                    if ($entryText.IndexOf([char]0xFFFD) -ge 0) {
                        throw "replacement character U+FFFD is present"
                    }
                    if ([System.Text.RegularExpressions.Regex]::IsMatch($entryText, "[\uE000-\uF8FF]")) {
                        throw "private-use characters associated with mojibake are present"
                    }

                    Test-MojibakeMarkers -Label $entryName -Text $entryText
                    Test-RequiredMarkers -RelativePath $entryName -Text $entryText

                    $repoBytes = [System.IO.File]::ReadAllBytes((Join-Path $repoRoot ($coreFile -replace "/", "\")))
                    if ((Get-BytesSha256 $entryBytes) -ne (Get-BytesSha256 $repoBytes)) {
                        throw "content hash differs from repository file"
                    }
                }
                catch {
                    Write-Fail "$entryName in archive: $($_.Exception.Message)"
                }
            }
        }
        finally {
            $archive.Dispose()
        }

        if ($failureCount -eq 0) {
            Write-Pass "$($manifest.archive) is strict UTF-8 and matches repository core files"
        }
    }

    if ([string]::IsNullOrWhiteSpace($ValidatorPath)) {
        $validatorCandidates = @()
        if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
            $validatorCandidates += Join-Path $env:CODEX_HOME "skills\.system\skill-creator\scripts\quick_validate.py"
        }
        if (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
            $validatorCandidates += Join-Path $env:USERPROFILE ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
        }
        $ValidatorPath = [string]($validatorCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1)
    }

    if ([string]::IsNullOrWhiteSpace($ValidatorPath)) {
        Write-Skip "skill validator was not found; pass -ValidatorPath to enable it"
    }
    elseif (-not (Test-Path -LiteralPath $ValidatorPath -PathType Leaf)) {
        Write-Fail "skill validator does not exist: $ValidatorPath"
    }
    elseif ($null -eq (Get-Command py -ErrorAction SilentlyContinue)) {
        Write-Fail "Python launcher 'py' is not available"
    }
    else {
        $creatorEncodingReady = $true
        try {
            $readEncodingPattern = 'read_text\(\s*encoding\s*=\s*["'']utf-8["'']\s*\)'
            $writeEncodingPattern = 'output_path\.write_text\([\s\S]{0,200}?encoding\s*=\s*["'']utf-8["'']'

            $validatorSource = (Read-StrictUtf8 $ValidatorPath).Text
            if (-not [System.Text.RegularExpressions.Regex]::IsMatch($validatorSource, $readEncodingPattern)) {
                throw "quick_validate.py does not declare UTF-8 when reading SKILL.md"
            }

            $generatorPath = Join-Path (Split-Path -Parent $ValidatorPath) "generate_openai_yaml.py"
            if (-not (Test-Path -LiteralPath $generatorPath -PathType Leaf)) {
                throw "generate_openai_yaml.py is missing beside the validator"
            }

            $generatorSource = (Read-StrictUtf8 $generatorPath).Text
            if (-not [System.Text.RegularExpressions.Regex]::IsMatch($generatorSource, $readEncodingPattern)) {
                throw "generate_openai_yaml.py does not declare UTF-8 when reading SKILL.md"
            }
            if (-not [System.Text.RegularExpressions.Regex]::IsMatch($generatorSource, $writeEncodingPattern)) {
                throw "generate_openai_yaml.py does not declare UTF-8 when writing openai.yaml"
            }
        }
        catch {
            $creatorEncodingReady = $false
            Write-Fail "skill-creator runtime encoding contract: $($_.Exception.Message)"
        }

        if ($creatorEncodingReady) {
            Write-Pass "skill-creator readers and writer declare UTF-8 explicitly"
        }

        & py -3 $ValidatorPath (Join-Path $repoRoot "claim")
        if ($LASTEXITCODE -ne 0) {
            Write-Fail "skill validator failed under the default Python runtime"
        }
        else {
            Write-Pass "skill validator passed under the default Python runtime"
        }
    }

    if ([string]::IsNullOrWhiteSpace($InstalledSkillPath)) {
        $installedCandidates = @()
        if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
            $installedCandidates += Join-Path $env:CODEX_HOME "skills\claim"
        }
        if (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
            $installedCandidates += Join-Path $env:USERPROFILE ".codex\skills\claim"
        }
        $InstalledSkillPath = [string]($installedCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Container } | Select-Object -First 1)
    }

    if ([string]::IsNullOrWhiteSpace($InstalledSkillPath)) {
        Write-Skip "installed Claim skill was not found; pass -InstalledSkillPath to compare it"
    }
    elseif (-not (Test-Path -LiteralPath $InstalledSkillPath -PathType Container)) {
        Write-Fail "installed Claim skill does not exist: $InstalledSkillPath"
    }
    else {
        foreach ($coreFile in $manifest.core_files) {
            $insideSkillPath = $coreFile -replace "^claim/", ""
            $repoFilePath = Join-Path $repoRoot ($coreFile -replace "/", "\")
            $installedFilePath = Join-Path $InstalledSkillPath ($insideSkillPath -replace "/", "\")
            if (-not (Test-Path -LiteralPath $installedFilePath -PathType Leaf)) {
                Write-Fail "installed file is missing: $insideSkillPath"
                continue
            }

            try {
                $installedRecord = Read-StrictUtf8 $installedFilePath
                Test-MojibakeMarkers -Label "installed/$insideSkillPath" -Text $installedRecord.Text
                Test-RequiredMarkers -RelativePath $coreFile -Text $installedRecord.Text
                if (
                    (Get-FileHash -LiteralPath $repoFilePath -Algorithm SHA256).Hash -ne
                    (Get-FileHash -LiteralPath $installedFilePath -Algorithm SHA256).Hash
                ) {
                    throw "content hash differs from repository file"
                }
            }
            catch {
                Write-Fail "installed/${insideSkillPath}: $($_.Exception.Message)"
            }
        }

        if ($failureCount -eq 0) {
            Write-Pass "installed Claim skill is strict UTF-8 and matches repository core files"
        }
    }
}
catch {
    Write-Fail $_.Exception.Message
}
finally {
    Pop-Location
}

if ($failureCount -gt 0) {
    Write-Host "Encoding validation failed with $failureCount error(s)." -ForegroundColor Red
    exit 1
}

Write-Host "Claim encoding validation passed." -ForegroundColor Green
exit 0
