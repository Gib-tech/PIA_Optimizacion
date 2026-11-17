# BP_DestruibleEntrega

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_DestruibleEntrega`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Copia funcional del destruible del equipo para caja, basurero, banca, barril, auto y fuente. Acepta daño positivo del protagonista: espada/martillo ligero (15), pesado (25) y pulso visible (20), sin exigir mejora del martillo ni IsAttacking en el receptor. El jugador valida ventanas y deduplicación; SistemasComplementarios valida la traza y munición. bBroken activa Chaos una sola vez y los restos expiran en ocho segundos. La decoración se restablece al cargar; las puertas de misión sí se guardan. Ver REVISION_JUGABLE.md.

## Entradas y responsabilidades del grafo

- **`Botón Destruible`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar ChaosBreakCount`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAnyDamage`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Condición`, `Asignar Health`, `Condición`, `Asignar bBroken`, `Condición`, `SetActorHiddenInGame`, `SetCollisionEnabled`, `SetVisibility`, `SetCollisionProfileName`, `SetSimulatePhysics`, `CrumbleActiveClusters`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetCollisionEnabled`, `SetSimulatePhysics`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Operaciones alcanzables desde `then`: `SetRestCollection`, `SetStaticMesh`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DestruibleEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAnyDamage`** en `ReceiveAnyDamage`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DestruibleEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnChaosBreakEvent__DelegateSignature`** en `Evaluation_ChaosBreak`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DestruibleEntrega`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `DestrModelo` — tipo `object`.
- `PickUpModelo` — tipo `object`.
- `Destruible?` — tipo `bool`.
- `NewVar` — tipo `object`.
- `WMensajeRef` — tipo `object`.
- `Recolectado?` — tipo `bool`.
- `Health` — tipo `real`.
- `bBroken` — tipo `bool`.
- `ChaosBreakCount` — tipo `int`.
- `BreakFX` — tipo `object`.
- `NombreDestruible` — tipo `string`.
- `ModeloIntacto` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 58 nodos con pines. Funciones referenciadas: `AddRadialImpulse`, `Add_IntInt`, `BooleanAND`, `CrumbleActiveClusters`, `Evaluation_ChaosBreak`, `FMax`, `Greater_DoubleDouble`, `IsValid`, `K2_GetComponentLocation`, `LessEqual_DoubleDouble`, `MakeTransform`, `Not_PreBool`, `OnChaosBreakEvent__DelegateSignature`, `ReceiveAnyDamage`, `ReceiveBeginPlay`, `SetActorHiddenInGame`, `SetAsset`, `SetCollisionEnabled`, `SetCollisionProfileName`, `SetLifeSpan`, `SetRestCollection`, `SetSimulatePhysics`, `SetStaticMesh`, `SetVisibility`, `Subtract_DoubleDouble`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C`
- `/Game/ThirdPerson/Blueprints/Entrega/FX/BP_RafagaRotura.BP_RafagaRotura_C`
- `/Game/ThirdPerson/RecursosPropios/Interfaz/Interfaz.Interfaz_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `c8c99b1172a65f7391e083feb47fa4270c4345a2f86919ae1ac4f5f8b45b49a4`.
