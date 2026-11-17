# BP_IAController

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_IAController`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.AIController'"`.

Posee al orbitador, inicializa BB_EnemyIA y ejecuta BT_EnemyIA. DetectionRadius y CombatTarget alimentan decisiones de árbol, no una cadena de decisiones en Actor Tick.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `RunBehaviorTree`, `SetValueAsFloat`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_IAController`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `DetectionRadiusKey` — tipo `name`.

## Operaciones y dependencias verificadas

La exportación contiene 8 nodos con pines. Funciones referenciadas: `GetBlackboard`, `ReceiveBeginPlay`, `RunBehaviorTree`, `SetValueAsFloat`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA.BT_EnemyIA`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `af9a35240e532947670259182eaddc3ea90a1c8c9d4aaef41f34bc00b9cd211e`.
