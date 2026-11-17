$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$taskProject = Join-Path $taskRoot 'Terreno.uproject'
$taskPlugin = Join-Path $taskRoot 'Intermediate/BPB3/BlueprintBuildBridge.uplugin'
if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) { throw 'Close the saved editor first.' }
Start-Process -FilePath 'C:/Program Files/Epic Games/UE_5.6/Engine/Binaries/Win64/UnrealEditor.exe' -ArgumentList @(('"' + $taskProject + '"'), '/Game/ThirdPerson/Maps/Nivel_Entrega', ('-PLUGIN="' + $taskPlugin + '"')) -WindowStyle Hidden
