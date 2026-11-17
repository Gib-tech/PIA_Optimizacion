# Kallari_AnimBlueprint

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ParagonKallari/Characters/Heroes/Kallari/Kallari_AnimBlueprint`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

- **`EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_BlendListByBool_1CBA846F4BAADB336D5BF9B9DD41BF5A`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_BlendListByBool_1CBA846F4BAADB336D5BF9B9DD41BF5A`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_BlendSpacePlayer_A6F86AA043B3C11E6B87F58D3ACE89B5`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_BlendSpacePlayer_A6F86AA043B3C11E6B87F58D3ACE89B5`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_TransitionResult_A4437730461FC5AA502E6D8E79D8A00C`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_TransitionResult_A4437730461FC5AA502E6D8E79D8A00C`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_TransitionResult_C2A8E7B34072B54E5A6D9A85055CE1FD`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_TransitionResult_C2A8E7B34072B54E5A6D9A85055CE1FD`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `BlueprintUpdateAnimation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_TransitionResult_45A5E87844662F4E52B9DAAE64DB5A97`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_Kallari_AnimBlueprint_AnimGraphNode_TransitionResult_45A5E87844662F4E52B9DAAE64DB5A97`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintInitializeAnimation`** en `BlueprintInitializeAnimation`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintBeginPlay`** en `BlueprintBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimNotify_SaveAttack`** en `AnimNotify_SaveAttack`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimNotify_ResetCombo`** en `AnimNotify_ResetCombo`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Attacking_Event_0`** en `Attacking_Event_0`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Kallari_AnimBlueprint`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_MacroInstance`, `Asignar IsInAir`, `Asignar Speed`, `Asignar Roll`, `Asignar Pitch`, `Asignar Yaw`, `Asignar YawDelta`, `Asignar RotationLastTick`, `K2Node_DynamicCast`, `Asignar IsAccelerating`, `Asignar FullBody`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintInitializeAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `K2Node_AddDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `Montage_Play`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimNotify_SaveAttack`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `ComboAttackSave`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimNotify_ResetCombo`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `ResetCombo`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Attacking_Event_0`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar isAttacking`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Speed` — tipo `real`.
- `IsInAir` — tipo `bool`.
- `Pitch` — tipo `real`.
- `Roll` — tipo `real`.
- `Yaw` — tipo `real`.
- `RotationLastTick` — tipo `struct`.
- `YawDelta` — tipo `real`.
- `IsAccelerating` — tipo `bool`.
- `Character` — tipo `object`.
- `isAttacking` — tipo `bool`.
- `CurrentAttack` — tipo `int`.
- `FullBody` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 187 nodos con pines. Funciones referenciadas: `AnimNotify_ResetCombo`, `AnimNotify_SaveAttack`, `Attacking_Event_0`, `BlueprintBeginPlay`, `BlueprintInitializeAnimation`, `BlueprintUpdateAnimation`, `BooleanAND`, `BreakRotator`, `ComboAttackSave`, `Divide_DoubleDouble`, `EqualEqual_DoubleDouble`, `FInterpTo`, `GetBaseAimRotation`, `GetCurrentAcceleration`, `GetCurveValue`, `GetMovementComponent`, `GetVelocity`, `Greater_DoubleDouble`, `IsFalling`, `K2_GetActorRotation`, `Montage_Play`, `Multiply_DoubleDouble`, `NormalizedDeltaRotator`, `Not_PreBool`, `ResetCombo`, `TryGetPawnOwner`, `VSize`.

- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/AimOffsets/Idle_AimOffset.Idle_AimOffset`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Blendspaces/JogFwdSlopeLean.JogFwdSlopeLean`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Idle_Combat_NonAdditive.Idle_Combat_NonAdditive`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Jog_Fwd_Start.Jog_Fwd_Start`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Jog_Fwd_Stop.Jog_Fwd_Stop`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Jump_Fall_Loop.Jump_Fall_Loop`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Jump_Mid.Jump_Mid`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Jump_Recovery_Additive.Jump_Recovery_Additive`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/Jump_Start.Jump_Start`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Animations/LevelStart_Montage.LevelStart_Montage`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/KallariPlayerCharacter.KallariPlayerCharacter_C`
- `/Game/ParagonKallari/Characters/Heroes/Kallari/Meshes/Kallari_Skeleton.Kallari_Skeleton`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `3973a90086ad16aca27682be2e17366a69e6a8b1fbc8987d9646525b64786165`.
