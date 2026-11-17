# BP_Modular_Master

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/SciFITrooper_Man_03/Blueprints/BP_Modular_Master`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/Engine.BlueprintGeneratedClass'/Game/SciFITrooper_Man_03/Blueprints/BP_Character_Master.BP_Character_Master_C'"`.

Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `ReceiveBeginPlay`, `K2Node_DynamicCast`, `Asignar IsModular`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Operaciones alcanzables desde `then`: `UserConstructionScript`, `SetLeaderPoseComponent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ExecuteUbergraph_BP_Modular_Master`. Operaciones alcanzables desde `then`: `ReceiveBeginPlay`, `K2Node_DynamicCast`, `Asignar IsModular`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_Modular_Master`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript_MERGED`. Operaciones alcanzables desde `then`: `UserConstructionScript`, `SetLeaderPoseComponent`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `TargetArmSpringLength_0` — tipo `real`.
- `Number_0` — tipo `int`.
- `LastRotation_0` — tipo `struct`.

## Operaciones y dependencias verificadas

La exportación contiene 35 nodos con pines. Funciones referenciadas: `GetAnimInstance`, `ReceiveBeginPlay`, `SetLeaderPoseComponent`, `UserConstructionScript`.

- `/Game/SciFITrooper_Man_03/Blueprints/AnimBP/ABP_SciFiTrooperManV3.ABP_SciFiTrooperManV3_C`
- `/Game/SciFITrooper_Man_03/Blueprints/BP_Character_Master.BP_Character_Master_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `3fb455a1d29d5d8eb81008420c54980ecca90c47ed70083cd90fea130ef44b92`.
