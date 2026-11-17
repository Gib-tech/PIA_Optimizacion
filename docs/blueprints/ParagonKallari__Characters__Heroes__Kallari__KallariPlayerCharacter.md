# KallariPlayerCharacter

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ParagonKallari/Characters/Heroes/Kallari/KallariPlayerCharacter`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Character'"`.

Personaje de demostración del pack Paragon Kallari, sin uso como protagonista de la misión. La revisión de UE5.6 retiró únicamente la acción ResetVR y su llamada obsoleta ResetOrientationAndPosition que impedían compilar al cargar el ejemplo. Los demás controles originales requieren sus mappings históricos y generan avisos si no están configurados; no se agregan a la misión para ocultar esos avisos.

## Entradas y responsabilidades del grafo

- **`EventGraph`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Jump`; desde `Released`: `StopJumping`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_LookUp_K2Node_InputAxisEvent_40`** en `EventGraph`. Operaciones alcanzables desde `then`: `AddControllerPitchInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_Turn_K2Node_InputAxisEvent_47`** en `EventGraph`. Operaciones alcanzables desde `then`: `AddControllerYawInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_MoveForward_K2Node_InputAxisEvent_79`** en `EventGraph`. Operaciones alcanzables desde `then`: `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_MoveRight_K2Node_InputAxisEvent_90`** en `EventGraph`. Operaciones alcanzables desde `then`: `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_TurnRate_K2Node_InputAxisEvent_38`** en `EventGraph`. Operaciones alcanzables desde `then`: `AddControllerYawInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_LookUpRate_K2Node_InputAxisEvent_53`** en `EventGraph`. Operaciones alcanzables desde `then`: `AddControllerPitchInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla LeftMouseButton`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Asignar SaveAttack`, `Asignar IsAttacking`, `K2Node_SwitchInteger`, `Asignar AttackCount`, `Asignar AttackCount`, `Asignar AttackCount`, `PlayAnimMontage`, `PlayAnimMontage`, `PlayAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_FaceButton_Left`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Asignar SaveAttack`, `Asignar IsAttacking`, `K2Node_SwitchInteger`, `Asignar AttackCount`, `Asignar AttackCount`, `Asignar AttackCount`, `PlayAnimMontage`, `PlayAnimMontage`, `PlayAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResetCombo`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar AttackCount`, `Asignar SaveAttack`, `Asignar IsAttacking`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComboAttackSave`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar SaveAttack`, `K2Node_SwitchInteger`, `Asignar AttackCount`, `Asignar AttackCount`, `Asignar AttackCount`, `PlayAnimMontage`, `PlayAnimMontage`, `PlayAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Attacking`** en `Attacking`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`InpAxisEvt_LookUp_K2Node_InputAxisEvent_40`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `AddControllerPitchInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_Turn_K2Node_InputAxisEvent_47`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `AddControllerYawInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_MoveForward_K2Node_InputAxisEvent_79`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_MoveRight_K2Node_InputAxisEvent_90`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `AddMovementInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_TurnRate_K2Node_InputAxisEvent_38`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `AddControllerYawInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InpAxisEvt_LookUpRate_K2Node_InputAxisEvent_53`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `AddControllerPitchInput`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResetCombo`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `Asignar AttackCount`, `Asignar SaveAttack`, `Asignar IsAttacking`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComboAttackSave`** en `ExecuteUbergraph_KallariPlayerCharacter`. Operaciones alcanzables desde `then`: `Condición`, `Asignar SaveAttack`, `K2Node_SwitchInteger`, `Asignar AttackCount`, `Asignar AttackCount`, `Asignar AttackCount`, `PlayAnimMontage`, `PlayAnimMontage`, `PlayAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComboAttackSave`** en `ComboAttackSave`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResetCombo`** en `ResetCombo`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisEvt_LookUp_K2Node_InputAxisEvent_40`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisEvt_LookUpRate_K2Node_InputAxisEvent_53`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisEvt_TurnRate_K2Node_InputAxisEvent_38`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisEvt_Turn_K2Node_InputAxisEvent_47`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisEvt_MoveRight_K2Node_InputAxisEvent_90`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputAxisHandlerDynamicSignature__DelegateSignature`** en `InpAxisEvt_MoveForward_K2Node_InputAxisEvent_79`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Jump_K2Node_InputActionEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Jump_K2Node_InputActionEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_FaceButton_Left_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_LeftMouseButton_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputTouchHandlerDynamicSignature__DelegateSignature`** en `InpTchEvt_Pressed`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputTouchHandlerDynamicSignature__DelegateSignature`** en `InpTchEvt_Released`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_KallariPlayerCharacter`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript_MERGED`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Attacking`** en `Attacking_MERGED`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `BaseTurnRate` — tipo `real`.
- `BaseLookUpRate` — tipo `real`.
- `Attacking` — tipo `mcdelegate`.
- `SaveAttack` — tipo `bool`.
- `IsAttacking` — tipo `bool`.
- `AttackCount` — tipo `int`.

## Operaciones y dependencias verificadas

La exportación contiene 163 nodos con pines. Funciones referenciadas: `AddControllerPitchInput`, `AddControllerYawInput`, `AddMovementInput`, `Attacking`, `BreakRotator`, `ComboAttackSave`, `GetControlRotation`, `GetForwardVector`, `GetRightVector`, `GetWorldDeltaSeconds`, `InpAxisEvt_LookUpRate_K2Node_InputAxisEvent_53`, `InpAxisEvt_LookUp_K2Node_InputAxisEvent_40`, `InpAxisEvt_MoveForward_K2Node_InputAxisEvent_79`, `InpAxisEvt_MoveRight_K2Node_InputAxisEvent_90`, `InpAxisEvt_TurnRate_K2Node_InputAxisEvent_38`, `InpAxisEvt_Turn_K2Node_InputAxisEvent_47`, `InpTchEvt_Pressed`, `InpTchEvt_Released`, `InputActionHandlerDynamicSignature__DelegateSignature`, `InputAxisHandlerDynamicSignature__DelegateSignature`, `InputTouchHandlerDynamicSignature__DelegateSignature`, `Jump`, `MakeRotator`, `Multiply_DoubleDouble`, `PlayAnimMontage`, `ResetCombo`, `StopJumping`, `UserConstructionScript`.

- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Attack_Melee_A_Montage.Attack_Melee_A_Montage`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Attack_Melee_B_Montage.Attack_Melee_B_Montage`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Attack_Melee_C_Montage.Attack_Melee_C_Montage`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `3db7e62334e9c045f0ee534e1667686473ee15b206e4327ccabbbe66ef22258c`.
