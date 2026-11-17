# BP_Hostage

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Character'"`.

Aliado escoltado con salud propia y cápsula que bloquea al protagonista. Interactuar rescata o reanuda seguimiento sólo si está a salvo; percepción y movimiento pertenecen a BT_Hostage. Recibir daño actualiza salud/aviso; morir termina la misión. La apariencia usa el sobreviviente existente, con copia propia de malla/esqueleto/AnimBlueprint.

## Entradas y responsabilidades del grafo

- **`ReceiveAnyDamage`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Condición`, `Asignar Health`, `Asignar InvulnerableUntil`, `Asignar DamageNoticeSerial`, `Condición`, `Asignar bIsDead`, `Asignar bUsingBeacon`, `DisableMovement`, `GetActorOfClass`, `Asignar Paso`, `GetActorOfClass`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Interactuar`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `SetValueAsBool`, `SetValueAsBool`, `SetValueAsBool`, `SetValueAsInt`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Interactuar`** en `Interactuar`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_Hostage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAnyDamage`** en `ReceiveAnyDamage`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Hostage`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Health` — tipo `real`.
- `MaxHealth` — tipo `real`.
- `bIsDead` — tipo `bool`.
- `InvulnerableUntil` — tipo `real`.
- `bUsingBeacon` — tipo `bool`.
- `ActivationProgress` — tipo `real`.
- `DamageNoticeSerial` — tipo `int`.

## Operaciones y dependencias verificadas

La exportación contiene 75 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_IntInt`, `BooleanAND`, `BooleanOR`, `DisableMovement`, `FMax`, `GetActorOfClass`, `GetBlackboard`, `GetController`, `GetDistanceTo`, `GetPlayerPawn`, `GetTimeSeconds`, `GetValueAsBool`, `GreaterEqual_DoubleDouble`, `Greater_DoubleDouble`, `Interactuar`, `IsValid`, `LessEqual_DoubleDouble`, `MakeLiteralName`, `Not_PreBool`, `ReceiveAnyDamage`, `SetGamePaused`, `SetValueAsBool`, `SetValueAsInt`, `StartOutcome`, `Subtract_DoubleDouble`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `f435ca8a5c37f66f02168733f5a485b43b3fe557155b05fc0ce735570bbf2fe8`.
