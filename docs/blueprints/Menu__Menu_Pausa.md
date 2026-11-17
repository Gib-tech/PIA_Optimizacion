# Menu_Pausa

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Menu/Menu_Pausa`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Interfaz de pausa con reanudar, guardar, opciones y regreso al menú. Los botones delegan en BP_DeliveryInterface y BP_DeliverySaveManager; no crean una segunda implementación del guardado.

## Entradas y responsabilidades del grafo

- **`Botón btn_reanudar_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `ClosePause`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_opciones_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `OpenOptions`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_irmenu_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `ClosePause`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_salvarjuego_pausa`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `SaveCheckpoint`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_reanudar_pausa_Control_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_opciones_pausa_Control_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_irmenu_pausa_Control_2_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Pausa_btn_salvarjuego_pausa_Control_3_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Pausa`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 31 nodos con pines. Funciones referenciadas: `ClosePause`, `Conv_StringToText`, `GetActorOfClass`, `OnButtonClickedEvent__DelegateSignature`, `OpenLevel`, `OpenOptions`, `SaveCheckpoint`, `SetText`.

- `/Game/LevelMenu/MainMenuLevel`
- `/Game/Menu/P_iramenu_OV.P_iramenu_OV`
- `/Game/Menu/P_opciones_OV.P_opciones_OV`
- `/Game/Menu/P_reanudar_OV.P_reanudar_OV`
- `/Game/Menu/P_salvarjuego_OV.P_salvarjuego_OV`
- `/Game/Menu/Pausa_pantalla_OV.Pausa_pantalla_OV`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager.BP_DeliverySaveManager_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `e2daf9e93b8ee35fc8431d7ab57b4cb2d45f2ef8384bb5f47d4436d06810d74d`.
