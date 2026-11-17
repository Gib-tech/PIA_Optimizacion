# BPC_E_Health

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.ActorComponent'"`.

Componente de salud enemiga. Descuenta el daño aceptado, emite E_Dead al llegar a cero y sirve como fuente de confirmación de impacto real.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`E_Decrease_Health`** en `E_Decrease_Health`. Operaciones alcanzables desde `then`: `Condición`, `Asignar E_Health`, `K2Node_CallDelegate`, `Condición`, `K2Node_CallDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`E_Updated_Heatlh`** en `E_Updated_Heatlh`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`E_Dead`** en `E_Dead`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `E_Health` — tipo `real`.
- `E_Updated_Heatlh` — tipo `mcdelegate`.
- `E_Dead` — tipo `mcdelegate`.

## Operaciones y dependencias verificadas

La exportación contiene 16 nodos con pines. Funciones referenciadas: `E_Dead`, `E_Decrease_Health`, `E_Updated_Heatlh`, `Greater_DoubleDouble`, `LessEqual_DoubleDouble`, `ReceiveBeginPlay`, `ReceiveTick`, `Subtract_DoubleDouble`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `1dd1adf648469ae5fd5d290f5855386be877a21daeabcfb5f4de8615f98ae3de`.
