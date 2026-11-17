# ABP_RehenSuperviviente

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/ABP_RehenSuperviviente`. **Tipo:** AnimBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.AnimInstance'"`.

Copia propia del AnimBlueprint de escolta compatible con el esqueleto del sobreviviente. Lee el Pawn válido, mezcla reposo/caminar/correr y conserva muerte. Las animaciones compatibles se reutilizan sin modificar el pack original.

## Entradas y responsabilidades del grafo

- **`BlueprintUpdateAnimation`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar speed`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`BlueprintUpdateAnimation`** en `BlueprintUpdateAnimation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_ABP_RehenSuperviviente`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `speed` — tipo `real`.
- `bIsModular` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 21 nodos con pines. Funciones referenciadas: `BlueprintUpdateAnimation`, `GetVelocity`, `IsValid`, `TryGetPawnOwner`, `VSizeXY`.

- `/Game/Characters/Mannequins/Animations/Manny/Unarmed_Idle_Anim1.Unarmed_Idle_Anim1`
- `/Game/ThirdPerson/Blueprints/Aliado/ThirdPersonWalk.ThirdPersonWalk`
- `/Game/ThirdPerson/Characters/Rehen/SKEL_RehenSuperviviente.SKEL_RehenSuperviviente`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `9801e95c49272a59012e446620c89bdd0e905037776dce6227e4b93c13292677`.
