# BPC_Health

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.ActorComponent'"`.

Componente de salud del jugador. Disminuye la vida con el daño recibido y comunica muerte. Botiquines limitan restauración a 100; el SaveManager restaura el valor del checkpoint.

## Entradas y responsabilidades del grafo

- **`Dead`** en `Dead`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Updated_Heatlh`** en `Updated_Heatlh`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Decrease_Health`** en `Decrease_Health`. Operaciones alcanzables desde `then`: `Asignar Health`, `K2Node_CallDelegate`, `Condición`, `K2Node_CallDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Increase_Health`** en `Increase_Health`. Operaciones alcanzables desde `then`: `Asignar Health`, `K2Node_CallDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Health` — tipo `real`.
- `Updated_Heatlh` — tipo `mcdelegate`.
- `Dead` — tipo `mcdelegate`.

## Operaciones y dependencias verificadas

La exportación contiene 19 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Dead`, `Decrease_Health`, `FClamp`, `Increase_Health`, `LessEqual_DoubleDouble`, `ReceiveBeginPlay`, `ReceiveTick`, `Subtract_DoubleDouble`, `Updated_Heatlh`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `70c919f23daf5601ca549fe84ea0087d66314df5a1717280cd4eecc73e5f8cb1`.
