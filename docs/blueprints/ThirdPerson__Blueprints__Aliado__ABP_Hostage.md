# ABP_Hostage

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/ABP_Hostage`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

AnimBlueprint original de la escolta con locomoción por velocidad y presentación de muerte. Se conserva para reproducir la integración; la apariencia actual usa ABP_RehenSuperviviente.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar speed`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `BlueprintUpdateAnimation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_ABP_Hostage`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `speed` — tipo `real`.
- `bIsModular` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 21 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `GetVelocity`, `IsValid`, `TryGetPawnOwner`, `VSizeXY`.

- `/Game/Characters/Mannequins/Animations/Manny/Unarmed_Idle_Anim1.Unarmed_Idle_Anim1`
- `/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin`
- `/Game/ThirdPerson/Blueprints/Aliado/ThirdPersonWalk.ThirdPersonWalk`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `1aeac7d72de4e7559ee4918f7448f4a93864cf348bb2cf9b933555a89ffc6cfb`.
