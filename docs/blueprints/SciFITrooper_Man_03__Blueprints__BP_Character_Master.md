# BP_Character_Master

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/SciFITrooper_Man_03/Blueprints/BP_Character_Master`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Character'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

- **`Tecla W`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `K2Node_MacroInstance`, `AddMovementInput`; desde `Released`: `K2Node_MacroInstance`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla D`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `K2Node_MacroInstance`, `AddMovementInput`; desde `Released`: `K2Node_MacroInstance`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla S`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `K2Node_MacroInstance`, `AddMovementInput`; desde `Released`: `K2Node_MacroInstance`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla A`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `K2Node_MacroInstance`, `AddMovementInput`; desde `Released`: `K2Node_MacroInstance`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `K2Node_MacroInstance`, `K2Node_MacroInstance`, `K2Node_MacroInstance`, `K2Node_MacroInstance`, `Asignar TargetArmLength`, `AddMovementInput`, `AddMovementInput`, `AddMovementInput`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla SpaceBar`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Jump`; desde `Released`: `StopJumping`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla MouseScrollDown`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Asignar TargetArmSpringLength`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla MouseScrollUp`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Asignar TargetArmSpringLength`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Tab`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `GetAllActorsOfClass`, `Asignar Number`, `Condición`, `Asignar Number`, `GetAllActorsOfClass`, `Condición`, `K2Node_Knot`, `Asignar Number`, `K2Node_Knot`, `-PossessToNewChar`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Escape`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `QuitGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `K2Node_CreateWidget`, `Asignar DemoMainWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveUnpossessed`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `K2Node_MacroInstance`, `K2Node_MacroInstance`, `K2Node_MacroInstance`, `K2Node_MacroInstance`, `FlushPersistentDebugLines`, `AddMovementInput`, `AddMovementInput`, `AddMovementInput`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla E`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `FlushPersistentDebugLines`, `CapsuleTraceSingleForObjects`, `K2Node_DynamicCast`, `-PossessToNewChar`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla P`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Asignar DebugTrace`, `-UpdateDebugTrace`, `Asignar DrawDebugTrace`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`-PossessToNewChar`** en `EventGraph`. Operaciones alcanzables desde `then`: `UnPossess`, `SetViewTargetWithBlend`, `Possess`, `SetControlRotation`, `Asignar DebugTrace`, `Asignar DemoMainWidget`, `Asignar DrawDebugTrace`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ExecuteUbergraph_BP_Character_Master`. Operaciones alcanzables desde `then`: `Secuencia`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `Asignar TargetArmLength`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `Secuencia`, `Secuencia`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ExecuteUbergraph_BP_Character_Master`. Operaciones alcanzables desde `then`: `Condición`, `Create`, `Asignar DemoMainWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveUnpossessed`** en `ExecuteUbergraph_BP_Character_Master`. Operaciones alcanzables desde `then`: `Secuencia`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `FlushPersistentDebugLines`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `K2Node_TunnelBoundary`, `Secuencia`, `Secuencia`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`-PossessToNewChar`** en `ExecuteUbergraph_BP_Character_Master`. Operaciones alcanzables desde `then`: `UnPossess`, `SetViewTargetWithBlend`, `Possess`, `SetControlRotation`, `Asignar DebugTrace`, `Asignar DemoMainWidget`, `Asignar DrawDebugTrace`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`-PossessToNewChar`** en `-PossessToNewChar`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveUnpossessed`** en `ReceiveUnpossessed`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisKeyEvt_MouseY_K2Node_InputAxisKeyEvent_2`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisKeyEvt_MouseX_K2Node_InputAxisKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_P_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_E_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Escape_K2Node_InputKeyEvent_2`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Escape_K2Node_InputKeyEvent_3`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Tab_K2Node_InputKeyEvent_4`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_MouseScrollUp_K2Node_InputKeyEvent_5`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_MouseScrollDown_K2Node_InputKeyEvent_6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_SpaceBar_K2Node_InputKeyEvent_7`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_SpaceBar_K2Node_InputKeyEvent_8`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_A_K2Node_InputKeyEvent_9`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_A_K2Node_InputKeyEvent_10`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_S_K2Node_InputKeyEvent_11`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_S_K2Node_InputKeyEvent_12`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_D_K2Node_InputKeyEvent_13`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_D_K2Node_InputKeyEvent_14`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_W_K2Node_InputKeyEvent_15`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_W_K2Node_InputKeyEvent_16`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_Character_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript_MERGED`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `TargetArmSpringLength` — tipo `real`.
- `Number` — tipo `int`.
- `DebugTrace` — tipo `bool`.
- `DemoMainWidget` — tipo `object`.
- `DrawDebugTrace` — tipo `byte`.

## Operaciones y dependencias verificadas

La exportación contiene 514 nodos con pines. Funciones referenciadas: `-PossessToNewChar`, `-UpdateDebugTrace`, `AddControllerPitchInput`, `AddControllerYawInput`, `AddMovementInput`, `AddToViewport`, `Add_DoubleDouble`, `Add_IntInt`, `Add_VectorVector`, `Array_Get`, `Array_LastIndex`, `BreakHitResult`, `BreakRotator`, `CapsuleTraceSingleForObjects`, `Create`, `EqualEqual_ObjectObject`, `FInterpTo`, `FMax`, `FMin`, `FlushPersistentDebugLines`, `GetActorForwardVector`, `GetAllActorsOfClass`, `GetControlRotation`, `GetForwardVector`, `GetPlayerController`, `GetRightVector`, `Greater_IntInt`, `InpAxisKeyEvt_MouseX_K2Node_InputAxisKeyEvent_0`, `InpAxisKeyEvt_MouseY_K2Node_InputAxisKeyEvent_2`, `InputActionHandlerDynamicSignature__DelegateSignature`, `InputAxisHandlerDynamicSignature__DelegateSignature`, `IsPlayerControlled`, `Jump`, `K2_GetActorLocation`, `MakeRotator`, `Multiply_DoubleDouble`, `Multiply_VectorFloat`, `Not_PreBool`, `Possess`, `QuitGame`, `ReceiveBeginPlay`, `ReceiveTick`, `ReceiveUnpossessed`, `SetControlRotation`, `SetViewTargetWithBlend`, `StopJumping`, `Subtract_DoubleDouble`, `UnPossess`, `UserConstructionScript`.

- `/Game/SciFITrooper_Man_03/DemoContent/W_DemoWidget.W_DemoWidget_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `c6cbda014b7c2d59ddd9f746028bf7d3a3cacab533233bebd64cd8011dc30729`.
