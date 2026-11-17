# BP_SaveInterface

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/BP_SaveInterface`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/CoreUObject.Interface'"`.

Contrato del guardado original. Revisar referencias antes de retirarlo; el flujo final de misión está en los Blueprints DeliverySave.

## Entradas y responsabilidades del grafo

- **`RequestSave`** en `RequestSave`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`RequestLoad`** en `RequestLoad`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 2 nodos con pines. Funciones referenciadas: `RequestLoad`, `RequestSave`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `f8784f778423d813df4f35f69fe9b834f2e1ddbd67a9bc8ffca6d058ded0ebc8`.
