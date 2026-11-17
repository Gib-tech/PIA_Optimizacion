# BP_PlayerEntrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/Engine.BlueprintGeneratedClass'/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C'"`.

Personaje jugable de la entrega. Añade ventanas de impacto, control de recuperación, daño a puertas/Chaos y brazos de primera persona. BrazosFP muestrea copias de animación sin notifies: postura preparada en reposo y posición sincronizada del ataque real. EspadaFP y MartilloFP son sólo presentación; la malla y las armas originales conservan el daño real.

## Entradas y responsabilidades del grafo

- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `Secuencia`, `SetVisibility`, `Secuencia`, `Condición`, `SetVisibility`, `Condición`, `Condición`, `Condición`, `Condición`, `Asignar LastFirstPerson`, `SetVisibility`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `Secuencia`, `K2_AttachToComponent`, `ReceiveBeginPlay`, `K2_AttachToComponent`, `K2_SetRelativeLocationAndRotation`, `K2Node_ClearDelegate`, `K2_SetRelativeLocation`, `SetLeaderPoseComponent`, `K2Node_AddDelegate`, `Asignar bUsePawnControlRotation`, `SetAnimationMode`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GrantHammerUpgrade`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bHammerUpgraded`, `Asignar bDoorPending`, `Asignar RequiredDoor`, `Asignar UpgradeUntil`, `Asignar IsAttacking`, `Asignar bLightAttackActive`, `StopAnimMontage`, `Asignar bSaveLightAttack`, `ResetState`, `SetCollisionEnabled`, `SetVisibility`, `SetVisibility`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Operaciones alcanzables desde `then`: `UserConstructionScript`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GrantHammerUpgrade`** en `GrantHammerUpgrade`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_PlayerEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_PlayerEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_PlayerEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `HeavyHitActors` — tipo `object`.
- `HeavyDamage` — tipo `real`.
- `bHammerUpgraded` — tipo `bool`.
- `UpgradeUntil` — tipo `real`.
- `RequiredDoor` — tipo `object`.
- `bDoorPending` — tipo `bool`.
- `bHitboxOnHammer` — tipo `bool`.
- `SwordHitboxRelativeTransform` — tipo `struct`.
- `bHeavyWindowManaged` — tipo `bool`.
- `HeavyWindowStart` — tipo `real`.
- `HeavyWindowEnd` — tipo `real`.
- `LastAttackMontage` — tipo `object`.
- `LastAttackPosition` — tipo `real`.
- `LastFirstPerson` — tipo `bool`.
- `FPBobTime` — tipo `real`.
- `FPSwayYaw` — tipo `real`.
- `FPSwayPitch` — tipo `real`.
- `FPLastYaw` — tipo `real`.
- `FPLastPitch` — tipo `real`.
- `FPHeight` — tipo `real`.
- `FPForward` — tipo `real`.
- `LastFPAnimation` — tipo `object`.
- `FPIdleSwordPosition` — tipo `real`.
- `FPIdleHammerPosition` — tipo `real`.
- `FPRollSword` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 415 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `ApplyDamage`, `Array_AddUnique`, `Array_Clear`, `Array_Contains`, `BooleanAND`, `BooleanOR`, `BreakTransform`, `BreakVector`, `ComposeRotators`, `Divide_DoubleDouble`, `E_Decrease_Health`, `EqualEqual_ObjectObject`, `FClamp`, `GetAnimInstance`, `GetController`, `GetCurrentMontage`, `GetDistanceTo`, `GetPlayerController`, `GetRelativeTransform`, `GetSocketTransform`, `GetTimeSeconds`, `GetVelocity`, `GrantHammerUpgrade`, `GreaterEqual_DoubleDouble`, `HideBoneByName`, `IsValid`, `K2_AttachToComponent`, `K2_SetRelativeLocation`, `K2_SetRelativeLocationAndRotation`, `K2_SetRelativeTransform`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `LineOfSightTo`, `MakeRotator`, `MakeTransform`, `MakeVector`, `Montage_GetPosition`, `Montage_Stop`, `Multiply_DoubleDouble`, `NotEqual_BoolBool`, `NotEqual_ObjectObject`, `Not_PreBool`, `PlaySound2D`, `ReceiveBeginPlay`, `ReceiveTick`, `ResetState`, `SelectFloat`, `SelectInt`, `SetAnimation`, `SetAnimationMode`, `SetBoxExtent`, `SetCollisionEnabled`, `SetCollisionResponseToChannel`, `SetFieldOfView`, `SetFocusToGameViewport`, `SetInputMode_GameOnly`, `SetLeaderPoseComponent`, `SetOwnerNoSee`, `SetPosition`, `SetRelativeScale3D`, `SetViewportMouseCaptureMode`, `SetVisibility`, `Sin`, `SpawnSystemAttached`, `StopAnimMontage`, `Subtract_DoubleDouble`, `TransformLocation`, `UserConstructionScript`, `VSizeXY`, `WeaponToBack`.

- `/Game/ThirdPerson/Animations/Attack_1_Montage.Attack_1_Montage`
- `/Game/ThirdPerson/Animations/Attack_2_Montage.Attack_2_Montage`
- `/Game/ThirdPerson/Animations/Attack_3_Montage.Attack_3_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/Hammer/HA_1_Montage.HA_1_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/Hammer/HA_2_Montage.HA_2_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/FA_1_Montage.FA_1_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/FA_2_Montage.FA_2_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/L_FA_1_Montage.L_FA_1_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/L_FA_3_Montage.L_FA_3_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/L_FA_4_Montage.L_FA_4_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/ataque_rapido_1_Montage.ataque_rapido_1_Montage`
- `/Game/ThirdPerson/Animations/Fast_attacks/sword/ataque_rapido_2_Montage.ataque_rapido_2_Montage`
- `/Game/ThirdPerson/Animations/Heavy_attacks/Sword/H_attack_1_Montage.H_attack_1_Montage`
- `/Game/ThirdPerson/Animations/Heavy_attacks/Sword/H_attack_2_Montage.H_attack_2_Montage`
- `/Game/ThirdPerson/Animations/Heavy_attacks/Sword/H_attack_3_Montage.H_attack_3_Montage`
- `/Game/ThirdPerson/Audio/SW_Upgrade.SW_Upgrade`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestructibleDoor.BP_DestructibleDoor_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestruibleEntrega.BP_DestruibleEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/FX/NS_HammerUpgrade.NS_HammerUpgrade`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_Attack_1.AFP_Attack_1`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_Attack_2.AFP_Attack_2`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_Attack_3.AFP_Attack_3`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_FA_1.AFP_FA_1`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_FA_2.AFP_FA_2`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_HA_1.AFP_HA_1`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_HA_2.AFP_HA_2`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_H_attack_1.AFP_H_attack_1`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_H_attack_2.AFP_H_attack_2`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_H_attack_3.AFP_H_attack_3`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_L_FA_1.AFP_L_FA_1`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_L_FA_3.AFP_L_FA_3`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_L_FA_4.AFP_L_FA_4`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_ataque_rapido_1.AFP_ataque_rapido_1`
- `/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_ataque_rapido_2.AFP_ataque_rapido_2`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `45dad7779a95cdecd6c1cea881e0957ef72905eceb58e8312fbd65c8136b8b56`.
