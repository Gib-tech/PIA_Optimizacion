# BP_BaseEnemy

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Character'"`.

Enemigo orbitador y base común de combate. Expone acciones que invocan las tareas del Behavior Tree: ataque, orientación, defensa, interrupción y muerte. Valida objetivo, distancia, cono, montaje y línea de visión antes de aplicar daño. El árbol decide; el actor ejecuta.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar LastFeedbackHealth`, `K2Node_AddDelegate`, `K2Node_AddDelegate`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Enemy_Death`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bIsDead`, `Asignar bAttackInProgress`, `StopAnimMontage`, `K2Node_DynamicCast`, `StopLogic`, `DisableMovement`, `SetActorEnableCollision`, `Condición`, `Condición`, `Condición`, `PlayAnimMontage`, `Asignar FinalPeersAlive`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnHealthChanged`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar LastDamageAmount`, `Condición`, `K2Node_DynamicCast`, `Asignar LastFeedbackHealth`, `Asignar EnemyHitUntil`, `Condición`, `Asignar LastEnemyDamage`, `Condición`, `PlaySound2D`, `Asignar NextStaggerAt`, `SetValueAsBool`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Attack`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar AttackVictim`, `Asignar bAttackInProgress`, `Asignar bAttackResolved`, `Asignar NextAttackAt`, `StopMovement`, `PlayAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResolveAttack`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Condición`, `Asignar bAttackResolved`, `ApplyDamage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EndAttack`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bAttackInProgress`, `StopAnimMontage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UpdateStrike`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `K2_SetActorRotation`, `Condición`, `Condición`, `Condición`, `Asignar bAttackResolved`, `ApplyDamage`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`FinishFinalWords`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Asignar bFinalWordsPending`, `PlayAnimMontage`, `SetLifeSpan`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`FinishFinalWords`** en `FinishFinalWords`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UpdateStrike`** en `UpdateStrike`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`EndAttack`** en `EndAttack`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ResolveAttack`** en `ResolveAttack`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Attack`** en `Attack`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnHealthChanged`** en `OnHealthChanged`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Enemy_Death`** en `Enemy_Death`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BaseEnemy`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `bIsDead` — tipo `bool`.
- `bAttackInProgress` — tipo `bool`.
- `AttackVictim` — tipo `object`.
- `ContactDamage` — tipo `real`.
- `CombatTarget` — tipo `object`.
- `ChargeVictim` — tipo `object`.
- `bAttackResolved` — tipo `bool`.
- `LastFeedbackHealth` — tipo `real`.
- `LastDamageAmount` — tipo `real`.
- `NextStaggerAt` — tipo `real`.
- `StaggerCooldown` — tipo `real`.
- `NextAttackAt` — tipo `real`.
- `bFinalWordsPending` — tipo `bool`.
- `FinalPeersAlive` — tipo `int`.
- `EncounterZone` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 225 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_IntInt`, `ApplyDamage`, `Attack`, `BooleanAND`, `BooleanOR`, `BreakRotator`, `DisableMovement`, `Dot_VectorVector`, `EndAttack`, `Enemy_Death`, `EqualEqual_IntInt`, `FMin`, `FindLookAtRotation`, `FinishFinalWords`, `GetActorForwardVector`, `GetActorOfClass`, `GetAnimInstance`, `GetBlackboard`, `GetController`, `GetDistanceTo`, `GetHUD`, `GetPlayerController`, `GetRealTimeSeconds`, `GetTimeSeconds`, `GreaterEqual_DoubleDouble`, `Greater_DoubleDouble`, `IsValid`, `K2_GetActorLocation`, `K2_GetActorRotation`, `K2_SetActorRotation`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `Less_IntInt`, `LineOfSightTo`, `MakeLiteralName`, `MakeRotator`, `Montage_GetPosition`, `Montage_IsPlaying`, `Montage_Pause`, `Montage_SetPosition`, `Not_PreBool`, `OnHealthChanged`, `PlayAnimMontage`, `PlaySound2D`, `RInterpTo_Constant`, `ReceiveBeginPlay`, `ResolveAttack`, `SetActorEnableCollision`, `SetLifeSpan`, `SetValueAsBool`, `StartRevelation`, `StopAnimMontage`, `StopLogic`, `StopMovement`, `Subtract_DoubleDouble`, `Subtract_VectorVector`, `UpdateStrike`, `UserConstructionScript`, `Vector_Normal2D`.

- `/Game/ThirdPerson/Audio/SW_DoorHit.SW_DoorHit`
- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyAttack_Entrega.AM_EnemyAttack_Entrega`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyDeath_Entrega.AM_EnemyDeath_Entrega`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BPI_Enemy.BPI_Enemy_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega.BP_HUD_Entrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `5ba1f48a03b1c0d6abb28042d12c5de9109aeefeca0942475b7b56cd06573836`.
