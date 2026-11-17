# Menu_Inicio

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/Menu/Menu_Inicio`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Menú de entrada con Nuevo juego, Continuar validado, opciones y salida. Nuevo juego sustituye el intento; Continuar restaura un checkpoint compatible sin repetir introducción.

## Entradas y responsabilidades del grafo

- **`Construct`** en `EventGraph`. Operaciones alcanzables desde `then`: `Secuencia`, `SetIsEnabled`, `Asignar bShowMouseCursor`, `DoesSaveGameExist`, `SetInputMode_GameAndUIEx`, `Condición`, `LoadGameFromSlot`, `K2Node_DynamicCast`, `SetIsEnabled`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_nuevojuego_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar bDeliveryContinue`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_continuar_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar bDeliveryContinue`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_salir_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `QuitGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_opciones_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `GetActorOfClass`, `K2Node_DynamicCast`, `OpenOptions`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Construct`** en `Construct`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_nuevojuego_menu_K2Node_ComponentBoundEvent_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_continuar_menu_K2Node_ComponentBoundEvent_3_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_salir_menu_K2Node_ComponentBoundEvent_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_opciones_menu_K2Node_ComponentBoundEvent_2_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Game Instance` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 57 nodos con pines. Funciones referenciadas: `BooleanAND`, `Construct`, `DoesSaveGameExist`, `EqualEqual_IntInt`, `GetActorOfClass`, `GetGameInstance`, `GetPlayerController`, `GreaterEqual_IntInt`, `Greater_DoubleDouble`, `Less_IntInt`, `LoadGameFromSlot`, `OnButtonClickedEvent__DelegateSignature`, `OpenLevel`, `OpenOptions`, `QuitGame`, `SetInputMode_GameAndUIEx`, `SetIsEnabled`.

- `/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C`
- `/Game/Menu/M_continuar_OV.M_continuar_OV`
- `/Game/Menu/M_nuevojuego_OV.M_nuevojuego_OV`
- `/Game/Menu/M_opciones_OV.M_opciones_OV`
- `/Game/Menu/M_salir_OV.M_salir_OV`
- `/Game/Menu/Menu_pantalla.Menu_pantalla`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C`
- `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySave.BP_DeliverySave_C`
- `/Game/ThirdPerson/Maps/Nivel_Entrega`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `07aaeeddb2a3b564a03145a9d0761a52037db42e4d5e2a10922f384714e75c30`.
