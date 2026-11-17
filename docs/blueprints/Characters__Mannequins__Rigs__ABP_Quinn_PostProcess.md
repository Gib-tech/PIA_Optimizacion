# ABP_Quinn_PostProcess

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Rigs/ABP_Quinn_PostProcess`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`AnimGraph__AnimFunc`** en `AnimGraph__AnimFunc`. Operaciones alcanzables desde `then`: `K2Node_FunctionResult`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AnimGraph__AnimFunc_MERGED`** en `AnimGraph__AnimFunc_MERGED`. Operaciones alcanzables desde `then`: `K2Node_FunctionResult`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 28 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `TryGetPawnOwner`.

- `/Game/Characters/Mannequins/Meshes/SKM_Quinn.SKM_Quinn`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`
- `/Game/Characters/Mannequins/Rigs/CR_Mannequin_Procedural.CR_Mannequin_Procedural_C`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_calf_l_pose.Quinn_calf_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_calf_r_pose.Quinn_calf_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_clavicle_l_pose.Quinn_clavicle_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_clavicle_r_pose.Quinn_clavicle_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_foot_l_pose.Quinn_foot_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_foot_r_pose.Quinn_foot_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_hand_l_pose.Quinn_hand_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_hand_r_pose.Quinn_hand_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_lowerarm_l_pose.Quinn_lowerarm_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_lowerarm_r_pose.Quinn_lowerarm_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_thigh_l_pose.Quinn_thigh_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_thigh_r_pose.Quinn_thigh_r_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_upperarm_l_pose.Quinn_upperarm_l_pose`
- `/Game/Characters/Mannequins/Rigs/Poses/Quinn/Quinn_upperarm_r_pose.Quinn_upperarm_r_pose`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `ad137c5c3b30b9e244af937d97a768e2e3a57f2ec36dbc174139ed90dfc28757`.
