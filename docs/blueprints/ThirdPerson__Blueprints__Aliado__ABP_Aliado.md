# ABP_Aliado

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/ABP_Aliado`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

AnimBlueprint de referencia del aliado original. Se conserva como fuente histórica; la entrega utiliza la especialización del rehén.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `speed` — tipo `real`.
- `bIsModular` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 13 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `TryGetPawnOwner`.

- `/Game/Characters/Mannequins/Animations/Manny/Unarmed_Idle_Anim1.Unarmed_Idle_Anim1`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`
- `/Game/ThirdPerson/Blueprints/Aliado/ThirdPersonWalk.ThirdPersonWalk`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `c28c72b8569e63f239f303d0c412fa9952b022f7120ba78815f887c1b86f1f6e`.
