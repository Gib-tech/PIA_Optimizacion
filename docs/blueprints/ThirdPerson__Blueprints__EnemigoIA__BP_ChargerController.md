# BP_ChargerController

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_ChargerController`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.AIController'"`.

Posee al embestidor e inicia BT_Charger con su Blackboard. Mantiene separada la arquitectura de decisiones de la del orbitador.

## Entradas y responsabilidades del grafo

- **`ReceivePossess`** en `EventGraph`. Operaciones alcanzables desde `then`: `UseBlackboard`, `K2Node_DynamicCast`, `Asignar CombatTarget`, `SetValueAsFloat`, `SetValueAsObject`, `RunBehaviorTree`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceivePossess`** en `ReceivePossess`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ChargerController`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 17 nodos con pines. Funciones referenciadas: `GetBlackboard`, `GetDistanceTo`, `GetPlayerPawn`, `MakeLiteralName`, `ReceivePossess`, `RunBehaviorTree`, `SetValueAsFloat`, `SetValueAsObject`, `UseBlackboard`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BB_Charger.BB_Charger`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BT_Charger.BT_Charger`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `623127173b7146ae62424248d0ca90e12b11ee0010838516ae8b1e1585f50ab8`.
