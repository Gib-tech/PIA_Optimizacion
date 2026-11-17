# BTTask_ActivateBeacon

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Aliado/BTTask_ActivateBeacon`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/AIModule.BTTask_BlueprintBase'"`.

Canalización de tres segundos mediante el árbol del aliado. Sólo continúa con baliza correcta, cercana y sin amenaza. Interrupción cancela la canalización sin conceder avance.

## Entradas y responsabilidades del grafo

- **`ReceiveExecuteAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar CachedPawn`, `FinishExecute`, `K2Node_DynamicCast`, `Asignar Beacon`, `FinishExecute`, `Asignar Elapsed`, `Asignar bUsingBeacon`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar Elapsed`, `Asignar ActivationProgress`, `Condición`, `CompleteActivation`, `Asignar bUsingBeacon`, `Asignar ActivationProgress`, `SetValueAsBool`, `FinishExecute`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar bUsingBeacon`, `Asignar ActivationProgress`, `SetValueAsBool`, `FinishAbort`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveAbortAI`** en `ReceiveAbortAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ActivateBeacon`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTickAI`** en `ReceiveTickAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ActivateBeacon`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveExecuteAI`** en `ReceiveExecuteAI`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BTTask_ActivateBeacon`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Elapsed` — tipo `real`.
- `CachedPawn` — tipo `object`.
- `Beacon` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 46 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `CompleteActivation`, `Divide_DoubleDouble`, `FMin`, `FinishAbort`, `FinishExecute`, `GetBlackboard`, `GetValueAsObject`, `GreaterEqual_DoubleDouble`, `MakeLiteralName`, `ReceiveAbortAI`, `ReceiveExecuteAI`, `ReceiveTickAI`, `SetValueAsBool`.

- `/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `1ab9003529de995f20507b8c9b7e532580d3f5707f0b681417ce39db6cee32fd`.
