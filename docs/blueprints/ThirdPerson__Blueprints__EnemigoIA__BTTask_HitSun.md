# BTTask_HitSun

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_HitSun`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Acción de aturdimiento; el nombre histórico HitSun se conserva para no romper referencias. Interrumpe el ataque y permite recuperación temporal antes de volver al árbol.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `PlayAnimMontage`, `Delay`, `SetValueAsBool`, `PrintString`, `FinishExecute`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `StopAnimMontage`, `FinishAbort`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `ReceiveAbortAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_HitSun`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_HitSun`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `CachedPawn` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 24 nodos con pines. Funciones referenciadas: `ActorHasTag`, `Delay`, `FinishAbort`, `FinishExecute`, `GetBlackboard`, `MakeLiteralName`, `Not_PreBool`, `PlayAnimMontage`, `PrintString`, `ReceiveAbortAI`, `ReceiveExecuteAI`, `SetValueAsBool`, `StopAnimMontage`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyHit_Entrega.AM_EnemyHit_Entrega`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `d12f13f028994c8566e00971266d8c9b042543b1139969786f836765707e5ad1`.
