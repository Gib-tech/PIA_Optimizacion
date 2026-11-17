# CR_Mannequin_Procedural

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Rigs/CR_Mannequin_Procedural`. **Tipo:** ControlRigBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/ControlRig.ControlRig'"`.

Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.

## Entradas y responsabilidades del grafo

Este Blueprint contiene datos, configuración o un rig. No presenta una entrada de ejecución K2 propia que describir como lógica de gameplay.

## Operaciones y dependencias verificadas

La exportación contiene 172 nodos con pines. Funciones referenciadas: .

- `/Game/Characters/Mannequins/Meshes/SKM_Quinn.SKM_Quinn`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `25ff60d9cb6d2e4503e34221a35842c2a1172255cd2f4abe1303c4134b88f15a`.
