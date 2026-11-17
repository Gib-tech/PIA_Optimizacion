# BTService_HostageSense

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/BTService_HostageSense`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTService_BlueprintBase'"`.

Evalúa amenazas, seguimiento y refugios locales con ruta completa. Escribe bMustFlee, bWaiting, bAccompanying, FleeLocation y Estado en el Blackboard. No sustituye el árbol con decisiones de movimiento por Tick.

## Entradas y responsabilidades del grafo

- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTService_HostageSense`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetValueAsObject`, `SetValueAsFloat`, `Asignar ThreatActor`, `GetAllActorsOfClass`, `K2Node_MacroInstance`, `Condición`, `SetValueAsBool`, `Asignar ThreatActor`, `Condición`, `Asignar SafeCandidate`, `Asignar BestDistance`, `GetAllActorsWithTag`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `ThreatActor` — tipo `object`.
- `Candidate` — tipo `object`.
- `SafeCandidate` — tipo `object`.
- `BestDistance` — tipo `real`.
- `MinEnemyDistance` — tipo `real`.
- `ThreatRadius` — tipo `real`.
- `SafeEnemyDistance` — tipo `real`.
- `SafePlayerDistance` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 101 nodos con pines. Funciones referenciadas: `BooleanAND`, `FMin`, `FindPathToLocationSynchronously`, `GetAllActorsOfClass`, `GetAllActorsWithTag`, `GetBlackboard`, `GetDistanceTo`, `GetPathLength`, `GetPlayerPawn`, `GetValueAsBool`, `GreaterEqual_DoubleDouble`, `IsPartial`, `IsValid`, `K2_GetActorLocation`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `LineOfSightTo`, `MakeLiteralName`, `Not_PreBool`, `ReceiveTickAI`, `SetValueAsBool`, `SetValueAsFloat`, `SetValueAsInt`, `SetValueAsObject`, `SetValueAsVector`.

- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `a3d8cc147ab3d860b8829883ea52d4a74cbc7aca00341c5f501c81cd4c9436cb`.
