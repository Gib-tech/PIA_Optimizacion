# Menu_Pausa

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/Menu/Menu_Pausa`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Interfaz de pausa con reanudar, guardar, opciones y regreso al menú. Los botones delegan en BP_DeliveryInterface y BP_DeliverySaveManager; no crean una segunda implementación del guardado.

## Entradas y responsabilidades del grafo

- **`PreConstruct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Construct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Tick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Botón btn_reanudar_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `SetGamePaused`, `RemoveFromParent`, `Asignar bShowMouseCursor`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_opciones_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `RemoveFromParent`, `K2Node_CreateWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_irmenu_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `RemoveFromParent`, `K2Node_CreateWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_salvarjuego_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `K2Node_AddDelegate`, `RequestSave`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveCompleted`** en `EventGraph`. Operaciones alcanzables desde `then`: `RemoveFromParent`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_reanudar_pausa_K2Node_ComponentBoundEvent_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_opciones_pausa_K2Node_ComponentBoundEvent_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_irmenu_pausa_K2Node_ComponentBoundEvent_2_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_salvarjuego_pausa_K2Node_ComponentBoundEvent_3_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`SaveCompleted`** en `SaveCompleted`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 34 nodos con pines. Funciones referenciadas: `AddToViewport`, `Construct`, `GetGameInstance`, `GetPlayerController`, `OnButtonClickedEvent__DelegateSignature`, `PreConstruct`, `RemoveFromParent`, `RequestSave`, `SaveCompleted`, `SetGamePaused`, `Tick`.

- `/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C`
- `/Game/LevelMenu/BP_SaveGame.BP_SaveGame_C`
- `/Game/LevelMenu/Menu/Menu_Inicio.Menu_Inicio_C`
- `/Game/LevelMenu/Menu/Menu_Opciones.Menu_Opciones_C`
- `/Game/LevelMenu/Menu/P_iramenu_OV.P_iramenu_OV`
- `/Game/LevelMenu/Menu/P_opciones_OV.P_opciones_OV`
- `/Game/LevelMenu/Menu/P_reanudar_OV.P_reanudar_OV`
- `/Game/LevelMenu/Menu/P_salvarjuego_OV.P_salvarjuego_OV`
- `/Game/LevelMenu/Menu/Pausa_pantalla_OV.Pausa_pantalla_OV`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `a42b30357b3e398475d1ff5433f3d9f9b7ca401e91226085e6fdd53dcefcef94`.
