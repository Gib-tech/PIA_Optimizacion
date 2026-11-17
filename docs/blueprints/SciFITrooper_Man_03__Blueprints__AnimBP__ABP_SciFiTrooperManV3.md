# ABP_SciFiTrooperManV3

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/SciFITrooper_Man_03/Blueprints/AnimBP/ABP_SciFiTrooperManV3`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar NormSpeed`, `Asignar IsInAir?`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_ModifyBone_2F57EABC4641408F453BBAAAAAD77BFD`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_ModifyBone_2F57EABC4641408F453BBAAAAAD77BFD`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_SciFiTrooperManV3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_ModifyBone_3D03C1BE4B89C9C0F97495B42AD75415`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_ModifyBone_3D03C1BE4B89C9C0F97495B42AD75415`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_SciFiTrooperManV3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_TransitionResult_DACC02EC43D21538B06826A2DDD83B49`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_TransitionResult_DACC02EC43D21538B06826A2DDD83B49`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_SciFiTrooperManV3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_TransitionResult_8565306B48D0E349F245BBA0365D3BCC`** en `EvaluateGraphExposedInputs_ExecuteUbergraph_ABP_SciFiTrooperManV3_AnimGraphNode_TransitionResult_8565306B48D0E349F245BBA0365D3BCC`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_ABP_SciFiTrooperManV3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `BlueprintUpdateAnimation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_ABP_SciFiTrooperManV3`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `NormSpeed` — tipo `real`.
- `IsInAir?` — tipo `bool`.
- `IsModular` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 59 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `Divide_DoubleDouble`, `GetInstanceAssetPlayerTimeFromEndFraction`, `IsFalling`, `Less_DoubleDouble`, `Not_PreBool`, `TryGetPawnOwner`, `VSize`.

- `/Game/SciFITrooper_Man_03/Blueprints/AnimBP/BS_TrooperManV3_1D.BS_TrooperManV3_1D`
- `/Game/SciFITrooper_Man_03/DemoContent/Anims/ThirdPersonJump_Loop.ThirdPersonJump_Loop`
- `/Game/SciFITrooper_Man_03/DemoContent/Anims/ThirdPersonJump_Start.ThirdPersonJump_Start`
- `/Game/SciFITrooper_Man_03/DemoContent/Anims/ThirdPerson_Jump.ThirdPerson_Jump`
- `/Game/SciFITrooper_Man_03/SkeletalMesh/CH_SciFiTrooper_Man_03_Skeleton.CH_SciFiTrooper_Man_03_Skeleton`
- `/Game/SciFITrooper_Man_03/SkeletalMesh/SK_SciFITrooper_Man_03.SK_SciFITrooper_Man_03`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `05130d831e4ffecbcc7ded37d968cf3ab6fc390349c602cc441683eae703bced`.
