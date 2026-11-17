# BP_DeliveryInterface

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Orquesta menú de pausa y opciones en ambos mapas. Conserva widget/foco de origen, detiene mundo y restaura modo de entrada/captura del ratón. P/Esc/START alternan pausa; las acciones se consumen antes del P heredado.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `DoesSaveGameExist`, `Condición`, `LoadGameFromSlot`, `SetBaseSoundMix`, `K2Node_DynamicCast`, `SetSoundMixClassOverride`, `Condición`, `Asignar MasterVolume`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ApplyVolume`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetBaseSoundMix`, `SetSoundMixClassOverride`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveVolume`** en `EventGraph`. Operaciones alcanzables desde `then`: `CreateSaveGameObject`, `K2Node_DynamicCast`, `Asignar Version`, `Asignar MasterVolume`, `SaveGameToSlot`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla P`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `RemoveFromParent`, `Condición`, `GetActorOfClass`, `SetVisibility`, `RemoveFromParent`, `Condición`, `Asignar bOptionsOpen`, `SetGamePaused`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Escape`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `RemoveFromParent`, `Condición`, `GetActorOfClass`, `SetVisibility`, `RemoveFromParent`, `Condición`, `Asignar bOptionsOpen`, `SetGamePaused`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_Special_Right`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `RemoveFromParent`, `Condición`, `GetActorOfClass`, `SetVisibility`, `RemoveFromParent`, `Condición`, `Asignar bOptionsOpen`, `SetGamePaused`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_FaceButton_Right`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `Condición`, `RemoveFromParent`, `Condición`, `GetActorOfClass`, `SetVisibility`, `RemoveFromParent`, `Condición`, `Asignar bOptionsOpen`, `SetGamePaused`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`TogglePause`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Condición`, `RemoveFromParent`, `Condición`, `GetActorOfClass`, `SetVisibility`, `RemoveFromParent`, `Condición`, `Asignar bOptionsOpen`, `SetGamePaused`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OpenPause`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `Condición`, `K2Node_DynamicCast`, `Condición`, `SetGamePaused`, `K2Node_CreateWidget`, `Asignar PauseWidget`, `AddToViewport`, `Asignar bPauseOpen`, `SetIgnoreMoveInput`, `SetIgnoreLookInput`, `Asignar bShowMouseCursor`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ClosePause`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `RemoveFromParent`, `SetGamePaused`, `Asignar bPauseOpen`, `SetIgnoreMoveInput`, `SetIgnoreLookInput`, `Asignar bShowMouseCursor`, `SetInputMode_GameOnly`, `SetFocusToGameViewport`, `SetViewportMouseCaptureMode`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OpenOptions`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar ReturnWidget`, `Asignar ReturnFocus`, `SetVisibility`, `K2Node_CreateWidget`, `Asignar OptionsWidget`, `AddToViewport`, `Asignar bOptionsOpen`, `K2Node_DynamicCast`, `SetInputMode_GameAndUIEx`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`CloseOptions`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `RemoveFromParent`, `SetVisibility`, `Asignar bOptionsOpen`, `SetInputMode_GameAndUIEx`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`CloseOptions`** en `CloseOptions`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OpenOptions`** en `OpenOptions`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ClosePause`** en `ClosePause`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OpenPause`** en `OpenPause`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`TogglePause`** en `TogglePause`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveVolume`** en `SaveVolume`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ApplyVolume`** en `ApplyVolume`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_FaceButton_Right_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_Special_Right_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Escape_K2Node_InputKeyEvent_2`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_P_K2Node_InputKeyEvent_3`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DeliveryInterface`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `bInitialized` — tipo `bool`.
- `bPauseOpen` — tipo `bool`.
- `bOptionsOpen` — tipo `bool`.
- `MasterVolume` — tipo `real`.
- `PauseWidget` — tipo `object`.
- `OptionsWidget` — tipo `object`.
- `ReturnWidget` — tipo `object`.
- `ReturnFocus` — tipo `object`.
- `OptionsData` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 128 nodos con pines. Funciones referenciadas: `AddToViewport`, `ApplyVolume`, `BooleanOR`, `CloseOptions`, `ClosePause`, `CreateSaveGameObject`, `DoesSaveGameExist`, `EqualEqual_IntInt`, `FClamp`, `GetActorOfClass`, `GetPlayerController`, `InputActionHandlerDynamicSignature__DelegateSignature`, `IsValid`, `Less_IntInt`, `LoadGameFromSlot`, `OpenOptions`, `OpenPause`, `ReceiveBeginPlay`, `RemoveFromParent`, `SaveGameToSlot`, `SaveVolume`, `SetBaseSoundMix`, `SetFocusToGameViewport`, `SetGamePaused`, `SetIgnoreLookInput`, `SetIgnoreMoveInput`, `SetInputMode_GameAndUIEx`, `SetInputMode_GameOnly`, `SetSoundMixClassOverride`, `SetViewportMouseCaptureMode`, `SetVisibility`, `TogglePause`, `UserConstructionScript`.

- `/Game/Menu/Menu_Opciones.Menu_Opciones_C`
- `/Game/Menu/Menu_Pausa.Menu_Pausa_C`
- `/Game/ThirdPerson/Audio/SM_TimeOutSettings.SM_TimeOutSettings`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryOptions.BP_DeliveryOptions_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `c68fc525a6a50b44f2791250e9af8c613d396b22f6e50c0b1893b99bc091f37e`.
