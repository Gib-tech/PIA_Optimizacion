# BTService_ChargerSense

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/EnemigoIA/BTService_ChargerSense`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTService_BlueprintBase'"`.

Servicio de percepción del embestidor. Actualiza Blackboard, objetivo y condiciones de carga. Conserva la víctima comprometida mientras dura una carga para no cambiarla a mitad.

## Entradas y responsabilidades del grafo

- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar ChosenTarget`, `GetActorOfClass`, `SetValueAsBool`, `Condición`, `Asignar ChosenTarget`, `Asignar CombatTarget`, `SetValueAsFloat`, `Condición`, `SetValueAsObject`, `SetValueAsObject`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTService_ChargerSense`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `ChosenTarget` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 43 nodos con pines. Funciones referenciadas: `BooleanAND`, `BooleanOR`, `GetActorOfClass`, `GetBlackboard`, `GetDistanceTo`, `GetPlayerPawn`, `GetValueAsBool`, `LessEqual_DoubleDouble`, `LineOfSightTo`, `MakeLiteralName`, `Not_PreBool`, `ReceiveTickAI`, `SetValueAsBool`, `SetValueAsFloat`, `SetValueAsObject`.

- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `5635a9ec7d28b1b65383b54ab722f1f4b9e8a05d0dc998a7ce5c99dd92c59921`.
