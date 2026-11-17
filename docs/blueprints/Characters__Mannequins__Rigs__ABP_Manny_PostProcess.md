# ABP_Manny_PostProcess

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Rigs/ABP_Manny_PostProcess`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`AnimGraph__AnimFunc`** en `AnimGraph__AnimFunc`. Operaciones alcanzables desde `then`: `K2Node_FunctionResult`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimGraph__AnimFunc_MERGED`** en `AnimGraph__AnimFunc_MERGED`. Operaciones alcanzables desde `then`: `K2Node_FunctionResult`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 28 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `TryGetPawnOwner`.

- `/Game/Characters/Mannequins/Meshes/SKM_Manny.SKM_Manny`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`
- `/Game/Characters/Mannequins/Rigs/CR_Mannequin_Procedural.CR_Mannequin_Procedural_C`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_calf_l_pose.Manny_calf_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_calf_r_pose.Manny_calf_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_clavicle_l_pose.Manny_clavicle_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_clavicle_r_pose.Manny_clavicle_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_foot_l_pose.Manny_foot_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_foot_r_pose.Manny_foot_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_hand_l_pose.Manny_hand_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_hand_r_pose.Manny_hand_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_lowerarm_l_pose.Manny_lowerarm_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_lowerarm_r_pose.Manny_lowerarm_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_thigh_l_pose.Manny_thigh_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_thigh_r_pose.Manny_thigh_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_upperarm_l_pose.Manny_upperarm_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Manny/Manny_upperarm_r_pose.Manny_upperarm_r_pose`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `bee10c8c593900db5fbf273a7748ee1a424caf9fa97401a9c66e7764837d9688`.
