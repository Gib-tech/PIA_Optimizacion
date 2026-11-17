# BTTask_ChargerWindup

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_ChargerWindup`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Anticipación visible de la embestida. Orienta al rival, comprueba visión y calcula ChargeGoal con predicción breve. Todavía no produce el golpe cercano.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `StopMovement`, `Asignar Elapsed`, `K2_SetFocus`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar Elapsed`, `K2_SetActorRotation`, `Condición`, `Condición`, `SetValueAsVector`, `FinishExecute`, `Asignar ChargeVictim`, `SetValueAsBool`, `FinishExecute`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `FinishAbort`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `ReceiveAbortAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerWindup`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerWindup`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerWindup`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Elapsed` — tipo `real`.
- `CachedPawn` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 53 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_VectorVector`, `BooleanAND`, `BreakRotator`, `FMin`, `FindLookAtRotation`, `FinishAbort`, `FinishExecute`, `GetBlackboard`, `GetVelocity`, `GreaterEqual_DoubleDouble`, `IsValid`, `K2_GetActorLocation`, `K2_GetActorRotation`, `K2_SetActorRotation`, `K2_SetFocus`, `LineOfSightTo`, `MakeLiteralName`, `MakeRotator`, `Multiply_VectorFloat`, `RInterpTo_Constant`, `ReceiveAbortAI`, `ReceiveExecuteAI`, `ReceiveTickAI`, `SetValueAsBool`, `SetValueAsVector`, `StopMovement`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `36cba809f5402e852f55bfbb032422c32404ad8270dc61c169ae9c20828623c3`.
