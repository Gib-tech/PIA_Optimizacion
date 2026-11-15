param(
    [ValidateSet('Development','Shipping')]
    [string]$Configuration = 'Development',
    [string]$EngineDirectory = 'C:/Program Files/Epic Games/UE_5.6'
)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskProject = Join-Path $taskRoot 'Terreno.uproject'
$taskOutput = Join-Path $taskRoot 'Deliverables'
$taskUat = Join-Path $EngineDirectory 'Engine/Build/BatchFiles/RunUAT.bat'
if (-not (Test-Path -LiteralPath $taskUat)) { throw "UAT not found: $taskUat" }
if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) {
    throw 'Save and close Unreal Editor before building; Live Coding prevents the build.'
}
New-Item -ItemType Directory -Path $taskOutput -Force | Out-Null
& $taskUat BuildCookRun "-project=$taskProject" -noP4 -platform=Win64 "-clientconfig=$Configuration" -build -cook '-map=/Game/LevelMenu/MainMenuLevel+/Game/ThirdPerson/Maps/Nivel_Entrega' -stage -pak -archive "-archivedirectory=$taskOutput" -utf8output -unattended 2>&1 | Tee-Object -FilePath (Join-Path $taskOutput 'build.log')
if ($LASTEXITCODE -ne 0) { throw "Packaging failed with exit code $LASTEXITCODE. See Deliverables/build.log." }
Write-Output "Windows package: $taskOutput/Windows"
