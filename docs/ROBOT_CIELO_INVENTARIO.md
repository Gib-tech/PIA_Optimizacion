# Revisión de BRUNO, cielo e inventario · 17/11/2026

Esta es la referencia vigente sobre estas tres áreas. Se conservan el diseño y los flujos de los menús. El propietario limitó el alcance a Unreal y documentación técnica: redes, campaña y promoción están fuera. Las capturas de requisitos son criterios que revisar, no instrucciones independientes ni prueba de cumplimiento.

## BRUNO y los créditos

BRUNO es una unidad de reciclaje fija, anclada al suelo y a la red del recinto. Su misión es ayudar a los dos viajeros; no puede atravesar la extracción. Su modelo mecánico original sustituye completamente al humano que duplicaba al sobreviviente. La clase conserva el nombre `BP_TecnicoTemporal` para no romper referencias ni guardados.

`ChasisRobot`, `CabezaRobot` y `AroConversion` son tres piezas del mismo robot, no tres diseños para inflar la rúbrica. Hay cuatro LOD por pieza, materiales compartidos y una luz pequeña sin sombras. La cabeza explora suavemente; el aro gira y la luz aumenta durante el proceso. Tick del robot sólo presenta estado: no decide ni entrega recursos. La fuente ensamblada y sus FBX están en `Tools/ArtSource/RobotBRUNO`, creados con `Tools/Blender/build_robot_bruno.py`. Son creación asistida original; no se atribuyen como trabajo manual de un alumno.

E/RB en un radio de 270 cm inicia el diálogo. Repetir mientras está abierto convierte **3 créditos en energía** y empieza un único trabajo. `BP_SistemasComplementarios` descuenta 3, guarda `RobotEnergy=3`, `FabricationProgress=0` y `bFabricating=true`. Durante **3 segundos de tiempo de juego** acumula progreso. Terminar limpia energía/proceso y entrega **1 botiquín** una sola vez. Interactuar mientras fabrica no vuelve a descontar; saldo insuficiente no inicia trabajo ni se vuelve negativo. Los créditos son celdas recuperadas, no un pago por el rescate.

`BP_DeliverySave` añade energía, trabajo activo y progreso al esquema 2. El SaveManager los serializa y restaura junto al inventario y la fase solar. El comienzo/fin del proceso dispara la solicitud de guardado seguro. Un guardado manual durante fabricación conserva el punto exacto; el autoguardado inicial puede reanudar desde su inicio si se cierra antes del siguiente checkpoint, sin volver a cobrar ni entregar dos botiquines. Los archivos anteriores usan cero/falso para estos campos.

## Qué ocurrió con el cielo

La revisión anterior escribió intensidades de **0,18–7,98** sobre una luz direccional que estaba configurada a **15 000 lux**. Ese error de unidades oscurecía la atmósfera aunque el sol estuviera arriba. Además, SkyLight capturaba una sola vez y no existía un fondo nocturno: al bajar el sol quedaba negro. Se corrige en el generador y en los assets, sin quitar SkyAtmosphere.

La vuelta dura 480 segundos. Ángulo solar = `35 + WorldSeconds × 0,75`; intensidad = `26000 × max(sen(ángulo), 0)` lux. Empieza alrededor de 14 913 lux y llega a 26 000 al mediodía. La luna ocupa la dirección opuesta, usa índice atmosférico 1 y alcanza 0,12 lux. SkyLight es móvil con captura continua a 128; la cúpula `M_CieloTemporal` combina SkyAtmosphere, discos solar/lunar y estrellas procedurales propias. El material Is Sky no recibe sombras, no colisiona ni afecta navegación. La noche se mantiene oscura y las luces locales conservan su función.

El cielo y la fabricación avanzan sólo en juego permitido. Pausa detiene reloj, proceso y animación. Checkpoint conserva `WorldSeconds`, por lo que Continuar no reinicia la hora. Las estrellas sólo se añaden de noche; no son una textura del Starter Content. Referencia del motor: [componentes y materiales Sky Atmosphere de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/sky-atmosphere-component-properties-in-unreal-engine?application_version=5.6).

## Inventario

I/SELECT abre tres tarjetas con cantidades reales, estado disponible/agotado y acción equivalente en teclado/mando: botiquines, cargas de pulso y créditos de energía. Iconos propios renderizados desde los modelos del proyecto; tipografía del inventario en atlas separados para leer cantidades y controles. Paleta de metal oscuro con acentos verde, cian y ámbar. El panel adapta tamaño a la resolución y oculta visualmente el diálogo inferior mientras está abierto; no cambia su estado ni la misión. El aviso explica que el mundo sigue activo y que P/START pausa.

El HUD sólo lee datos. H/LB y clic central/RT continúan pasando por las validaciones de `BP_SistemasComplementarios`. Se conservan guardado, curación hasta 100, consumo real y traza del pulso. Los menús principal, pausa y opciones conservan su diseño. Fuentes de iconos: `Tools/ArtSource/Inventario`; receta: `Tools/Blender/render_inventory_icons.py`.

## BP_CinematicDirector

Se reorganizan posiciones y recuadros en nueve secciones numeradas: arranque, actualización, introducción, revelación, desenlace, reproducción, omisión con teclado, omisión con mando y finalización. Los datos auxiliares quedan debajo de su consumidor; cada tramo se lee de izquierda a derecha. No se instala otro grafo ni se cambian funciones, valores de gameplay, GUID o enlaces. Abrir el editor hace explícito None en dos salidas Key sin uso; se registra esta normalización del motor y no afecta la ejecución.

La comparación de los 207 nodos conserva la misma huella lógica antes y después: `ccd9fbcb20c7f16c55f8ddd639b19e0a81c4b27b1c6982e7b3fc25754a98d8ed`. Prueba en `validation/cinematic-layout.json`. Los recuadros sólo existen en el editor y no ejecutan gameplay. No ejecutar `regenerate_current_presentation.py` para reaplicar este acomodo: ese script también reconstruye cinemáticas. Usar `Tools/layout_cinematic_graph.py` y `apply_cinematic_layout.py` con una exportación actual y verificar la huella.

## Pruebas y reproducción

- `validation/robot-cielo-inventario/energia-runtime.json`: recogida real en fixture, diálogo, gasto único, proceso de 3 s, pausa de un segundo real, animación, reanudación desde checkpoint, saldo insuficiente y compatibilidad aditiva.
- `validation/robot-cielo-inventario/muestras.json`: cámaras y fase preparadas para inspección visual; las capturas no son un recorrido natural.
- `validation/cinematic-layout.json`: igualdad de lógica antes/después del acomodo.
- La partida natural anterior con doce enemigos y extracción conjunta está en `validation/partida-completa-2026-11-17.json`. Sus condiciones no se presentan como una segunda partida en esta revisión.

Para reconstruir: Blender del robot/iconos → `prepare_robot_sky_revision.py` y `create_inventory_fonts.py` en editor con helper → generar exclusivamente systems/robot/manager/HUD → `install_robot_inventory_revision.py`. No usar el instalador general para este cambio: también reconstruye el director de cinemáticas. El helper C++ se carga únicamente en editor; el paquete ejecuta Blueprints sin Python ni ese módulo.

Cierre de validación: paquete final Win64 Development generado en 82,63 s, cook con 0 errores y la advertencia anterior de Scale. `validation/robot-cielo-inventario/paquete-final.json` registra teclas reales y recarga fría del ejecutable (2 botiquines, 2 cargas, 0 créditos). `recarga-fria.json` comprueba el editor normal sin helper, robot/cielo y lectura del save nativo con Unreal. Las partidas y preferencias originales están restauradas por SHA-256; no se incluyen guardados en el ZIP. Continúa pendiente la prueba con mando físico.
