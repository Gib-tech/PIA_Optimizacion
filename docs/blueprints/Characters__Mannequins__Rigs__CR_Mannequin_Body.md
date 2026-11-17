# CR_Mannequin_Body

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Rigs/CR_Mannequin_Body`. **Tipo:** ControlRigBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/ControlRig.ControlRig'"`.

Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.

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

- `/Game/Characters/Mannequins/Meshes/SKM_Manny.SKM_Manny`
- `/Game/Developers/Jeremie/MetaHuman/FootRoll/FootRoll_A.FootRoll_A`
- `/Game/Developers/Jeremie/MetaHuman/IKSpine/IKSpine_A_003.IKSpine_A_003`
- `/Game/Developers/Jeremie/MetaHuman/MetaHuman_ControlRig_Functions.MetaHuman_ControlRig_Functions`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `ab13fcb5f5549ed86f95ecbf075e5a941baf81488b4ff55dd20172b5be2af5bc`.
