# W_DemoWidget

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/SciFITrooper_Man_03/DemoContent/W_DemoWidget`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

- **`-UpdateDebugTrace`** en `-UpdateDebugTrace`. Operaciones alcanzables desde `then`: `SetText`, `SetColorAndOpacity`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PreConstruct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Construct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Tick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`-UpdateDebugTrace`** en `-UpdateDebugTrace_MERGED`. Operaciones alcanzables desde `then`: `SetText`, `SetColorAndOpacity`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 29 nodos con pines. Funciones referenciadas: `-UpdateDebugTrace`, `Construct`, `PreConstruct`, `SetColorAndOpacity`, `SetText`, `Tick`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `8b4346c036377e1eddfc8f84f8830d6fc6e247ad1872f7a74dc4d05eeffb6ea8`.
