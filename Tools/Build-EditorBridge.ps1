$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskPlugin=Join-Path $PSScriptRoot 'EditorBridge/BlueprintBuildBridge.uplugin'
$taskPackage=Join-Path $taskRoot 'Intermediate/BPB3'
& 'C:/Program Files/Epic Games/UE_5.6/Engine/Build/BatchFiles/RunUAT.bat' BuildPlugin "-Plugin=$taskPlugin" "-Package=$taskPackage" -TargetPlatforms=Win64 -NoDeleteHostProject -Unversioned -UTF8Output
if($LASTEXITCODE -ne 0){throw "Editor helper build failed: $LASTEXITCODE"}
