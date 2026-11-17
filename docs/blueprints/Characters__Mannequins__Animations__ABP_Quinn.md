# ABP_Quinn

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Characters/Mannequins/Animations/ABP_Quinn`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/Engine.AnimBlueprintGeneratedClass'/Game/Characters/Mannequins/Animations/ABP_Manny.ABP_Manny_C'"`.

Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `BlueprintUpdateAnimation`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 4 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `TryGetPawnOwner`.

- `/Game/Characters/Mannequins/Animations/ABP_Manny.ABP_Manny_C`
- `/Game/Characters/Mannequins/Animations/Quinn/BS_MF_Unarmed_WalkRun.BS_MF_Unarmed_WalkRun`
- `/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `0af475e119b9e0622789e8d160906a6a9406eabd739430dd9c48d9208f41d47a`.
