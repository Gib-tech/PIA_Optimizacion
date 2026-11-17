# BP_CombatZone

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.TriggerBox'"`.

Encuentro con dos oleadas de dos enemigos. Requiere rehén siguiendo y requisitos de progresión; mantiene lista de enemigos, fase e intermedio. La tercera instancia combina ambos tipos y solicita la revelación del último guardián. Phase 0 espera, 1 combate, 2 intermedio y 3 despejado.

## Entradas y responsabilidades del grafo

- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_SwitchInteger`, `Condición`, `Asignar LivingCount`, `Condición`, `GetActorOfClass`, `K2Node_MacroInstance`, `Array_Clear`, `Condición`, `Condición`, `Condición`, `Asignar CurrentWave`, `Condición`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartWave`** en `EventGraph`. Operaciones alcanzables desde `then`: `Array_Clear`, `Asignar CurrentWave`, `K2Node_SpawnActorFromClass`, `Asignar EncounterZone`, `Array_AddUnique`, `K2Node_SpawnActorFromClass`, `Asignar EncounterZone`, `Array_AddUnique`, `Asignar Phase`, `Asignar LivingCount`, `Asignar SpawnedCount`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_CombatZone`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`StartWave`** en `StartWave`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_CombatZone`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `EnemyClass` — tipo `class`.
- `SpawnPoint1` — tipo `object`.
- `SpawnPoint2` — tipo `object`.
- `Blocker` — tipo `object`.
- `RefugePoint` — tipo `object`.
- `EncounterEnemies` — tipo `object`.
- `CurrentWave` — tipo `int`.
- `WaveCount` — tipo `int`.
- `Phase` — tipo `int`.
- `LivingCount` — tipo `int`.
- `SpawnedCount` — tipo `int`.
- `NextWaveAt` — tipo `real`.
- `bCleared` — tipo `bool`.
- `RequiredZone` — tipo `object`.
- `AlternateEnemyClass` — tipo `class`.
- `bMixedEnemies` — tipo `bool`.
- `bFinalStand` — tipo `bool`.
- `bRevelationStarted` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 84 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_IntInt`, `Array_AddUnique`, `Array_Clear`, `BooleanAND`, `Conv_BoolToInt`, `EqualEqual_IntInt`, `GetActorOfClass`, `GetBlackboard`, `GetDistanceTo`, `GetPlayerPawn`, `GetTimeSeconds`, `GetValueAsBool`, `GreaterEqual_DoubleDouble`, `IsOverlappingActor`, `IsValid`, `K2_GetActorLocation`, `LessEqual_DoubleDouble`, `Less_IntInt`, `MakeLiteralName`, `MakeTransform`, `Not_PreBool`, `ReceiveTick`, `StartWave`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `3e5481ab908d37fb0ab958d36b7324fe49237ebb0df9b9d21e0007360a9829f0`.
