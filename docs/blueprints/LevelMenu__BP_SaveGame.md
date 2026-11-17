# BP_SaveGame

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/BP_SaveGame`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.SaveGame'"`.

Esquema de guardado original del menú. Se conserva por compatibilidad de recursos antiguos; no es la fuente autoritativa del checkpoint de Nivel_Entrega.

## Entradas y responsabilidades del grafo

- **`SaveData`** en `SaveData`. Operaciones alcanzables desde `then`: `K2Node_MacroInstance`, `SaveData`, `SaveData`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`LoadingRequested`** en `LoadingRequested`. Operaciones alcanzables desde `then`: `LoadData`, `LoadingRequested`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `PlayerLoc` — tipo `struct`.

## Operaciones y dependencias verificadas

La exportación contiene 9 nodos con pines. Funciones referenciadas: `LoadData`, `LoadingRequested`, `SaveData`.

- `/Game/LevelMenu/BP_Saveable.BP_Saveable_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `f6979f01025bca693f36ad6d37268bb7f79953b27c916be0f262120e9ef35d19`.
