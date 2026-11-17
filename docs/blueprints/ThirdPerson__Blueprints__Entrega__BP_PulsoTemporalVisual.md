# BP_PulsoTemporalVisual

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_PulsoTemporalVisual`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.StaticMeshActor'"`.

Frente cian que viaja desde el lado derecho del protagonista hasta el final del disparo. MoveComponentTo recorre la estela en 0,18 s. Dos anillos se expanden al llegar y el actor desaparece a los 0,52 s. BP_SistemasComplementarios resuelve la traza, el daño y las cargas.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetCustomPrimitiveDataFloat`, `SetCustomPrimitiveDataFloat`, `MoveComponentTo`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_PulsoTemporalVisual`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 11 nodos con pines. Funciones referenciadas: `GetTimeSeconds`, `MoveComponentTo`, `ReceiveBeginPlay`, `SetCustomPrimitiveDataFloat`, `UserConstructionScript`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `601d6e84d8d1c33048712cae9d82da343a52c378768d3cfe69ccfbc91a678f59`.
