# BP_BeaconEntrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.StaticMeshActor'"`.

Baliza A/B/C con identidad fija, aproximación y estado activado. Sólo acepta el siguiente elemento de la permutación revelada y la canalización válida del rehén. Actualiza luces y comunica avance al director.

## Entradas y responsabilidades del grafo

- **`CompleteActivation`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `Condición`, `Asignar bActivated`, `Asignar Paso`, `Condición`, `K2Node_DynamicCast`, `Asignar bUnlocked`, `SetMaterial`, `K2Node_DynamicCast`, `GrantHammerUpgrade`, `SpawnSystemAtLocation`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `SetMaterial`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_BeaconEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`CompleteActivation`** en `CompleteActivation`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_BeaconEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Index` — tipo `int`.
- `RequiredZone` — tipo `object`.
- `Door` — tipo `object`.
- `bActivated` — tipo `bool`.
- `ActivationProgress` — tipo `real`.
- `ApproachPoint` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 97 nodos con pines. Funciones referenciadas: `Add_IntInt`, `BooleanAND`, `Clamp`, `CompleteActivation`, `EqualEqual_IntInt`, `EqualEqual_ObjectObject`, `GetActorOfClass`, `GetBlackboard`, `GetHorizontalDistanceTo`, `GetPlayerPawn`, `GetValueAsBool`, `GrantHammerUpgrade`, `GreaterEqual_DoubleDouble`, `Greater_DoubleDouble`, `K2_GetActorLocation`, `LessEqual_DoubleDouble`, `Less_IntInt`, `MakeLiteralName`, `Not_PreBool`, `ReceiveTick`, `SelectInt`, `SetMaterial`, `SpawnSystemAtLocation`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestructibleDoor.BP_DestructibleDoor_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Environment/Baliza/M_Baliza_Activada.M_Baliza_Activada`
- `/Game/ThirdPerson/Environment/Baliza/M_Baliza_Espera.M_Baliza_Espera`
- `/Game/ThirdPerson/Environment/Baliza/M_Baliza_Siguiente.M_Baliza_Siguiente`
- `/Game/ThirdPerson/Environment/Progression/M_DoorPowered.M_DoorPowered`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `34bdd3044d5e9956a4deb58e7f029c05c4de77995c192c6a8dc61db5ce7e2d6e`.
