# HealthBar

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Menu/HealthBar`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Barra de salud de interfaz original. La ruta distingue copias del menú y recursos propios; no confundir cantidad de widgets con sistemas diferentes.

## Entradas y responsabilidades del grafo

- **`PreConstruct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Construct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Tick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 3 nodos con pines. Funciones referenciadas: `Construct`, `PreConstruct`, `Tick`.

- `/Game/Menu/Barra_vida_OV.Barra_vida_OV`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `d5c7c5ba078d9db97e3873eee539de3166e58f6692bfade83867ff7a4671a145`.
