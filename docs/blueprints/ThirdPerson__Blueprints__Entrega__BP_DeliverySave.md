# BP_DeliverySave

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySave`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.SaveGame'"`.

Datos locales de checkpoint, esquema 2 con extensiones aditivas. Sólo escalares y transforms; no guarda referencias a actores del mapa. Incluye aliados, encuentros, balizas/puertas, secuencia/tiempo e inventario.

## Entradas y responsabilidades del grafo

Este Blueprint contiene datos, configuración o un rig. No presenta una entrada de ejecución K2 propia que describir como lógica de gameplay.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Version` — tipo `int`.
- `Paso` — tipo `int`.
- `PlayerHealth` — tipo `real`.
- `PlayerLocation` — tipo `struct`.
- `PlayerRotation` — tipo `struct`.
- `ControlRotation` — tipo `struct`.
- `HammerUpgraded` — tipo `bool`.
- `HammerEquipped` — tipo `bool`.
- `HostageHealth` — tipo `real`.
- `HostageLocation` — tipo `struct`.
- `HostageRotation` — tipo `struct`.
- `Rescued` — tipo `bool`.
- `Accompanying` — tipo `bool`.
- `Waiting` — tipo `bool`.
- `Zone1Cleared` — tipo `bool`.
- `Zone1Wave` — tipo `int`.
- `Zone1Phase` — tipo `int`.
- `Zone1Spawned` — tipo `int`.
- `Zone2Cleared` — tipo `bool`.
- `Zone2Wave` — tipo `int`.
- `Zone2Phase` — tipo `int`.
- `Zone2Spawned` — tipo `int`.
- `Door1Health` — tipo `real`.
- `Door1Unlocked` — tipo `bool`.
- `Door1Destroyed` — tipo `bool`.
- `Door1Cracked` — tipo `bool`.
- `Beacon1Activated` — tipo `bool`.
- `Door2Health` — tipo `real`.
- `Door2Unlocked` — tipo `bool`.
- `Door2Destroyed` — tipo `bool`.
- `Door2Cracked` — tipo `bool`.
- `Beacon2Activated` — tipo `bool`.
- `Door3Health` — tipo `real`.
- `Door3Unlocked` — tipo `bool`.
- `Door3Destroyed` — tipo `bool`.
- `Door3Cracked` — tipo `bool`.
- `Beacon3Activated` — tipo `bool`.
- `OrderCode` — tipo `int`.
- `MissionElapsed` — tipo `real`.
- `OrderCode_0` — tipo `int`.
- `MissionElapsed_0` — tipo `real`.
- `FinalStandRevision` — tipo `int`.
- `OrderRevealed` — tipo `bool`.
- `Zone3Cleared` — tipo `bool`.
- `Zone3Wave` — tipo `int`.
- `Zone3Phase` — tipo `int`.
- `Zone3Spawned` — tipo `int`.
- `ExtrasRevision` — tipo `int`.
- `Botiquines` — tipo `int`.
- `Cargas` — tipo `int`.
- `Creditos` — tipo `int`.
- `WorldSeconds` — tipo `real`.
- `Recogido1` — tipo `bool`.
- `Recogido2` — tipo `bool`.
- `Recogido3` — tipo `bool`.
- `Recogido4` — tipo `bool`.
- `FirstPerson` — tipo `bool`.
- `RobotEnergy` — tipo `int`.
- `bFabricating` — tipo `bool`.
- `FabricationProgress` — tipo `real`.
- `MesaRecogido1` — tipo `bool`.
- `MesaRecogido2` — tipo `bool`.
- `MesaRecogido3` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 0 nodos con pines. Funciones referenciadas: .


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `de045ce7e8a5cd9e8f766d226cbb05bc1280cdd88f69d01a1232539e40abb310`.
