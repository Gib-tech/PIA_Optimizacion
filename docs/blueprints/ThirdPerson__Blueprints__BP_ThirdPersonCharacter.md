# BP_ThirdPersonCharacter

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Character'"`.

Personaje base del equipo. Procesa Enhanced Input, locomoción, salto, cámaras, equipamiento y combos con montajes y AnimNotifies. BP_PlayerEntrega lo especializa para el nivel final. No duplicar aquí lógica de misión.

## Entradas y responsabilidades del grafo

- **`Acción IA_Jump`** en `EventGraph`. Operaciones alcanzables desde `Started`: `Jump`; desde `Completed`: `StopJumping`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Acción IA_Move`** en `EventGraph`. Operaciones alcanzables desde `Triggered`: `Condición`, `AddMovementInput`, `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Acción IA_Look`** en `EventGraph`. Operaciones alcanzables desde `Triggered`: `AddControllerYawInput`, `AddControllerPitchInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `WeaponToBack`, `K2Node_CreateWidget`, `Asignar Health_Widget`, `AddToViewport`, `K2Node_AddDelegate`, `K2Node_AddDelegate`, `K2Node_DynamicCast`, `K2Node_MacroInstance`, `AddMappingContext`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Acción IA_Camera`** en `EventGraph`. Operaciones alcanzables desde `Started`: `Condición`, `SetActive`, `SetActive`, `SetActive`, `SetActive`, `Asignar CamaraPrimera`, `Asignar CamaraPrimera`, `Asignar bUseControllerRotationYaw`, `Asignar bUseControllerRotationYaw`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón CapsuleComponent`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `K2Node_SpawnActorFromClass`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Q`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `K2Node_MacroInstance`, `Condición`, `SphereTraceSingle`, `Condición`, `K2Node_DynamicCast`, `PlaySound2D`, `SetVisibility`, `Asignar Recolectado?`, `RemoveFromParent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`LightAttackEvent`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `PerformLightAttack`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveLightAttack`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar bSaveLightAttack`, `Condición`, `SetState`, `LightAttackEvent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResetState`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bLightAttackActive`, `SetState`, `Asignar AttackIndex`, `Asignar bSaveLightAttack`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Update_Health_Bar`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetPercent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`TheHeavyIsDead`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_PlayMontage`, `DisableInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón WeaponHitbox`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `PrintString`, `Condición`, `E_Decrease_Health`, `K2Node_DynamicCast`, `SetValueAsBool`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartWeaponSheatheTimer`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2_ClearAndInvalidateTimerHandle`, `K2_SetTimerDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AutoSheatheWeapon`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Acción IA_Light_Attack`** en `EventGraph`. Operaciones alcanzables desde `Started`: `Condición`, `Asignar IsAttacking`, `Asignar bLightAttackActive`, `Condición`, `WeaponToHand`, `WeaponToHand`, `K2Node_PlayMontage`, `K2Node_PlayMontage`, `Asignar LightSwingIndex`, `Asignar IsAttacking`, `K2Node_SwitchName`, `Asignar LightSwingIndex`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Acción IA_Heavy_Attack`** en `EventGraph`. Operaciones alcanzables desde `Started`: `Condición`, `Asignar IsAttacking`, `Condición`, `WeaponToHand`, `K2Node_PlayMontage`, `K2Node_PlayMontage`, `Condición`, `Asignar IsAttacking`, `Condición`, `Asignar IsAttacking`, `Asignar AttackIndex`, `Asignar AttackIndex`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAnyDamage`** en `EventGraph`. Operaciones alcanzables desde `then`: `Decrease_Health`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Acción IA_SwitchToHammer`** en `EventGraph`. Operaciones alcanzables desde `Started`: `Condición`, `SetVisibility`, `SetVisibility`, `Asignar bIsHammerEquipped`, `Asignar bIsSwordEquipped`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Acción IA_SwitchToSword`** en `EventGraph`. Operaciones alcanzables desde `Started`: `Condición`, `SetVisibility`, `SetVisibility`, `Asignar bIsHammerEquipped`, `Asignar bIsSwordEquipped`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla P`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `RemoveFromParent`, `K2Node_CreateWidget`, `SetGamePaused`, `Asignar MenuPausa`, `Asignar bShowMouseCursor`, `SetGamePaused`, `Asignar bPaused`, `AddToViewport`, `Asignar bShowMouseCursor`, `Asignar bPaused`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`SetState`** en `SetState`. Operaciones alcanzables desde `then`: `Condición`, `Asignar CurrentState`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GetState`** en `GetState`. Operaciones alcanzables desde `then`: `GetState`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`IsStateEqualToAny`** en `IsStateEqualToAny`. Operaciones alcanzables desde `then`: `IsStateEqualToAny`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PerformLightAttack`** en `PerformLightAttack`. Operaciones alcanzables desde `then`: `Asignar LightAttackMontage`, `Condición`, `SetState`, `PlayAnimMontage`, `K2Node_MacroInstance`, `Condición`, `Asignar AttackIndex`, `PerformLightAttack`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`WeaponToHand`** en `WeaponToHand`. Operaciones alcanzables desde `then`: `K2_AttachToComponent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`WeaponToBack`** en `WeaponToBack`. Operaciones alcanzables desde `then`: `K2_AttachToComponent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Q_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputDebugKeyHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_One_K2Node_InputDebugKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyEnd_9FF672534E0742C3165BC2829F6451C6`** en `OnNotifyEnd_9FF672534E0742C3165BC2829F6451C6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyBegin_9FF672534E0742C3165BC2829F6451C6`** en `OnNotifyBegin_9FF672534E0742C3165BC2829F6451C6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnInterrupted_9FF672534E0742C3165BC2829F6451C6`** en `OnInterrupted_9FF672534E0742C3165BC2829F6451C6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnBlendOut_9FF672534E0742C3165BC2829F6451C6`** en `OnBlendOut_9FF672534E0742C3165BC2829F6451C6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnCompleted_9FF672534E0742C3165BC2829F6451C6`** en `OnCompleted_9FF672534E0742C3165BC2829F6451C6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Camera_K2Node_EnhancedInputActionEvent_8`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Light_Attack_K2Node_EnhancedInputActionEvent_7`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyEnd_B1D9C2584090EC2B498CE6856211E185`** en `OnNotifyEnd_B1D9C2584090EC2B498CE6856211E185`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyBegin_B1D9C2584090EC2B498CE6856211E185`** en `OnNotifyBegin_B1D9C2584090EC2B498CE6856211E185`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnInterrupted_B1D9C2584090EC2B498CE6856211E185`** en `OnInterrupted_B1D9C2584090EC2B498CE6856211E185`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnBlendOut_B1D9C2584090EC2B498CE6856211E185`** en `OnBlendOut_B1D9C2584090EC2B498CE6856211E185`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnCompleted_B1D9C2584090EC2B498CE6856211E185`** en `OnCompleted_B1D9C2584090EC2B498CE6856211E185`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyEnd_965BC224475DCE4765B98C92C55FF498`** en `OnNotifyEnd_965BC224475DCE4765B98C92C55FF498`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyBegin_965BC224475DCE4765B98C92C55FF498`** en `OnNotifyBegin_965BC224475DCE4765B98C92C55FF498`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnInterrupted_965BC224475DCE4765B98C92C55FF498`** en `OnInterrupted_965BC224475DCE4765B98C92C55FF498`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnBlendOut_965BC224475DCE4765B98C92C55FF498`** en `OnBlendOut_965BC224475DCE4765B98C92C55FF498`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnCompleted_965BC224475DCE4765B98C92C55FF498`** en `OnCompleted_965BC224475DCE4765B98C92C55FF498`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Heavy_Attack_K2Node_EnhancedInputActionEvent_6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Look_K2Node_EnhancedInputActionEvent_5`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Move_K2Node_EnhancedInputActionEvent_4`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_SwitchToHammer_K2Node_EnhancedInputActionEvent_3`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_SwitchToSword_K2Node_EnhancedInputActionEvent_2`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_P_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyEnd_BE81063D47C5DDA4FE877EB89802D805`** en `OnNotifyEnd_BE81063D47C5DDA4FE877EB89802D805`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyBegin_BE81063D47C5DDA4FE877EB89802D805`** en `OnNotifyBegin_BE81063D47C5DDA4FE877EB89802D805`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnInterrupted_BE81063D47C5DDA4FE877EB89802D805`** en `OnInterrupted_BE81063D47C5DDA4FE877EB89802D805`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnBlendOut_BE81063D47C5DDA4FE877EB89802D805`** en `OnBlendOut_BE81063D47C5DDA4FE877EB89802D805`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnCompleted_BE81063D47C5DDA4FE877EB89802D805`** en `OnCompleted_BE81063D47C5DDA4FE877EB89802D805`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Jump_K2Node_EnhancedInputActionEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EnhancedInputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_IA_Jump_K2Node_EnhancedInputActionEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyEnd_768583BD4986C9573E58F99554E4F809`** en `OnNotifyEnd_768583BD4986C9573E58F99554E4F809`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnNotifyBegin_768583BD4986C9573E58F99554E4F809`** en `OnNotifyBegin_768583BD4986C9573E58F99554E4F809`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnInterrupted_768583BD4986C9573E58F99554E4F809`** en `OnInterrupted_768583BD4986C9573E58F99554E4F809`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnBlendOut_768583BD4986C9573E58F99554E4F809`** en `OnBlendOut_768583BD4986C9573E58F99554E4F809`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnCompleted_768583BD4986C9573E58F99554E4F809`** en `OnCompleted_768583BD4986C9573E58F99554E4F809`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`LightAttackEvent`** en `LightAttackEvent`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveLightAttack`** en `SaveLightAttack`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResetState`** en `ResetState`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComponentHitSignature__DelegateSignature`** en `BndEvt__BP_ThirdPersonCharacter_CapsuleComponent_K2Node_ComponentBoundEvent_0_ComponentHitSignature__DelegateSignature`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Update_Health_Bar`** en `Update_Health_Bar`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`TheHeavyIsDead`** en `TheHeavyIsDead`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComponentBeginOverlapSignature__DelegateSignature`** en `BndEvt__BP_ThirdPersonCharacter_WeaponHitbox_K2Node_ComponentBoundEvent_1_ComponentBeginOverlapSignature__DelegateSignature`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartWeaponSheatheTimer`** en `StartWeaponSheatheTimer`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AutoSheatheWeapon`** en `AutoSheatheWeapon`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAnyDamage`** en `ReceiveAnyDamage`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ThirdPersonCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `CamaraPrimera` — tipo `bool`.
- `CurrentState` — tipo `byte`.
- `LightAttackCombo_S` — tipo `object`.
- `AttackIndex` — tipo `int`.
- `bSaveLightAttack` — tipo `bool`.
- `IsAttacking` — tipo `bool`.
- `ActualAttack` — tipo `int`.
- `Health_Widget` — tipo `object`.
- `HitActors` — tipo `object`.
- `bWeaponDown` — tipo `bool`.
- `WeaponSheatheDelay` — tipo `real`.
- `WeaponSheatheTimer` — tipo `struct`.
- `HeavyAttackCombo` — tipo `object`.
- `bLightAttackActive` — tipo `bool`.
- `LightSwingIndex` — tipo `int`.
- `bIsHammerEquipped` — tipo `bool`.
- `bIsSwordEquipped` — tipo `bool`.
- `bPaused` — tipo `bool`.
- `MenuPausa` — tipo `object`.
- `LightAttackCombo_H` — tipo `object`.
- `Hammer_HeavyAttackCombo` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 498 nodos con pines. Funciones referenciadas: `ActorHasTag`, `AddControllerPitchInput`, `AddControllerYawInput`, `AddMappingContext`, `AddMovementInput`, `AddToViewport`, `Add_IntInt`, `Add_VectorVector`, `Array_Contains`, `Array_Length`, `AutoSheatheWeapon`, `BreakHitResult`, `ComponentBeginOverlapSignature__DelegateSignature`, `ComponentHitSignature__DelegateSignature`, `Conv_VectorToTransform`, `Decrease_Health`, `DisableInput`, `Divide_DoubleDouble`, `E_Decrease_Health`, `EnableInput`, `EnhancedInputActionHandlerDynamicSignature__DelegateSignature`, `GetActorForwardVector`, `GetBlackboard`, `GetControlRotation`, `GetController`, `GetForwardVector`, `GetOverlappingActors`, `GetPlayerController`, `GetRightVector`, `GetState`, `GreaterEqual_IntInt`, `InputActionHandlerDynamicSignature__DelegateSignature`, `InputDebugKeyHandlerDynamicSignature__DelegateSignature`, `IsStateEqualToAny`, `IsValid`, `Jump`, `K2_AttachToComponent`, `K2_ClearAndInvalidateTimerHandle`, `K2_GetComponentLocation`, `K2_SetTimerDelegate`, `LaunchCharacter`, `Less_IntInt`, `LightAttackEvent`, `MakeLiteralName`, `Multiply_VectorVector`, `Not_PreBool`, `PerformLightAttack`, `PlayAnimMontage`, `PlaySound2D`, `PrintString`, `ReceiveAnyDamage`, `ReceiveBeginPlay`, `RemoveFromParent`, `ResetState`, `SaveLightAttack`, `SetActive`, `SetCollisionEnabled`, `SetGamePaused`, `SetPercent`, `SetState`, `SetValueAsBool`, `SetVisibility`, `SphereTraceSingle`, `StartWeaponSheatheTimer`, `StopJumping`, `Subtract_IntInt`, `TheHeavyIsDead`, `Update_Health_Bar`, `UserConstructionScript`, `WeaponToBack`, `WeaponToHand`.

- `/Game/Menu/Menu_Pausa.Menu_Pausa_C`
- `/Game/ThirdPerson/Animations/Attack_3_Montage.Attack_3_Montage`
- `/Game/ThirdPerson/Animations/Death_Montage.Death_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/FA_1_Montage.FA_1_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/FA_2_Montage.FA_2_Montage`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/Health.Health_C`
- `/Game/ThirdPerson/Blueprints/DañoDes.DañoDes_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`
- `/Game/ThirdPerson/Blueprints/Enums/E_States.E_States`
- `/Game/ThirdPerson/Bp_Modelos/BP_DestruiblePick.BP_DestruiblePick_C`
- `/Game/ThirdPerson/Input/Actions/IA_Camera.IA_Camera`
- `/Game/ThirdPerson/Input/Actions/IA_Heavy_Attack.IA_Heavy_Attack`
- `/Game/ThirdPerson/Input/Actions/IA_Jump.IA_Jump`
- `/Game/ThirdPerson/Input/Actions/IA_Light_Attack.IA_Light_Attack`
- `/Game/ThirdPerson/Input/Actions/IA_Look.IA_Look`
- `/Game/ThirdPerson/Input/Actions/IA_Move.IA_Move`
- `/Game/ThirdPerson/Input/Actions/IA_SwitchToHammer.IA_SwitchToHammer`
- `/Game/ThirdPerson/Input/Actions/IA_SwitchToSword.IA_SwitchToSword`
- `/Game/ThirdPerson/Input/IMC_Default.IMC_Default`
- `/Game/ThirdPerson/RecursosPropios/Interfaz/Interfaz.Interfaz_C`
- `/Game/ThirdPerson/RecursosPropios/Sonido/collect-5930.collect-5930`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `4a67046f3e02d33d291ebb90155b49f36b25ed08e55d87d7e545657db50ee50b`.
