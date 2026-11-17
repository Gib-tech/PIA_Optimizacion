# CR_Mannequin_Procedural

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Survival_Character/Demo/Characters/Mannequins/Rigs/CR_Mannequin_Procedural`. **Tipo:** ControlRigBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/ControlRig.ControlRig'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

Este Blueprint contiene datos, configuración o un rig. No presenta una entrada de ejecución K2 propia que describir como lógica de gameplay.

## Operaciones y dependencias verificadas

La exportación contiene 172 nodos con pines. Funciones referenciadas: .

- `/Game/Survival_Character/Demo/Characters/Mannequins/Meshes/SKM_Quinn.SKM_Quinn`
- `/Game/Survival_Character/Meshes/SKEL_Survival_Character.SKEL_Survival_Character`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `31592d5469d4d35f760a2dbb64269838fcd7624578efe7cb2e1d152e649a14cb`.
