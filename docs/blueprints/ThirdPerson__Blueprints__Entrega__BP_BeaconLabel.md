# BP_BeaconLabel

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconLabel`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.TextRenderActor'"`.

Identificación visual estable de baliza. Su letra representa lugar, no turno de la secuencia.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `Asignar DirectorDeCine`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2_SetActorRotation`, `Condición`, `SetActorHiddenInGame`, `K2_SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_BeaconLabel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_BeaconLabel`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Beacon` — tipo `object`.
- `DirectorDeCine` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 28 nodos con pines. Funciones referenciadas: `Conv_StringToText`, `FindLookAtRotation`, `GetActorOfClass`, `GetCameraLocation`, `GetPlayerCameraManager`, `IsValid`, `K2_GetActorLocation`, `K2_SetActorRotation`, `K2_SetText`, `ReceiveBeginPlay`, `ReceiveTick`, `SetActorHiddenInGame`, `Subtract_IntInt`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega.BP_BeaconEntrega_C`
- `/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `83c730053ea5bd43cad83b63260115390a3369fbd7bae908bed9f61c1fc0996c`.
