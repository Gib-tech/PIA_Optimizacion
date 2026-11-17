# BP_DoorFragment

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DoorFragment`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.StaticMeshActor'"`.

Fragmento visual/físico de puerta. Aplica movimiento/rotación de rotura, ignora peones/cámara y expira para limitar coste. No cuenta como tipo distinto de destruible por cada fragmento.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetStaticMesh`, `SetSimulatePhysics`, `AddImpulse`, `SetPhysicsAngularVelocityInDegrees`, `SetLifeSpan`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DoorFragment`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `ShardMesh` — tipo `object`.
- `BreakVelocity` — tipo `struct`.

## Operaciones y dependencias verificadas

La exportación contiene 16 nodos con pines. Funciones referenciadas: `AddImpulse`, `Multiply_VectorFloat`, `RandomFloatInRange`, `RandomUnitVector`, `ReceiveBeginPlay`, `SetLifeSpan`, `SetPhysicsAngularVelocityInDegrees`, `SetSimulatePhysics`, `SetStaticMesh`, `UserConstructionScript`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `4ed924816ce8ce1852e066029f839671f8bb25ab1e271aa256ff42979d7f6c4b`.
