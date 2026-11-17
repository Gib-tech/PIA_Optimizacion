# CR_Mannequin_BasicFootIK

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Rigs/CR_Mannequin_BasicFootIK`. **Tipo:** ControlRigBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/ControlRig.ControlRig'"`.

Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.

## Entradas y responsabilidades del grafo

Este Blueprint contiene datos, configuración o un rig. No presenta una entrada de ejecución K2 propia que describir como lógica de gameplay.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `ZOffset_L_Target` — tipo `real`.
- `ZOffset_R_Target` — tipo `real`.
- `ZOffset_L` — tipo `real`.
- `ZOffset_R` — tipo `real`.
- `ZOffset_Pelvis` — tipo `real`.
- `ShouldDoIKTrace` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 45 nodos con pines. Funciones referenciadas: .

- `/Game/Characters/Mannequins/Meshes/SKM_Manny.SKM_Manny`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `6318c626cd22e2bf14d94993830345d9855cf4b8640693baccb1dee25c605271`.
