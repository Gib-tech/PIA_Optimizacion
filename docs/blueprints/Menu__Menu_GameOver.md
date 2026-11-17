# Menu_GameOver

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Menu/Menu_GameOver`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Pantalla original de fin de partida. El desenlace de entrega usa director, cinemática y HUD con R/Enter; esta pantalla permanece como recurso histórico.

## Entradas y responsabilidades del grafo

- **`PreConstruct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Construct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Tick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Botón Button`** en `EventGraph`. Operaciones alcanzables desde `then`: `RemoveFromParent`, `K2Node_CreateWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_reintentar_gameover`** en `EventGraph`. Operaciones alcanzables desde `then`: `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_GameOver_Button_K2Node_ComponentBoundEvent_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_GameOver`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_GameOver_btn_reintentar_gameover_K2Node_ComponentBoundEvent_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_GameOver`. Las condiciones del grafo deciden qué rama se ejecuta.

## Operaciones y dependencias verificadas

La exportación contiene 13 nodos con pines. Funciones referenciadas: `AddToViewport`, `Construct`, `OnButtonClickedEvent__DelegateSignature`, `OpenLevel`, `PreConstruct`, `RemoveFromParent`, `Tick`.

- `/Game/Menu/G_reintentar_OV.G_reintentar_OV`
- `/Game/Menu/Gameover_pantalla_OV.Gameover_pantalla_OV`
- `/Game/Menu/Menu_Inicio.Menu_Inicio_C`
- `/Game/Menu/P_iramenu_OV.P_iramenu_OV`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `295209f0fa4142ee455f45c3546bc94a0ae9e6420c243885d3d32c2ef4e58a55`.
