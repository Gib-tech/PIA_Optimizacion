# CR_Mannequin_Body

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/CR_Mannequin_Body`. **Tipo:** ControlRigBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/ControlRig.ControlRig'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

Este Blueprint contiene datos, configuración o un rig. No presenta una entrada de ejecución K2 propia que describir como lógica de gameplay.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `L Arm IK Mode` — tipo `bool`.
- `R Arm IK Mode` — tipo `bool`.
- `L Leg IK Mode ` — tipo `bool`.
- `R Leg IK Mode` — tipo `bool`.
- `Spine IK Mode` — tipo `bool`.
- `Neck IK Mode` — tipo `bool`.
- `Spine Offsets` — tipo `struct`.
- `Spine Length` — tipo `real`.
- `Neck Length` — tipo `real`.
- `L Arm IK Align` — tipo `bool`.
- `R Arm IK Align` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 1930 nodos con pines. Funciones referenciadas: .

- `/Game/Developers/Jeremie/MetaHuman/FootRoll/FootRoll_A.FootRoll_A`
- `/Game/Developers/Jeremie/MetaHuman/IKSpine/IKSpine_A_003.IKSpine_A_003`
- `/Game/Developers/Jeremie/MetaHuman/MetaHuman_ControlRig_Functions.MetaHuman_ControlRig_Functions`
- `/Game/Survival_Character/Demo/Characters/Mannequins/Meshes/SKM_Manny.SKM_Manny`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `d15e49f214b020b6db98ff2d5b0b7cf001731e7a95b6bd31a876382c88a2f494`.
