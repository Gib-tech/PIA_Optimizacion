# Menu_Opciones

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Menu/Menu_Opciones`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Interfaz de calidad, resolución, modo de pantalla y volumen. Aplica y guarda cada selección. Vuelve a la instancia de menú/pausa de origen y mantiene la partida detenida cuando corresponde.

## Entradas y responsabilidades del grafo

- **`Construct`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_viewdistance1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetViewDistanceQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_viewdistance2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetViewDistanceQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_viewdistance3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetViewDistanceQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetAntiAliasingQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetAntiAliasingQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetAntiAliasingQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_antialiasing4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetAntiAliasingQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetShadowQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetShadowQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetShadowQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_shadow4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetShadowQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetTextureQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetTextureQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetTextureQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_texture4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetTextureQuality`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion1_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetScreenResolution`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion2_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetScreenResolution`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion3_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetScreenResolution`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_resolucion4_O`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetScreenResolution`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_display0`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetFullscreenMode`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_display1`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetFullscreenMode`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_display2`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetGameUserSettings`, `SetFullscreenMode`, `ApplySettings`, `ConfirmVideoMode`, `SaveSettings`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_volume0`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar MasterVolume`, `ApplyVolume`, `SaveVolume`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_volume1`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar MasterVolume`, `ApplyVolume`, `SaveVolume`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_volume2`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar MasterVolume`, `ApplyVolume`, `SaveVolume`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_volume3`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `Asignar MasterVolume`, `ApplyVolume`, `SaveVolume`, `SetText`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_volver_opciones`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `CloseOptions`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_volver_opciones_Control_26_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_volume3_Control_25_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_volume2_Control_24_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_volume1_Control_23_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_volume0_Control_22_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_display2_Control_21_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_display1_Control_20_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_display0_Control_19_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion4_O_Control_18_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion3_O_Control_17_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion2_O_Control_16_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_resolucion1_O_Control_15_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture4_O_Control_14_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture3_O_Control_13_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture2_O_Control_12_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_texture1_O_Control_11_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow4_O_Control_10_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow3_O_Control_9_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow2_O_Control_8_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_shadow1_O_Control_7_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing4_O_Control_6_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing3_O_Control_5_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing2_O_Control_4_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_antialiasing1_O_Control_3_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_viewdistance3_O_Control_2_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_viewdistance2_O_Control_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Opciones_btn_viewdistance1_O_Control_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Construct`** en `Construct`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Opciones`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `PreviousMenu` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 317 nodos con pines. Funciones referenciadas: `ApplySettings`, `ApplyVolume`, `CloseOptions`, `Concat_StrStr`, `ConfirmVideoMode`, `Construct`, `Conv_StringToText`, `GetActorOfClass`, `GetAntiAliasingQuality`, `GetGameUserSettings`, `GetShadowQuality`, `GetTextureQuality`, `GetViewDistanceQuality`, `OnButtonClickedEvent__DelegateSignature`, `SaveSettings`, `SaveVolume`, `SetAntiAliasingQuality`, `SetFullscreenMode`, `SetScreenResolution`, `SetShadowQuality`, `SetText`, `SetTextureQuality`, `SetViewDistanceQuality`.

- `/Game/Menu/Menu_Pausa.Menu_Pausa_C`
- `/Game/Menu/O_volver_OV.O_volver_OV`
- `/Game/Menu/Opciones_pantalla_vacia.Opciones_pantalla_vacia`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `9b500fe04bdcac03afbd69fe14efb0ca5c6e79b1eb6986e88c0f1dc8964dd9db`.
