# BTTask_ChargerCharge

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_ChargerCharge`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Desplazamiento rápido hacia el punto comprometido. Al llegar se detiene y solicita el montaje cercano; UpdateStrike comprueba contacto durante la animación. Abortar cancela daño pendiente y recupera velocidad.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `Asignar Elapsed`, `Asignar RepathAt`, `Asignar bAttackStarted`, `Asignar GlobalAnimRateScale`, `Asignar MaxWalkSpeed`, `MoveToLocation`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar Elapsed`, `Condición`, `UpdateStrike`, `Condición`, `Condición`, `StopMovement`, `Condición`, `StopMovement`, `Asignar GlobalAnimRateScale`, `StopMovement`, `Condición`, `Asignar GlobalAnimRateScale`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `StopMovement`, `Asignar GlobalAnimRateScale`, `EndAttack`, `Asignar MaxWalkSpeed`, `SetValueAsBool`, `SetValueAsBool`, `FinishAbort`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `ReceiveAbortAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerCharge`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerCharge`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerCharge`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Elapsed` — tipo `real`.
- `bHit` — tipo `bool`.
- `CachedPawn` — tipo `object`.
- `bAttackStarted` — tipo `bool`.
- `RepathAt` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 110 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_VectorVector`, `Attack`, `BooleanAND`, `BreakRotator`, `Dot_VectorVector`, `EndAttack`, `FMin`, `FindLookAtRotation`, `FinishAbort`, `FinishExecute`, `GetActorForwardVector`, `GetBlackboard`, `GetDistanceTo`, `GetValueAsVector`, `GetVelocity`, `GreaterEqual_DoubleDouble`, `K2_GetActorLocation`, `K2_GetActorRotation`, `K2_SetActorRotation`, `LessEqual_DoubleDouble`, `LineOfSightTo`, `MakeLiteralName`, `MakeRotator`, `MoveToLocation`, `Multiply_VectorFloat`, `RInterpTo_Constant`, `ReceiveAbortAI`, `ReceiveExecuteAI`, `ReceiveTickAI`, `SetValueAsBool`, `StopMovement`, `Subtract_VectorVector`, `UpdateStrike`, `Vector_Normal2D`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `7870475a0760270a687150bfb2eb356e58f54a84fed23acd0cee2e7b0c67852c`.
