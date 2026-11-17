# Project context

**Integración visual vigente,16/11:** se incorporan edificio, farol, escombros, auto destruido y árbol Fab como cinco modelos nuevos, en ocho instancias alrededor de accesos/jardín/servicio. Cuatro LOD en edificio/farol/escombros/árbol y Nanite en el auto; los cinco modelos LOD anteriores y la arquitectura Nanite se conservan. Autoría de edificio/farol queda por confirmar por indicación del propietario. Escombros de matousekfoto, auto de Renafox y árbol de danpetro son recursos externos con atribución, no modelos propios acreditados. Fuentes, ajustes y demostración: `MODELOS_EQUIPO.md`, `CREDITOS_MODELOS.md` y handoff vigente. La captura del equipo es un checklist de referencia; las cantidades ya implementadas no se rehacen por aparecer como pendientes históricos.

**Ampliación vigente,16/11:** tercer encuentro «Guardia final» antes del patio, dos oleadas mixtas de dos enemigos. Al vencer al último, el guardián agonizante revela la permutación real A/B/C mediante una cuarta Level Sequence de12s, `LS_Revelacion`. El orden y la siguiente baliza permanecen ocultos hasta terminar u omitir. El reloj y la escolta se suspenden durante el diálogo y se reanudan después. Avisos de guardado limitados a4s. Esquema2 con revisión aditiva para conservar checkpoints antiguos. Esta ampliación sustituye las menciones históricas de sólo dos zonas/tres cinemáticas. Commit anterior de cinemáticas `6773b75` publicado en origin por solicitud del propietario.

**Cinemáticas,16/11:** tres Level Sequences bajo `/Game/ThirdPerson/Cinematics`: introducción18s, derrota8s y victoria14s. Relato decidido por el agente con autorización creativa: cautivo como firma de sincronización, recinto fuera del tiempo y extracción conjunta. Partituras sintéticas propias, cámaras/cortes/fundidos y subtítulos españoles. Espacio omite; Continuar no repite introducción. Director de presentación Blueprint-only. La derrota distingue quién cae; no cambia las condiciones ni el balance de la misión. Diseño: `CINEMATICAS.md`; aceptación visual del propietario pendiente.

**Revisión vigente de fluidez (16/11):** acercamiento y alineación progresiva, contacto durante una ventana corta de montaje, recuperación mínima3s, cargas con anticipación y retirada más breve; Actor Tick enemigo permanece desactivado. Se corrigieron el bloqueo físico entre aliados en puertas y el contador de balizas durante derrota. El último recorrido del agente desde Nuevo juego terminó en victoria02:43, jugador7.6/rehén20.8, sin teletransportes ni cambios de vida/daño. Detalle y evidencia final en HANDOFF.md; los tiempos de ataques anteriores quedan como historial.

**Combate y rúbrica, revisión posterior del16/11:** el embestidor ya no ejecuta el golpe antes de acercarse; la animación y el daño coinciden al llegar. HUD avisa de daño real al rehén y confirma daño a rivales con sonido y marca/cifra. Vida/daño y árboles conservados. Auditoría runtime confirma16diseños visuales agrupando variantes, seis destruibles y cinco modelos con cuatro LOD; veinte capturas sin LOD forzado acreditan transiciones por distancia. Pendientes vigentes y alcance académico en `PLAN_ADAPTACION_EVALUACION.md`.

**Carga del paquete,16/11:** se protege el aviso del rehén hasta que exista su referencia; la Geometry Collection de la fuente usa una copia compatible del material existente, evitando caer al material por defecto. Padres/instancia propiedad del proyecto; plugin Fab intacto.

**Revisión vigente de paredes/visibilidad (2026-11-16):** 104 componentes con proyección de textura en unidades del mundo, once texturas optimizadas y modelos sin recorte duro por distancia. Once props de evaluación no espaciales evitan descarga visible al cambiar de celda. Cuatro LOD, Nanite y oclusión se conservan. Evidencia: `validation/walls-visibility-2026-11-16.json`. Commit y push autorizados al cerrar.

## Escenario revisado por dirección del propietario — 16 noviembre 2026

**Verified:** distribución de terreno por máscara de usos propia con cuatro texturas existentes, sin franjas por Y. Rescate/depósito cubiertos, diez edificios Nanite separados y props reagrupados. Rect interior, Point interior y Spot del poste tienen fuentes físicas y radios/culling propios; cielo sin captura continua. Física Chaos sólo al romper y Niagara ambiental con culling reanudable. `ESCENARIO_COMPOUND.md` sustituye descripciones anteriores de terreno/luces. Gameplay/árboles/daño13.2 y objetivos se conservan.

## Rework de evaluación — 16 noviembre 2026

**Verified:** `Nivel_Entrega` ahora usa World Partition, Landscape real de cinco texturas, cuatro mallas de arquitectura Nanite, cinco modelos con cuatro LOD, seis tipos de destruibles Chaos y ocho sistemas Niagara integrados. Level Blueprint contiene dos macros, dos funciones y dos eventos propios en uso. Las coordenadas de misión, dos zonas y daño 13.2 se conservan. Fuentes y límites actuales en `HANDOFF.md`, `PLAN_ADAPTACION_EVALUACION.md` y `GUIA_DEMOSTRACION_EVALUACION.md`; las descripciones anteriores de suelo Static Mesh corresponden al escenario previo.

## Estado vigente — 2026-11-16

- **Stated:** el propietario recibió el modelo `Baliza.glb` y pidió atender las condiciones nuevas de Adame. Confirmó una zona accesible con orden aleatorio real; la posible ampliación de zonas enemigas queda como propuesta, sin cantidad nueva definida.
- **Verified en PIE:** balizas A/B/C fijas en el patio final, modelo del equipo, seis secuencias posibles, luces azul/verde y HUD con orden, siguiente baliza, progreso y cronómetro desde el rescate. Guardado de secuencia/tiempo en esquema 2. R reinicia; Continuar restaura el mismo intento. Las dos primeras puertas dependen de sus oleadas y la tercera de completar la secuencia. Sustituye la ruta fija baliza 1 → 2 → 3 descrita abajo.
- **Verified:** las dos zonas de combate conservan 2 × 2 enemigos y los mismos árboles/balance. No se añadió otra zona en esta intervención. Evidencia, paquete y límites en el handoff vigente.

Facts below are separated from the assignment brief. Do not merge the two.

## Estado verificado — 2026-11-15

- FIN-03/04: interfaz Blueprint-only común en menú y misión, P/Esc para pausa/reanudar, opciones persistentes de gráficos/pantalla/volumen y leyenda de teclado/ratón. C alterna primera/tercera persona, Y martillo y T espada. Primera persona a altura de ojos, sigue orientación y oculta la malla propia; tercera conserva brazo y colisión. Mando pendiente por petición del propietario; las pruebas del agente no son aceptación manual.

- Persistencia de entrega añadida mediante `BP_DeliverySave` y `BP_DeliverySaveManager`: puntos de control seguros, F5, Continuar validado y R tras derrota recupera el último punto. Guarda también escolta, zonas, balizas y puertas. Las menciones históricas a Continuar deshabilitado quedan sustituidas; pruebas y límites en el handoff actual.
- Recorrido automatizado completo sin teletransportes ni modificaciones de vida/daño: victoria, ocho enemigos, tres balizas/puertas y extracción; última muestra a 147.2 s con jugador y rehén en 47.2 de vida. No es aceptación manual del propietario ni un objetivo de tiempo para el jugador.

- Refinamiento de puertas: geometría agrietada y fragmentos comparten las mismas divisiones irregulares (42/56/72 piezas). La primera malla sustituye la máscara de material anterior; los cuatro escombros cuadrados quedan sustituidos por piezas reales de cada panel. Fuentes originales conservadas; generación en Tools/Blender/build_fractured_doors.py y Tools/ArtSource/Fracture.

- Progresión actual: tres puertas destructibles propias con muros visibles; sólo el rehén canaliza las balizas despejadas. Vida del rehén 100 con HUD; enemigos pueden atacarlo. Cada baliza equipa/carga el martillo y habilita su puerta, que requiere dos golpes pesados. El NavMesh se actualiza después de la rotura. Ver pruebas de agente en el handoff actual.

- Entrega indicada por el propietario: miércoles 18 de noviembre de 2026.
- `Nivel_Entrega` incorpora el FBX de `Escenario.zip` de Ian, dos zonas con dos oleadas de dos enemigos cada una, tres balizas provisionales, extracción y rehén con Behavior Tree propio. La primera zona genera orbitadores; la segunda, embestidores con `BT_Charger` propio.
- Inicio del editor: `/Game/ThirdPerson/Maps/Nivel_Entrega`. Inicio del juego: `/Game/LevelMenu/MainMenuLevel`. Nuevo juego del menú abre el nivel nuevo.
- Sistemas nuevos bajo `Content/ThirdPerson/Blueprints/Entrega/` y `Content/ThirdPerson/Blueprints/Aliado/`; importación bajo `Content/ThirdPerson/Environment/EscenarioIan/`.
- `BP_PlayerEntrega` hereda del personaje original y añade pesado al embestidor/puertas habilitadas, mejora del martillo y alineación/ventana de su hitbox. `ABP_EnemyEntrega` conserva la locomoción del pack mediante un gráfico enlazado y añade un Slot para los montajes propios. Los originales del equipo se conservan.
- Refinamiento: malla original `SK_SciFiWarrior02`, materiales originales y escala 1 en ambos enemigos; `ContactDamage=13.2` (+120% sobre 6). Camara con sonda de 24 cm, brazo 350 cm y pivote Z55. Sectores de Ian con prismas convexos por cara que conservan sus puertas. Presentacion actual: recuadro contextual negro/blanco con texto progresivo y audio propio; señal E/RB sobre el rehén cuando espera a salvo.
- El proyecto sigue sin módulo C++ de gameplay. UAT puede generar targets temporales dentro de `Intermediate` por los plugins habilitados.
- Consultar `HANDOFF.md` actual para pruebas, controles y límites. La sección de hechos de octubre que sigue se conserva como historia y no define los mapas actuales.

## Verified repository facts

Checked on 2026-10-11.

| Fact | Source |
| --- | --- |
| Workspace folder | `PIA_Optimizacion` |
| Unreal project file | `Terreno.uproject` |
| Engine | Unreal Engine 5.6 (`EngineAssociation`: `5.6`) |
| Code | No `.h`, `.cpp`, or `.cs` gameplay source files were found. Blueprint project. |
| Editor startup map | `/Game/ThirdPerson/Maps/ThirdPersonMap` |
| Default game map | `/Game/ThirdPerson/Maps/ThirdPersonMap` |
| Default game mode | `/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode` |
| Other project map found | `/Game/LevelMenu/MainMenuLevel` |

Enabled plugins in `Terreno.uproject`: ModelingToolsEditorMode, MotionTrajectory, PoseSearch, MotionWarping, AnimationWarping, Chooser, AnimationLocomotionLibrary.

### Gameplay assets that exist

Enemy AI folder: `Content/ThirdPerson/Blueprints/EnemigoIA/`

- `BP_BaseEnemy`
- `BP_IAController`
- `BPI_Enemy`
- `BB_EnemyIA`
- `BT_EnemyIA`
- `BTService_LocatePlayer`
- `BTTask_Attack`
- `BTTask_Defend`
- `BTTask_HitSun` (the hit-stun task; the asset name is spelled HitSun)
- `BTTask_Roam`
- `Enemy_Death`
- `Enemy_Death_Montage`

Related gameplay assets under `Content/ThirdPerson/Blueprints/`:

- `BP_ThirdPersonCharacter`
- `BP_ThirdPersonGameMode`
- `BP_TargetDummy`
- `Enums/E_States`
- `AnimNotifies/SaveLightAttack_AN`
- `AnimNotifies/BPC_Health`
- `AnimNotifies/Enemy_Health/BPC_E_Health`
- `AnimNotifies/ResetState_AN`
- `AnimNotifies/Health`
- `DañoDes`
- `PSD_Player`
- `PSS_Player`

Attack content that exists as assets, with no graph behavior confirmed:

- `Content/ThirdPerson/Animations/Fast_attacks/sword/`
- `Content/ThirdPerson/Animations/Heavy_attacks/Sword/`
- `Content/ThirdPerson/Input/Actions/IA_Heavy_Attack`

No asset whose file name identifies a hostage, escort follower, zone lock, conditional spawn, hammer, or wave manager was found. Absence of a matching file name is not proof that the feature is absent inside an unnamed Blueprint.

### Third-party content present

These folders are packaged content, not the assigned AI feature: `ParagonKallari`, `SciFiCharacterPack`, `SciFITrooper_Man_03`, `SciFiWarrior02`, `FreeAnimationLibrary`, `RamsterZ_FreeAnims_Volume1`, `Survival_Character`, `Fab`, `Characters`, `LevelPrototyping`.

## Stated premise

The protagonist is a time traveler who fights other time travelers to rescue a hostage. Environment models are justified by that premise. No further lore, character names, or faction names were provided.

## Stated game loop

This is a fast action game. The stated sequence is:

1. The player searches for the hostage and defeats enemies.
2. The player must find a second weapon, the hammer, before progressing.
3. The player reunites with the hostage and escorts the hostage to the final area.
4. The hostage escapes. The player must survive enemy waves. The wave size depends on how many enemies remain in the level, and the section has a time limit.
5. A progression system strengthens the character during the level.

Numeric values for the time limit, wave counts, hammer location, and progression rewards were not provided.

## Stated schedule and scope

- AI work is documented against Week 7 of the course schedule. The week-by-week calendar itself is not in the repository.
- The final delivery is Week 12, 19–25 October 2026.
- Extras wait until the essential work items are done.
- On the owner's board, the first AI is marked Done and still needs the combat integrations in `AI_REQUIREMENTS.md`. The second AI is To Do.

## Course rubric

Source: `FE-OV 1.docx`, supplied by the owner on 2026-10-11. The file header says the course is Optimización de Videojuegos, semester January–June 2025. The owner separately set the final delivery to 19–25 October 2026. Advertising, social networks, and the promo site are out of scope for this agent.

Development items marked as requirements on the final checklist:

- Two different attack types.
- Death message and return to the startup menu.
- At least three different objectives required to win.
- Two enemies with different advanced AI. Different behavior, not a different mesh on the same behavior.
- Local save of health, ammo, money, and position.
- At least two custom macros, two custom events, and two custom functions in the level, none of them engine defaults.
- Interface, Nanite, World Partition or World Composition, lighting, LODs, 15 models, 6 destructibles, 8 particle systems, and a working graphics options menu.

The full project text also asks for keyboard, mouse, and gamepad with matching actions, first- and third-person camera, a health bar, inventory, two NPCs with dialogue, day and night, and audio. Water is listed in the full text, and the final checklist marks the water body as not required.

Only the AI items are in the current work queue. The rest stay recorded so another agent does not treat them as invented extras or as this queue.

## Locked decisions

Orbit distances, defend timing, Print String text, hostage spacing, zone lock, conditional spawn, and the second enemy behavior are Decisions in `AI_REQUIREMENTS.md`. The owner delegated those choices on 2026-10-11. On 2026-10-14 the owner changed the orbit to radius 180 (band 150–210) and light damage to 25. On 2026-10-18 the owner changed light damage again, to combo 15 / 15 / 19.

## Verified graph facts

Exported from the open editor on 2026-10-14. The full per-asset state is in `HANDOFF.md` → "Saved asset state".

- Git: branch `main` (commit `7198fa9`) is the original project. Branch `feat/ai` holds the AI work. Assets are in Git LFS, so `git diff` on a `.uasset` only shows pointers. Compare behavior by exporting both versions.
- `BT_EnemyIA` is the five-branch Selector in `HANDOFF.md`. `BTService_LocatePlayer` sits on that Selector. On `main` the tree was smaller: a Selector containing a chase Sequence (Rotate to face → Move To `TargetActor` → Attack with Cooldown and Force Success) and Roam → Wait.
- Agent PIE on 2026-10-14 showed roam, orbit, defend, and attack running.
- `BP_ThirdPersonCharacter` Event AnyDamage calls `BPC_Health.Decrease_Health` with the event's Damage pin. A debug key still calls that function with Damage 25. Enemy Apply Damage is 10 and now reaches the player.
- `E_States` has two values: Nothing and Attack. `ResetState` calls `SetState` with Nothing.
- `SaveLightAttack_AN` calls `SaveLightAttack`. `bSaveLightAttack` buffers the next light-combo input.
- `BPC_E_Health.E_Decrease_Health` subtracts the Damage argument and fires `E_Dead` at 0 or below. BeginPlay and Tick on that component do not continue.
- `BP_BaseEnemy` Attack binds `E_Dead` (this belongs on BeginPlay), sphere-traces with radius 200, and applies damage 10 to the hit actor, then plays a montage with no asset set. `E_Dead` calls `Enemy_Death`, which only plays `Enemy_Death_Montage`.
- `BP_IAController` writes Blackboard `DetectionRadius` as 1500 on BeginPlay. That matches the locked value.
- The player weapon overlap casts to `BP_BaseEnemy`, prints `Hitbox detectada`, and does not execute `E_Decrease_Health`. That call is on the graph with Damage 100 and an empty execute pin.

## Unknown

- Walkable coordinates in `ThirdPersonMap`. Place new zones in reachable space and record the actor labels in `HANDOFF.md`. Do not invent landmark names.
- Hammer effect, progression rewards, survival time limit, and the wave-count formula.
- Which existing montage fits the enemy attack. The `BP_BaseEnemy` Play Montage node is empty.
