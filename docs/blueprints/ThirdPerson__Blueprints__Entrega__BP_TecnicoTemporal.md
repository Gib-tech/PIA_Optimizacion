# BP_TecnicoTemporal

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Blueprints/Entrega/BP_TecnicoTemporal`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.SkeletalMeshActor'"`.

BRUNO es un robot de apoyo original fijado al suelo y a la red del recinto: no puede salir con los viajeros. ChasisRobot, CabezaRobot y AroConversion sustituyen por completo la malla humana heredada; el nombre de clase se conserva para compatibilidad. Tick sólo anima cabeza/aro/luz según bFabricating. BP_SistemasComplementarios decide conversación, energía y fabricación; este actor nunca concede recursos.

## Entradas y responsabilidades del grafo

- **`ReceiveTick`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar TiempoVisual`, `Secuencia`, `Condición`, `Condición`, `GetActorOfClass`, `K2_SetRelativeRotation`, `Asignar Sistema`, `K2_SetRelativeRotation`, `SetIntensity`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `ReceiveTick`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_TecnicoTemporal`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `TiempoVisual` — tipo `real`.
- `Sistema` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 35 nodos con pines. Funciones referenciadas: `Add_DoubleDouble`, `GetActorOfClass`, `IsValid`, `K2_SetRelativeRotation`, `MakeRotator`, `Multiply_DoubleDouble`, `Not_PreBool`, `ReceiveTick`, `SelectFloat`, `SetIntensity`, `Sin`, `UserConstructionScript`.

- `/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `521481fc51d2785edb35cc10187ab169da87f7f691f93c52cf4e35a7e40a1dd5`.
