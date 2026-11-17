# BP_DestructibleDoor

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DestructibleDoor`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.StaticMeshActor'"`.

Puerta de misión. Bloqueada hasta recibir carga de progresión. Dos golpes pesados de martillo mejorado reducen 50→25→0: primero grietas geométricas, después fragmentos correspondientes y actualización de navegación.

## Entradas y responsabilidades del grafo

- **`ReceiveAnyDamage`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Condición`, `Asignar Health`, `PlaySound2D`, `Condición`, `Asignar bCracked`, `Condición`, `SetStaticMesh`, `Asignar bDestroyed`, `Asignar bDoorPending`, `SetActorEnableCollision`, `SetActorHiddenInGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveAnyDamage`** en `ReceiveAnyDamage`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DestructibleDoor`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `BeaconIndex` — tipo `int`.
- `bUnlocked` — tipo `bool`.
- `bDestroyed` — tipo `bool`.
- `Health` — tipo `real`.
- `bCracked` — tipo `bool`.
- `CrackedMesh` — tipo `object`.
- `FragmentMeshes` — tipo `object`.
- `FragmentOffsets` — tipo `struct`.
- `DoorHeight` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 79 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_VectorVector`, `BooleanAND`, `BreakVector`, `FMax`, `FMin`, `GetTransform`, `Greater_DoubleDouble`, `K2_GetActorLocation`, `K2_GetActorRotation`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `MakeTransform`, `MakeVector`, `Multiply_DoubleDouble`, `Multiply_VectorFloat`, `Not_PreBool`, `PlaySound2D`, `ReceiveAnyDamage`, `SetActorEnableCollision`, `SetActorHiddenInGame`, `SetStaticMesh`, `SpawnSystemAtLocation`, `Subtract_DoubleDouble`, `Subtract_VectorVector`, `TransformDirection`, `TransformLocation`, `UserConstructionScript`, `Vector_Normal2D`.

- `/Game/ThirdPerson/Audio/SW_DoorBreak.SW_DoorBreak`
- `/Game/ThirdPerson/Audio/SW_DoorHit.SW_DoorHit`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DoorFragment.BP_DoorFragment_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/FX/NS_DoorBreak.NS_DoorBreak`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `24855ef359e610a4f20380ef35b5e1e85da3e3fe73b17cdd0829b0c0bbf64102`.
