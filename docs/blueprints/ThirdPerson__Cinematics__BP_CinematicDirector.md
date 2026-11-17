# BP_CinematicDirector

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Cinematics/BP_CinematicDirector`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Director de introducción, derrota, victoria y revelación final. Reproduce Level Sequence/audio, bloquea/restaura entrada y cámara, permite omisión y muestra la permutación real. No cambia las condiciones de victoria ni el daño.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetManualCameraFade`, `K2Node_DynamicCast`, `Asignar bShouldIntro`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Condición`, `Condición`, `GetActorOfClass`, `Condición`, `Asignar Hero`, `Asignar bActive`, `GetActorOfClass`, `Condición`, `Asignar Hostage`, `Stop`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartIntro`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar Kind`, `Asignar bActive`, `Asignar StartedAt`, `Asignar Duration`, `Asignar EndsAt`, `Asignar SavedViewTarget`, `SetCinematicMode`, `SetOwnerNoSee`, `SetVisibility`, `DisableInput`, `DisableInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartRevelation`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Asignar RevealEnemy`, `Asignar RevealedSequence`, `Asignar Kind`, `Asignar bNarrativePaused`, `StopMovement`, `K2Node_DynamicCast`, `Condición`, `StopMovementImmediately`, `StopLogic`, `StopAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartOutcome`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Stop`, `Asignar bNarrativePaused`, `SetCinematicMode`, `Asignar bOutcomeStarted`, `Condición`, `Asignar Kind`, `FinishFinalWords`, `Condición`, `K2_AddLocalOffset`, `Condición`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PlayCinema`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bActive`, `Asignar StartedAt`, `Asignar Duration`, `Asignar EndsAt`, `Asignar SavedViewTarget`, `SetCinematicMode`, `SetOwnerNoSee`, `SetVisibility`, `DisableInput`, `DisableInput`, `DisableInput`, `DisableInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla SpaceBar`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Asignar bActive`, `Condición`, `Stop`, `SetCinematicMode`, `SetOwnerNoSee`, `SetVisibility`, `SetViewTargetWithBlend`, `EnableInput`, `EnableInput`, `DisableInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_FaceButton_Bottom`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Asignar bActive`, `Condición`, `Stop`, `SetCinematicMode`, `SetOwnerNoSee`, `SetVisibility`, `SetViewTargetWithBlend`, `EnableInput`, `EnableInput`, `DisableInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`FinishCinema`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar bActive`, `Condición`, `Stop`, `SetCinematicMode`, `SetOwnerNoSee`, `SetVisibility`, `SetViewTargetWithBlend`, `EnableInput`, `EnableInput`, `DisableInput`, `Condición`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`FinishCinema`** en `FinishCinema`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PlayCinema`** en `PlayCinema`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartOutcome`** en `StartOutcome`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartRevelation`** en `StartRevelation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartIntro`** en `StartIntro`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_FaceButton_Bottom_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_SpaceBar_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_CinematicDirector`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `bShouldIntro` — tipo `bool`.
- `bInitialized` — tipo `bool`.
- `bActive` — tipo `bool`.
- `bOutcomeStarted` — tipo `bool`.
- `Kind` — tipo `int`.
- `StartedAt` — tipo `real`.
- `Duration` — tipo `real`.
- `EndsAt` — tipo `real`.
- `Hero` — tipo `object`.
- `Hostage` — tipo `object`.
- `Director` — tipo `object`.
- `Interface` — tipo `object`.
- `GameHUD` — tipo `object`.
- `SequencePlayer` — tipo `object`.
- `SequenceActor` — tipo `object`.
- `SavedViewTarget` — tipo `object`.
- `RevealEnemy` — tipo `object`.
- `RevealedSequence` — tipo `string`.

## Operaciones y dependencias verificadas

La exportación contiene 230 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `BooleanAND`, `BooleanOR`, `CreateLevelSequencePlayer`, `DisableInput`, `DisableMovement`, `EnableInput`, `EqualEqual_IntInt`, `FinishCinema`, `FinishFinalWords`, `GetActorOfClass`, `GetAllActorsOfClass`, `GetController`, `GetGameInstance`, `GetHUD`, `GetPlayerCameraManager`, `GetPlayerController`, `GetPlayerPawn`, `GetTimeSeconds`, `GetViewTarget`, `GreaterEqual_DoubleDouble`, `Greater_IntInt`, `InputActionHandlerDynamicSignature__DelegateSignature`, `IsValid`, `K2_AddLocalOffset`, `K2_GetActorLocation`, `K2_GetActorRotation`, `K2_SetActorLocation`, `K2_SetActorRotation`, `Less_IntInt`, `MakeLiteralBool`, `Not_PreBool`, `Play`, `PlayCinema`, `ReceiveBeginPlay`, `ReceiveTick`, `ResetState`, `RestartLogic`, `SelectInt`, `SelectRotator`, `SetCinematicMode`, `SetCollisionProfileName`, `SetFocusToGameViewport`, `SetGamePaused`, `SetInputMode_GameOnly`, `SetManualCameraFade`, `SetOwnerNoSee`, `SetSimulatePhysics`, `SetViewTargetWithBlend`, `SetViewportMouseCaptureMode`, `SetVisibility`, `StartIntro`, `StartOutcome`, `StartRevelation`, `Stop`, `StopAnimMontage`, `StopCameraFade`, `StopLogic`, `StopMovement`, `StopMovementImmediately`, `UserConstructionScript`.

- `/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C`
- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/Health.Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega.BP_HUD_Entrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Cinematics/LS_Derrota.LS_Derrota`
- `/Game/ThirdPerson/Cinematics/LS_Intro.LS_Intro`
- `/Game/ThirdPerson/Cinematics/LS_Revelacion.LS_Revelacion`
- `/Game/ThirdPerson/Cinematics/LS_Victoria.LS_Victoria`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `04d83109111c51e33e5fad62ef209fe7654b225532f872cdaa205abcb59bb94d`.
