# BP_HUD_Entrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.HUD'"`.

Presentación de misión: salud, objetivos, orden/tiempo, diálogo progresivo, señales del rehén, daño real e inventario. Lee datos de actores; no concede objetivos ni aplica daño por dibujar.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `GetActorOfClass`, `GetActorOfClass`, `Asignar CachedDirector`, `Asignar CachedCinema`, `GetActorOfClass`, `Asignar CachedExtras`, `GetActorOfClass`, `Asignar CachedHostage`, `Asignar LastHostageHitSerial`, `K2Node_DynamicCast`, `Asignar CachedBeacon1`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Enter`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Asignar ForceReveal`, `Asignar DismissedDialog`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_DPad_Up`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Asignar ForceReveal`, `Asignar DismissedDialog`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveDrawHUD`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `Condición`, `Condición`, `Condición`, `Secuencia`, `Secuencia`, `DrawRect`, `Condición`, `GetActorOfClass`, `Condición`, `Condición`, `Condición`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_HUD_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveDrawHUD`** en `ReceiveDrawHUD`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_HUD_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_DPad_Up_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_HUD_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Enter_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_HUD_Entrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `CachedDirector` — tipo `object`.
- `CachedHostage` — tipo `object`.
- `AmbientAudio` — tipo `object`.
- `CurrentDialog` — tipo `int`.
- `LastDialog` — tipo `int`.
- `DismissedDialog` — tipo `int`.
- `VisibleCharacters` — tipo `int`.
- `DialogStarted` — tipo `real`.
- `LastBeepAt` — tipo `real`.
- `LastHealth` — tipo `real`.
- `CharactersPerSecond` — tipo `real`.
- `HoldSeconds` — tipo `real`.
- `UIAudioVolume` — tipo `real`.
- `ForceReveal` — tipo `bool`.
- `DialogueVisible` — tipo `bool`.
- `FullText` — tipo `string`.
- `VisibleText` — tipo `string`.
- `Speaker` — tipo `string`.
- `ActionHint` — tipo `string`.
- `HurtPulseUntil` — tipo `real`.
- `HostageSpeaking` — tipo `bool`.
- `HostagePromptVisible` — tipo `bool`.
- `HostagePromptInRange` — tipo `bool`.
- `CurrentVoiceCue` — tipo `object`.
- `LastHostageHitSerial` — tipo `int`.
- `HostageHurtUntil` — tipo `real`.
- `HostageAlertCooldown` — tipo `real`.
- `EnemyHitUntil` — tipo `real`.
- `LastEnemyDamage` — tipo `real`.
- `CachedBeacon1` — tipo `object`.
- `CachedBeacon2` — tipo `object`.
- `CachedBeacon3` — tipo `object`.
- `CachedCinema` — tipo `object`.
- `LastStatusText` — tipo `string`.
- `LastStatusSerial` — tipo `int`.
- `StatusUntil` — tipo `real`.
- `StatusNoticeVisible` — tipo `bool`.
- `DisplayedOrder` — tipo `string`.
- `CachedExtras` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 1166 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_IntInt`, `Add_VectorVector`, `BooleanAND`, `BooleanOR`, `BreakVector`, `Concat_StrStr`, `Conv_BoolToInt`, `Conv_IntToDouble`, `Conv_IntToString`, `Divide_DoubleDouble`, `Divide_IntInt`, `DrawRect`, `DrawText`, `DrawTexture`, `EqualEqual_IntInt`, `EqualEqual_StrStr`, `FClamp`, `FFloor`, `FMax`, `FMin`, `GetActorOfClass`, `GetBlackboard`, `GetComponentByClass`, `GetDistanceTo`, `GetPlayerController`, `GetPlayerPawn`, `GetRealTimeSeconds`, `GetTimeSeconds`, `GetValueAsBool`, `GreaterEqual_DoubleDouble`, `GreaterEqual_IntInt`, `Greater_DoubleDouble`, `Greater_IntInt`, `InputActionHandlerDynamicSignature__DelegateSignature`, `IsOverlappingActor`, `IsValid`, `K2_GetActorLocation`, `Left`, `Len`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `Less_IntInt`, `LineOfSightTo`, `MakeColor`, `MakeLiteralName`, `Min`, `Multiply_DoubleDouble`, `Multiply_IntInt`, `NotEqual_IntInt`, `NotEqual_StrStr`, `Not_PreBool`, `Percent_IntInt`, `PlaySound2D`, `Project`, `RandomFloatInRange`, `ReceiveBeginPlay`, `ReceiveDrawHUD`, `SelectColor`, `SelectFloat`, `SelectInt`, `SpawnSound2D`, `Subtract_DoubleDouble`, `Subtract_IntInt`, `UserConstructionScript`.

- `/Game/ThirdPerson/Audio/SW_Alert.SW_Alert`
- `/Game/ThirdPerson/Audio/SW_Ambience.SW_Ambience`
- `/Game/ThirdPerson/Audio/SW_Clear.SW_Clear`
- `/Game/ThirdPerson/Audio/SW_Defeat.SW_Defeat`
- `/Game/ThirdPerson/Audio/SW_HostageVoice_1.SW_HostageVoice_1`
- `/Game/ThirdPerson/Audio/SW_HostageVoice_2.SW_HostageVoice_2`
- `/Game/ThirdPerson/Audio/SW_HostageVoice_3.SW_HostageVoice_3`
- `/Game/ThirdPerson/Audio/SW_Open.SW_Open`
- `/Game/ThirdPerson/Audio/SW_PlayerHurt.SW_PlayerHurt`
- `/Game/ThirdPerson/Audio/SW_Rescue.SW_Rescue`
- `/Game/ThirdPerson/Audio/SW_Text.SW_Text`
- `/Game/ThirdPerson/Audio/SW_Victory.SW_Victory`
- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager.BP_DeliverySaveManager_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestruibleEntrega.BP_DestruibleEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_TecnicoTemporal.BP_TecnicoTemporal_C`
- `/Game/ThirdPerson/Blueprints/Entrega/FX/T_DamageCorners.T_DamageCorners`
- `/Game/ThirdPerson/Blueprints/Entrega/F_DialogueMono.F_DialogueMono`
- `/Game/ThirdPerson/Blueprints/Entrega/Inventario/F_InventarioNumero.F_InventarioNumero`
- `/Game/ThirdPerson/Blueprints/Entrega/Inventario/F_InventarioTexto.F_InventarioTexto`
- `/Game/ThirdPerson/Blueprints/Entrega/Inventario/T_Inv_BotiquinTemporal.T_Inv_BotiquinTemporal`
- `/Game/ThirdPerson/Blueprints/Entrega/Inventario/T_Inv_CeldaTemporal.T_Inv_CeldaTemporal`
- `/Game/ThirdPerson/Blueprints/Entrega/Inventario/T_Inv_CreditoCronal.T_Inv_CreditoCronal`
- `/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `873df7c2d0c40befb373e4515934fd5a2252ba4aa0375c36cf62bbe2ee39955b`.
