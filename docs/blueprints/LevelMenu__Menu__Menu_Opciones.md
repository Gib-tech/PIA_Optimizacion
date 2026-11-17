# Menu_Opciones

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/Menu/Menu_Opciones`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Interfaz de calidad, resolución, modo de pantalla y volumen. Aplica y guarda cada selección. Vuelve a la instancia de menú/pausa de origen y mantiene la partida detenida cuando corresponde.

## Entradas y responsabilidades del grafo

- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow1_O_K2Node_ComponentBoundEvent_12_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow2_O_K2Node_ComponentBoundEvent_13_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow3_O_K2Node_ComponentBoundEvent_14_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow4_O_K2Node_ComponentBoundEvent_15_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture1_O_K2Node_ComponentBoundEvent_16_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture2_O_K2Node_ComponentBoundEvent_17_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture3_O_K2Node_ComponentBoundEvent_18_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture4_O_K2Node_ComponentBoundEvent_19_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_salir_menu_K2Node_ComponentBoundEvent_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`PreConstruct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Construct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Tick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Botón btn_volver_opciones`** en `EventGraph`. Operaciones alcanzables desde `then`: `RemoveFromParent`, `K2Node_CreateWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_viewdistance1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_viewdistance2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_viewdistance3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `ExecuteConsoleCommand`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion2_O_K2Node_ComponentBoundEvent_2_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion3_O_K2Node_ComponentBoundEvent_3_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion4_O_K2Node_ComponentBoundEvent_4_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion1_O_K2Node_ComponentBoundEvent_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_viewdistance1_O_K2Node_ComponentBoundEvent_5_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_viewdistance2_O_K2Node_ComponentBoundEvent_6_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_viewdistance3_O_K2Node_ComponentBoundEvent_7_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing1_O_K2Node_ComponentBoundEvent_8_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing2_O_K2Node_ComponentBoundEvent_9_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing3_O_K2Node_ComponentBoundEvent_10_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing4_O_K2Node_ComponentBoundEvent_11_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `PreviousMenu` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 85 nodos con pines. Funciones referenciadas: `AddToViewport`, `Construct`, `ExecuteConsoleCommand`, `OnButtonClickedEvent__DelegateSignature`, `PreConstruct`, `RemoveFromParent`, `Tick`.

- `/Game/LevelMenu/Menu/Menu_Inicio.Menu_Inicio_C`
- `/Game/LevelMenu/Menu/Menu_Pausa.Menu_Pausa_C`
- `/Game/LevelMenu/Menu/O_volver_OV.O_volver_OV`
- `/Game/LevelMenu/Menu/Opciones_pantalla_vacia.Opciones_pantalla_vacia`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `fda250ac6817881ef451a3511d2f464b6e57fe800ad95371292c0834e20cd4be`.
