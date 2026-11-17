# BP_LuminariaPared

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_LuminariaPared`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Luminaria reutilizable colocada sobre paredes mediante trazas. Soporte, carcasa, difusor cálido y foco inclinado de 3200 lúmenes, radio 1450 cm y sombras. Sin Tick ni colisión/navegación; luces limitadas a 6500 cm con desvanecimiento de 1400 cm. Hay 41 instancias en los diez sectores del mapa. Ver REVISION_JUGABLE.md y prepare_daynight_wall_lights.py.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveActorBeginOverlap`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 4 nodos con pines. Funciones referenciadas: `ReceiveActorBeginOverlap`, `ReceiveBeginPlay`, `ReceiveTick`, `UserConstructionScript`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `bb1d96a23e8c5e2c4ebfabf5220afd7f371d3cd96235e9f158c0685e323de251`.
