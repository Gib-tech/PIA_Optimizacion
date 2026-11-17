# BP_RehenIndicador

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_RehenIndicador`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.TextRenderActor'"`.

Indicador histórico de texto flotante. El HUD actual dibuja la placa E/RB; conservarlo no implica que esté activo en el nivel final.

## Entradas y responsabilidades del grafo

- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2_SetActorRotation`, `Condición`, `K2_SetActorLocation`, `Condición`, `K2_SetText`, `Condición`, `K2_SetText`, `Condición`, `Condición`, `K2_SetText`, `K2_SetText`, `K2_SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ExecuteUbergraph_BP_RehenIndicador`. Operaciones alcanzables desde `then`: `K2_SetActorRotation`, `Condición`, `K2_SetActorLocation`, `Condición`, `K2_SetText`, `Condición`, `K2_SetText`, `Condición`, `Condición`, `K2_SetText`, `K2_SetText`, `K2_SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_RehenIndicador`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript_MERGED`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Rehen` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 88 nodos con pines. Funciones referenciadas: `Add_VectorVector`, `BooleanOR`, `Conv_StringToText`, `FindLookAtRotation`, `GetBlackboard`, `GetCameraLocation`, `GetDistanceTo`, `GetPlayerCameraManager`, `GetPlayerPawn`, `GetValueAsBool`, `IsValid`, `K2_GetActorLocation`, `K2_SetActorLocation`, `K2_SetActorRotation`, `K2_SetText`, `LessEqual_DoubleDouble`, `MakeLiteralName`, `ReceiveTick`, `UserConstructionScript`.


## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `109b17f286fb1f667207dfc46243750cd6ed76f8cb5ccf5c84f00bbb06cf0543`.
