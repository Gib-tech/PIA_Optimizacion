# BP_DeliverySaveManager

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Valida momentos seguros, serializa checkpoint y restaura mundo/aliados/cámara. Reintenta hitos pendientes cuando termina el peligro. No sobrescribe un checkpoint seguro en mitad de una oleada, ataque, huida, canalización o desenlace.

## Entradas y responsabilidades del grafo

- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `GetActorOfClass`, `Condición`, `Asignar bSaveSucceeded`, `K2Node_DynamicCast`, `Condición`, `Asignar Hero`, `CreateSaveGameObject`, `Asignar StatusText`, `GetActorOfClass`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InitializeCheckpoint`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Hero`, `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Hostage`, `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Director`, `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar Extras`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla F5`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Asignar bSaveSucceeded`, `Condición`, `CreateSaveGameObject`, `Asignar StatusText`, `K2Node_DynamicCast`, `Asignar SaveData`, `Asignar Version`, `Asignar FinalStandRevision`, `Asignar ExtrasRevision`, `Asignar OrderCode`, `Asignar MissionElapsed`, `Asignar OrderRevealed`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveCheckpoint`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bSaveSucceeded`, `Condición`, `CreateSaveGameObject`, `Asignar StatusText`, `K2Node_DynamicCast`, `Asignar SaveData`, `Asignar Version`, `Asignar FinalStandRevision`, `Asignar ExtrasRevision`, `Asignar OrderCode`, `Asignar MissionElapsed`, `Asignar OrderRevealed`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`RestoreCheckpoint`** en `EventGraph`. Operaciones alcanzables desde `then`: `LoadGameFromSlot`, `K2Node_DynamicCast`, `Asignar SaveData`, `Asignar bSaveSucceeded`, `Condición`, `Condición`, `Asignar OrderCode`, `Asignar StatusText`, `CreateSaveGameObject`, `Asignar StatusText`, `Asignar MissionElapsed`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`RestoreCheckpoint`** en `RestoreCheckpoint`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliverySaveManager`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveCheckpoint`** en `SaveCheckpoint`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliverySaveManager`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InitializeCheckpoint`** en `InitializeCheckpoint`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliverySaveManager`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliverySaveManager`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_F5_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliverySaveManager`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `bInitialized` — tipo `bool`.
- `bSaveSucceeded` — tipo `bool`.
- `bHasCheckpoint` — tipo `bool`.
- `StatusText` — tipo `string`.
- `SaveData` — tipo `object`.
- `Hero` — tipo `object`.
- `Hostage` — tipo `object`.
- `Director` — tipo `object`.
- `Instance` — tipo `object`.
- `bRestoring` — tipo `bool`.
- `Beacon1` — tipo `object`.
- `Beacon2` — tipo `object`.
- `Beacon3` — tipo `object`.
- `StatusSerial` — tipo `int`.
- `Extras` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 586 nodos con pines. Funciones referenciadas: `Add_IntInt`, `BooleanAND`, `BooleanOR`, `CreateSaveGameObject`, `EnableInput`, `EqualEqual_IntInt`, `GetActorOfClass`, `GetBlackboard`, `GetControlRotation`, `GetGameInstance`, `GetPlayerController`, `GetValueAsBool`, `GreaterEqual_IntInt`, `Greater_DoubleDouble`, `Greater_IntInt`, `Increase_Health`, `InitializeCheckpoint`, `InputActionHandlerDynamicSignature__DelegateSignature`, `IsMovingOnGround`, `K2_GetActorLocation`, `K2_GetActorRotation`, `K2_SetActorLocationAndRotation`, `Less_IntInt`, `LoadGameFromSlot`, `MakeLiteralName`, `NotEqual_BoolBool`, `NotEqual_DoubleDouble`, `NotEqual_IntInt`, `Not_PreBool`, `ReceiveTick`, `RestoreCheckpoint`, `SaveCheckpoint`, `SaveGameToSlot`, `SelectInt`, `SetActive`, `SetActorEnableCollision`, `SetActorHiddenInGame`, `SetControlRotation`, `SetMaterial`, `SetStaticMesh`, `SetValueAsBool`, `SetVisibility`, `UserConstructionScript`.

- `/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C`
- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySave.BP_DeliverySave_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestructibleDoor.BP_DestructibleDoor_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C`
- `/Game/ThirdPerson/Environment/Progression/M_DoorPowered.M_DoorPowered`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `9f83719eb3aa796bef9005d6a94d6c8ce0e169c72e330aceb8cf03a85efa8305`.
