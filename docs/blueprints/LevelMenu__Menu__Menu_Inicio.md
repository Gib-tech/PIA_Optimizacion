# Menu_Inicio

[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)

**Ruta de Unreal:** `/Game/LevelMenu/Menu/Menu_Inicio`. **Tipo:** WidgetBlueprint.
**Clase padre:** `"/Script/CoreUObject.Class'/Script/UMG.UserWidget'"`.

Menú de entrada con Nuevo juego, Continuar validado, opciones y salida. Nuevo juego sustituye el intento; Continuar restaura un checkpoint compatible sin repetir introducción.

## Entradas y responsabilidades del grafo

- **`PreConstruct`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Construct`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar Game Instance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Tick`** en `EventGraph`. Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.
- **`Botón btn_nuevojuego_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `CreateSaveGame`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_salir_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `QuitGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_opciones_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `RemoveFromParent`, `K2Node_CreateWidget`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_continuar_menu`** en `EventGraph`. Operaciones alcanzables desde `then`: `K2Node_AddDelegate`, `LoadGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GameLoadCompleted`** en `EventGraph`. Operaciones alcanzables desde `then`: `OpenLevelBySoftObjectPtr`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Construct`** en `ExecuteUbergraph_Menu_Inicio`. Operaciones alcanzables desde `then`: `K2Node_DynamicCast`, `Asignar Game Instance`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_nuevojuego_menu`** en `ExecuteUbergraph_Menu_Inicio`. Operaciones alcanzables desde `then`: `CreateSaveGame`, `OpenLevel`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_salir_menu`** en `ExecuteUbergraph_Menu_Inicio`. Operaciones alcanzables desde `then`: `QuitGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_opciones_menu`** en `ExecuteUbergraph_Menu_Inicio`. Operaciones alcanzables desde `then`: `RemoveFromParent`, `Create`, `AddToViewport`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Botón btn_continuar_menu`** en `ExecuteUbergraph_Menu_Inicio`. Operaciones alcanzables desde `then`: `K2Node_AddDelegate`, `LoadGame`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GameLoadCompleted`** en `ExecuteUbergraph_Menu_Inicio`. Operaciones alcanzables desde `then`: `OpenLevelBySoftObjectPtr`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`GameLoadCompleted`** en `GameLoadCompleted`. Operaciones alcanzables desde `then`: `K2Node_SetVariableOnPersistentFrame`, `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_continuar_menu_K2Node_ComponentBoundEvent_3_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_opciones_menu_K2Node_ComponentBoundEvent_2_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_salir_menu_K2Node_ComponentBoundEvent_1_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`OnButtonClickedEvent__DelegateSignature`** en `BndEvt__Menu_Inicio_btn_nuevojuego_menu_K2Node_ComponentBoundEvent_0_OnButtonClickedEvent__DelegateSignature`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.
- **`Construct`** en `Construct`. Operaciones alcanzables desde `then`: `ExecuteUbergraph_Menu_Inicio`. Las condiciones del grafo deciden qué rama se ejecuta.

## Campos propios declarados

Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.

- `Game Instance` — tipo `object`.

## Operaciones y dependencias verificadas

La exportación contiene 56 nodos con pines. Funciones referenciadas: `AddToViewport`, `Construct`, `Create`, `CreateSaveGame`, `GameLoadCompleted`, `GetGameInstance`, `LoadGame`, `OnButtonClickedEvent__DelegateSignature`, `OpenLevel`, `OpenLevelBySoftObjectPtr`, `PreConstruct`, `QuitGame`, `RemoveFromParent`, `Tick`.

- `/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C`
- `/Game/LevelMenu/BP_SaveGame.BP_SaveGame_C`
- `/Game/LevelMenu/Menu/M_continuar_OV.M_continuar_OV`
- `/Game/LevelMenu/Menu/M_nuevojuego_OV.M_nuevojuego_OV`
- `/Game/LevelMenu/Menu/M_opciones_OV.M_opciones_OV`
- `/Game/LevelMenu/Menu/M_salir_OV.M_salir_OV`
- `/Game/LevelMenu/Menu/Menu_Opciones.Menu_Opciones_C`
- `/Game/LevelMenu/Menu/Menu_Pausa.Menu_Pausa_C`
- `/Game/LevelMenu/Menu/Menu_pantalla.Menu_pantalla`
- `/Game/ThirdPerson/Maps/ThirdPersonMap.ThirdPersonMap`

## Cómo modificarlo sin romper el flujo

1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.
2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.
3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.
4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.

**Huella de exportación:** `c947469ad663d9969757296ed22db72b86147fb925fe4c0c114ffb849ec5991c`.
