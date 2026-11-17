# BPI_Enemy

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BPI_Enemy`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/CoreUObject.Interface'"`.

Contrato de acciones de enemigo utilizado desde tareas del árbol. Permite solicitar ataque/defensa/interrupción sin trasladar la decisión al actor.

## Entradas y responsabilidades del grafo

- **`Attack`** en `Attack`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Operaciones y dependencias verificadas

La exportación contiene 1 nodos con pines. Funciones referenciadas: `Attack`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `9e9514a8639072236e94f8faee5684141ec374fe92bf8b961fc629840274a1ee`.
