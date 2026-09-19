param(
    [Parameter(Mandatory=$true)][string]$QtRoot,
    [string]$EngineRoot = "$PSScriptRoot/../engine",
    [string]$DesktopRoot = "$PSScriptRoot/../desktop",
    [string]$Generator = "Visual Studio 18 2026",
    [int]$Jobs = 6,
    [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
$taskRoot = (Resolve-Path "$PSScriptRoot/..").Path
$EngineRoot = (Resolve-Path $EngineRoot).Path
$DesktopRoot = (Resolve-Path $DesktopRoot).Path
$QtRoot = (Resolve-Path $QtRoot).Path
$taskBuild = "$taskRoot/build/native"
$taskRelease = "$taskRoot/releases/AstroDB"

function Invoke-CMake {
    & cmake @args
    if($LASTEXITCODE -ne 0) { throw "CMake failed: $args" }
}

& $Python "$PSScriptRoot/prepare_sqlite.py" "$taskBuild/sqlite"
if($LASTEXITCODE -ne 0) { throw "SQLite preparation failed" }
Invoke-CMake -S "$taskBuild/sqlite" -B "$taskBuild/sqlite/build" -G $Generator -A x64
Invoke-CMake --build "$taskBuild/sqlite/build" --config Release --parallel $Jobs
Invoke-CMake -S $EngineRoot -B "$EngineRoot/build/astro" -G $Generator -A x64 "-DBUILD_UNITTESTS=OFF" "-DDISABLE_UNITY=ON" "-DOVERRIDE_GIT_DESCRIBE=v2.0.0" "-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
Invoke-CMake --build "$EngineRoot/build/astro" --config Release --target shell duckdb --parallel $Jobs
Invoke-CMake -S $DesktopRoot -B "$DesktopRoot/build/astro" -G $Generator -A x64 "-DQT_MAJOR=Qt6" "-DCMAKE_PREFIX_PATH=$QtRoot" "-DSQLite3_INCLUDE_DIR=$taskBuild/sqlite/sqlite-amalgamation-3530400" "-DSQLite3_LIBRARY=$taskBuild/sqlite/build/Release/sqlite3.lib" "-DASTRODB_ENGINE_ROOT=$EngineRoot" "-DASTRODB_ENGINE_LIBRARY=$EngineRoot/build/astro/src/Release/astrodb_engine.lib" "-DFORCE_INTERNAL_QSCINTILLA=ON" "-DBUILD_STABLE_VERSION=ON" "-DBUILD_ASTRODB_TESTS=ON" "-DENABLE_TESTING=ON" "-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
Invoke-CMake --build "$DesktopRoot/build/astro" --config Release --parallel $Jobs

$env:PATH = "$QtRoot/bin;$EngineRoot/build/astro/src/Release;$env:PATH"
$env:QT_QPA_PLATFORM = "offscreen"
& ctest --test-dir "$DesktopRoot/build/astro" -C Release --output-on-failure
if($LASTEXITCODE -ne 0) { throw "Native tests failed" }
& $Python "$PSScriptRoot/test_native.py" "$EngineRoot/build/astro/Release/astrodb.exe"
if($LASTEXITCODE -ne 0) { throw "Native shell tests failed" }

New-Item -ItemType Directory -Force -Path $taskRelease | Out-Null
Copy-Item -LiteralPath "$EngineRoot/build/astro/Release/astrodb.exe" -Destination $taskRelease
Copy-Item -LiteralPath "$EngineRoot/build/astro/src/Release/astrodb_engine.dll" -Destination $taskRelease
Copy-Item -LiteralPath "$DesktopRoot/build/astro/Release/AstroDB Desktop.exe" -Destination $taskRelease
& "$QtRoot/bin/windeployqt.exe" --release --no-translations --no-compiler-runtime "$taskRelease/AstroDB Desktop.exe"
if($LASTEXITCODE -ne 0) { throw "Qt deployment failed" }
$taskLicenses = "$taskRelease/licenses"
New-Item -ItemType Directory -Force -Path $taskLicenses | Out-Null
Copy-Item -LiteralPath "$EngineRoot/LICENSE" -Destination "$taskLicenses/Engine-MIT.txt"
Get-ChildItem -LiteralPath $DesktopRoot -Filter "LICENSE*" | Copy-Item -Destination $taskLicenses
Get-ChildItem -LiteralPath "$QtRoot" -Filter "LICENSE*" | Copy-Item -Destination $taskLicenses
if(Test-Path "$QtRoot/sbom") {
    Copy-Item -LiteralPath "$QtRoot/sbom" -Destination "$taskLicenses/Qt-SBOM" -Recurse -Force
}
& $Python "$PSScriptRoot/package_licenses.py" $EngineRoot $DesktopRoot $taskLicenses
if($LASTEXITCODE -ne 0) { throw "License packaging failed" }
Copy-Item -LiteralPath "$taskRoot/THIRD_PARTY_NOTICES.md" -Destination $taskLicenses
$taskVswhere = "${env:ProgramFiles(x86)}/Microsoft Visual Studio/Installer/vswhere.exe"
$taskVs = & $taskVswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
$taskCrt = Get-ChildItem "$taskVs/VC/Redist/MSVC/*/x64/Microsoft.VC*.CRT" -Directory | Sort-Object FullName -Descending | Select-Object -First 1
if(!$taskCrt) { throw "Visual C++ runtime directory not found" }
Get-ChildItem -LiteralPath $taskCrt.FullName -Filter "*.dll" | Copy-Item -Destination $taskRelease
Copy-Item -LiteralPath "$taskRoot/README.md" -Destination $taskRelease
Write-Output "Built AstroDB in $taskRelease"
