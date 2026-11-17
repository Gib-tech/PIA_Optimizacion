# BP_DestruiblePick

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/ThirdPerson/Bp_Modelos/BP_DestruiblePick`. **Tipo:** Blueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/Engine.Actor'"`.

Prototipo de destruible del equipo conservado como fuente. El mapa entregable usa BP_DestruibleEntrega para evitar mezclar lógica de ejemplo y daño final.

## Entradas y responsabilidades del grafo

- **`ReceiveBeginPlay`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_CreateWidget`, `Asignar WMensajeRef`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveActorBeginOverlap`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`ReceiveTick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Botón Colision`** en `EventGraph`. Operaciones alcanzables desde `then`: `Condición`, `Condición`, `AddToViewport`, `AddToViewport`, `Asignar Text`, `Asignar Text`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón Destruible`** en `EventGraph`. Operaciones alcanzables desde `then`: `Asignar Destruible?`, `PlaySound2D`, `Asignar Text`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`UserConstructionScript`** en `UserConstructionScript`. Operaciones alcanzables desde `then`: `SetRestCollection`, `SetStaticMesh`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnChaosBreakEvent__DelegateSignature`** en `BndEvt__BP_DestruiblePick_Destruible_K2Node_ComponentBoundEvent_2_OnChaosBreakEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DestruiblePick`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComponentEndOverlapSignature__DelegateSignature`** en `BndEvt__BP_DestruiblePick_Colision_K2Node_ComponentBoundEvent_1_ComponentEndOverlapSignature__DelegateSignature`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DestruiblePick`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ComponentBeginOverlapSignature__DelegateSignature`** en `BndEvt__BP_DestruiblePick_Colision_K2Node_ComponentBoundEvent_0_ComponentBeginOverlapSignature__DelegateSignature`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_BP_DestruiblePick`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`ReceiveBeginPlay`** en `ReceiveBeginPlay`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_BP_DestruiblePick`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `DestrModelo` — tipo `object`.
- `PickUpModelo` — tipo `object`.
- `Destruible?` — tipo `bool`.
- `NewVar` — tipo `object`.
- `WMensajeRef` — tipo `object`.
- `Recolectado?` — tipo `bool`.

## Operaciones y dependencias verificadas

La exportación contiene 45 nodos con pines. Funciones referenciadas: `AddToViewport`, `ComponentBeginOverlapSignature__DelegateSignature`, `ComponentEndOverlapSignature__DelegateSignature`, `OnChaosBreakEvent__DelegateSignature`, `PlaySound2D`, `ReceiveActorBeginOverlap`, `ReceiveBeginPlay`, `ReceiveTick`, `RemoveFromParent`, `SetRestCollection`, `SetStaticMesh`, `UserConstructionScript`.

- `/Game/ThirdPerson/RecursosPropios/Interfaz/Interfaz.Interfaz_C`
- `/Game/ThirdPerson/RecursosPropios/Sonido/wood-crate-destory-2-97263.wood-crate-destory-2-97263`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `06277b0fb0533e773b2404f49ac70e20799d227c76b9bb6d1d7b699705578462`.
