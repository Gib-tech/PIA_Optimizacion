# BP_ZonaIndicador

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_ZonaIndicador`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.TextRenderActor'"`.

Indicador histórico de zona. Las alertas finales son recuadros contextuales del HUD; comprobar instancias antes de reutilizar este prototipo.

## Entradas y responsabilidades del grafo

- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2_SetActorRotation`, `K2Node_SwitchInteger`, `K2_SetText`, `K2_SetText`, `K2_SetText`, `K2_SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ExecuteUbergraph_BP_ZonaIndicador`. Operaciones alcanzables desde `then`: `K2_SetActorRotation`, `K2Node_SwitchInteger`, `K2_SetText`, `K2_SetText`, `K2_SetText`, `K2_SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_ZonaIndicador`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript_MERGED`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Zona` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 44 nodos con pines. Funciones referenciadas: `Conv_StringToText`, `FindLookAtRotation`, `GetCameraLocation`, `GetPlayerCameraManager`, `K2_GetActorLocation`, `K2_SetActorRotation`, `K2_SetText`, `ReceiveTick`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `b29f982e782ff47e8114e931acd34c6a7001df08425d1433f4d246608eb2b3dd`.
