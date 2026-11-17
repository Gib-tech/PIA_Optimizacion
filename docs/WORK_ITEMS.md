# Work items

> **Versión actual.** Ciclo de 8 min desde la tarde, BRUNO por proximidad y diez objetos rompibles de un golpe. La revisión de jugabilidad reúne los valores y pruebas actuales. [Ver controles y cambios](REVISION_JUGABLE.md).

> **Revisión posterior, 17/11:** ciclo de 20 min con transiciones suaves; 41 luminarias de pared; seis props con espada/martillo ligero/pesado y pulso. Matriz de 30 combinaciones, ciclo completo, pausa, guardado y guardas del pulso comprobados. El catálogo incluye BP_LuminariaPared (103 fichas). Ver [CICLO_LUCES_Y_ATAQUES.md](CICLO_LUCES_Y_ATAQUES.md) y su evidencia; el texto inferior conserva el historial.

> **Estado vigente, 17/11 — revisión de BRUNO, cielo e inventario.** Alcance: requisitos de Unreal y documentación técnica en español. Redes, campaña, video promocional y documentos administrativos quedan fuera por indicación expresa del propietario. Se conserva el diseño de los menús; se rediseña el inventario. BRUNO usa modelo mecánico original, convierte 3 créditos en energía y fabrica 1 botiquín en 3 s. Ver [ROBOT_CIELO_INVENTARIO.md](ROBOT_CIELO_INVENTARIO.md). El texto posterior conserva historial cuando describe otra revisión.

## Revisión actual — 17 de noviembre de 2026

Implementados: presentación FP con brazos/armas y recuperación; rehén sobreviviente con locomoción; inventario/suministros/pulso/curación/créditos; Bruno con diálogo/compra; ciclo solar/guardado; estanque; seis modelos de apoyo; paridad de enlaces de pausa/inventario/resultados; guía y catálogo españoles. Ver informes de validación para distinguir implementación, prueba aislada y partida completa.

Pendientes externos: nombres del cronograma, cuentas/publicaciones públicas (45 borradores preparados), autoría académica y mando físico/PC de presentación. El inventario histórico de abajo se conserva como trazabilidad; consultar REVISION_REQUISITOS_2026-11-16.md para el cierre de cada criterio actual.

## Integración de cinco modelos y checklist del equipo — 2026-11-16

- **Stated:** archivos edificio/farol/escombros/auto y enlace del árbol; integrar/pulir lo necesario del checklist. Propietario confirma autores de edificio/farol por determinar.
- **Implemented / Ready para aceptación visual:** cinco diseños nuevos, cuatro LOD en cuatro de ellos y Nanite en el auto, ocho instancias estáticas, dos luces de farol limitadas y fondo de horizonte sin colisión. Escombros reducidos a45000triángulos con atlas horneado; auto con geometría/UV originales y Nanite. Se conservan cinco modelos LOD anteriores, Nanite, WP, iluminación existente y gameplay.
- **Verified en fixture preparado:** cinco assets/instancias detectados en PIE y doce caminos de navegación completos con props colocados. No se acredita nueva partida natural ni aceptación manual. Evidencia visual, LOD y paquete en handoff vigente.
- **Documentación:** `MODELOS_EQUIPO.md`, `CREDITOS_MODELOS.md`; créditos incluidos en ZIP. Los recursos externos no completan por inferencia la autoría de cinco modelos propios. Documentación académica/cronograma real, evidencia externa y presentación siguen requiriendo al equipo.

## Guardia final, revelación y aviso breve — 2026-11-16

- **Stated:** añadir una horda; el último enemigo anuncia el orden de balizas antes de morir; quitar el aviso de checkpoint persistente. Commit/push de cambios anteriores también solicitados.
- **Implemented / Ready para aceptación:** tercer encuentro residente,2×2enemigos mixtos; `LS_Revelacion`12s con tres planos y partitura propia. Disparo por muerte real del último enemigo, orden real subtitulado, finalización normal de muerte tras el diálogo. Orden/HUD/luz de siguiente baliza aparecen al terminar u omitir con Espacio. Avisos de guardado duran4s.
- **Verified en fixtures PIE:** requisito de escolta/zona2, dos árboles ejecutándose, ausencia de disparo en muertes anteriores, seis permutaciones, reloj/checkpoint suspendidos y control restaurado; guardado posterior/Continuar; migración de checkpoints previos con/sin balizas iniciadas; Espacio físico y prioridad de derrota durante el diálogo. Guardados del usuario se restauran al terminar QA. No es una nueva partida natural ni aceptación manual.
- **Pendiente de aceptación:** estética y dificultad de la horda en PC de presentación. No marcar Passed por las pruebas del agente. Diseño y reproducción en `CINEMATICAS.md`; evidencia/paquete en handoff vigente.

## Cinemáticas de introducción, derrota y victoria — 2026-11-16

- **Stated:** encargo actual de planear y hacer las tres escenas con libertad narrativa basada en las mecánicas; los otros pendientes de la captura no amplían esta tarea.
- **Implemented / Ready para aceptación visual:** `LS_Intro`18s, `LS_Derrota`8s y `LS_Victoria`14s, cámaras animadas, cortes, fundidos, subtítulos y tres partituras propias. `BP_CinematicDirector` enlaza comienzo y resultados; no requiere Python/helper en el juego.
- **Verified en PIE:** reproducción, retorno de cámara/posición y HUD; omisión física con Espacio en primera persona; R tras derrota; Continuar sin introducción; derrota por jugador/rehén y condición de extracción conjunta. Pruebas aisladas con estados preparados, no una nueva partida completa ni aceptación manual. La evidencia final y el paquete quedan en el handoff vigente.
- **Pendiente:** aceptación estética del propietario y PC de presentación. Guion, assets y reproducción en `CINEMATICAS.md`.

## Revisión activa de fluidez — 2026-11-16

**Stated:** mejorar ataque/movimiento enemigo y jugar un recorrido normal en tiempo real. **Implemented / pruebas del agente:** actualización de golpe desde tareas activas, giro progresivo, aproximación/carga/recuperación revisadas, aturdimiento limitado, colisión suave entre aliados y contador real de balizas. Mantener pendiente la aceptación del propietario de AI1-T5/FIN-01; no usar las pruebas del agente para cambiarla a Passed. Resultados finales y pendientes de evaluación en HANDOFF.md y PLAN_ADAPTACION_EVALUACION.md.

## Ataque, avisos y auditoría vigente — 2026-11-16

- **Verified:** cuatro casos de IA real (dos rivales × jugador/rehén), daño13.2 durante el montaje y sin deslizamiento; solicitudes lejanas rechazadas. Esquiva y cancelación no producen golpe tardío. Regresión de daño ligero/pesado y contactos duplicados aprobada.
- **Verified:** aviso visual/sonoro del rehén por daño aceptado; confirmación visual/sonora de daño a rivales, incluso letal. Curación, restauración y gracia de daño no generan falsas confirmaciones. Audio de impacto renderizado con RMS no cero.
- **Verified:** dieciséis diseños visuales conservadores cargados, cinco modelos con4LOD y transiciones reales por distancia, seis fracturas Chaos y lógica del Level BP ejecutada. Extracción marcada residente para corregir referencia desde director no espacial.
- **Pendiente:** aceptación del propietario/Adame, documentación/cronograma, evidencia de redes y video, interpretación de guardado, PC de presentación y alcance del texto general. Auditoría completa en `PLAN_ADAPTACION_EVALUACION.md`.

## Corrección de paredes y desapariciones — 2026-11-16

- **Verified:** 104 componentes de pared usan proyección métrica de 4 m con tres texturas existentes, incluidos límites y marcos escalados. Geometría/colisión conservadas.
- **Verified:** once texturas de superficie/props con mipmaps, streaming y límites 1024/2048; fuentes conservadas.
- **Verified:** modelos sin límite duro por distancia y once props no espaciales; se conservan cinco modelos con cuatro LOD y arquitectura Nanite. Evidencia vigente en `validation/walls-visibility-2026-11-16.json`.
- **Stated:** commit y push a origin al finalizar. La aceptación visual del propietario y PC de presentación siguen pendientes.

## Escenario con función y descarte — 2026-11-16

- **Stated:** el propietario solicita revisar distribución de terreno/objetos, justificar iluminación y optimizar trabajo fuera de vista usando assets existentes.
- **Verified:** máscara de usos propia con cuatro texturas sustituye las franjas por Y; diez edificios Nanite con pivotes/bounds locales sustituyen cuatro sectores; rescate/depósito cubiertos, props reagrupados y alineados al suelo por bounds de la malla visible. Se preserva escala vertical2 del escenario (muros~4m, pasos transitables) y cubiertas a4.2m.
- **Verified:** Rect/Point/Spot con fuentes visibles, radios10/7/11m, descarte24m/fade3.5m y una sola sombra local. Cielo sin captura continua, Lumen/exposición del nivel revisados. Revisión posterior: todos los modelos sin corte duro por distancia; once props residentes; LOD/Nanite/oclusión activos. No hay lógica de ocultación que detenga la misión fuera de cámara.
- **Verified en PIE:** Niagara ambiental activo cerca, inactivo lejos, activo al volver e inactivo al mirar fuera de su esfera de bounds; fuentes y prueba en `compound-visibility-2026-11-16.json`. Seis fracturas por golpes siguen funcionando con física bajo demanda; validación de bases y arquitectura/exportes nativos. Pruebas y paquete finales en handoff.
- **Pendiente:** aceptación visual del propietario y medición comparativa de rendimiento/PC de presentación. No se deduce mejora de FPS sólo de configurar descarte. Reproducción: `ESCENARIO_COMPOUND.md`.

## Rework de evaluación — 2026-11-16

- **Verified / Ready para demostración:** FIN-12 World Partition convertido oficialmente y funcionando en PIE; FIN-13 cuatro mallas de arquitectura Nanite; FIN-14 cinco modelos con cuatro LOD geométricos cada uno; FIN-16 dos macros, dos funciones y dos eventos del Level Blueprint ejecutados por timers. Guía: `GUIA_DEMOSTRACION_EVALUACION.md`. La demostración visual de transiciones LOD ante Adame sigue pendiente.
- **Verified:** Landscape real con cinco texturas y mezcla automática/pintable; seis colecciones diferentes con fractura Chaos por arma; ocho sistemas Niagara distintos integrados; iluminación Directional/Sky y tres tipos locales con coste acotado. FIN-15 todavía necesita medición en otra PC. No acreditar sólo por nombre de asset.
- **Verified:** defaults de primera ejecución a pantalla completa; BeginPlay/reanudar recuperan GameOnly, foco y captura permanente. Corregido el bloqueo de ataque al recibir martillo y la distancia horizontal del canalizado de balizas. Paquete y prueba física se registran en el handoff actual.
- **Stated / Unknown:** el propietario aún no tiene confirmación de Adame sobre munición/dinero. Guardado conserva datos aplicables, sin economía ficticia. Documentación académica/cronograma, redes, video, autoría/modelos propios, modelo final del rehén y aceptación manual continúan pendientes.
- Plan ejecutado y pendientes: `PLAN_ADAPTACION_EVALUACION.md`. Las secciones anteriores a este rework se conservan como historial; sus cifras de paquete y estado Unknown no describen esta revisión.

## Baliza definitiva y tercer objetivo — 2026-11-16

- **FIN-05 / In progress, Ready para aceptación:** secuencia real aleatoria A/B/C en patio accesible, orden/siguiente/progreso/cronómetro visibles, activación exclusiva del rehén en su turno. R sortea otro intento; Continuar conserva el checkpoint. Las seis permutaciones y el rechazo fuera de orden pasaron en PIE con preparación aislada; no es una partida manual completa ni aceptación de Adame.
- **FIN-07 / In progress, Ready para aceptación:** modelo del equipo `Baliza.glb` importado; cuerpo y materiales luminosos separados, nombres fijos y puntos alcanzables. Las primeras dos puertas ahora se cargan por sus oleadas y la última por completar las tres balizas. Sustituye el criterio histórico de una puerta por cada baliza.
- **Decision:** cronómetro desde rescate, sin límite impuesto; esquema de guardado 2 para secuencia/tiempo y nueva disposición. Se conservan ambas zonas de 2 oleadas × 2 enemigos. La ampliación de encuentros sugerida por el propietario queda por valorar en el recorrido manual.
- **Pendiente:** aceptación manual del circuito nuevo, valoración de cantidad de combate, modelo final del rehén, mando y otra PC. El recorrido automatizado del 15 de noviembre corresponde a la disposición anterior.
- **Verified:** Win64 Development y ZIP actualizados: 0 errores / 15 advertencias previas, CRC aprobado. Menú/Nuevo juego, rescate físico E, cronómetro, pausa y Continuar con el mismo orden/tiempo observados en Windows. Informe `docs/validation/beacon-sequence-2026-11-16.json`.

## FIN 03 y FIN 04 actuales — 2026-11-15

- **FIN-03 / In progress, Ready para aceptación con teclado/ratón:** pausa total P/Esc, reanudar con foco/cursor correcto, opciones desde ambos menús, regreso a la misma pausa, salida real al menú y guardado seguro integrado. Resolución, calidad, pantalla y volumen aplicados y persistidos. Conserva arte original; corrige textos que interceptaban clics y añade leyenda de controles.
- **FIN-04 / In progress:** cámara primera/tercera, movimiento, mirada, salto, armas y ataques comprobados con acciones Enhanced Input; teclado/ratón documentado en LEEME y pausa. Falta confirmar C/Y/T físicos: las pulsaciones del automatizador no cambiaron vista/arma, sin causa determinada. **Mando expresamente pendiente:** no se acredita paridad ni navegación de resultados con mando. No marcar Done.
- **Verified:** informes de opciones, pausa, cámara y regresión de combate en `docs/validation/delivery-controls-2026-11-15.json`; las pruebas del agente no sustituyen aceptación manual del propietario. No se alteran árboles ni daño.

## FIN 01 y FIN 02 actuales — 2026-11-15

- **FIN-01 / In progress, Ready para aceptación:** recorrido del agente completo en PIE por movimiento, interacción y ataques de gameplay, sin teletransportes ni cambios de salud/daño. Victoria con ambas zonas, tres balizas/puertas y extracción. También observadas derrota del jugador, derrota del rehén, R de recuperación y Enter al menú. Falta el recorrido manual y aceptación del propietario sobre el paquete final.
- **FIN-02 / In progress, Ready para aceptación:** puntos de control automáticos seguros, F5, restauración de jugador/rehén/arma/escolta/progresión y Continuar condicionado a un archivo compatible. R tras derrota recupera el punto, Nuevo juego comienza de cero. Guardado de mitad de combate sustituido por el último punto seguro. Cerrar/reabrir y Continuar comprobados en el ejecutable.
- **Verified:** pruebas en `docs/validation/delivery-walk-2026-11-15.json`, `delivery-save-2026-11-15.json`, `delivery-menu-2026-11-15.json` y `delivery-continue-2026-11-15.json`. Recompilación de seis Blueprints; sin cambios en los árboles ni en el balance. Win64/ZIP actualizados, 549384059 bytes, CRC aprobado; cook 0 errores/15 advertencias previas. Informe global en `docs/validation/delivery-checkpoints-2026-11-15.json`.

## Plan de cierre de entrega final — 2026-11-15

- **Verified:** revisión documental y lista consolidada en [PENDIENTES_ENTREGA_FINAL.md](PENDIENTES_ENTREGA_FINAL.md), con prioridades, dependencias y condiciones de cierre. No modifica estados de aceptación ni acredita pruebas nuevas.
- **Stated:** el propietario confirma que un compañero reemplazará el modelo provisional del rehén. La integración y su regresión están en FIN-06.
- **Unknown / pendiente:** aceptación de una partida manual completa, modelos definitivos, mando físico, otra PC y requisitos de rúbrica sin evidencia consolidada. Guardado/Continuar quedan actualizados en FIN-02, arriba. Revisar la lista antes de reutilizar las filas históricas siguientes.

## Dificultad y fractura actuales — 2026-11-15

- **In progress / Ready para aceptación:** daño enemigo 13.2 (+120% sobre 6) y puertas con grietas geométricas que se separan en 42/56/72 piezas irregulares coincidentes.
- **Verified:** siete informes aprobados en docs/validation/fracture-difficulty-2026-11-15.json: daño real de ambos enemigos, rehén, martillo físico, tres fracturas/navegación, misión completa aislada y compilación de 20 Blueprints. Son pruebas del agente, no aceptación del propietario.
- **Verified / Ready para aceptación:** Win64/ZIP actualizados, 739814428 bytes, CRC completo aprobado; cook 0 errores/21 advertencias anteriores. Menú/Nuevo juego/HUD/señal comprobados en el ejecutable.
- **Pendiente:** recorrido manual completo y aceptación del propietario. Las capas anteriores se conservan debajo como historial.

## Capa actual de feedback — 2026-11-15

- **In progress / Ready para aceptación:** placa flotante E/RB del rehén, voz sintética propia, fijación de ambos enemigos, locomoción tras pesado de espada y grietas al primer golpe válido.
- **Verified:** siete informes del agente aprobados en docs/validation/hostage-feedback-2026-11-15.json; capturas de señal/puerta y 10 montajes físicos. No equivalen a aceptación del propietario.
- **Verified / Ready para aceptación:** Win64/ZIP actualizados, 737914216 bytes, CRC completo aprobado; cook 0 errores/21 advertencias. Señal y rescate comprobados en el ejecutable.
- **Pendiente:** recorrido manual completo y aceptación del propietario.

## Refinamiento actual — 2026-11-15

- **In progress / Ready para aceptación:** refugios locales del rehén con límite de recorrido; retirada breve del embestidor, regreso al combate y orientación por movimiento; corrección de espera de giro del orbitador.
- **In progress / Ready para aceptación:** daño de los 10 montajes de ataque, incluido cuarto ligero de espada, ligeros de martillo y pesados contra orbitadores; un impacto por enemigo/ataque.
- **In progress / Ready para aceptación:** punzada roja tenue de esquinas de 0.38 s al perder vida; renovación con cada golpe y control negativo de curación.
- **Verified:** pruebas del agente en docs/validation/refinement-2026-11-15.json. No equivalen a aceptación del propietario. Los checks históricos de pesado inmune/15-15-19 representan la versión anterior y no son criterios vigentes.
- **Verified / Ready para aceptación:** Win64/ZIP actualizados (737829582 bytes), CRC completo aprobado, cook 0 errores/21 advertencias; menú, Nuevo juego, rescate y HUD comprobados en el ejecutable.
- **Pendiente:** recorrido completo manual y aceptación del propietario.

Refinamiento 2026-11-15: aspecto Warrior original restaurado por elección expresa; contacto 6; prismas de colisión en cuatro sectores; cámara con sonda 24; recuadro contextual inspirado en Undertale para rescate/alertas/oleadas y audio propio. El texto flotante fue rechazado y retirado. Pruebas y límites en HANDOFF actual; aceptación del propietario pendiente.

Status values: `Todo`, `In progress`, `Blocked`, `Done`.

## Prioridad actual — entrega 2026-11-18

- **Ready para aceptación del propietario:** puertas a medida, vida/daño del rehén, balizas exclusivas del rehén después de hordas, mejora automática del martillo con FX/audio y dos impactos físicos para romper cada puerta. Árbol de escolta con canalización interrumpible y navegación dinámica. Pruebas del agente en `docs/validation/progression-2026-11-15.json`.

- **Ready para aceptación del propietario:** nivel nuevo con escenario de Ian, navegación y dos zonas de oleadas; balizas 1 → 2 → 3 y extracción; HUD con objetivos, victoria/derrota y reintento.
- **Ready para aceptación del propietario:** rehén con árbol propio, seguimiento, detección visual de enemigos, huida a refugio alcanzable y reanudación por E/RB. Pruebas del agente aprobadas en PIE; no equivalen a aceptación del propietario.
- **Ready para aceptación:** Nuevo juego abre el nivel nuevo. Continuar restaura un checkpoint compatible de objetivos y escolta; ver FIN-02 actual.
- **Ready para aceptación del propietario:** paquete Win64 Development y ZIP en `Deliverables`, actualizado con puertas/balizas del rehén y martillo mejorado. UAT terminó correctamente (0 errores de cook, 21 advertencias). Ejecutable: canalización, equipamiento automático y dos ataques pesados físicos rompen la puerta correspondiente y mantienen las siguientes intactas. CRC del ZIP de **737832544 bytes** aprobado. Evidencia en `docs/validation/progression-2026-11-15.json`; sigue pendiente una partida completa manual.
- **Todo / dependencia del equipo:** modelo definitivo de baliza; coordinación de partículas con Dany.
- **Ready para aceptación:** embestidor con árbol propio, daño ligero/pesado, oleadas 2 × 2 por zona, barreras y animaciones con cancelación. Pruebas automatizadas de PIE aprobadas; ver evidencia en el handoff.
- **Ready para aceptación:** guardado por puntos seguros implementado. Pendiente el recorrido manual del propietario de principio a fin.

`Done` requires the acceptance check in `AI_REQUIREMENTS.md`. The owner's board says AI 1 is Done. These rows stay `In progress` or `Todo` until Play In Editor on `ThirdPersonMap` shows the behavior. `In progress` means the saved asset already contains that work.

Numbers and tree order are locked in `AI_REQUIREMENTS.md`. The exact click steps for every open row are in `HANDOFF.md` → "Pending work, in order".

## AI 1 — Orbiter

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI1-01 | Done | Rebuild `BT_EnemyIA` into the five-branch tree: hit stun, defend, attack, orbit, roam. | Owner passed AI1-T1, AI1-T2, AI1-T3, and AI1-T6 on 2026-10-21. Force Success was removed from Attack on 2026-10-14. |
| AI1-02 | In progress | Add an orbit task that holds the 150–210 band around a 180 unit radius (owner decision 2026-10-14; was 320–480 / 400). | Step 0 and Step 0b saved. Agent PIE 2026-10-14 after Step 0b: distances 150–170, orbit point moved, enemies changed position around the player. Reach Test Includes Agent Radius is off on the orbit Move To. Done after the owner's AI1-T2 and AI1-T5 pass. |
| AI1-03 | Done | Apply damage only from a player light attack, and set `bReceivingDamage` only when health actually drops. | Owner passed AI1-T4 on 2026-10-21. Select is 15 / 15 / 19 from `LightSwingIndex`. `FA_1_Montage` EnableHitbox is at 0.08 s and DisableHitbox at 0.34 s. |
| AI1-04 | Done | Print String on attack start, defend start, and hit-stun end, using the three Spanish lines. | Owner passed AI1-T2, AI1-T3, and AI1-T4 on 2026-10-21, which include the attack, defend, and hit-stun lines. |
| AI1-05 | Done | Cleanup: remove the `BTTask_Roam` debug prints and the orphan Branch. Clear the `BTTask_HitSun` error badge. | Roam cleanup saved 2026-10-14; owner asked not to play-test it. HitSun's graph node has no `ErrorType`. Two leftover objects are in the asset text and are not Event Graph nodes. |
| AI1-06 | Done | Enemy death: bind `E_Dead` on BeginPlay, and stop the tree, movement, and collision on death. Add `bIsDead` and a health guard. | Owner passed AI1-T6 on 2026-10-21. The enemy stops and disappears. No death montage plays. The owner accepted that: the montage belongs to the 3D animation team. |
| AI1-07 | Done | Player receives enemy damage (Event AnyDamage → `BPC_Health.Decrease_Health`). | Owner on 2026-10-21: an enemy hit removes 10 health. |

## AI 2 — Hostage escort

Build recipe: `HANDOFF.md` → "After AI 1: AI 2 hostage build recipe".

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI2-01 | In progress | `BP_Hostage`, `BB_Hostage`, `BT_Hostage`, controller, sense service, arrival task and animation copy saved. | Ready for owner acceptance. Agent PIE 2026-11-15 passed follow, visual threat, reachable refuge and manual E resume. Current request supersedes old auto-resume distances; see current handoff. |
| AI2-02 | In progress | Create `BP_CombatZone` with an entrance blocker and a flee-point reference. Place one in reachable space on `ThirdPersonMap`. | Implementado en Nivel_Entrega: Zona_01_Orbitadores y Zona_02_Embestidores, barreras y refugios. Pruebas del agente aprobadas; aceptación pendiente. |
| AI2-03 | In progress | Create `BP_HostageSpawnZone`. Spawn 2 enemies once, only while the hostage is accompanying. | Integrado en BP_CombatZone: escolta requerida para activar 2 oleadas de 2 enemigos; sin un volumen duplicado. 0 spawns al entrar solo y al reentrar tras completar. |
| AI2-04 | In progress | Resume escort through explicit interaction within 400 units when there is no visible nearby threat. | Agent PIE passed manual E resume; owner acceptance pending. Combat-zone blocker release remains Todo with AI2-02. Auto-resume is superseded by the owner's 2026-11-15 request. |

## AI 3 — Charger

Required by the course rubric. Different tree from the orbiter. Not a second mesh on `BT_EnemyIA`. Build recipe: `HANDOFF.md` → "After AI 2: AI 3 charger build recipe".

| ID | Status | Item | Notes |
| --- | --- | --- | --- |
| AI3-01 | In progress | Create `BP_ChargerEnemy`, `BB_Charger`, `BT_Charger`, and a controller for that tree. | Guardado y probado: daño, preparar, cargar, retirarse/recuperarse, perseguir y patrullar. Segundo árbol distinto de BT_EnemyIA. |
| AI3-02 | In progress | Charge contact damages the player. Light and heavy attacks both damage the charger. | Carga causa 10 una vez; ligero 15/15/19 y pesado 25 en embestidor, pesado 0 en orbitador. Pruebas de manejadores aprobadas; aceptación pendiente. |

## Order

1. AI 1 playtests: T1–T4, T6, and the 10-damage hit passed on 2026-10-21. The death montage is accepted as the animation team's work. AI1-02 stays open because the owner said the orbit does not flow naturally (AI1-T5).
2. AI2-01 through AI2-04.
3. AI3-01 and AI3-02. A second spawn zone may use `BP_ChargerEnemy` after AI3-01 exists.

## Not in this queue

| ID | Status | Item |
| --- | --- | --- |
| LOOP-01 | In progress | Martillo equipado automáticamente por baliza y necesario para romper puertas. Ready para aceptación. |
| LOOP-02 | In progress | Mejora del martillo con FX/audio y habilitación por puerta; no es un sistema general de estadísticas. Ready para aceptación. |
| LOOP-03 | Not scheduled | Post-escape survival waves and time limit. |
| RUBRIC-01 | Not scheduled | Non-AI course rows: menus, save, dialogue NPCs, objectives, camera, gamepad parity, Nanite, World Partition, LODs, particles, destructibles. |

Advertising and social networks are out of scope.

## Editor tests

These are partial Play In Editor checks on `ThirdPersonMap`. Run one when its row says `Ready`. A pass here shows the behavior saved so far. It does not set a work item to `Done`; `Done` still requires the acceptance checks in `AI_REQUIREMENTS.md`.

Test status values: `Not ready`, `Ready`, `Passed`, `Failed`. A test is `Passed` (**Verified**) only after the owner sees it in Play In Editor and the result is written in the log below. Neither an export nor an agent-run PIE counts as a pass.

How to run: open `ThirdPersonMap` and press Play. Press `'` (apostrophe) for the gameplay debugger, then the Behavior Tree category (numpad 2 by default), to see which branch is active. The enemies start about 3700 units from `PlayerStart` toward −Y. Walk toward them.

| ID | Status | Becomes ready | Check |
| --- | --- | --- | --- |
| AI1-T1 | Passed | — | Walk toward an enemy. Inside 1500 units it leaves roam and starts orbit, defend, or attack. Far away, it wanders and pauses about 3 seconds between walks. |
| AI1-T2 | Passed | — | After it detects you, stand still. It circles close, near 180 units, and does not walk onto your capsule. It prints `Enemigo: va a atacar` about every 3 s while circling. Step back past 210 (still inside 1500) and it follows. Walk into it, inside 150, and it backs out. |
| AI1-T3 | Passed | After step 1 (accent), to check the exact text. | Inside 220, with the 3 second cooldown ready, the screen shows `Enemigo: va a atacar` for about 2 seconds. Inside 600, at least 6 seconds after the last defend, it shows `Enemigo: se está defendiendo` for about 2 seconds, and the enemy faces you without moving for 1.5 seconds. |
| AI1-T4 | Passed | The 15 / 15 / 19 Select and the `FA_1_Montage` hit window are saved. | Swings 1 and 2 drop 15 health. Swing 3 drops 19. About 0.6 seconds later the screen shows `Enemigo: ya no recibe daño`. Two full combos leave 2 health. The next light hit kills. A heavy attack does not drop that health and does not show that line. |
| AI1-T5 | Ready | — | Stand between 1000 and 1500 units from an enemy. It detects you and comes in to orbit. |
| AI1-T6 | Passed | — | Kill an enemy. It stops moving, stops printing, and disappears after a few seconds. The death montage is not playing. The owner accepted that on 2026-10-21: the montage is the 3D animation team's work. |

### Result log

| Date | Test | Result | What was seen |
| --- | --- | --- | --- |
| 2026-10-13 | AI1-T1, AI1-T2, AI1-T3 | Failed | Play In Editor on `ThirdPersonMap`. The enemy did not orbit, defend, or attack. The log repeated `BTService_LocatePlayer`: Accessed None reading `K2Node_DynamicCast_AsBP_Third_Person_Character` from Set Blackboard Value as Float, Branch, and Set Blackboard Value as Vector. |
| 2026-10-13 | AI1-T1, AI1-T2 | Failed | Fourth play. The startup attack line is gone. Both enemies printed defend about 9 seconds into the play and did not walk. (The agent-height explanation logged at the time was wrong. The cause was Force Success on Attack plus Defend never finishing.) |
| 2026-10-13 | AI1-T1 | Failed | After the editor closed at 21:56, the next play brought back the `BTService_LocatePlayer` Accessed None error. `BTTask_Defend` printed `Hello`. |
| 2026-10-13 | AI1-T1, AI1-T2 | Failed | Agent-run PIE, not the owner. No Accessed None. No movement during 60 s of roam. When the player was teleported 450 units from an enemy, the Blackboard got the target, distance, and orbit point. Both enemies printed defend once and froze, because `BTTask_Defend` had no Finish Execute. |
| 2026-10-14 | (informal) | Owner report | After Force Success was removed, the owner reported "now they're moving". This is not a formal check of any row. |
| 2026-10-14 | AI1-T1, AI1-T2, AI1-T3 | Agent PIE, not a pass | Roam: both enemies walked, then waited. When the player was teleported 450 units away, the enemy orbited at 387–719 units (mostly 387–464) without touching the capsule. Defend printed every 8–10 s and finished. Attack printed once. No errors in the log. The owner must still run these for a pass. |
| 2026-10-14 | AI1-T2 | Agent PIE, not a pass | After Step 0 (150 / 210 / 180 / 40). Player teleported 450 units from enemy 0. Both enemies closed in, then froze at 213 and 145 for at least 45 s of game time. Orbit points sat on the 180 circle and did not rotate. Attack and defend kept printing. No `Accessed None`. They never entered 150–210, so they did not circle. |
| 2026-10-14 | AI1-T2 | Agent PIE, not a pass | After Step 0b. Distances at 98 s were 170 and 154; at 152 s they were 161 and 170. Both enemies moved around the player and `OrbitLocation` changed. Attack lines continued. No `Accessed None`. The step-back and step-in parts of AI1-T2 were not run. The owner must still pass this test. |
| 2026-10-21 | AI1-T1, AI1-T2, AI1-T3, AI1-T4 | Passed | Owner on `ThirdPersonMap`. T1 through T4 passed. On T5 the owner saw the enemy come in, and said the orbit does not flow naturally. Several behaviors feel unnatural. T5 is not a pass. T6 was not run. |
| 2026-10-21 | AI1-T6, AI1-07 | Passed | Owner: an enemy hit removes 10 health. On death the enemy stands still and disappears. No death montage plays. The owner accepted that as the 3D animation team's work. |
