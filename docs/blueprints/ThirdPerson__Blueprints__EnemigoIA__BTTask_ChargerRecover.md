# BTTask_ChargerRecover

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_ChargerRecover`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Pausa breve de recuperación de la embestida. Finaliza/aborta para ceder la siguiente decisión al árbol.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `SetValueAsBool`, `FinishExecute`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ChargerRecover`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `CachedPawn` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 12 nodos con pines. Funciones referenciadas: `FinishExecute`, `GetBlackboard`, `MakeLiteralName`, `ReceiveExecuteAI`, `SetValueAsBool`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `f347123963e8d4df9833bbbf0d2ea6ee1cf2ad348b48e0e838d1235111d2cfef`.
