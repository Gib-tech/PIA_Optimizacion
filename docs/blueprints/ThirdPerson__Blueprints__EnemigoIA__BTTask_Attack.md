# BTTask_Attack

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_Attack`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Acerca y alinea al orbitador antes de solicitar Attack. Durante la ejecución actualiza la ventana del golpe mediante UpdateStrike. Finalización y aborto detienen movimiento y cancelan el ataque.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `Asignar StrikeTarget`, `Asignar Elapsed`, `Asignar RepathAt`, `Asignar bAttackStarted`, `K2_SetFocus`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar Elapsed`, `Condición`, `UpdateStrike`, `Condición`, `Condición`, `StopMovement`, `Condición`, `StopMovement`, `EndAttack`, `StopMovement`, `Condición`, `EndAttack`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `StopMovement`, `EndAttack`, `FinishAbort`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `ReceiveAbortAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_Attack`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_Attack`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_Attack`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Target` — tipo `struct`.
- `Elapsed` — tipo `real`.
- `bHit` — tipo `bool`.
- `Enemy` — tipo `object`.
- `Elapsed_0` — tipo `real`.
- `bHit_0` — tipo `bool`.
- `Enemy_0` — tipo `object`.
- `CachedPawn` — tipo `object`.
- `StrikeTarget` — tipo `object`.
- `bAttackStarted` — tipo `bool`.
- `RepathAt` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 79 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Attack`, `BreakRotator`, `Dot_VectorVector`, `EndAttack`, `FMin`, `FindLookAtRotation`, `FinishAbort`, `FinishExecute`, `GetActorForwardVector`, `GetDistanceTo`, `GreaterEqual_DoubleDouble`, `K2_GetActorLocation`, `K2_GetActorRotation`, `K2_SetActorRotation`, `K2_SetFocus`, `LessEqual_DoubleDouble`, `MakeRotator`, `MoveToLocation`, `RInterpTo_Constant`, `ReceiveAbortAI`, `ReceiveExecuteAI`, `ReceiveTickAI`, `StopMovement`, `Subtract_VectorVector`, `UpdateStrike`, `Vector_Normal2D`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `768d864eb77996b814fe64d6cbf3b37f1cf88818c37a78c865509bdefecd5b59`.
