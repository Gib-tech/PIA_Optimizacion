# BTTask_Roam

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_Roam`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Una acción de patrulla. Escoge destino navegable y termina o aborta para devolver el control al Behavior Tree.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_AIMoveTo`, `FinishExecute`, `FinishExecute`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_Roam`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnSuccess_9928681640477A1A6E9FE4BC4FE9C57C`** en `OnSuccess_9928681640477A1A6E9FE4BC4FE9C57C`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_Roam`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnFail_9928681640477A1A6E9FE4BC4FE9C57C`** en `OnFail_9928681640477A1A6E9FE4BC4FE9C57C`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_Roam`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `RoamRadius` — tipo `real`.
- `Acceptance Radius` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 17 nodos con pines. Funciones referenciadas: `FinishExecute`, `K2_GetActorLocation`, `K2_GetRandomReachablePointInRadius`, `ReceiveExecuteAI`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `744b98adf213350d23107a33eb55579d3864f0c1dcb95be0d1a5b5303017d472`.
