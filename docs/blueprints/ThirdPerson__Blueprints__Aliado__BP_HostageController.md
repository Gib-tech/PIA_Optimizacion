# BP_HostageController

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/BP_HostageController`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.AIController'"`.

Posee al aliado e inicia BT_Hostage/BB_Hostage. El jugador nunca posee al rehén; E/RB comunica intención y el árbol decide la acción.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `RunBehaviorTree`, `SetValueAsBool`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_HostageController`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 9 nodos con pines. Funciones referenciadas: `GetBlackboard`, `MakeLiteralName`, `ReceiveBeginPlay`, `RunBehaviorTree`, `SetValueAsBool`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Aliado/BT_Hostage.BT_Hostage`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `2eccc152cbc01c2ea7fc4a3fc4d3187e9651a22d76f3f578641aff631ca74f5c`.
