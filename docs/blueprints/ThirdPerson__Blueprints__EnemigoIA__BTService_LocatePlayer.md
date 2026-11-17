# BTService_LocatePlayer

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTService_LocatePlayer`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTService_BlueprintBase'"`.

Servicio de percepción del orbitador. Escribe objetivo, distancias, visión y fijación del rehén en el Blackboard. El rehén rescatado puede tener prioridad; no aplica daño ni mueve al enemigo.

## Entradas y responsabilidades del grafo

- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar ChosenTarget`, `GetActorOfClass`, `SetValueAsBool`, `Condición`, `Asignar ChosenTarget`, `Asignar CombatTarget`, `SetValueAsFloat`, `Condición`, `SetValueAsObject`, `SetValueAsObject`, `SetValueAsVector`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTService_LocatePlayer`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `PlayerCharacter` — tipo `object`.
- `SearchRadius` — tipo `struct`.
- `TargetActor` — tipo `struct`.
- `DistanceToTargetKey` — tipo `struct`.
- `OrbitLocationKey` — tipo `struct`.
- `ChosenTarget` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 60 nodos con pines. Funciones referenciadas: `Add_VectorVector`, `BooleanAND`, `BooleanOR`, `GetActorOfClass`, `GetBlackboard`, `GetDistanceTo`, `GetPlayerPawn`, `GetValueAsBool`, `GreaterEqual_DoubleDouble`, `K2_GetActorLocation`, `LessEqual_DoubleDouble`, `LineOfSightTo`, `MakeLiteralName`, `Multiply_VectorFloat`, `Normal`, `Not_PreBool`, `ReceiveTickAI`, `RotateAngleAxis`, `SelectFloat`, `SelectVector`, `SetValueAsBool`, `SetValueAsFloat`, `SetValueAsObject`, `SetValueAsVector`, `Subtract_VectorVector`.

- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `142d73a8190fa04ff3dd1d47e205c8a34dad954ddc244c3323debdb48a99f212`.
