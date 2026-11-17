# BP_Knife_Mann

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/RamsterZ_FreeAnims_Volume1/Demo/Mannequin/Character/Mesh/BP_Knife_Mann`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

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

**Huella de exportación:** `2e5d456a6c2f31587d27f45c6e65fabbc014ce99b0adb06c51188b363a33a4cf`.
