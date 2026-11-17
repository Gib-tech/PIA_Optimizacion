# ABP_Manny

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Animations/ABP_Manny`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

AnimBlueprint del protagonista usado con la malla del viajero. Mezcla locomoción, salto/caída y slots de montajes. Las notificaciones gobiernan buffer de combo y recuperación; no deben volver a dispararse desde los brazos de cámara.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_VariableGet`, `Secuencia`, `K2Node_Knot`, `K2Node_Knot`, `K2Node_Knot`, `Asignar Velocity`, `Asignar ShouldMove`, `Asignar IsFalling`, `Asignar GroundSpeed`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintInitializeAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar Character`, `Asignar MovementComponent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimNotify_canAttack`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar IsAttacking`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `BlueprintUpdateAnimation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_ABP_Manny`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintInitializeAnimation`** en `BlueprintInitializeAnimation`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_Manny`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_Manny_AnimGraphNode_TransitionResult_305F37BB4A5AD886760B8E99A5C561E1`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_Manny_AnimGraphNode_TransitionResult_305F37BB4A5AD886760B8E99A5C561E1`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_Manny`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimNotify_canAttack`** en `AnimNotify_canAttack`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_Manny`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Character` — tipo `object`.
- `MovementComponent` — tipo `object`.
- `Velocity` — tipo `struct`.
- `GroundSpeed` — tipo `real`.
- `ShouldMove` — tipo `bool`.
- `IsFalling` — tipo `bool`.
- `As BP Third Person Character` — tipo `object`.
- `Is Sword Equipped` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 113 nodos con pines. Funciones referenciadas: `AnimNotify_canAttack`, `BlueprintInitializeAnimation`, `BlueprintUpdateAnimation`, `BooleanAND`, `GetCurrentAcceleration`, `GetOwningActor`, `Greater_DoubleDouble`, `IsFalling`, `NotEqual_VectorVector`, `Not_PreBool`, `VSizeXY`.

- `/Game/Characters/Mannequins/Animations/Manny/BS_Hammer_WalkRun.BS_Hammer_WalkRun`
- `/Game/Characters/Mannequins/Animations/Manny/BS_MM_WalkRun.BS_MM_WalkRun`
- `/Game/Characters/Mannequins/Animations/Manny/Falling_Idle_Loop.Falling_Idle_Loop`
- `/Game/Characters/Mannequins/Animations/Manny/Jumping_Up.Jumping_Up`
- `/Game/Characters/Mannequins/Animations/Manny/MM_Fall_Loop.MM_Fall_Loop`
- `/Game/Characters/Mannequins/Animations/Manny/MM_Idle.MM_Idle`
- `/Game/Characters/Mannequins/Animations/Manny/MM_Jump.MM_Jump`
- `/Game/Characters/Mannequins/Animations/Manny/MM_Land.MM_Land`
- `/Game/Characters/Mannequins/Animations/Manny/Unarmed_Idle_Anim1.Unarmed_Idle_Anim1`
- `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`
- `/Game/Characters/Mannequins/Rigs/CR_Mannequin_BasicFootIK.CR_Mannequin_BasicFootIK_C`
- `/Game/ThirdPerson/Animations/Idles/Standing_Idle_Anim.Standing_Idle_Anim`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `db629682bcab46be46637b405a8e33f5ab1a72ec2c44ae7ad6233ea794c00e99`.
