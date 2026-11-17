# ABP_Quinn_PostProcess

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/ABP_Quinn_PostProcess`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 21 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `TryGetPawnOwner`.

- `/Game/Survival_Character/Demo/Characters/Mannequins/Meshes/SKM_Quinn.SKM_Quinn`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/CR_Mannequin_Procedural.CR_Mannequin_Procedural_C`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_calf_l_pose.Quinn_calf_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_calf_r_pose.Quinn_calf_r_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_clavicle_l_pose.Quinn_clavicle_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_clavicle_r_pose.Quinn_clavicle_r_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_foot_l_pose.Quinn_foot_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_foot_r_pose.Quinn_foot_r_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_hand_l_pose.Quinn_hand_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_hand_r_pose.Quinn_hand_r_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_lowerarm_l_pose.Quinn_lowerarm_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_lowerarm_r_pose.Quinn_lowerarm_r_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_thigh_l_pose.Quinn_thigh_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_thigh_r_pose.Quinn_thigh_r_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_upperarm_l_pose.Quinn_upperarm_l_pose`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_upperarm_r_pose.Quinn_upperarm_r_pose`
- `/Game/Survival_Character/Meshes/SKEL_Survival_Character.SKEL_Survival_Character`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `8c3a27c827e5d4baa83ba678d8ccbae111ed157efebbddada065c7151e67ec4a`.
