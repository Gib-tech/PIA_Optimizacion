# BP_DirectorEntrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Coordina rescate, tres encuentros, orden aleatorio de balizas y extracción conjunta. Paso 0–3 representa avance de balizas; 4 victoria, 5 derrota del jugador y 6 derrota del rehén. El cronómetro y las señales se suspenden durante la revelación. No decide las acciones de los enemigos.

## Entradas y responsabilidades del grafo

- **`Tecla E`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `GetActorOfClass`, `Interactuar`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_RightShoulder`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `GetActorOfClass`, `Interactuar`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `Secuencia`, `Asignar CurrentBeacon`, `Condición`, `Condición`, `Secuencia`, `Condición`, `GetActorOfClass`, `GetActorOfClass`, `K2Node_DynamicCast`, `K2Node_DynamicCast`, `Asignar Paso`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Enter`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `SetGamePaused`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla R`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `SetGamePaused`, `K2Node_DynamicCast`, `Asignar bDeliveryContinue`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar OrderCode`, `Condición`, `Asignar OrderCode`, `Asignar LastBeaconOrder`, `Asignar CurrentBeacon`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_FaceButton_Bottom`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `SetGamePaused`, `K2Node_DynamicCast`, `Asignar bDeliveryContinue`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_DPad_Down`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `SetGamePaused`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_DPad_Down_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_FaceButton_Bottom_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_R_K2Node_InputKeyEvent_2`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Enter_K2Node_InputKeyEvent_3`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_RightShoulder_K2Node_InputKeyEvent_4`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_E_K2Node_InputKeyEvent_5`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DirectorEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Baliza1` — tipo `object`.
- `Baliza2` — tipo `object`.
- `Baliza3` — tipo `object`.
- `Salida` — tipo `object`.
- `Paso` — tipo `int`.
- `Zona1` — tipo `object`.
- `Zona2` — tipo `object`.
- `OrderCode` — tipo `int`.
- `MissionElapsed` — tipo `real`.
- `CurrentBeacon` — tipo `object`.
- `OrderCode_0` — tipo `int`.
- `MissionElapsed_0` — tipo `real`.
- `CurrentBeacon_0` — tipo `object`.
- `Zona3` — tipo `object`.
- `bOrderRevealed` — tipo `bool`.
- `bNarrativePaused` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 219 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_IntInt`, `BooleanAND`, `BooleanOR`, `Clamp`, `EqualEqual_IntInt`, `GetActorOfClass`, `GetBlackboard`, `GetComponentByClass`, `GetDistanceTo`, `GetGameInstance`, `GetHorizontalDistanceTo`, `GetPlayerPawn`, `GetValueAsBool`, `GrantHammerUpgrade`, `GreaterEqual_IntInt`, `InputActionHandlerDynamicSignature__DelegateSignature`, `Interactuar`, `IsValid`, `LessEqual_DoubleDouble`, `Less_IntInt`, `MakeLiteralName`, `Not_PreBool`, `OpenLevel`, `Percent_IntInt`, `RandomInteger`, `ReceiveBeginPlay`, `ReceiveTick`, `SetGamePaused`, `SetMaterial`, `SetValueAsBool`, `SetValueAsObject`, `StartOutcome`, `UserConstructionScript`.

- `/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C`
- `/Game/LevelMenu/MainMenuLevel`
- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestructibleDoor.BP_DestructibleDoor_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C`
- `/Game/ThirdPerson/Environment/Progression/M_DoorPowered.M_DoorPowered`
- `/Game/ThirdPerson/Maps/Nivel_Entrega`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `413781a4554fbccedc62aafef527fd825fd0b878355bad0af2ea9c40d2a6f3c6`.
