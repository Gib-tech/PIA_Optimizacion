# BP_SistemasComplementarios

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Inventario, suministros únicos, curación, pulso y ciclo solar. Curar llama Increase_Health, que limita a 100 y notifica al HUD. E/RB recoge una sola pieza apuntada de la mesa; sus tres flags MesaRecogido se guardan en ExtrasRevision 3. Si no hay pieza, valida BRUNO apuntado/cercano o reenvía Interactuar al rehén. El pulso aplica 20 de daño al primer enemigo o destruible visible hasta ocho metros, con consumo y recuperación; genera un trazo visual sin daño. BRUNO convierte tres créditos durante tres segundos en un botiquín sin duplicar consumos/recompensas. WorldSeconds, fabricación y animación usan tiempo de juego y se detienen con pausa. El SaveManager conserva energía/proceso y fase. DayCycleDuration=1200 s, mínimo 300, define la vuelta solar; smoothstep suaviza sol, luna, ambiente y estrellas. Sun llega a 26000 lux; Moon a 1,2; Sky usa captura continua. Ver CICLO_LUCES_Y_ATAQUES.md.

## Entradas y responsabilidades del grafo

- **`DispararPulso`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Condición`, `Asignar LastPulseAt`, `Asignar Cargas`, `SphereTraceSingle`, `Secuencia`, `K2Node_DynamicCast`, `Asignar Notice`, `K2Node_SpawnActorFromClass`, `Condición`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_RightTrigger`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `Asignar LastPulseAt`, `Asignar Cargas`, `SphereTraceSingle`, `Secuencia`, `K2Node_DynamicCast`, `Asignar Notice`, `K2Node_SpawnActorFromClass`, `Condición`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla MiddleMouseButton`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `Asignar LastPulseAt`, `Asignar Cargas`, `SphereTraceSingle`, `Secuencia`, `K2Node_DynamicCast`, `Asignar Notice`, `K2Node_SpawnActorFromClass`, `Condición`, `K2Node_DynamicCast`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`HablarConTecnico`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `LineTraceSingle`, `Condición`, `Asignar MesaRecogido1`, `Condición`, `Asignar Botiquines`, `Asignar MesaRecogido2`, `Condición`, `SetActorHiddenInGame`, `Asignar Cargas`, `Asignar MesaRecogido3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_RightShoulder`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `LineTraceSingle`, `Condición`, `Asignar MesaRecogido1`, `Condición`, `Asignar Botiquines`, `Asignar MesaRecogido2`, `Condición`, `SetActorHiddenInGame`, `Asignar Cargas`, `Asignar MesaRecogido3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla E`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `LineTraceSingle`, `Condición`, `Asignar MesaRecogido1`, `Condición`, `Asignar Botiquines`, `Asignar MesaRecogido2`, `Condición`, `SetActorHiddenInGame`, `Asignar Cargas`, `Asignar MesaRecogido3`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UsarBotiquin`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Condición`, `Asignar Botiquines`, `Asignar Notice`, `Increase_Health`, `Asignar NoticeUntil`, `PlaySound2D`, `Asignar Notice`, `Asignar NoticeUntil`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_LeftShoulder`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `Asignar Botiquines`, `Asignar Notice`, `Increase_Health`, `Asignar NoticeUntil`, `PlaySound2D`, `Asignar Notice`, `Asignar NoticeUntil`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla H`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Condición`, `Asignar Botiquines`, `Asignar Notice`, `Increase_Health`, `Asignar NoticeUntil`, `PlaySound2D`, `Asignar Notice`, `Asignar NoticeUntil`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AlternarInventario`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `Asignar InventoryOpen`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla Gamepad_Special_Left`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Asignar InventoryOpen`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tecla I`** en `EventGraph`. Operaciones alcanzables desde `Pressed`: `Condición`, `Condición`, `Asignar InventoryOpen`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `Condición`, `Condición`, `Condición`, `Condición`, `Condición`, `Condición`, `Condición`, `GetActorOfClass`, `Condición`, `Condición`, `Condición`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_I_K2Node_InputKeyEvent_7`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_Special_Left_K2Node_InputKeyEvent_6`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_H_K2Node_InputKeyEvent_5`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_LeftShoulder_K2Node_InputKeyEvent_4`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_E_K2Node_InputKeyEvent_3`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_RightShoulder_K2Node_InputKeyEvent_2`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_MiddleMouseButton_K2Node_InputKeyEvent_1`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`InputActionHandlerDynamicSignature__DelegateSignature`** en `InpActEvt_Gamepad_RightTrigger_K2Node_InputKeyEvent_0`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`AlternarInventario`** en `AlternarInventario`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UsarBotiquin`** en `UsarBotiquin`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`HablarConTecnico`** en `HablarConTecnico`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`DispararPulso`** en `DispararPulso`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_SistemasComplementarios`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `bInitialized` — tipo `bool`.
- `InventoryOpen` — tipo `bool`.
- `Botiquines` — tipo `int`.
- `Cargas` — tipo `int`.
- `Creditos` — tipo `int`.
- `WorldSeconds` — tipo `real`.
- `LastPulseAt` — tipo `real`.
- `DialogUntil` — tipo `real`.
- `DialogSpeaker` — tipo `string`.
- `DialogText` — tipo `string`.
- `Notice` — tipo `string`.
- `NoticeUntil` — tipo `real`.
- `Hero` — tipo `object`.
- `Director` — tipo `object`.
- `Tecnico` — tipo `object`.
- `Sun` — tipo `object`.
- `Sky` — tipo `object`.
- `Recogido1` — tipo `bool`.
- `Suministro1` — tipo `object`.
- `Recogido2` — tipo `bool`.
- `Suministro2` — tipo `object`.
- `Recogido3` — tipo `bool`.
- `Suministro3` — tipo `object`.
- `Recogido4` — tipo `bool`.
- `Suministro4` — tipo `object`.
- `RobotEnergy` — tipo `int`.
- `bFabricating` — tipo `bool`.
- `FabricationProgress` — tipo `real`.
- `SkyDome` — tipo `object`.
- `SkyMID` — tipo `object`.
- `Moon` — tipo `object`.
- `ItemMesa1` — tipo `object`.
- `MesaRecogido1` — tipo `bool`.
- `ItemMesa2` — tipo `object`.
- `MesaRecogido2` — tipo `bool`.
- `ItemMesa3` — tipo `object`.
- `MesaRecogido3` — tipo `bool`.
- `ObjetoEnMira` — tipo `int`.
- `DestruibleEnMira` — tipo `object`.
- `bRobotEnMira` — tipo `bool`.
- `DayCycleDuration` — tipo `real`.
- `DayCycleDuration_0` — tipo `real`.

## Operaciones y dependencias verificadas

La exportación contiene 651 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `Add_IntInt`, `Add_VectorVector`, `AlternarInventario`, `ApplyDamage`, `BooleanAND`, `BreakHitResult`, `Concat_StrStr`, `Conv_IntToString`, `CreateDynamicMaterialInstance`, `DegSin`, `DispararPulso`, `Divide_DoubleDouble`, `E_Decrease_Health`, `EnableInput`, `EqualEqual_ObjectObject`, `FClamp`, `FFloor`, `FMax`, `FindLookAtRotation`, `GetActorOfClass`, `GetCameraLocation`, `GetCameraRotation`, `GetDistanceTo`, `GetForwardVector`, `GetPlayerCameraManager`, `GetPlayerController`, `GetTimeSeconds`, `GreaterEqual_DoubleDouble`, `GreaterEqual_IntInt`, `Greater_DoubleDouble`, `Greater_IntInt`, `HablarConTecnico`, `Increase_Health`, `InputActionHandlerDynamicSignature__DelegateSignature`, `Interactuar`, `IsMoveInputIgnored`, `IsValid`, `K2_SetActorRotation`, `LessEqual_DoubleDouble`, `Less_DoubleDouble`, `Less_IntInt`, `LineTraceSingle`, `MakeRotator`, `MakeTransform`, `MakeVector`, `Multiply_DoubleDouble`, `Multiply_VectorFloat`, `Not_PreBool`, `PlaySound2D`, `ReceiveTick`, `SelectVector`, `SetActorEnableCollision`, `SetActorHiddenInGame`, `SetIntensity`, `SetScalarParameterValue`, `SphereTraceSingle`, `Subtract_DoubleDouble`, `Subtract_IntInt`, `UsarBotiquin`, `UserConstructionScript`, `Vector_Distance`.

- `/Game/ThirdPerson/Audio/SW_Rescue.SW_Rescue`
- `/Game/ThirdPerson/Audio/SW_Upgrade.SW_Upgrade`
- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C`
- `/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C`
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DestruibleEntrega.BP_DestruibleEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_PulsoTemporalVisual.BP_PulsoTemporalVisual_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_TecnicoTemporal.BP_TecnicoTemporal_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `beb53d726852a1a9e9a578c329998d806efbcb10c04a385096a7273cb54ef2f0`.
