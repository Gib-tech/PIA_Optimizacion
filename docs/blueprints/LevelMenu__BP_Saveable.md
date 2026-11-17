# BP_Saveable

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/BP_Saveable`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/CoreUObject.Interface'"`.

Interfaz original para objetos guardables. No confundir su presencia con que todos los actores estén serializados; las propiedades finales se enumeran en BP_DeliverySave.

## Entradas y responsabilidades del grafo

- **`SaveData`** en `SaveData`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`LoadData`** en `LoadData`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 2 nodos con pines. Funciones referenciadas: `LoadData`, `SaveData`.

- `/Game/LevelMenu/BP_SaveGame.BP_SaveGame_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `ba4959946bafb06a2c2cc9c1ce9bd2759366f8dd40e1f270ac9c6c2c34c1c640`.
