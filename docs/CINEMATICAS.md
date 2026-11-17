# TIME OUT — dirección e integración de cinemáticas

Fecha: 16 de noviembre de 2026.

**Stated:** el propietario encarga planear y realizar introducción, derrota y victoria, con libertad creativa basada en las mecánicas. La captura del equipo aporta el pendiente de tres cinemáticas; los demás puntos no amplían esta tarea.

**Verified (contexto previo):** protagonista viajero temporal; rescate y escolta, dos encuentros, martillo cargado, puertas con dos golpes pesados, tres balizas en orden aleatorio y extracción conjunta. El cronómetro empieza al rescatar y no tiene límite impuesto.

**Decision creativa:** el recinto está desanclado del tiempo. El cautivo conoce la firma de las tres balizas y sólo él puede sincronizarlas. Las zonas bloquean el paso y su energía carga el martillo; la secuencia cambia en cada intento por inestabilidad temporal. La extracción requiere a ambos. No se añaden reglas, enemigos, cuenta regresiva ni una supervivencia posterior.

## Introducción — «Una señal entre épocas» (18 s)

1. 0–6 s. Travelling exterior hacia el acceso del recinto. CONTROL: «El salto te ha dejado en un recinto fuera del tiempo.»
2. 6–12 s. Aproximación a la habitación del cautivo. REHÉN: «Sólo yo puedo sincronizar las balizas. Ayúdame a salir.»
3. 12–18 s. Plano del viajero y la ruta inmediata, regreso a su cámara. CONTROL: «Despeja las zonas. Carga el martillo. Escolta su señal hasta la salida.» Título TIME OUT y «Ningún salto vale dejar a alguien atrás».

Sólo comienza en un intento nuevo. Continuar entra directamente en el checkpoint. El jugador conserva su posición, cámara y estado. Durante la escena se bloquean acciones, interacción y pausa; Espacio permite omitir.

## Derrota — «La señal se apaga» (8 s)

Una cámara situada respecto a la víctima se retira lentamente; funciona en cualquier punto del mapa. Imagen desaturada por la atmósfera y fundido a negro. Motivo musical descendente.

- Si cae el viajero: CONTROL: «Hemos perdido tu señal. El salto quedó incompleto.»
- Si cae el rehén: CONTROL: «Su señal se ha apagado. Sin él, no hay camino de vuelta.»
- Cierre: «El tiempo permite otro intento.»

Después se conserva la pantalla de resultado: R inicia otro intento; Enter vuelve al menú; Continuar conserva su checkpoint seguro. La escena no cambia vida, daño, IA ni el resultado.

## Victoria — «Volver juntos» (14 s)

1. 0–5 s. Cámara sobre la zona azul mostrando el encuentro de los dos personajes.
2. 5–10 s. Retirada ascendente hacia el último acceso; la señal azul encuadra la salida. REHÉN: «Las tres señales coinciden. Esta vez volvemos juntos.»
3. 10–14 s. Apertura de plano y fundido. CONTROL: «Extracción confirmada. Dos viajeros. Una misma línea temporal.» Título «A SALVO».

La escena sólo se dispara tras la condición de victoria existente, con ambos en extracción. Motivo de tres notas resuelto en acorde.

## Entrega técnica y aceptación

**Decision:** tres Level Sequences editables, cámaras con claves y cortes, fundidos y partituras sintéticas propias; director de presentación Blueprint-only. Subtítulos en español y formato panorámico adaptados al viewport. Sin dependencia runtime del helper del editor ni Python. El volumen respeta Opciones; omitir detiene el audio y restaura la cámara/entrada. Los resultados detienen las IA y se pausan después de la escena.

**Verified / pruebas del agente:** las tres escenas y ambas variantes de derrota pasaron en PIE; omisión física en primera persona, R tras derrota, Continuar sin escena, control negativo de extracción en solitario y reloj congelado. Win64 compiló con0errores/15advertencias previas, ZIP623284496bytes con CRC aprobado y sin guardados/helper. Introducción/subtítulos/retorno al juego/pausa observados en el ejecutable; recarga fría sin helper, sin PIE ni paquetes sucios. Evidencia: `validation/cinematics-2026-11-16.json`. Son fixtures preparados y smoke de introducción, no una nueva partida completa.

**Unknown:** aceptación visual del propietario y rendimiento en la PC de presentación. Las pruebas del agente se distinguen de esa aceptación.

## Recursos y reproducción

Secuencias: `/Game/ThirdPerson/Cinematics/LS_Intro`, `LS_Derrota` y `LS_Victoria`. Cada una tiene cámaras spawnable animadas, pista Camera Cuts, fundido y audio. Abrirlas en Sequencer permite retocar tiempos y planos. La derrota utiliza un origen dinámico situado en la víctima, por lo que su previsualización aislada en el editor aparece alrededor del origen del mundo. La victoria añade una esfera aditiva con Fresnel (`M_ExtractionShell`) que crece alrededor de la extracción; se destruye al terminar/omitir.

El actor residente `Cinematicas_TIME_OUT` usa `BP_CinematicDirector`. Guarda la vista original, oculta temporalmente el widget de vida, controla entrada/cámara y ofrece `StartIntro`, `StartOutcome` y `FinishCinema`. Los tres disparadores originales de Paso4/5/6 llaman a StartOutcome en vez de pausar inmediatamente; si falta el actor de presentación, conservan la pausa anterior como fallback. La interfaz de resultado se muestra después del film.

El rehén muerto usa ragdoll con su Physics Asset; el jugador conserva el montaje de muerte del equipo, elevando sólo su malla42cm al perder para que la pose final no quede semienterrada. Ambos ajustes ocurren después del resultado. No cambian cápsula, posición guardada, salud ni daño. Al omitir se detiene la secuencia y se restituyen sus estados; no quedan cámaras, audio ni esfera nuevos en el mundo.

Para regenerar, con PIE detenido y el helper BPB3 de `Tools/EditorBridge` cargado sólo en editor:

1. Local: `python Tools/build_cinematic_audio.py`.
2. Mediante `Tools/UnrealPython/run.py`: `prepare_cinematic_sequences.py` y `prepare_cinematic_runtime.py`.
3. Local: `python Tools/UnrealPython/generate_cinematics.py`.
4. Mediante el runner: `install_cinematic_runtime.py` y `validate_cinematic_assets.py`.
5. Guardar/cerrar editor, ejecutar `Tools/Build-Delivery.ps1` y `Tools/Archive-Delivery.py`.

No reconstruir el mapa ni los árboles. Las recetas vigentes de director, rehén y HUD ya incluyen los hooks de presentación.

El director fija negro en BeginPlay antes de que existan sus referencias de HUD/jugador. Libera ese negro al comenzar Sequencer, que aporta su propio fundido, o al completar la restauración de Continuar. Esto cubre la transición inicial observada en el ejecutable durante la carga del recinto.

QA: `start_cinematic_qa.py` respalda SaveGames y activa temporalmente30FPS/sin throttling; `verify_cinematic_runtime.py` lee `Intermediate/inspect/cinematics/mode.txt` (`intro`, `defeat-player`, `defeat-hostage` o `victory`). Esperar `CINEMA_FIXTURE_COMPLETE` antes de detener PIE. Son fixtures con daño/posiciones/estados preparados, no partidas de aceptación. `verify_cinematic_skip.py` arma una omisión física con Espacio en primera persona. `travel_cinematic_continue.py` y `verify_cinematic_continue.py` comprueban la carga con la misma bandera de Continuar. Al acabar PIE ejecutar `finish_cinematic_qa.py` para restaurar partidas y preferencias. Los callbacks retienen sus referencias: no reemplazar sus variables globales desde otra prueba.
