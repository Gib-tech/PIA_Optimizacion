# BTTask_ChargerRetreat

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_ChargerRetreat`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Retirada local navegable respecto al objetivo de combate real. Limita longitud y duración para mantener al rival en el encuentro y evitar recorridos lejanos.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `Asignar Elapsed`, `K2_ClearFocus`, `Asignar MaxWalkSpeed`, `Asignar BestDistance`, `Asignar RetreatGoal`, `FindPathToLocationSynchronously`, `Condición`, `Asignar RetreatGoal`, `Secuencia`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar Elapsed`, `Condición`, `StopMovement`, `Condición`, `Asignar MaxWalkSpeed`, `FinishExecute`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `StopMovement`, `Asignar MaxWalkSpeed`, `FinishAbort`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerRetreat`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerRetreat`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `ReceiveAbortAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerRetreat`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Elapsed` — tipo `real`.
- `BestDistance` — tipo `real`.
- `CachedPawn` — tipo `object`.
- `RetreatGoal` — tipo `struct`.

## Operaciones y dependencias verificadas

La exportación contiene 167 nodos con pines. Funciones referenciadas: `Abs`, `Add_DoubleDouble`, `Add_VectorVector`, `BooleanAND`, `FindPathToLocationSynchronously`, `FinishAbort`, `FinishExecute`, `GetPathLength`, `GreaterEqual_DoubleDouble`, `IsPartial`, `IsValid`, `K2_ClearFocus`, `K2_GetActorLocation`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `MoveToLocation`, `Multiply_VectorFloat`, `Not_PreBool`, `ReceiveAbortAI`, `ReceiveExecuteAI`, `ReceiveTickAI`, `RotateAngleAxis`, `StopMovement`, `Subtract_DoubleDouble`, `Subtract_VectorVector`, `Vector_Distance2D`, `Vector_Normal2D`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `40e92c1e67ba6483b257100f668dfd2f901511d25c4e65001c6cf1666e7262ff`.
