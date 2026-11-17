# BP_GameInstance

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/BP_GameInstance`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.GameInstance'"`.

Persiste intención de Nuevo juego/Continuar y datos entre cambios de mapa. El disco lo gestiona el SaveManager de entrega; conserva las interfaces de guardado originales como historia.

## Entradas y responsabilidades del grafo

- **`SaveGame`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `K2Node_AsyncAction`, `SaveGameToSlot`, `K2Node_CallDelegate`, `K2Node_CallDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`RequestSave`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetAllActorsWithInterface`, `SaveData`, `SaveGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`CreateSaveGame`** en `EventGraph`. Operaciones alcanzables desde `then`: `CreateSaveGameObject`, `Asignar SaveGameVar`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`RequestLoad`** en `EventGraph`. Operaciones alcanzables desde `then`: `LoadingRequested`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`LoadGame`** en `EventGraph`. Operaciones alcanzables desde `then`: `DoesSaveGameExist`, `Condición`, `Condición`, `K2Node_AsyncAction`, `LoadGameFromSlot`, `K2Node_DynamicCast`, `K2Node_DynamicCast`, `Asignar SaveGameVar`, `Asignar SaveGameVar`, `K2Node_CallDelegate`, `K2Node_CallDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GameSaved`** en `GameSaved`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`GameLoaded`** en `GameLoaded`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`LoadGame`** en `LoadGame`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`RequestLoad`** en `RequestLoad`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`CreateSaveGame`** en `CreateSaveGame`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`RequestSave`** en `RequestSave`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveGame`** en `SaveGame`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Completed_FADCE93345AD81DE8189588E3467B3F8`** en `Completed_FADCE93345AD81DE8189588E3467B3F8`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Completed_0FF322BE40C6B7256B2DEEBF69ED6B45`** en `Completed_0FF322BE40C6B7256B2DEEBF69ED6B45`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_GameInstance`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `SaveGameVar` — tipo `object`.
- `Slot Name` — tipo `string`.
- `GameSaved` — tipo `mcdelegate`.
- `GameLoaded` — tipo `mcdelegate`.
- `bDeliveryContinue` — tipo `bool`.
- `LastBeaconOrder` — tipo `int`.
- `LastBeaconOrder_0` — tipo `int`.

## Operaciones y dependencias verificadas

La exportación contiene 56 nodos con pines. Funciones referenciadas: `CreateSaveGame`, `CreateSaveGameObject`, `DoesSaveGameExist`, `GameLoaded`, `GameSaved`, `GetAllActorsWithInterface`, `LoadGame`, `LoadGameFromSlot`, `LoadingRequested`, `RequestLoad`, `RequestSave`, `SaveData`, `SaveGame`, `SaveGameToSlot`.

- `/Game/LevelMenu/BP_SaveGame.BP_SaveGame_C`
- `/Game/LevelMenu/BP_SaveInterface.BP_SaveInterface_C`
- `/Game/LevelMenu/BP_Saveable.BP_Saveable_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `b2e493a7face3e331abc27276f25a22761a46059ca2405d35b932b37730ad8c2`.
