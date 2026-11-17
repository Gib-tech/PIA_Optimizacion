# BP_TargetDummy

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/BP_TargetDummy`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Actor de práctica original. Útil para depurar contactos; no sustituye pruebas contra enemigos con controlador y Behavior Tree activos.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveActorBeginOverlap`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`UserConstructionScript`** en `UserConstructionScript_MERGED`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 5 nodos con pines. Funciones referenciadas: `ReceiveActorBeginOverlap`, `ReceiveBeginPlay`, `ReceiveTick`, `UserConstructionScript`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `3ca271aecfde4ce75b6f685198ddb6aad5df5472c6341975f18edc77bd3a7288`.
