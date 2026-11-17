# ABP_EnemyEntrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/ABP_EnemyEntrega`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Envuelve la locomoción original del pack y añade DefaultSlot para montajes de combate. Ignora root motion en las acciones de enemigo para que la navegación controle el desplazamiento.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar NormSpeed`, `Asignar IsInAir?`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `BlueprintUpdateAnimation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_ABP_EnemyEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `NormSpeed` — tipo `real`.
- `IsInAir?` — tipo `bool`.
- `IsModular` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 17 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `Divide_DoubleDouble`, `IsFalling`, `TryGetPawnOwner`, `VSize`.

- `/Game/SciFITrooper_Man_03/Blueprints/AnimBP/ABP_SciFiTrooperManV3.ABP_SciFiTrooperManV3_C`
- `/Game/SciFITrooper_Man_03/SkeletalMesh/CH_SciFiTrooper_Man_03_Skeleton.CH_SciFiTrooper_Man_03_Skeleton`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `43e06dcc7829b718d4e96a451e4c126bac4d823b401fa84502c0a125f1db431a`.
