# Handoff

Living note for the next agent. Replace the "Current handoff" section when work changes. Keep older entries under History.

Read order: `GOVERNANCE.md`, `PROJECT_CONTEXT.md`, `AI_REQUIREMENTS.md`, `WORK_ITEMS.md`, this file.

This file is written so a smaller model can continue without re-auditing. Every step below names the exact asset, node, and pin. Follow the steps in order. When a step's result does not match what is written here, stop and use the escalation rule in `GOVERNANCE.md` ("When to escalate").

## Current handoff

- **2026-11-16, última solicitud:** corregir ataque enemigo lejano seguido de carrera/daño tardío, avisar del daño al rehén y confirmar daño a rivales; después verificar qué falta de la rúbrica. Commit/push siguen autorizados a `origin/codex/entrega-18nov-ia-oleadas`.
- **Verified ataque:** `generate_combat_feedback.py` envuelve legacy_base_enemy de generate_combat_graphs. Attack exige objetivo válido, distancia<=220 y LOS; detiene navegación y resetea bAttackResolved. ResolveAttack consume una sola oportunidad dentro de montaje activo0.30..0.70s; tareas lo llaman a0.45. Fallo/cancelación no deja daño atrasado. Ambos árboles y ContactDamage13.2 conservados.
- **Verified embestidor:** preparación0.8s mira al objetivo y avisa, sin ejecutar el montaje de golpe. ChargeVictim/ChargeGoal se fijan al salir; carrera900cm/s hasta1s, llegada<=180cm detiene movimiento, llama Attack y espera montaje1.3s antes de retirada. El ciclo incluye esa ejecución cercana; no afirmar misma cadencia efectiva histórica. `generate_combat_graphs.windup/charge/base_enemy` delegan a la receta nueva; `generate_progression_graphs.enemy_actions` ya no necesita insertar otro snapshot.
- **Verified señales:** BaseEnemy.OnHealthChanged compara LastFeedbackHealth real; pérdida (incluso letal) da impacto2D existente SW_DoorHit(vol.3/pitch1.3), EnemyHitUntil(.18s) y LastEnemyDamage al HUD. Curación/contacto sin daño no confirman. El HUD mantiene el volumen global de opciones. Rehén incrementa DamageNoticeSerial sólo al aceptar daño hostil; aviso2.4s y alerta con cooldown1.2s. El serial no se persiste y no salta por restaurar salud/checkpoint. La alerta es texto y sonido, no voz hablada nueva.
- **Reproducción de gráficos:** editor BPB3 opcional, PIE detenido. Local: `generate_combat_feedback.py`, `generate_combat_graphs.attack_task()`, `generate_progression_graphs.hostage()`, `generate_dialogue_hud.py`; luego `install_combat_feedback.py`. Añade campos antes de importar; orden rehén→HUD→base→tareas→compilar hijo. Recompila/guarda Director y SaveManager al final: cambiar clase del rehén puede dejar temporalmente al director pendiente de recompilar y bloquear PIE con modal. No reemplazar con recetas antiguas ni instalar el mapa otra vez. Juego sigue Blueprint-only; helper sólo editor.
- **Verified:** diez Blueprints de combate/exportes sin errores; cuatro casos de árboles reales (dos enemigos×jugador/rehén), daño durante montaje y sin deslizamiento; solicitudes lejanas rechazadas. Esquiva, retorno tardío y cancelación no dañan. Regresión de ligeros15/15/19/22 y pesado25 contra ambos, sin duplicados. Señales incluyen letal y negativos de curación/restauración/gracia. Impacto de audio renderizado RMS0.004052. Evidencia central `validation/combat-and-rubric-2026-11-16.json`.
- **QA:** pruebas `verify_enemy_strike_timing.py`, `verify_enemy_strike_misses.py`, `verify_combat_feedback.py`; son fixtures aislados, no partida natural. Callbacks deben terminar antes de parar PIE. Audio requiere foco en viewport PIE (un Message Log superpuesto dejaba el dispositivo inactivo); exportar WAV a ruta absoluta. Captura normal Shot conserva avisos cortos; HighResShot podía consumir varios segundos de preparación y dejarlos expirar. Respaldo previo de assets en Intermediate/inspect/combat-timing-backup. Se restauró throttlingTrue/t.MaxFPS0 y no se guardaron preferencias de QA.
- **Verified World Partition:** Salida_Extraccion era TriggerBox espacial y el Director persistente lo referenciaba; ahora residente, Modify/paquete externo guardado y receta prepare_world_partition corregida. Cook final0errores MapCheck. Conservar las reglas de guardado externo de entradas históricas.
- **Verified auditoría:** `audit_delivery_requirements.py` confirma16diseños visuales cargados, agrupando copias/variantes;15si se excluye Manny. Esto acredita cantidad, no autoría. Cinco modelos×cuatro LOD nativos; `capture_delivery_lods.py` con factores de radio4/16/24/80 y FOV60 muestra blanco/rojo/verde/azul, sin LOD forzado. Veinte capturas en validation/lod-demo-2026-11-16. Seis destruibles fracturados de nuevo por dos pesados del binding real; funciones/macros/eventos de Level BP ejecutados. Rúbrica y pendientes vigentes: `PLAN_ADAPTACION_EVALUACION.md`.
- **Pendiente académico/exterior:** documentación académica/cronograma; evidencia de3redes públicas con15posts cada una (hoja marcada verde, no se afirma que falten posts); video>=3min; confirmar munición/dinero con Adame y aplicabilidad de inventario, segundo NPC dialogante, día/noche y5modelos propios. Esos tres sistemas generales no tienen implementación acreditada actual. Agua aparece REQ No. Rehén final aún pendiente del compañero. No atribuir autoría por nombre de carpeta ni aceptación por color de hoja.
- **Límites de aceptación:** partida manual completa, dificultad, PC de presentación/rendimiento, preguntas del equipo y aceptación de Adame. Mando aplazado. El bot del escenario actual perdió en zona2; no atribuirle victoria natural por estos fixtures. Balizas, esquema2, geometría/terreno/luz/Niagara y ajustes de paredes/visibilidad de la entrada anterior se conservan.
- **Verified paquete:** Win64 Development BUILD SUCCESSFUL/ExitCode0, cook0errores/15advertencias previas, ZIP622936009bytes, CRC completo aprobado, sin Saved/PDB/helper. Smoke Windows de Nuevo juego/E/rescate/reloj/HUD y salida limpia; no combate completo. Editor normal reabierto sin helper, PIE detenido, sin paquetes sucios. Recarga fría pasó campos nuevos sin falsas señales y los11modelos con límite efectivo0, evitando regresión de coches. ZIP local en Deliverables ignorado por Git; fuentes/pruebas/documentos sí se versionan.

## History

### Paredes/visibilidad antes de corrección de combate — 2026-11-16

- **2026-11-16, solicitud vigente:** corregir todas las paredes con textura estirada, optimizar texturas y evitar desaparición visible de coches. El propietario autorizó **commit y push a origin al terminar**, en `codex/entrega-18nov-ia-oleadas`. La restricción histórica de sólo commit local queda sustituida.
- **Verified:** 104 componentes de pared (edificios, límites, marcos y módulos) usan tres materiales `Environment/Atmosphere/M_WallMetric_*`, con las texturas existentes y WorldAlignedTexture XYZ a 400 cm. La escala no depende de UV/escala del actor. No se cambió geometría/colisión.
- **Verified:** once texturas de superficie/props con compresión de mundo opaca, mipmaps, streaming y máximo1024/2048 según detalle. Madera/metal no POT se remuestrean a POT al construir, sin alterar sus fuentes. No se modifican assets Fab. Receta: `optimize_delivery_surface_textures.py`; conserva antes/después en Intermediate/inspect/surface_texture_budget.json.
- **Verified:** todos los StaticMesh/GeometryCollection colocados sin límite duro de distancia, **LDMaxDrawDistance y CachedMaxDrawDistance = 0**, never_distance_cullTrue. Los once props LOD/destruibles no son espaciales y permanecen residentes al cambiar de celda. Arquitectura conserva World Partition/Nanite; los cinco modelos de evaluación conservan cuatro LOD clásicos. Luces y Niagara mantienen sus límites documentados: no confundir culling de efectos/luz con cortes de modelos.
- **Corrección importante de herramientas:** editar una propiedad de componente Blueprint reconstruye el actor y convierte referencias anteriores en TRASH. `fix_wall_mapping_and_model_visibility.py` reúne nombres y resuelve de nuevo cada componente antes de editar. Al acabar todas las reconstrucciones aplica SetCullDistance1→0 para actualizar también CachedMaxDrawDistance; cambiar sólo LD/never dejaba el coche Chaos con caché6000. Guardar paquetes externos de WP, además del umap.
- **Reproducción:** editor con Nivel_Entrega abierto y región completa cargada, PIE detenido. Si se regenera escena, terminar con `optimize_delivery_surface_textures.py` → **`fix_wall_mapping_and_model_visibility.py`** → `validate_wall_visibility_fix.py` → `verify_compound_editor.py`. El último arreglo de material debe ir después de prepare_compound_scene, que asigna los materiales originales. No necesita helper; la reconstrucción completa de escena sí usa Tools/EditorBridge BPB3 editor-only.
- **Verified:** auditoría de104paredes/11props, cinco modelos con4LOD y dos coches sin corte efectivo en PIE. Comparación desde misma cámara exterior a más de90m: el corte antiguo6000 del coche estático se simula sólo en PIE; con la configuración final ambos coches se ven. Capturas de rescate/arena/módulo verificadas. Prueba runtime reproducible: `verify_wall_model_runtime.py` en PIE fresco. Evidencia vigente: `docs/validation/walls-visibility-2026-11-16.json`. Las pruebas son del agente, no aceptación del propietario.
- **Continuidad:** esta revisión conserva el rework de evaluación y las balizas A/B/C aleatorias/reloj/guardado esquema2, combate Blueprint-only, dos zonas2×2 y daño13.2. Los informes compound anteriores son históricos y sus distancias38/60/180m ya no describen los modelos actuales. No ejecutar fix_delivery_lighting ni reconstructores anteriores del mapa. Conservación detallada de colliders, refugios, luz y Niagara en la entrada histórica siguiente y `ESCENARIO_COMPOUND.md`.
- **Límites:** aceptación visual/dificultad del propietario, PC de presentación, mando y confirmación de munición/dinero con Adame pendientes. El bot del escenario actual perdió en zona2; no atribuir victoria natural a esta revisión. No se afirma mejora de FPS sin comparación medida.
- **Verified paquete:** Win64 Development BUILD SUCCESSFUL/ExitCode0, cook0errores; 30 advertencias que corresponden a las mismas15únicas previas, sin nuevas de materiales. ZIP **622921207 bytes**, CRC completo aprobado. Smoke nativo de Nuevo juego y paredes del recinto; no es recorrido completo. Editor normal reabierto, validación de104paredes y11modelos repetida tras recarga en frío; sin PIE ni paquetes sucios. Se genera con `Tools/Build-Delivery.ps1` (editor cerrado) y `Tools/Archive-Delivery.py`. Resultado y tamaño finales se registran en la evidencia vigente. ZIP local ignorado por Git; fuentes, recursos, recetas y evidencia sí se versionan.


### Dirección de escenario previa a corrección de paredes/visibilidad — 2026-11-16

- **2026-11-16, dirección del propietario:** rehacer terreno/distribución/luz con función usando assets existentes y reducir trabajo fuera de vista. **Verified:** revisión descrita en `ESCENARIO_COMPOUND.md`. La distribución en franjas, cuatro sectores monolíticos y luces genéricas de la revisión anterior quedan sustituidos. Gameplay Blueprint-only, mismas dos zonas/árboles/daño13.2/objetivos. Munición/dinero aún por confirmar con Adame; no se agregó economía.

### Escena y optimización vigentes

- Landscape real de cuatro componentes, nuevo `Environment/Atmosphere/M_TerrenoRecorrido` con máscara de usos propia (senderos, patios, grava, roca) y **cuatro** texturas existentes; no bandas por Y ni textura ornamental de pared en caminos. `terrain_layout.json` + `Tools/build_terrain_control_map.py` son la fuente. Material anterior `/Game/Landscape` conservado, ya no es el asignado.
- Diez `SM_Walls_*` separan edificios con pivotes/bounds locales, UV/materiales originales y Nanite. Fuente original conserva **escala2 en XYZ**: muros~4m. Durante desarrollo se omitió Z y el bot encontró un dintel bajo; ya se corrigió y el auditor nativo exige alturas390..410cm. Cubiertas de rescate/depósito a420cm y prolongación395..420cm. No regenerar con escalaXYsola.
- Props agrupados por uso; dos coches en estacionamiento sur, fuera de refugios. Caja/basurero/banca/barril/auto/fuente conservan seis GC; cinco modelos con cuatro LOD se conservan. Alinear por `SystemLibrary.get_component_bounds` de la malla visible, **no GetActorBounds**, que incluía componentes auxiliares del tutorial y elevaba objetos. Bases de las seis colecciones verificadas aZ0, física desactivada intactas; se activa justo antes de CrumbleActiveClusters, eventos Chaos reales comprobados por golpes. Restos8s. No se guarda decoración rota.
- **Corrección final de impactos reales:** las GC traían GenerateOverlapEventsFalse y no bastaba llamar al binding en una prueba. Se reutiliza `Colision` como proxy QueryOnly ajustado a bounds visibles, ObjectTypeDestructible, GenerateOverlapEventsTrue, PawnBlock/CameraIgnore. GC renderiza sin colisión/simulación intacta. Al romper: proxyNoCollision → GCQueryAndPhysics → SetSimulatePhysicsTrue → Crumble/impulso. `fit_compound_query_colliders.py` + `install_compound_logic.py`; receta Scene ya lo conserva. **Verified físico:** dos ataques pesados por acción/montaje real, sin ApplyDamage ni llamada manual al overlap, salud50→25→0 y20 eventos Chaos. Prueba aislada con posición/martillo preparados: `compound-physical-attack-2026-11-16.json`.
- Dos refugios nuevos próximos al acceso del depósito (-2150,-4600) y (-2150,-5500), tags RefugioRehen, no espaciales. Evitan exigir cruzar la arena para retirarse. Los árboles y límites de huida siguen iguales. Autos nunca deben tapar los puntos existentes; prueba específica de bounds/rutas de refugios.
- Luces Rect en techo de rescate, Point en depósito y Spot del poste del patio, con luminarias visibles. Radios10/7/11m, draw24m/fade3.5m, sólo Rect con sombras locales, sin volumétricos locales. Sol móvil15000lux; Sky móvil con sombras y captura **no continua**; volumen Iluminacion_Entrega con Lumen y exposición-.75, adaptación4/2. **No ejecutar fix_delivery_lighting.py**, que desactiva GI y sombras del cielo por un arreglo histórico del mesh combinado.
- Rotaciones siempre por keywords pitch/yaw/roll. Python Rotator posicional era roll,pitch,yaw y hacía mirar luces de lado. Auditor runtime exige forwardZ Rect<-0.99 y Spot<-0.7.
- Descarte efectivo verificado: props38/60m, arquitectura/cubiertas180m, bounds_scale1, never_distance_cullFalse; occlusion queries y Nanite frustum/HZB activados. Cinco LOD permanecen antes del descarte. No se detiene IA/misión fuera de cámara ni se promete coste cero de luz/sombras sobre superficies visibles.
- Copias ambientales NS_Compound_Hojas/Polvo/Extraccion usan NET_CompoundAmbient: distancia24m, visibilidad/frustum1s, comprobación Low1s, **DeactivateImmediateResume**. Prueba real: activo cerca → inactivo lejos → activo al volver → inactivo mirando fuera. La cámara debe estar fuera de la esfera conservadora del sistema para probar frustum. No usar IsPaused como prueba: devuelve pausa solicitada por usuario, no estado interno de scalability. `is_culled_by_scalability` no está reflejada; se verifica componente activo/inactivo con reacción inmediata. No se cambian fuentes Niagara del equipo.

### Fuentes, guardado y pruebas

- Helper editor-only en Tools/EditorBridge, Build-EditorBridge.ps1 → Intermediate/BPB3. Nuevo LoadEditorRegion carga región completa (-6500,-12500,-1000)..(6500,1000,3000) mediante adaptador oficial user-created. Sin dependencia runtime del helper. Exportar fuentes con export_compound_sources.py; Blender build_compound_shelters.py genera14FBX y flag reimport; preparar terreno/scene/fx y generar/install_compound_logic. Ver receta completa en ESCENARIO_COMPOUND.
- **World Partition:** llamar Modify en actores/componentes y guardar paquetes `/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/`, además del umap. Sin ello PIE/cook podían leer transformaciones anteriores aunque el editor mostrase cambios. prepare_compound_scene/fx guardan explícitamente esos paquetes. Navegación sigue dinámica convencional dentro de WP, Recast is_world_partitionedFalse/force_rebuild_on_loadTrue.
- **Verified:** geometría/altura, bases y distancias efectivas; seis fracturas con física bajo demanda; macros/eventos/funciones de Level BP y captura; seis secuencias/18canales, guardado/reloj/extracción aislados en mapa nuevo. Informes `compound-*-2026-11-16.json` y global `compound-2026-11-16.json`. Estos son tests del agente, no aceptación del propietario.
- **Límite de recorrido:** el bot atravesó accesos y combatió, pero no completó una victoria natural en esta revisión; informe final termina en derrota del jugador en la segunda zona, anteriores en derrota del rehén. Se corrigieron bloqueo de dintel y props/refugios; no se alteró salud/daño. Bot usa dirección antes de encadenar, prioriza amenazas al rehén y pesado en zona2. No atribuir la victoria4:37 de la revisión anterior al escenario actual. Dificultad y experiencia requieren partida manual del propietario.
- Antes de cerrar: desregistrar callbacks Slate o esperar marcador terminal; no detener PIE con pruebas activas. Restaurar bThrottleCPUWhenNotForegroundTrue/t.MaxFPS0 (cambio temporal de QA). Guardar sólo contenido propio; descartar caches Fab incidentales sin sobrescribir recursos ajenos.
- **Verified paquete final:** Win64 Development BUILD SUCCESSFUL, 0 errores/15 advertencias previas, ZIP **633779230 bytes**, CRC aprobado, sin Saved/PDB/helper. Smoke nativo y límites en `docs/validation/compound-2026-11-16.json`. La prueba natural no es victoria; aceptar visual/dificultad con propietario. Editor normal reabierto sin PIE y sin paquetes sucios.


### Rework de rúbrica anterior a dirección de escenario — 2026-11-16

- Fecha **2026-11-16**. Rama `codex/entrega-18nov-ia-oleadas`. **Stated:** adaptar a la rúbrica con rework necesario, primera ejecución en pantalla completa y corregir ratón. El propietario aún debe confirmar con Adame si munición/dinero son obligatorios. No se agregó economía. Plan y guía: `PLAN_ADAPTACION_EVALUACION.md`, `GUIA_DEMOSTRACION_EVALUACION.md`.

### Implementación verificada

- `Nivel_Entrega` convertido **in place** por WorldPartitionConvertCommandlet oficial; commandlet Exit0, 0 errores/15 advertencias. Backups preconversión en `Intermediate/inspect/evaluation-backup`. Actores esenciales de misión no espaciales; configuración de grid predeterminada del conversor, sin afirmar celdas personalizadas. Recast usa **is_world_partitioned=False, runtime_generation=DYNAMIC, force_rebuild_on_load=True** dentro del mapa WP: no hay navchunks particionados. Activar el flag de Recast sin construir chunks dejó cero tiles; no repetirlo.
- Cuatro paredes de Ian sin caras horizontales del suelo: FBX reproducibles bajo `Tools/ArtSource/EvaluationWalls`, receta Blender `prepare_evaluation_walls.py`. Conservan materiales y colisiones por cara; Nanite habilitado. Landscape real plano, cuatro componentes, origen (-6300,-12000,-2), escala100. `/Game/Landscape` conserva cinco capas pintables; incorpora mezcla automática de las cinco texturas por **WorldPosition.Y escalar** donde no hay pesos pintados. El import inicial no creó weightmaps; no afirmar terreno pintado. Backup `M_Landscape_Equipo_Original`.
- Cinco copias de modelos del equipo `Environment/Evaluation/SM_LOD_{Banco,Car,Tree1,Light_Pole,fuente}` con cuatro LOD reales, screen sizes 1/.45/.20/.07 y Nanite **desactivado**. Conteos geométricos nativos en informe de mundo. Iluminación Directional+Sky y tres tipos locales Point/Spot/Rect sin sombras y maxdraw4500/fade500.
- `BP_DestruibleEntrega` conserva Geometry Collections del equipo: caja/basurero/banca/barril/auto/fuente. Vida50, daño por overlap del arma, dos pesados; CrumbleActiveClusters, impulso, eventos reales OnChaosBreakEvent, restos ignoran Pawn/Camera, lifespan8. El jugador añade ECC_Destructible al hitbox y usa caché de impactos para un daño por ataque. Decoración rota no se guarda; no bloquea misión.
- Ocho Niagara distintos: NS_Hojas/Polvo/Luces ambiente, NS_Explocion barril, NS_ChispaImpacto otros destruibles, NS_HammerUpgrade, NS_DoorBreak y NS_FuegArtificiales al terminar secuencia. Señal FX_Extraccion usa NS_Luces: es otra instancia, no noveno sistema.
- Level Blueprint real tiene macros AmbosAliadosVivos/SecuenciaResuelta, funciones ConsultarAliados/ConsultarSecuencia y eventos InicializarSenales/SincronizarExtraccion. BeginPlay programa delegados de timer (.01 una vez / .2 repetido); contadores prueban eventos activos, funciones usan macros y controlan señal extracción. No declarar sólo gráficos desconectados.
- Defaults GameUserSettings pantalla completa0 y resolución escritorio, respetando Saved posteriores. Gameplay BeginPlay y reanudar: ocultar cursor, GameOnly, foco viewport, captura permanente incluyendo clic inicial. InputModeGameOnly hace el bloqueo LockOnCapture nativo.
- Correcciones encontradas en regresión: `GrantHammerUpgrade` limpia bSaveLightAttack y llama ResetState después de StopAnimMontage para no quedarse en Attack sin montaje. CompleteActivation usa **GetHorizontalDistanceTo <=220**: el modelo tiene origen en el suelo y la cápsula del rehén centro Z88; distancia 3D rechazaba llegadas válidas del BT. Se conservan demás guardas, árboles, dos zonas de 2x2 y daño13.2.

### Herramientas y reproducción

- Helper **editor-only** versionado en `Tools/EditorBridge`; `Tools/Build-EditorBridge.ps1` genera `Intermediate/BPB3`, usa -NoDeleteHostProject. Editor para instalar arranca con -PLUGIN a BPB3; el proyecto/paquete no depende del plugin. Métodos extra: is_partitioned, get_level_blueprint, create_evaluation_landscape, install_named_graph, get_lod_geometry. No editar sólo la copia Intermediate.
- Preparaciones: prepare_evaluation_landscape, props, level, terrain_material; generadores generate_evaluation_graphs/level. No volver a correr el constructor viejo del mapa ni convertir otra vez. `finalize_evaluation_world.py` mantiene navegación convencional dentro de WP.
- **Orden importante:** install_evaluation_graphs instala destruible → jugador → director → interfaz → Menu_Pausa → Menu_Opciones → inicio. Al reemplazar interfaz, el helper compila temporalmente sin firmas: reinstalar sus widgets llamadores evita errores activos y modal de PIE. install_beacon_sequence instala director → baliza → **BTTask_ActivateBeacon** → resto. Suprimir el task posterior rompe pines al cambiar firma.
- Editor en segundo plano puede limitar PIE a3FPS. Para pruebas se cambió temporalmente bThrottleCPUWhenNotForeground=False con set_property_text y t.MaxFPS60, sin SaveConfig. Restaurar True y t.MaxFPS0 al cerrar. Callbacks Slate de pruebas deben desregistrarse antes de parar PIE, o pueden escribir errores de mundo obsoleto.

### Validación y límites

- **Verified en PIE:** mapa particionado, Landscape cargado, inventario runtime30 rutas (27 sin primitivas/auxiliar; no equivale a 27 diseños originales), cinco LOD por geometría, Level eventos/funciones/macros activos y captura permanente. Seis colecciones fracturadas por dos impactos pesados desde binding del arma: eventos Chaos reales, no sólo bBroken.
- **Verified:** recorrido completo con movimiento/ataques de gameplay, sin teletransportes ni ajustes de salud/daño: victoria C>A>B en 4:37, jugador73.6 y rehén20.8. `evaluation-walk-2026-11-16.json` y captura de victoria. Hubo derrotas previas del bot; se mejoró su orientación antes de encadenar ataques. Durante el recorrido aprobado se ajustó su ruta de salida del pedestal para no empujarlo directamente; no se alteró el mundo ni se reposicionó al personaje. Esto no sustituye aceptación manual.
- **Verified:** seis permutaciones / 18 canalizaciones reales del BT, rutas, rechazo fuera de turno, checkpoint, reloj/pausa, 24 reinicios sin repetición y extracción; `evaluation-sequence-2026-11-16.json`. Amenaza visible interrumpe y reinicia canalización, mantiene puerta sellada; `evaluation-interrupt-2026-11-16.json`. Compilados/exportados15 Blueprints + Level Blueprint; cook es puerta final de compilación.
- **Pendientes:** demostración visual de LOD/Nanite ante Adame, aceptación manual en paquete, rendimiento en otra PC, autoría e inventario académico de quince modelos, documentación/cronograma/redes/video, modelo final del rehén y mando. Munición/dinero por confirmar con Adame.
- **Verified paquete:** Win64 Development BUILD SUCCESSFUL / ExitCode0, cook0 errores/15 advertencias previas. ZIP `Deliverables/TimeOut_Avance_18Nov2026.zip`, **685046189 bytes**, CRC aprobado, sin Saved/PDB. README actualizado incluido. `docs/validation/evaluation-2026-11-16.json` reúne el informe, límites y evidencia.
- **Verified UI nativa:** perfil de QA separado por -UserDir, sin flags de ventana/resolución: primer arranque completo1920×1080. Cámara por movimiento de puntero sin clic extra tras Nuevo juego en completa y ventana1280×720, reanudar, regresar de Alt-Tab y Continuar. Reiniciar conserva ventana elegida. E rescata; F5 guarda ordenABC a~23s; cerrar/reabrir y Continuar muestra Partida restaurada con mismo orden y tiempo. Sin bordes también permite mover cámara. CUA mueve puntero mediante scroll, rueda sin binding de gameplay. Capturas y log en validation. No fue una partida completa en Win64. Advertencia runtime heredada: Health widget ya agregado una vez por entrada, sin barra duplicada observada; ningún Error/AccessedNone. Juego de QA cerrado; editor normal reabierto en Nivel_Entrega, sin helper, sin PIE, ping sin paquetes sucios.


### Balizas y secuencia anterior al rework — 2026-11-16

- Fecha **2026-11-16**. Rama `codex/entrega-18nov-ia-oleadas`. **Stated:** integrar `Baliza.glb` y condiciones de Adame; el propietario confirma **orden real aleatorio en zona accesible**. Sugiere valorar más zonas enemigas, sin fijar cantidad. No se añadieron encuentros ni se cambió el balance. Las instrucciones citadas son criterios aportados por el propietario; aceptación de Adame/propietario pendiente.

### Funcionamiento vigente

- **Verified en PIE:** modelo del equipo bajo `/Game/ThirdPerson/Environment/Baliza/SM_Baliza`, tres zonas de material conservadas (cuerpo, brillo, detalle). Altura 150 cm, origen en base. Fuente original intacta `Tools/ArtSource/Baliza/Baliza.glb`; conversión reproducible `Tools/Blender/prepare_beacon_model.py`. `Index` 1/2/3 ahora identifica permanentemente A/B/C, nunca el turno.
- **Verified:** A en (-2600,-8500,0), B en (0,-9100,0), C en (2600,-8500,0); aproximaciones a +190 Y. `BP_BeaconLabel` muestra los nombres mirando a cámara. Espera tenue, siguiente azul y activada verde cambian sólo el material luminoso. Hay seis refugios locales nuevos etiquetados `RefugioRehen`, sin cambiar el árbol del rehén.
- **Decision / Verified:** seis permutaciones reales `ABC, ACB, BAC, BCA, CAB, CBA`, sorteadas en BeginPlay. GI `LastBeaconOrder` evita repetir el intento anterior en la misma sesión. `BP_DirectorEntrega.OrderCode`, `CurrentBeacon` y `Paso` determinan el siguiente destino. La canalización de 3 s sigue en `BTTask_ActivateBeacon` / `BT_Hostage`; exige ambas zonas despejadas, rehén vivo/rescatado/acompañando/sin amenaza y baliza correcta. Fuera de turno no avanza.
- **Decision / Verified:** primera y segunda puerta se cargan al despejar las oleadas de su zona y equipan el martillo. Esto hace accesible el patio antes de la secuencia. Completar las tres balizas habilita la tercera puerta. Se conservan dos golpes pesados, fractura y extracción con jugador/rehén. Las asociaciones `Baliza1/2/3.Door` se conservan para serializar las tres puertas, pero ya no deciden el orden de activación.
- **Decision / Verified:** `MissionElapsed` cuenta desde rescate, se detiene durante pausa y en resultados. HUD persistente muestra secuencia, siguiente, 0–3 balizas y MM:SS. No hay límite inventado. **R desde cualquier resultado inicia de cero y sortea otra secuencia**; ya no restaura derrota. **Continuar** conserva el checkpoint con su orden y tiempo. Esquema 2 en la ranura existente: archivos de esquema 1 son incompatibles con la disposición nueva. Opciones de audio siguen esquema 1 separado.

### Pruebas, paquete y límites

- **Verified:** `docs/validation/beacon-sequence-2026-11-16.json`: seis rutas dirigidas completas, seis permutaciones con 18 canalizaciones reales del BT, rechazo fuera de turno, primeras puertas por oleadas, dos golpes de puerta, pausa/reanudación del reloj, restauración de orden/tiempo/activaciones, 24 inicializaciones sin repetir el orden anterior y extracción con reloj detenido. Son pruebas **aisladas** con encuentros/posiciones preparados; no acreditan recorrido manual ni sustituyen el recorrido natural del 15 de noviembre, que corresponde al diseño anterior.
- **Verified:** un enemigo visible aborta canalización, reinicia progreso, provoca huida y mantiene la puerta final sellada. Nueve Blueprints compilados/exportados, tres modelos/nombres y seis refugios comprobados; ningún paquete sucio. Captura de interfaz `docs/validation/beacon-hud-2026-11-16.png`.
- **Verified:** Win64 Development **BUILD SUCCESSFUL / ExitCode 0**, cook **0 errores / 15 advertencias previas**. ZIP `Deliverables/TimeOut_Avance_18Nov2026.zip`, **549625110 bytes**, CRC aprobado y sin Saved/PDB. Log `docs/validation/beacon-package-log-2026-11-16.txt`. En el ejecutable: Nuevo juego mostró A > C > B; E rescató, reloj avanzó de 00:00 a 00:14; F5 guardó en 00:18; Escape congeló 00:24 entre dos observaciones; volver al menú y Continuar recuperó A > C > B y 00:18. No fue un recorrido completo. Juego de prueba cerrado; editor normal reabierto en Nivel_Entrega, sin PIE.
- **Pendiente:** partida manual del circuito nuevo, valorar si conviene añadir otra zona enemiga en el patio, aceptación de Adame/propietario, modelo final del rehén, mando y otra PC. FIN-05/07 Ready para aceptación; no marcar Done.

### Reproducción y precauciones

- Editor con helper BPB2 sólo para instalar, como antes. PIE detenido, `Nivel_Entrega` abierto: Blender `prepare_beacon_model.py` → `import_beacon_model.py` → `prepare_beacon_sequence.py`. Este último añade campos de director/GI/SaveGame, coloca modelos/nombres/aproximaciones/refugios y conserva las dos zonas.
- Local: `generate_beacon_sequence.py`, `generate_progression_graphs.activate_task()`, `generate_delivery_save.py`, `generate_delivery_controls.py`, `generate_dialogue_hud.py`; después `install_beacon_sequence.py`. Instala director → baliza → **BTTask_ActivateBeacon** → nombres → guardado → inicio → HUD. Reinstalar el task después de reemplazar CompleteActivation evita pines huérfanos por pérdida temporal de firma.
- `generate_progression_graphs.director()` y `beacon()` ahora delegan a la receta nueva. No reconstruir el mapa ni reinstalar fuentes antiguas; para regenerar controles/guardado conservar esta receta y el HUD actual.
- PIE fresco: `verify_beacon_sequence.py` (termina en victoria pausada), otro PIE fresco para `verify_beacon_interrupt.py`; detener y ejecutar `validate_beacon_sequence_assets.py`. Salidas en `Intermediate/inspect`. Después cerrar editor → `Tools/Build-Delivery.ps1` → `Tools/Archive-Delivery.py`.
- **Tooling corregido:** la aproximación inicial +230 Y excedía el rango de 220 cm; +190 Y pasó las seis secuencias. La proyección Python `NavigationSystemV1.project_point_to_navigation` emitió un ensure no fatal del CDO; evitar ese wrapper y usar consultas de rutas válidas como en estas pruebas. No hubo crash; los fallos de pruebas iniciales están sustituidos por informes aprobados.


### Pausa y controles — 2026-11-15

- Fecha **2026-11-15**. Rama `codex/entrega-18nov-ia-oleadas`. Base FIN-01/02 guardada en **cf28f39**. **Stated:** continuar FIN-03/04 y commitear; **el mando queda pendiente** por instrucción del propietario. Commits locales autorizados, sin push.
- **Verified:** `BP_DeliveryInterface`, actor único `Interfaz_Entrega` en MainMenuLevel y Nivel_Entrega, centraliza pausa y opciones. `BP_DeliveryOptions` y `SM_TimeOutSettings` son recursos propios. Gameplay sigue Blueprint-only, sin dependencia runtime del helper BPB2; árboles, Blackboards y balance 13.2 conservados.

### Pausa, opciones y controles

- **Verified:** P/Esc abre/reanuda pausa; dentro de opciones vuelve al widget de origen. Entrada de interfaz con prioridad 10 consume P/Esc antes del P heredado. SetGamePaused detiene mundo/IA/daño/oleadas; movimiento y mirada se ignoran. Opciones colapsa el menú de origen y lo recupera con foco; desde pausa mantiene el mundo detenido. Reanudar devuelve entrada GameOnly y oculta cursor. Ir al menú usa OpenLevel para descargar la misión. E/RB de interacción ya no ejecuta durante pausa; no se acredita soporte completo de mando.
- **Verified:** Salvar juego llama al gestor seguro vigente, muestra su confirmación/rechazo y conserva el checkpoint si hay combate. FIN-02 y su ranura `TimeOut_Delivery_v1` siguen vigentes.
- **Decision / Verified:** resolución 1280×720/1600×900/1920×1080/2560×1440; calidad de distancia, suavizado, sombras y texturas; ventana/sin bordes/completa. GameUserSettings aplica/confirma/guarda al elegir. Volumen 0/25/50/100% mediante SoundMix y archivo `TimeOut_Options_v1`, esquema 1, independiente del progreso. Nuevo juego conserva opciones.
- **Verified:** se conserva el arte de los menús; textos independientes ahora ignoran hit tests y ya no absorben clics. Creación de widgets usa UMGEditor.K2Node_CreateWidget; el tipo BlueprintGraph del generador antiguo no creaba opciones. Textos nuevos usan Roboto runtime, y la pausa ofrece leyenda de controles.
- **Decision / Verified:** C conserva IA_Camera. FPC adjunta a cápsula Z64/FOV90, sigue rotación y oculta la malla del propietario; TPC restaura cuerpo visible y conserva brazo350/sonda24. Y equipa martillo y T espada. WASD/flechas, ratón, espacio, clic izquierdo/derecho, E, F5, Enter y resultados R/Enter documentados en LEEME. No se amplió la entrada de mando.

### Evidencia y límites

- **Verified:** `docs/validation/delivery-controls-2026-11-15.json` reúne opciones, pausa, cámara/entrada, audio, diez ataques y compilación. Son pruebas del agente, **no aceptación manual del propietario**. FIN-03 Ready para aceptar con teclado/ratón; FIN-04 sigue In progress hasta aceptación y eventual paridad con mando.
- **Verified en PIE:** todas las opciones llamadas por sus eventos OnClicked reales y comprobadas con getters nativos/archivo. Pausa abierta por P, tiempo mundial constante durante un segundo real, bloqueo de movimiento/mirada, guardado seguro y rechazo en oleada, regreso al mismo widget pausado. Cámara/armas/movimiento/salto/ataque por acciones Enhanced Input inyectadas durante fotogramas reales; diez montajes conservaron daño y cierre de hitbox. Grabaciones del submix maestro: RMS al 25% / RMS al 100% = **0.269**, confirma efecto real del volumen.
- **Límite explícito:** el automatizador de ventanas no produjo cambios visibles con sus pulsaciones breves de C/Y en PIE o Win64; sí lo hicieron las acciones Enhanced Input. No atribuir una causa ni afirmar validación física de esos atajos. El propietario debe confirmar C/Y/T con su teclado al aceptar FIN-04. P/Esc y navegación de menús sí se observaron en el ejecutable. Mando y otra PC siguen pendientes.
- **Verified:** Win64 Development BUILD SUCCESSFUL / ExitCode0, cook **0 errores y 15 advertencias previas** (Scale de Niagara y poses Manny). ZIP `Deliverables/TimeOut_Avance_18Nov2026.zip`, **549387901 bytes**, CRC aprobado, excluye Saved/PDB. Menú/opciones/cambio real a ventana, ajuste de calidad, guardado desde pausa, Escape/P y descarga real de la misión observados en Win64. Evidencia final y límites detallados en el informe y `delivery-controls-package-log.txt`.

### Fuentes y reproducción

- **Verified:** abrir editor con helper BPB2 sólo para instalar gráficos. `prepare_delivery_controls.py` prepara recursos/diseño y coloca gestor en ambos mapas; PIE debe estar detenido. `generate_delivery_controls.py` genera los seis gráficos; `install_delivery_controls.py` los instala en orden interfaz → pausa → opciones → inicio → jugador → director. `validate_delivery_controls.py` compila/exporta y comprueba un gestor por mapa. No reconstruir el mapa ni reinstalar recetas antiguas.
- **Advertencia de continuidad:** el generador nuevo envuelve las fuentes previas de combate/guardado. Si se regenera menú, director o jugador con scripts anteriores, terminar con esta receta para conservar pausa/opciones/cámara. Las llamadas a eventos propios se comparten por entradas exec antes de que exista su firma reflejada; no reintroducir llamadas que el importador descarte.
- **Verified:** pruebas `verify_delivery_options.py`, `verify_delivery_pause.py`, `verify_delivery_camera_controls.py`, `verify_delivery_volume.py` y análisis externo `analyze_delivery_volume.py`. La prueba de pausa requiere pausa ya abierta por P; la de cámara requiere TPC y partida reanudada. La de audio exporta full/quarter.wav y necesita varios segundos sin detener PIE; analizar después. Son pruebas aisladas, no un recorrido de aceptación.
- **Verified:** LEEME actualizado. Guardar/cerrar editor, esperar cierre del proceso, `Tools/Build-Delivery.ps1` → `Tools/Archive-Delivery.py`. Los archivos de QA se respaldan en Intermediate/inspect/fin03-04-backup; el ZIP no contiene Saved. Editor normal debe quedar en Nivel_Entrega, sin PIE ni paquetes sucios.
- **Siguiente:** aceptación manual de FIN-01/02/03 y teclado/ratón de FIN-04. Reanudar FIN-06 al recibir el modelo final del rehén; baliza/FX y auditorías de rúbrica siguen pendientes. El mando se retoma cuando lo indique el propietario.

### Cierre FIN 01 y FIN 02 anterior a pausa/opciones

- Fecha **2026-11-15**. Rama `codex/entrega-18nov-ia-oleadas`, base de gameplay `c88bafb`. **Stated:** el propietario pide empezar FIN-01 y FIN-02. No se hizo commit ni push en esta intervención.
- **Verified:** guardado y restauración Blueprint-only mediante `/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySave` y `BP_DeliverySaveManager`, actor único `Guardado_Entrega` en `Nivel_Entrega`. Los Behavior Trees, enemigos, combate y balance 13.2 no se modificaron.

### Persistencia y controles vigentes

- **Decision / Verified:** checkpoints automáticos al rescatar, despejar una zona, activar una baliza o cambiar salud de puerta, una vez seguro. **F5** guarda manualmente. Se exige jugador vivo/en suelo/sin ataque, rehén vivo/sin amenaza/huida/canalización y ambas zonas fuera de oleada o intermedio. El último checkpoint se conserva durante el combate: no se serializa una oleada a mitad.
- **Verified:** se persisten vida, posición y rotación de jugador/rehén, orientación de cámara, arma y mejora, rescate/seguimiento/espera, Paso, balizas, salud/grietas/desbloqueo/rotura de puertas y estado/oleada/conteo de zonas completadas. No se guardan referencias de actores del mapa ni escombros temporales. Al cargar se reponen mallas y colisión sin ejecutar otra vez recompensas, canalización ni fractura.
- **Verified:** ranura independiente `TimeOut_Delivery_v1`, esquema 1. El menú conserva su diseño; Continuar se habilita sólo con archivo legible, compatible y personajes vivos. Nuevo juego inicia desde cero y reemplaza el punto. **R tras derrota recupera el último checkpoint; R tras victoria inicia desde cero**. Enter conserva el regreso al menú. HUD muestra guardado/restauración o espera de seguridad.
- **Verified:** `Config/DefaultInput.ini` elimina sólo el DebugExecBinding de F5 (`viewmode shadercomplexity`), que entraba en conflicto en Win64 Development. No alterar otras teclas de depuración para resolver este caso.

### Pruebas y límites

- **Verified:** recorrido automatizado completo en PIE, mediante movimiento de gameplay, interacción y delegados de entrada de ataques; **sin teletransportes ni modificaciones de salud/daño**. Dos zonas de 2×2, tres balizas y puertas, extracción y victoria. Última muestra a 147.2 s: jugador y rehén en 47.2 de vida. `docs/validation/delivery-walk-2026-11-15.json` y `delivery-walk-victory.png`.
- **Verified:** `delivery-save-2026-11-15.json`: snapshot/restauración de vida, escolta, arma, progreso, grietas y puerta abierta; bloqueos durante combate/intermedio/canalización/ataque/muerte. Son pruebas aisladas que preparan estados en PIE, distintas del recorrido anterior.
- **Verified:** `delivery-menu-2026-11-15.json`: archivo válido habilita Continuar; ausente/incompatible/corrupto lo deshabilita; los bytes originales se restauran al terminar la prueba.
- **Verified:** `delivery-continue-2026-11-15.json`: Continuar carga un mundo nuevo y recupera Paso 3, salud, escolta, zonas y puertas sin duplicar enemigos. Comprobado después de cerrar/reabrir el editor y mediante clic real del menú. Derrota del jugador por daño real + tecla física R recuperó el checkpoint. F5 físico guardó. Muerte del rehén por daño hostil produjo derrota y Enter físico regresó al menú.
- **Verified:** seis Blueprints de integración compilados/exportados y sin errores activos. Las pruebas del agente no son aceptación del propietario. **FIN-01 y FIN-02 permanecen Ready para aceptación**, con recorrido manual del paquete final, mando físico y otra PC pendientes.
- **Verified:** Win64 Development final: BUILD SUCCESSFUL / ExitCode 0, cook 0 errores y 15 advertencias anteriores (pin Scale de Niagara del jugador y poses Manny). ZIP `Deliverables/TimeOut_Avance_18Nov2026.zip`, **549384059 bytes**, CRC completo aprobado. Menú/Nuevo juego/E/rescate/checkpoint/F5 comprobados en el ejecutable; cerrar/reabrir conserva la partida y Continuar restaura la escolta. F5 conserva el renderizado normal. El guard de existencia del menú usa sus pines de ejecución nativos y no añade advertencias. Informe global `docs/validation/delivery-checkpoints-2026-11-15.json`, resumen del cook `delivery-checkpoints-package-log.txt`; capturas `delivery-save-native.png` y `delivery-continue-native.png`.

### Fuentes y reproducción

- **Verified:** `delivery_save_schema.py` define campos/ranura. `prepare_delivery_save.py` prepara los dos Blueprints y el campo de GI; exige `Nivel_Entrega` abierto y PIE detenido. `generate_delivery_save.py` genera gestor/menú/director, y `generate_dialogue_hud.py` genera el HUD con estado del guardado. `install_delivery_save.py` instala esos cuatro EventGraphs con el helper local BPB2. `prepare_delivery_menu.py` sólo prepara presentación predeterminada; Construct decide disponibilidad en runtime. `validate_delivery_save_assets.py` compila/exporta y comprueba un único gestor.
- **Verified:** el helper nativo permanece sólo en `Intermediate/BPB2`, cargado mediante argumento del editor; no es dependencia del juego. En importación inicial, llamadas a un evento propio pueden desaparecer si la firma todavía no existe. El generador comparte entradas de ejecución de las acciones locales en lugar de importar llamadas sin firma.
- **Verified:** pruebas nuevas en `Tools/UnrealPython/verify_delivery_save.py`, `verify_delivery_menu_states.py`, `verify_delivery_continue.py` y `playthrough_delivery_inputs.py`. Este último requiere Nuevo juego; un archivo `Intermediate/inspect/stop_delivery_walk.flag` detiene su callback. No ejecutar pruebas de estados aislados simultáneamente con el recorrido.
- **Verified:** fuente de LEEME actualizada en `Tools/Delivery-README.txt`. Guardar/cerrar Unreal antes de `Tools/Build-Delivery.ps1`, luego `Tools/Archive-Delivery.py`. El ZIP excluye Saved y partidas de pruebas.
- **Verified al cerrar:** los checkpoints creados por QA se respaldaron en `Intermediate/inspect/fin01-02-backup/test-saves` y se retiraron de las carpetas jugables; se empieza con Nuevo juego. Editor normal reabierto en Nivel_Entrega, sin argumento del helper; ping: sin PIE y DIRTY (none).
- **Siguiente paso:** aceptar manualmente la versión empaquetada; después continuar las integraciones del equipo de FIN-06/07/08 y la auditoría de rúbrica. Modelos finales del rehén/baliza, mando físico, otra PC y requisitos Unknown conservan su estado pendiente.


### Estado anterior del 15 de noviembre antes de FIN 01 y FIN 02

- Fecha **2026-11-15**. Rama `codex/entrega-18nov-ia-oleadas`. Base anterior `af8ddcf`. Commits locales autorizados; sin push solicitado.
- **Stated:** aumentar un 120% el daño enemigo y hacer trizas las puertas siguiendo sus grietas, sustituyendo los cuadros separados anteriores.
- **Verified:** Blueprint-only y Behavior Trees/Blackboards conservados. El helper nativo se usa sólo en el editor desde Intermediate; no es dependencia del proyecto/juego.

### Daño y puertas vigentes

- **Stated / Verified:** `BP_BaseEnemy.ContactDamage` y `BP_ChargerEnemy.ContactDamage` = **13.2** (6 × 2.2). Se aplica tanto a jugador como rehén. Este valor sustituye el contacto 6 de todas las entradas históricas. Se conservan ventanas, interrupción y gracia del rehén de 0.8 s.
- **Verified:** `BP_DestructibleDoor` conserva 50 de salud, baliza habilitadora y dos pesados de martillo energizado de 25. Al primero cambia su panel por `SM_DoorCracked_01/02/03`: fracturas geométricas de 0.7 cm. Al segundo genera **exactamente esas piezas**, con sus centroides y mallas originales: **42 / 56 / 72** fragmentos irregulares. Incluyen los cortes del panel, refuerzos y cerradura. Marco conservado. Ya no usa la máscara M_DoorCracked para el primer impacto ni cuatro cubos genéricos como escombros; recursos anteriores conservados como historia.
- **Decision / Verified:** piezas con casco convexo de su propio polígono, impulso alejándose del atacante, dispersión radial, velocidad angular inicial aleatoria 180–420 grados/s y vida 4 s. Ignoran Pawn/Camera y no afectan navegación. El paso se abre aun con los escombros presentes. Rejillas de fractura Voronoi con mayor densidad alrededor del impacto; no se modificó el Progression.blend original.

### Evidencia y reproducción

- **Verified:** `docs/validation/fracture-difficulty-2026-11-15.json`: golpes reales de ambos enemigos al jugador/rehén de 13.2, gracia/interrupción/muerte conservadas; dos impactos físicos de martillo; tres puertas con posiciones iniciales coincidentes a 0.0 cm, todas las piezas móviles y con giro, paso abierto durante escombros y limpieza a 4 s; misión completa aislada y compilación de 20 Blueprints. Capturas fracture-cracks-preview.png y door-shatter-late-preview.png.
- **Verified / límite:** pruebas del agente en PIE con teletransportes y condiciones aisladas, no aceptación del propietario ni recorrido manual completo. La prueba específica de fractura aplica eventos de daño reales; verify_real_hammer.py comprueba por separado entrada física/montaje/solapamiento del martillo.
- **Continuidad:** `Tools/Blender/build_fractured_doors.py` abre `Tools/ArtSource/Progression/Progression.blend` y genera FBX/manifest/FracturedDoors.blend en `Tools/ArtSource/Fracture`. Luego `generate_progression_graphs.py` → `prepare_fractured_doors.py` → `install_fractured_doors.py`. Preparar agrega variables/ExposeOnSpawn y asigna las tres instancias; instalar sólo reinstala fragmento y puerta. Generador de gráficos compartidos: generate_fracture_graphs.py. Los activos están bajo `/Game/ThirdPerson/Environment/Progression/Fracture`. No reconstruir el mapa ni reinstalar recetas antiguas de IA.
- **Verified:** fuentes de feedback/IA anteriores siguen vigentes; ver entrada anterior para señal E/RB, voz propia, fijación y recuperación de espada.
- **Verified:** Win64 Development: BUILD SUCCESSFUL / ExitCode 0, cook 0 errores y 21 advertencias de recursos anteriores. ZIP actualizado `Deliverables/TimeOut_Avance_18Nov2026.zip`, **739814428 bytes**, CRC completo aprobado. Prueba nativa: menú y Nuevo juego cargan Nivel_Entrega, HUD y placa E/RB visibles. Daño/fractura detallados comprobados en PIE. Log: `docs/validation/fracture-difficulty-package-log.txt`. Editor normal restaurado en Nivel_Entrega, sin helper.
- **Unknown / pendiente:** aceptación del propietario, recorrido manual completo, mando físico, otra PC, guardado/Continuar y modelos definitivos del equipo.

### Revisión documental de cierre — 2026-11-15

- **Stated:** el propietario pide contexto de gobernanza/documentos y una lista de pendientes; confirma que un compañero entregará el modelo definitivo del rehén.
- **Verified:** se añadió `docs/PENDIENTES_ENTREGA_FINAL.md` con 23 pendientes priorizados, dependencias del equipo, condiciones de cierre y requisitos de rúbrica separados entre pendientes confirmados y Unknown. Se enlazó desde WORK_ITEMS. No se modificaron assets, mapas, balance ni configuraciones; no se hicieron pruebas nuevas ni commit/push en esta revisión.
- **Verified documental:** el estado de gameplay y del paquete sigue siendo el descrito arriba. Los informes del agente no equivalen a aceptación del propietario. Los tres modelos de puerta documentados no acreditan por sí solos seis elementos destruibles; tres balizas repetidas tampoco acreditan por sí solas tres objetivos distintos.
- **Siguiente paso propuesto:** recorrido manual del paquete actual para detectar bloqueos, comenzar guardado completo/Continuar y coordinar la entrega del rehén con esqueleto, materiales y animaciones. Auditar menú/controles y los requisitos Unknown antes de decidir qué contenido adicional falta.
- **Unknown:** fecha y formato del recurso final del rehén, responsables finales del cierre y cumplimiento en Nivel_Entrega de los requisitos no acreditados (Nanite, World Partition, LODs, cantidades, inventario y segundo NPC).

### Estado anterior del 15 de noviembre — antes de dificultad y fractura geométrica

- Fecha **2026-11-15**. Rama `codex/entrega-18nov-ia-oleadas`. Commits locales autorizados; no push solicitado. Base anterior `bbf1f98`. Entrega 18 de noviembre.
- **Stated:** añadir señal flotante con tecla para llamar al rehén, diferenciar su voz (referencias de estilo: Canelita/Sans), fijación de los enemigos en el rehén detectado, eliminar deslizamiento en recuperación de pesado de espada y agrietar puertas al primer impacto del martillo energizado.
- **Verified:** continúa Blueprint-only, con los tres Behavior Trees/Blackboards; sin Source ni dependencia del helper nativo en el proyecto/juego.

### Cambios actuales

- **Verified / Decision:** `BP_HUD_Entrega` proyecta una placa compacta **E / RB** sobre la cabeza del rehén. Aparece al esperar rescate/reanudación a ≤1200 cm, con visión y dentro de pantalla. Se oculta siguiendo, huyendo, usando baliza, muerto o tapado por pared. `HostagePromptInRange` corresponde al alcance de interacción existente de 400 cm; la señal distante guía para acercarse. Esta petición sustituye la prohibición histórica de toda señal flotante; los otros textos siguen en el recuadro.
- **Verified:** voz original en `/Game/ThirdPerson/Audio/SW_HostageVoice_1/2/3`, tres sílabas sintéticas de 68 ms con armónicos/formantes y variación ligera de tono. El speaker REHÉN usa estas voces; narrador/alertas conservan SW_Text. Se conserva ENTER para revelar/cerrar sin ráfaga de sonidos. Generador `Tools/generate_hostage_voice.py`; WAVs en Tools/AudioSource.
- **Verified / Decision:** `BTService_LocatePlayer` y `BTService_ChargerSense` escriben `bHostageLocked` en sus Blackboards. Adquieren al rehén rescatado/vivo/visible a ≤650 cm, aunque el jugador esté más cerca. Retienen la prioridad aunque se pierda visión brevemente y hasta 1800 cm. Liberan al morir, dejar de estar rescatado o superar el límite. Los árboles siguen decidiendo órbita, preparación, carga, ataque y retirada; no se trasladaron decisiones a Tick de un Pawn. Una carga ya comprometida conserva ChargeVictim hasta terminar; la siguiente decisión usa la fijación. El jugador cercano ya no roba la prioridad: se protege al rehén atacando a sus perseguidores.
- **Verified / Decision:** `BP_PlayerEntrega` libera el montaje de pesado de espada al habilitarse nuevamente la acción, con límites de recuperación H_attack_1 1.18 s, H_attack_2 1.05 s, H_attack_3 1.70 s y blend-out 0.12 s. Apaga hitbox, limpia estado/índice y devuelve el arma al reposo. Así vuelve la locomoción al moverse, en lugar de arrastrar la pose final. No se modificaron los montajes originales ni sus ventanas de daño.
- **Verified:** `BP_DestructibleDoor` activa `bCracked` y asigna `M_DoorCracked` a las superficies del panel tras el primer daño válido (50→25). Máscara procedural de fracturas ramificadas, núcleo oscuro y bordes ámbar; coordenadas mundiales X/Z para las tres medidas de puerta. El segundo pesado conserva rotura/escombros/audio. Cerrada, ligero o martillo sin energizar: ni daño ni grietas. Marco y luz de baliza conservados.
- **Verified:** material y máscara en `/Game/ThirdPerson/Environment/Progression/M_DoorCracked` y `T_DoorCracks`; fuente `Tools/generate_door_cracks.py` → `Tools/ArtSource/UI/T_DoorCracks.tga`. En MaterialEditingLibrary, ComponentMask usa entrada vacía y TextureSample usa UVs; se verificaron conexiones y render. El flujo de grietas está conectado directamente entre daño y comprobación de rotura.

### Pruebas y continuidad

- **Verified:** siete informes aprobados en `docs/validation/hostage-feedback-2026-11-15.json`: HUD/voz/fijación y sus controles de liberación; movimiento tras los tres pesados a 500 cm/s sin pose de ataque; golpes inválidos sin grietas; primer impacto físico agrieta y segundo rompe; diez montajes con daño físico correcto; misión completa aislada (hordas/balizas/puertas); recompilación de 19 Blueprints. Capturas `hostage-prompt-preview.png` y `cracked-door-preview.png` bajo docs/validation.
- **Verified:** estas pruebas usan condiciones aisladas/teletransportes en PIE. No son aceptación del propietario ni un recorrido manual completo. La fijación sustituye la expectativa histórica de poder interceptar aggro por proximidad. `verify_hostage_combat.py` se actualizó para esa prioridad; la prueba específica nueva es `verify_hostage_feedback.py`.
- **Continuidad:** fuentes de gráficos vigentes `generate_progression_graphs.py` y `generate_dialogue_hud.py`. Orden para reproducir esta capa: generar WAVs/máscara → ambos generadores de gráficos → `prepare_hostage_feedback.py` → `install_hostage_feedback.py`. El instalador refresca también baliza/tarea de canalización porque llaman a eventos del jugador. No ejecutar recetas antiguas de reconstrucción completa ni sobrescribir el árbol del orbitador; conserva su tarea FaceCombatTarget del avance anterior.
- **Verified:** Win64 Development actualizado: BUILD SUCCESSFUL / ExitCode 0; cook 0 errores y 21 advertencias de recursos anteriores. ZIP `Deliverables/TimeOut_Avance_18Nov2026.zip`, **737914216 bytes**, CRC completo aprobado. Prueba del ejecutable: menú, Nuevo juego, señal E/RB visible y rescate E que la oculta. Las pruebas detalladas de fijación, voz, tres recuperaciones y grietas son de PIE. Log resumido en `docs/validation/hostage-feedback-package-log.txt`.
- **Unknown / pendiente:** recorrido manual completo, aceptación del propietario, mando físico, otra PC, guardado/Continuar y modelos definitivos del equipo.


### Estado anterior del 15 de noviembre — antes de señal, voz, fijación y grietas

- Fecha: **2026-11-15**. Rama `codex/entrega-18nov-ia-oleadas`; commits locales autorizados, sin push solicitado. Entrega: 18 de noviembre.
- **Stated:** el propietario reportó huida excesiva del rehén en la segunda baliza y enemigos que se alejaban caminando de espaldas. Pidió refinar ambas IA, dar daño a todos los ataques y una punzada roja tenue al recibir daño; delegó el balance pendiente.
- **Verified:** gameplay Blueprint-only; tres Behavior Trees/Blackboards conservados. No se añadió Source ni plugin al proyecto. La herramienta nativa de edición permanece exclusivamente en Intermediate y se carga sólo con un argumento del editor.

### IA y refugios

- **Verified:** `BP_CombatZone` ya no fuerza una huida a `RefugePoint` antes de generar la oleada. `BTService_HostageSense` detecta amenazas y propone al Blackboard un refugio cuya ruta es completa, de hasta **1800 cm**, a ≤1600 cm del rehén y ≤1800 cm del jugador. Prioriza la longitud real de navegación. Si no existe una ruta segura local, espera y vuelve a evaluar; no elige un destino remoto.
- **Decision:** seguridad mínima del refugio: 600 cm del jugador y 950 cm de cada enemigo vivo. Se conserva visión de amenaza de 800 cm, la espera en refugio y la reanudación manual E/RB.
- **Verified:** cinco TargetPoints adicionales con tag `RefugioRehen`: `Refugio_Local_01_Izq` (-1000,-1500,0), `Refugio_Local_01_Der` (1000,-1500,0), `Refugio_Local_02_Norte` (-4300,-4322,0), `Refugio_Local_02_Oeste` (-4600,-4500,0), `Refugio_Local_02_Sur` (-4300,-5700,0). El servicio comprueba seguridad/ruta en ejecución; las marcas no son destinos obligatorios.
- **Verified / Decision:** el embestidor busca retirada mediante un abanico local de 420 cm (0/±45/±90 grados), ruta completa ≤650 cm, separación final ≥300 cm y preferencia por 550 cm del jugador. Camina a 400; termina al llegar a 90 cm o en 1.4 s, restaura velocidad 600 y recupera 0.8 s. Se conserva preparación 0.8 s, carga 900, contacto 6, objetivo comprometido y cooldown 2 s.
- **Verified:** `BP_ChargerController` inicializa objetivo/distancia antes de iniciar `BT_Charger`. La rama de persecución admite cualquier distancia >0 con objetivo válido para que el cooldown no desemboque en patrulla. La carga limpia el foco; locomoción orientada al movimiento en ambos enemigos, giro 540 grados/s.
- **Verified:** el orbitador conserva prioridad daño > defensa > ataque > órbita > patrulla y radio 180/banda 150–210. Se corrigió la multiplicación del vector de órbita (`Multiply_VectorFloat`). Dos tareas nativas RotateToFace se sustituyeron por `BTTask_FaceCombatTarget`, acción breve que termina en todos sus caminos; la espera nativa se bloqueaba al orientar la locomoción por movimiento. La tarea también precede la defensa. La orientación de ataque se fija explícitamente. Detección: orbitador 1500, embestidor 1800.
- **Verified:** `BT_EnemyIA` tiene tanto los NodeInstance del editor como Children de ejecución apuntando a la nueva tarea. Al modificarlo hay que mantener ambas representaciones. `finalize_orbiter_refinement.py` realiza ambas escrituras. No ejecutar las recetas antiguas de reconstrucción del árbol.

### Daño y presentación

- **Decision / Verified:** espada ligera **15/15/19/22**; martillo ligero **15/15**; los tres pesados de espada y el pesado del martillo causan **25 a ambos enemigos**. La inmunidad histórica del orbitador al pesado queda sustituida por esta petición. Salud enemiga 100 y contacto 6 conservados.
- **Verified:** `BP_PlayerEntrega` vuelve a enlazar WeaponHitbox una vez al iniciar y centraliza el daño en su manejador; el personaje padre y sus montajes/FX no se modificaron. Caché por animación/ataque evita duplicados, incluso ligeros; requiere enemigo vivo, distancia ≤300 cm y visión. Hitbox espada 45×45×90 de semiextensión; martillo conserva 35×45×145. La espada se configura también en el primer BeginPlay.
- **Decision / Verified:** ventanas suplementarias (segundos de montaje): H_attack_1 0.82–1.05; H_attack_2 0.28–0.75; H_attack_3 0.50–1.25; L_FA_4 0.18–0.65; HA_1 0.55–0.90; HA_2 0.16–0.50. Martillo pesado conserva Attack_3 0.252330–1.183353. Se limpia colisión/estado al interrumpir; los ligeros originales 1–3 mantienen sus notifies.
- **Verified:** `BP_HUD_Entrega` detecta descenso de vida real y dibuja `FX/T_DamageCorners` rojo tenue con pico alfa 0.30 y caída cuadrática en **0.38 s**. Otro golpe renueva la punzada; curarse no la dispara. El centro permanece transparente y el HUD se dibuja encima. Máscara procedural reproducible con `Tools/generate_damage_overlay.py`; captura `docs/validation/damage-pulse-preview.png`.
- **Verified:** se conserva misión de tres balizas, dos hordas 2×2, puertas de 50 con dos pesados de martillo mejorado, canalización de rehén 3 s, equipamiento automático, salud del rehén y condiciones de extracción/derrota. Ver historial para el circuito detallado.

### Verificación y continuidad

- **Verified:** evidencia nueva en `docs/validation/refinement-2026-11-15.json`; muestras completas de PIE en `Intermediate/inspect/*_assertions.json`. `verify_ai_refinement.py` observa la segunda zona y varios ciclos; `verify_orbiter_refinement.py` observa cierre de distancia/órbita/ataque; `verify_all_attack_windows.py` ejecuta entradas reales y comprueba 10 montajes contra solapamientos físicos; `verify_combat_damage.py` comprueba cantidades/duplicados; `verify_damage_pulse.py` comprueba golpe, renovación, caída y control negativo de curación.
- **Verified:** segunda zona: refugio alcanzado con ruta de 1099.7 cm, separación máxima del rehén 1037.3 cm y 12 ciclos de carga observados; enemigos a ≤640.3 cm, fracción de muestras móviles mirando hacia avance 1.0. Orbitador: se acercó hasta 167.3 cm, atacó y orbitó; después de 3 s, distancia máxima 280.7 cm, fracción móvil hacia avance 1.0. Pasaron los 10 montajes físicos, cantidades/duplicados, punzada/curación, regresión de misión y martillo físico/interrupción. Ocho informes del agente aprobados; compilación/cook final sin errores.
- **Verified:** son pruebas aisladas con teletransportes y controles de daño en memoria, no aceptación del propietario ni recorrido completo a pie. No marcar las pruebas antiguas como aceptación de estos cambios; sus valores de inmunidad eran históricos.
- **Continuidad:** generar `generate_hostage_graphs.py` → `generate_progression_graphs.py` → `generate_dialogue_hud.py` → `generate_ai_refinement.py`; instalar con `install_ai_refinement.py`, `finalize_orbiter_refinement.py`, `place_local_refuges.py` y `validate_refinement_assets.py`. No instalar el BP_Hostage sencillo emitido por la receta de escolta: la receta de progresión debe generarse después para conservar vida/canalización.
- **Verified:** Win64 Development reconstruido: BUILD SUCCESSFUL / ExitCode 0; cook 0 errores y 21 advertencias. ZIP actualizado `Deliverables/TimeOut_Avance_18Nov2026.zip`, **737829582 bytes**, CRC completo aprobado. Prueba nativa: menú → Nuevo juego → Nivel_Entrega, rescate E, HUD y descenso de vida con la tecla de depuración existente. Las pruebas detalladas de IA/10 ataques/puertas son de PIE. Resumen del empaquetado en `docs/validation/refinement-package-log.txt`.
- **Unknown / pendiente:** aceptación manual del propietario, recorrido completo, mando físico, rendimiento en otra PC, guardado completo/Continuar y modelos definitivos del equipo.



### Estado anterior del 15 de noviembre — antes de refugios locales y daño completo

- Fecha: **2026-11-15**, entrega miércoles **18 de noviembre de 2026**. Rama `codex/entrega-18nov-ia-oleadas`. Commits locales autorizados; no push solicitado. Base anterior `065a54d` (diálogo/audio), `6cb95de` (cámara/paredes), `d641200` (enemigos/oleadas).
- **Stated, petición nueva:** puertas destruibles hechas a medida; sólo el rehén activa balizas después de la horda; vida del rehén visible; equipar automáticamente el martillo con partículas de mejora y habilitar la destrucción de la puerta correspondiente.
- **Verified:** todo el gameplay sigue en Blueprints. No se añadió módulo nativo ni plugin al proyecto o al ejecutable. Blender generó el kit propio en `Tools/ArtSource/Progression`; el generador está en `Tools/Blender/build_progression_assets.py`.

### Circuito actual de la misión

1. E / RB rescata al rehén o lo vuelve a llamar desde el refugio. El jugador ya no activa balizas directamente.
2. Entrar en una zona con el rehén siguiéndolo a ≤600 cm genera dos oleadas de dos enemigos. Zona 1: orbitadores. Zona 2: embestidores. Intermedio 3 s; las zonas no repiten.
3. Al despejar, recuperar al rehén con E / RB y llevarlo cerca de la baliza. Dentro de 650 cm, el director escribe disponibilidad en Blackboard. `BT_Hostage` decide ir al punto de aproximación y canalizar durante 3 s. Prioridad: huir > baliza > esperar > seguir > idle.
4. Amenaza visible interrumpe la canalización, reinicia su progreso y mantiene baliza/puerta bloqueadas. La huida y reanudación manual se conservan.
5. `BP_BeaconEntrega.CompleteActivation` comprueba orden, horda despejada, rehén vivo/rescatado, proximidad y canalización completa. Incrementa Paso una sola vez, enciende la baliza y desbloquea sólo su puerta.
6. `BP_PlayerEntrega.GrantHammerUpgrade` cancela el ataque activo, apaga colisión, equipa martillo (`bIsHammerEquipped=true`, `bIsSwordEquipped=false`), ajusta su caja de impacto y emite `NS_HammerUpgrade`/`SW_Upgrade`.
7. Cada puerta tiene 50 de vida y recibe 25 por golpe pesado del martillo mejorado, una vez por ataque. Ligero, espada, martillo sin mejora y puertas aún selladas reciben 0. Al segundo golpe desaparece el panel, aparecen cuatro escombros físicos, partículas y sonido; el marco permanece. Los escombros ignoran Pawn/cámara/navegación y duran 4 s.
8. La tercera baliza exige haber despejado ambas hordas mediante el orden de Paso; no se inventó una tercera horda. Romper la última puerta permite llegar a la extracción azul con el rehén. Paso 4 gana; 5 es muerte del jugador y 6, muerte del rehén. R reintenta; Enter vuelve al menú.

### Puertas, navegación y presentación

- **Verified:** paneles ajustados a 258×256, 344×333 y 600×350 cm; centros aproximados `(0,-4021,0)`, `(-21,-6261,0)` y `(0,-10200,0)`. Muros visibles de piedra/refuerzo metálico cruzan las rutas laterales del suelo, dejando sólo la abertura de la puerta. `BP_CombatZone` ya no abre ni oculta barreras.
- **Verified:** NavMesh Dynamic. Las pruebas contrastan las rutas con cada puerta cerrada y después de romperla. Las balizas tienen `ApproachPoint` a 180 cm hacia +Y: pedir un MoveTo al centro sólido del cilindro daba una ruta inválida. `BeaconTarget` es el punto alcanzable; `ActiveBeacon` es la baliza que usa la tarea.
- **Verified:** HUD negro/blanco de texto progresivo conservado, sin TextRender. Añade vida numérica/barra del rehén (roja al ≤30%), progreso de canalización y explicación de la mejora/puerta. Sonidos propios de golpe, rotura y mejora, además de los nueve anteriores. Los FX del equipo de ataque/daño no se modificaron.
- Se conserva el aspecto Warrior original de ambos enemigos, materiales/escala 1, salud 100, ligero 15/15/19, pesado 25 sólo al embestidor y contacto 6. Cámara: sonda 24, brazo 350, pivote Z55, sin lag de posición; colisiones por prismas de las paredes originales.

### Vida, objetivos y ciclos de ataque

- **Verified:** rehén con 100 de vida, sin fuego amigo y gracia compartida de 0.8 s entre impactos. Ambos enemigos pueden elegirlo si está rescatado/vivo/visible, a ≤650 cm y al menos 150 cm más cerca que el jugador. El jugador dentro de 220 cm tiene prioridad para poder interceptarlos.
- El servicio escribe `CombatTarget`; el árbol conserva la decisión de orbitar/atacar/embestir. La carga fija `ChargeVictim` al terminar la preparación, sin retargetear el contacto a otro actor a mitad del movimiento.
- **Verified:** se corrigió en el hijo `BP_PlayerEntrega` un problema heredado: el pesado no tenía conectados los callbacks Enable/DisableHitbox y el hitbox permanecía sobre la espada guardada. Ahora sigue el arma equipada; conserva/restaura el transform original de la espada. Para el pesado del martillo usa la ventana existente de `Attack_3_Montage` (0.252330–1.183353 s) y limpia colisión/estado al interrumpirse. Los montajes originales del equipo no se editaron.

### Pruebas del agente y continuidad

- Evidencia de esta entrega en `docs/validation/progression-2026-11-15.json`. Pruebas: `verify_progression.py`, `verify_hostage_combat.py`, `verify_beacon_interrupt.py`, `verify_real_hammer.py`. Se usan teletransportes/daño de prueba sólo en PIE para aislar condiciones; no equivalen a una partida completa a pie ni a aceptación del propietario.
- `generate_progression_graphs.py` es la fuente actual de los gráficos. Genera T3D para revisar/pegar en los EventGraphs. Orden: puerta/escombros → jugador → baliza → rehén/tarea → director/HUD → servicios/tareas enemigas. `prepare_progression.py` prepara campos/arte; `finalize_progression_tree.py` resuelve claves y puntos de aproximación; `place_progression.py` coloca el kit. No volver a ejecutar las recetas iniciales que recrean todo el proyecto.
- La utilidad nativa usada localmente para editar está exclusivamente bajo `Intermediate` (ignorado); no es una dependencia de los assets ni del juego. No añadirla a `Terreno.uproject`.
- **Verified:** reconstrucción Win64 Development terminada, BUILD SUCCESSFUL / ExitCode 0; cook con 0 errores y 21 advertencias. ZIP actualizado: `Deliverables/TimeOut_Avance_18Nov2026.zip`, **737832544 bytes**, CRC completo aprobado. En el ejecutable se comprobó canalización real del rehén, Paso 1, martillo equipado/espada desactivada y dos entradas de ataque pesado mediante Enhanced Input: puerta 50 → 25 → 0 y destruida; las otras permanecieron en 50/sin destruir. La prueba aisló la primera baliza marcando hordas despejadas sólo en memoria y teletransportando actores; no sustituye el recorrido completo. Captura nativa en `docs/validation/progression-preview.png`.
- Para reconstruir: guardar todo, cerrar editor y ejecutar `Tools/Build-Delivery.ps1`; `Tools/Archive-Delivery.py` prepara el ZIP excluyendo símbolos y Saved. Evidencia final en `docs/validation/progression-2026-11-15.json`.
- **Unknown / pendiente del equipo:** modelo definitivo de baliza y coordinación de partículas de Dany. Las balizas físicas continúan provisionales. Guardado completo/Continuar, mando físico, rendimiento en otra PC y recorrido manual completo siguen pendientes. Nuevo juego y reinicio permiten jugar desde cero.



### Estado anterior del 15 de noviembre — antes de puertas destruibles

- Fecha: **2026-11-15**. Entrega: **miércoles 18 de noviembre de 2026**.
- **Stated:** el propietario autorizó trabajo autónomo, priorizó segundo enemigo y oleadas, pidió refinar IA/animaciones, rama nueva y commits. Rama: `codex/entrega-18nov-ia-oleadas`. El avance anterior quedó en `3383b43`; IA, oleadas y animaciones en `d641200`; el refinamiento posterior de cámara/paredes, aspecto y señales corresponde al commit actual. No se pidió push. `origin/main` seguía en `68eb221` tras fetch al comenzar este avance.
- **Verified:** `/Game/ThirdPerson/Maps/Nivel_Entrega` contiene los cuatro sectores de Ian de `Escenario.zip`, suelo, límites, navegación, rehén, tres balizas y extracción. Los sectores usan escala 2 por el tamaño original de sus puertas. Las cuatro instancias enemigas fijas se sustituyeron por encuentros de oleadas.
- **Verified:** Nuevo juego abre este mapa; el juego inicia en `MainMenuLevel`. `BP_GameMode_Menu` evita el personaje/barra detrás del menú. Continuar permanece deshabilitado: no hay persistencia de esta misión.

### Combate y animación

- **Verified:** `BP_BaseEnemy` conserva salud 100 y sólo acepta ligero por el camino original del personaje: **15 / 15 / 19**. `BTTask_Attack` mantiene la tarea activa durante el golpe; el impacto ocurre a 0.45 s, exige distancia ≤220 y visión, aplica 6 una vez y finaliza a 1.3 s. `ReceiveAbortAI` cancela el ataque y su montaje.
- **Verified:** el decorador de daño de `BT_EnemyIA` era Self y no interrumpía ramas inferiores. Ahora es **Both**. Se restauraron los tiempos documentados: ataque 3 s y defensa 6 s. Se conservan órbita 180, banda 150–210, defensa de 1.5 s y aturdimiento de 0.6 s. Las tres líneas de Print del orbitador se conservan.
- **Verified:** `BP_ChargerEnemy` hereda la salud/muerte del enemigo base, pero usa `BP_ChargerController`, `BB_Charger` y **su propio `BT_Charger`**. El controlador arranca el árbol en On Possess para que exista un Pawn antes de ejecutar tareas.
- **Verified:** prioridad del árbol nuevo: daño → carga → retirada/recuperación → crear distancia si está demasiado cerca → preparar → perseguir → patrullar. El servicio sólo escribe distancia/objetivo cada 0.2 s. No usa la órbita ni los Print propios del orbitador.
- **Decision de ajuste:** detección 1800; preparar entre 250 y 700 durante 0.8 s; carga de 900 cm/s hacia una posición comprometida del jugador, hasta 1 s o contacto a 180 cm; contacto 6 una vez con visión. Retirada hacia un TargetPoint navegable, a ≥1100 del jugador y en dirección contraria, hasta llegar a distancia 1000 o timeout 4 s; espera 2 s antes de recuperarse. Persecución acepta 450 para entrar con margen en el rango de preparación. El timeout evita quedarse bloqueado si el escenario impide la retirada.
- **Verified:** `BP_PlayerEntrega` hereda del personaje original. Su manejador adicional de WeaponHitbox acepta sólo pesado contra el embestidor, con caché por golpe; conserva el manejador ligero original. **Decision:** daño pesado 25. El orbitador sigue inmune al pesado. No se añadió otro sistema de salud.
- **Verified / elección expresa del propietario:** ambos enemigos recuperaron `SK_SciFiWarrior02`, materiales originales y escala 1. Se retiraron armadura naranja y aumento 1.08. Conservan `ABP_EnemyEntrega` (locomoción enlazada → DefaultSlot → salida); PIE confirma instancia animada, movimiento de huesos y montajes con la malla restaurada. La sustitución por Trooper del avance anterior queda revertida.
- **Verified:** montajes propios `AM_EnemyAttack_Entrega`, `AM_EnemyHit_Entrega`, `AM_EnemyDeath_Entrega`. Se usa `enemigo_lastimado1`, compatible con Trooper; `enemigo_lastimado` corresponde a Manny. El AnimBP propio usa Ignore Root Motion para que el árbol controle la traslación. La reacción dura 0.6 s; muerte reproduce 2.433 s, detiene árbol/movimiento/colisión y elimina el actor a los 3 s. Sin auto blend out en muerte para evitar levantarse al acabar.
- **Verified:** no se editaron las animaciones ni los efectos originales de los compañeros; los montajes y el AnimBP son copias propias de entrega.

### Paredes, cámara y señales — refinamiento solicitado

- **Stated:** recuperar aspecto anterior; arreglar cámara contra paredes y atasco del jugador, señal de rescate dentro del juego, explicar qué activa enemigos y bajar su daño.
- **Verified:** `ContactDamage` editable en BP_BaseEnemy vale **6** (antes 10) y alimenta ResolveAttack y BTTask_ChargerCharge. Se conservan salud 100, combo 15/15/19 y pesado 25.
- **Verified:** los cuatro sectores de Ian usan SimpleAndComplex con prismas convexos extruidos por cara y doble cara para trazas. Se conservan huecos: navegación alcanza las tres balizas y extracción. Receta `build_precise_wall_collision.py`. Una descomposición convexa global cerraba algunas puertas; no repetirla.
- **Verified:** BP_PlayerEntrega llama al BeginPlay del padre y configura CameraBoom: brazo 350 cm, sonda 24 cm, pivote Z55, colisión activa, sin retardo de posición y retardo de rotación 18. Rehén y enemigos ignoran Camera; paredes la bloquean.
- **Verified:** `verify_wall_camera.py` sostuvo movimiento hacia tres paredes por 3 s y retroceso por 1 s: todas detuvieron al jugador y permitieron escapar >427 cm. Cámara se retrajo a 40 cm y recuperó 350 al girar hacia espacio libre. Es una muestra reproducible, no prueba de cada esquina.
- **Stated / Verified, refinamiento posterior:** el propietario rechazó el texto flotante y pidió un recuadro tipo Undertale y audio. Se retiraron TODOS los TextRenderActor del nivel (incluidas etiquetas de balizas), indicadores de rehén/zonas y ocho líneas de suelo. Los assets antiguos quedan sin instancias; place_delivery_guidance.py impide restaurarlos accidentalmente.
- **Verified:** BP_HUD_Entrega dibuja un recuadro inferior negro/blanco, Consolas precalculada en F_DialogueMono, 42 caracteres/s, ENTER revela y luego cierra; mensajes informativos desaparecen tras lectura +4.5 s. Prompts de interacción persisten hasta actuar o cerrar. Lee director, Blackboard, distancia, fase y oleada sin cambiar gameplay; marcador pequeño arriba a la derecha. Resultados conservan R/Enter para reiniciar/menú. Fuentes: generate_dialogue_hud.py, create_dialogue_font.py y prepare_dialogue_presentation.py. Nueve sonidos originales bajo ThirdPerson/Audio (generador y WAV en Tools): texto suave con variación de tono, avisos de contexto, rescate, daño, victoria/derrota y ambiente en bucle sin persistir entre niveles.

### Oleadas y misión

- **Verified:** `BP_CombatZone` combina la condición de escolta y el control de combate; no hace falta un segundo volumen superpuesto llamado `BP_HostageSpawnZone`.
- `Zona_01_Orbitadores`: centro (0, -2700, 150), extensión (1300, 1000, 250), clase BP_BaseEnemy; refugio `Refugio_Rehen_01`.
- `Zona_02_Embestidores`: centro (-3200, -4800, 150), extensión (1000, 900, 250), clase BP_ChargerEnemy; refugio `Refugio_Rehen_04`.
- **Verified:** entrar solo no genera enemigos. Entrar con rehén acompañando a ≤600 cm inicia dos oleadas de dos enemigos. El rehén recibe destino de huida fuera del volumen. La barrera se activa mientras haya combate y durante el intermedio de 3 s; al morir el último enemigo de la segunda oleada, se abre y la zona queda completada para toda la partida. Reentrar no repite enemigos. La segunda oleada no exige volver a traer al rehén.
- **Verified:** se cuentan enemigos válidos con `bIsDead=false`; los cadáveres no retrasan la siguiente oleada. SpawnPoints y refugios están sobre navegación. Las barreras se ocultan y no colisionan antes/después del encuentro.
- **Verified:** baliza 1 exige zona 1 completada y baliza 2 exige zona 2 completada. Se activan 1 → 2 → 3 una vez con E/RB. El HUD muestra objetivo, estado del rehén, estado de zona, oleada y vivos. Las balizas siguen siendo cilindros naranja/verde hasta recibir el modelo definitivo.
- **Verified:** extracción exige las tres balizas, jugador a ≤300 de la salida, rehén a ≤600 y acompañando. Ganar/morir pausa. R reinicia mapa, salud, escolta, oleadas, barreras y balizas; Enter vuelve al menú al terminar.

### Escolta conservada

- `BP_Hostage`, controlador, `BT_Hostage`/`BB_Hostage`, servicio, tarea y `ABP_Hostage` están en `/Game/ThirdPerson/Blueprints/Aliado/`. El original `ABP_Aliado` permanece intacto.
- El árbol decide huir → esperar → seguir → idle; el servicio escribe Blackboard. E/RB interactúa a 400 cm. Sigue a 400 cm/s al superar 500 cm y termina MoveTo a 300. Ve amenazas vivas con LOS hasta 800 cm; busca uno de 13 refugios alcanzables a ≥1000 del jugador y ≥1200 de enemigos vivos. Al llegar espera **otra interacción**, no vuelve automáticamente.
- `PlayerActor` de BB_Hostage debe ser Object con BaseClass Actor; el decorador de distancia de seguimiento usa Lower Priority. El rehén es invulnerable y usa maniquí provisional.

### Pruebas del agente, no aceptación del propietario

- Evidencia resumida en `docs/validation/combat-2026-11-15.json`. Los observadores de PIE usan callbacks y escriben resultados sin bloquear el editor.
- Manejadores reales de daño: ligero 15/15/19 en ambos enemigos; pesado 25 sólo en embestidor; solapamiento pesado repetido e inactivo no añaden daño. Se invocaron los manejadores para aislar condiciones; falta aceptación manual de combos/controlador físico.
- Árbol real del embestidor: observadas preparación, carga y retirada, velocidad máxima 900 y distancia de retirada >1000.
- Ciclo real del orbitador: interrupción durante preparación causó 0 daño; golpe completo quitó 10 a los 0.446 s y terminó a 1.3 s; muerte detuvo árbol y colisión, reprodujo montaje y eliminó cadáver.
- Ambas zonas: entrar sin rehén → 0 spawns; entrar acompañado → 2 + 2; intermedios de aproximadamente 3.0 s, muerte deja de contar inmediatamente, barrera se abre y reentrada genera 0 enemigos adicionales.
- Flujo con E real y teletransportes de aislamiento: baliza bloqueada antes de completar zona, activación ordenada tras oleadas, salida solo mantiene Paso 3, recuperar rehén con E en salida produce Paso 4 y pausa; R vuelve a salud 100, Paso 0, ambas zonas sin iniciar y todas las balizas pendientes.
- Pruebas anteriores de escolta: seguimiento, huida ante enemigo visible, espera y reanudación sólo con E. No equivalen a una partida completa recorrida a mano.

- **Verified, presentación nueva:** progresión de texto, Enter revela/cierra, rescate cambia diálogo, auto ocultado, prompt para reanudar y ambiente reproduciéndose. Ambas oleadas actualizan avisos y conservan 2x2/sin respawn. Texto de victoria funciona pausado; teclas físicas R reinician y Enter conserva regreso al menú. Evidencia en validation/presentation-2026-11-15.json.

### Paquete y pendientes

- **Verified:** paquete actualizado `Deliverables/Windows/Terreno.exe` y `Deliverables/TimeOut_Avance_18Nov2026.zip` (**737270129 bytes**, CRC completo aprobado). Win64 Development, BUILD SUCCESSFUL, ExitCode 0, cook 0 errores/34 advertencias de recursos anteriores. Prueba del ejecutable actualizado: menú, Nuevo juego, escenario iluminado, HUD, recuadro de rescate/interacción E y audio. Capturas internas de Unreal conservan la frase completa tras >80 s; el volcado del ejecutable conserva FullText=VisibleText y 49 caracteres. La captura automatizada de ventana de Windows a veces omitía glifos; usar F9 (Shot showui) para evidencia visual. Vista en validation/dialogue-preview.png. La prueba completa de oleadas/animaciones se hizo en PIE. `Tools/Delivery-README.txt` genera el LEEME del paquete.
- Iluminación se mantiene corregida sólo en el nivel nuevo: PostProcess GI None, Skylight sin sombras y sectores sin contribución DF. No modificar los materiales antiguos de Landscape por las advertencias de SM5.
- Pendiente del equipo: modelo final de baliza y del aliado; coordinar partículas/notifies con Dany, sin trabajarlos simultáneamente.
- Pendiente de aceptación: recorrido completo sin teletransportes, balance de ocho enemigos, mando físico y rendimiento en otra computadora. Persistencia completa de misión y supervivencia posterior a extracción no están implementadas.

### Herramientas y continuidad

- `run.py` ejecuta Python de editor y ahora retorna código distinto de cero si falla. Los assets guardados son la entrega; no se ejecuta Python durante el juego empaquetado.
- `generate_combat_graphs.py`, `generate_charger_tree.py`, `generate_wave_graphs.py` y `generate_delivery_graphs.py` son fuentes revisables de portapapeles Blueprint. Tras pegar, compilar/exportar y usar `inspect_blueprint_active.py`: los T3D pueden retener objetos huérfanos con errores antiguos; contar sólo Nodes del gráfico activo.
- No invocar directamente en un nodo genérico funciones BlueprintInternalUseOnly de spawn: se filtran al pegar. Se usa el nodo nativo SpawnActorFromClass. Tampoco pegar llamadas a eventos propios antes de que exista su firma; la zona comparte las conexiones de ejecución de generación.
- `create_charger_wave_assets.py` y `place_delivery_encounters.py` son recetas iniciales protegidas: no repetir sobre los assets/nivel terminado. `finalize_charger_runtime.py`, `finalize_combat_delivery.py` y `finalize_orbiter_tree.py` aplican defaults propios.
- Pruebas: `verify_combat_damage.py`, `verify_charger_cycle.py`, `verify_delivery_waves.py`, `verify_enemy_animation_lifecycle.py`, `verify_wall_camera.py`, siempre en PIE; la de oleadas requiere zonas recién iniciadas. `playtest_combat_waves.py` es diagnóstico, no código de gameplay.
- Para empaquetar, guardar todo, detener PIE y cerrar Unreal (Live Coding bloquea UAT). Ejecutar `Tools/Build-Delivery.ps1` y después `python Tools/Archive-Delivery.py`. Deliverables e Intermediate están ignorados por Git.


### Avance anterior del 15 de noviembre — antes del segundo enemigo

- Fecha: **2026-11-15**. Entrega indicada por el propietario: **miércoles 18 de noviembre de 2026**.
- **Stated:** el propietario pidió avanzar de forma autónoma, importar el escenario de Ian y priorizar la escolta del rehén. Las instrucciones antiguas que pedían que el propietario hiciera cada clic ya no describen este encargo.
- **Verified:** nuevo nivel guardado `/Game/ThirdPerson/Maps/Nivel_Entrega`. Usa los cuatro sectores de `Downloads/Escenario.zip`, suelo, límites, navegación, cuatro instancias del enemigo existente, tres balizas provisionales y una salida azul. Las puertas del FBX original medían aproximadamente 1.29 m; los sectores se colocaron a escala uniforme 2 para permitir el paso de las cápsulas.
- **Verified:** `/Game/Menu/Menu_Inicio` → Nuevo juego abre el nivel nuevo. `MainMenuLevel` usa `BP_GameMode_Menu` para evitar el personaje y su barra de vida detrás del menú. El mapa inicial del juego es el menú; el mapa inicial del editor es `Nivel_Entrega`.
- **Verified:** la misión usa `BP_DirectorEntrega`, `BP_HUD_Entrega` y `BP_GameMode_Entrega` bajo `/Game/ThirdPerson/Blueprints/Entrega`. Activa balizas 1 → 2 → 3 una sola vez, luego exige jugador y rehén juntos en extracción. La muerte del jugador produce derrota. **R** reinicia y **Enter** vuelve al menú después de ganar o morir.
- **Verified:** interacción con **E** o **RB/R1** cerca del rehén o la baliza. RB se eligió porque X/cuadrado ya está asignado al ataque ligero; no se cambió el mapa de entradas del personaje.
- **Verified:** `/Game/ThirdPerson/Blueprints/Aliado/` contiene `BP_Hostage`, `BP_HostageController`, `BB_Hostage`, `BT_Hostage`, `BTService_HostageSense`, `BTTask_HostageArrive` y `ABP_Hostage`. El original `ABP_Aliado` del compañero permanece intacto. La copia añade actualización de velocidad para sus transiciones idle/caminar.
- **Verified:** la decisión de movimiento del rehén se ejecuta en `BT_Hostage`: huir → esperar interacción → seguir → idle. El servicio sólo actualiza Blackboard; las tareas MoveTo ejecutan el movimiento. `Interactuar` escribe el estado tras comprobar distancia y ausencia de amenaza. El director recibe las teclas porque un Pawn controlado por IA no recibe las entradas del jugador directamente.
- **Decision del agente bajo la autonomía concedida:** interacción 400 cm; iniciar seguimiento a más de 500 cm y terminar MoveTo a 300 cm; velocidad 400 cm/s; enemigo vivo visible hasta 800 cm; refugio navegable a ≥1000 cm del jugador y ≥1200 cm de todos los enemigos vivos. Son ajustes iniciales, no decisiones expresas del propietario. El servicio revisa cada 0.5 s y elige el refugio alcanzable más cercano entre 13 TargetPoints etiquetados `RefugioRehen`.
- **Verified:** `Rehen_Entrega` empieza cerca del jugador. Si ve una amenaza después de ser rescatado, huye; al llegar espera. Acercarse sin interactuar **no** reanuda la escolta. Esto sustituye el requisito antiguo de reanudación automática a 400 cm.
- **Verified:** `PlayerActor` en `BB_Hostage` debe ser Object con **BaseClass Actor**. Con UObject, el filtro de MoveTo vacía la selección al guardar. El decorador de distancia de seguimiento usa **Lower Priority**, para que la marcha llegue hasta 300 cm sin abortarse a 500 cm.
- **Verified:** no se editaron el combate, los montajes ni las partículas del equipo. El modelo definitivo de baliza está pendiente de la subida del compañero; los cilindros naranja/verde ya permiten jugar.
- **Verified:** Continuar se deshabilitó en el menú de esta entrega porque el guardado existente no persiste balizas/estado de escolta y apuntaba al mapa anterior. Nuevo juego funciona. No afirmar soporte de guardado de esta misión.
- **Verified:** todos los paquetes estaban guardados antes de cerrar Unreal para UAT. El primer empaquetado se detuvo por Live Coding activo; el empaquetado final terminó **BUILD SUCCESSFUL**, ExitCode 0, configuración Win64 Development. Cook final: 0 errores y 20 advertencias de recursos existentes; los intentos anteriores también advirtieron sobre poses de Manny obsoletas y el material Landscape del mapa anterior al cocinar SM5. No se modificaron esos recursos ajenos a la misión nueva.
- **Verified:** paquete jugable `Deliverables/Windows/Terreno.exe`; ZIP `Deliverables/TimeOut_Avance_18Nov2026.zip` (736346100 bytes), con verificación CRC completa aprobada. Incluye `LEEME.txt`; omite símbolos de depuración y datos locales de guardado. Conservar la carpeta Windows completa al ejecutar.
- **Verified:** prueba fuera del editor: menú, Nuevo juego, nivel nuevo, HUD E/RB, interacción E y cambio a estado de escolta. Continuar aparece deshabilitado. La primera prueba reveló paredes negras por iluminación indirecta; se corrigió **sólo en Nivel_Entrega** con `Iluminacion_Entrega` (PostProcess unbound, GI dinámica None), sin sombras de Skylight y sin contribución DF de los cuatro sectores; las sombras del sol permanecen. El ejecutable final se volvió a abrir sin comandos de diagnóstico y mostró las texturas/iluminación correctas.
- Sin commit ni push. Los nuevos `.uasset` y `.umap` están pendientes de añadir a Git por el propietario.

### Cómo probar lo nuevo

1. Abrir `Terreno.uproject` con UE 5.6. El editor abre `Nivel_Entrega`.
2. Play: acercarse al maniquí aliado del inicio y pulsar E; caminar y observar el seguimiento.
3. Acercarse a un enemigo: el rehén debe buscar un refugio. Ir a buscarlo, despejar amenazas y pulsar E cerca para recuperarlo.
4. Activar las balizas numeradas en orden y llevar al rehén a la salida azul. El HUD muestra el objetivo y el estado de la escolta.
5. Para comprobar el flujo de menú, abrir `MainMenuLevel`, Play y Nuevo juego.

### Pruebas del agente, no aceptación del propietario

- **Verified, PIE 2026-11-15:** E rescata al aliado; sigue a 400 cm/s, la variable `speed` de `ABP_Hostage` también vale aproximadamente 400 al moverse y se detiene a unos 297 cm del jugador.
- **Verified, PIE:** amenaza visible a 600 cm activa huida; el aliado recorre el NavMesh, llega a ≤80 cm del refugio y queda `bWaiting=true`, `bMustFlee=false`, `bAccompanying=false`. Se observó espera con el jugador cerca, y reanudación sólo después de E.
- **Verified, PIE:** baliza lejana y baliza fuera de orden no avanzan el objetivo; cada activación correcta cambia a verde; repetir E no vuelve a avanzar. Extracción anticipada no gana.
- **Verified, PIE final de extracción:** con las tres balizas activas, el jugador solo en salida quedó en Paso 3 sin pausa. Llevar al aliado, interactuar y estar ambos en la salida produjo Paso 4 y pausa. Se usaron teletransportes de prueba para aislar condiciones; no equivalen a una partida completa recorrida a mano.
- **Verified, PIE:** daño real de 100 a través de GameplayStatics produce salud 0, Paso 5 y pausa. R reinicia balizas/salud; Enter retorna al menú. Los enemigos existentes se movieron y quitaron 10 de salud por golpe.
- **Verified, PIE:** Nuevo juego abre `Nivel_Entrega`, sin advertencia de iluminación pendiente después de pasar las luces a Movable. El aliado responde a E después de entrar desde el menú.
- **Unknown:** validación con mando físico, partida completa sin teletransportes, aceptación del propietario y rendimiento en otra computadora.

### Pendientes inmediatos

- Integrar el modelo final de baliza cuando el compañero lo suba; conservar orden, referencias del director y colores de activación.
- Coordinar con Dany las partículas/notifies de ataque y daño. No trabajarlos simultáneamente.
- Recorrer la misión completa y ajustar refugios/población enemiga si la dificultad lo requiere. El rehén es invulnerable y utiliza el maniquí provisional.
- El segundo enemigo de la rúbrica (charger), las zonas de oleadas/bloqueo y la persistencia completa de misión siguen pendientes; no se presentaron como terminados.

### Herramientas y precauciones

- `python Tools/UnrealPython/run.py Tools/UnrealPython/ping.py` comprueba el editor remoto. `check_delivery_routes.py` valida caminos; `playtest_hostage.py` y `playtest_delivery.py` actúan sólo sobre PIE mediante archivos JSON en `Intermediate/inspect`.
- `generate_delivery_graphs.py`, `generate_hostage_graphs.py`, `generate_hostage_tree.py` y `generate_hostage_animation.py` generan texto de portapapeles revisable. Se pega en el gráfico correspondiente mediante la UI y después se compila/exporta. No se ejecuta Python durante el juego empaquetado.
- Los scripts de importación/creación son recetas de la construcción inicial; **no volver a ejecutar toda la secuencia sobre el nivel terminado**. `resize_delivery_level.py` tiene una protección contra aplicación doble. Los assets guardados son la entrega principal.
- Exportaciones y registros están bajo `Intermediate/inspect`; UAT genera paquetes locales bajo `Deliverables` (ignorado por Git).
- Reconstrucción del paquete: guardar y cerrar Unreal, ejecutar `powershell -NoProfile -File Tools/Build-Delivery.ps1`; después `python Tools/Archive-Delivery.py`. El log de compilación queda en `Deliverables/build.log`, la prueba final en `Deliverables/package-smoke-final.log`. Actualizar el ZIP después de cambiar assets; el ZIP actual corresponde al último paquete probado.



### Handoff anterior — 2026-10-21

- Date: 2026-10-21
- Branch: `main`, same commit as `feat/ai`. `BP_ThirdPersonCharacter` keeps the AI wiring and the weapon graph. Do not replace it with the menu zip's copy.
- Menu widgets from the partner zip (UE 5.4) are in `Content/Menu` (`/Game/Menu/...`). `MainMenuLevel` now opens `/Game/Menu/Menu_Inicio`. `DefaultEngine.ini` sets `GameInstanceClass` to the existing `BP_GameInstance`. The old widgets under `Content/LevelMenu/Menu` are still there. Pause on **P** is not on this player Blueprint yet.
- `hammer` is a child of the character mesh, Parent Socket `HammerSocket` (bone `hand_r` on `SK_SciFITrooper_Man_03`). Component location and rotation are 0. Visible is off, so it starts hidden. Hidden in Game is off, because the Set Visibility nodes only change the Visible flag.
- Keys in `IMC_Default`: `Y` is `IA_SwitchToSword`, `T` is `IA_SwitchToHammer`. `Y` shows the hammer and hides the sword. `T` shows the sword and hides the hammer. The visibility pins are the opposite of the event names.
- Reference copy of `main` before the merge: worktree `../PIA_Optimizacion_main`.
- Weapon graph exported 2026-10-21. Dirty packages were none. Both events fire on **Started**, and the False pin of each Branch is empty. A few unused nodes remain (an unwired Widget Set Visibility, an unwired NOT, and an unwired Set `Weapon`); they are not on the exec chain.
  - `IA_SwitchToSword`, if `bIsSwordEquipped` is false: Set Visibility `hammer` true → Set Visibility `Weapon` false → `bIsSwordEquipped` true → `bIsHammerEquipped` false. Propagate to Children off.
  - `IA_SwitchToHammer`, if `bIsHammerEquipped` is false: Set Visibility `hammer` false → Set Visibility `Weapon` true → `bIsSwordEquipped` false → `bIsHammerEquipped` true.
  - The visibility pins are the opposite of the event names. Confirm with the author before changing them.
- `main` is no longer the untouched original. The AI reference for "how it was before" remains `7198fa9`.
- Only the owner commits. Do not push this merge unless the owner asks.
- Area: AI 1 orbiter. Its movement works. Combat integration and cleanup are still open.
- Editor: Unreal Engine 5.6.1, Spanish UI, project `Terreno.uproject`, map `ThirdPersonMap`.

### TL;DR

On 2026-10-14 the owner resolved both open decisions: orbit at 180 (band 150–210) and light damage 25. On 2026-10-18 the owner replaced the flat 25 with combo damage **15 / 15 / 19** (swings 1 and 2, then the finisher). That Select is saved, and `FA_1_Montage` now has the hit window. Step 0, Step 0b, and the light hitbox switch are saved. Agent PIE after Step 0b showed both enemies inside 150–210 (distances 150–170), orbit points moving between samples, and `Enemigo: va a atacar` about every 3 seconds. The remaining AI 1 work is the owner's PIE checks. The player damage wire is saved. The owner finished the defend accent and the Roam debug cleanup on 2026-10-14 and asked not to play-test either. AI 2 and AI 3 have not started.

### What fixed movement (read this before touching any tree)

`BTTask_Attack` sat directly on the root Selector with a **Force Success** decorator. Force Success turns *any* result into success, including the result of its sibling Blackboard decorator failing. A Selector stops at the first child that succeeds, so every pass through the tree ended at Attack, and Orbit and Roam never ran. The enemy only rotated (the Defend branch faces the player). Removing Force Success fixed it.

Rule: never put Force Success on a direct child of a Selector. See the pitfalls list in `GOVERNANCE.md`.

### Verified in agent PIE on 2026-10-14

These were run through `Tools/UnrealPython/` (see `GOVERNANCE.md` → Agent tooling).

- Roam: with the player at spawn (about 3500 units away), both enemies walked (path status MOVING, speed up to 600), then stood for the Wait. `TargetActor` = None, `DistanceToTarget` = 100000, `DetectionRadius` = 1500.
- Orbit: the player was teleported 450 units from enemy 0. Over 30 seconds the enemy stayed 387–719 units away (mostly 387–464). Its position and `OrbitLocation` kept changing around the player. It never touched the capsule.
- Defend: `Enemigo: se esta defendiendo` printed about every 8–10 seconds (6 s cooldown + 1.5 s task). The task now finishes.
- Attack: `Enemigo: va a atacar` printed once when the distance briefly dropped to 220 or less.
- No `Accessed None` errors in `Saved/Logs/Terreno.log`.
- Hit stun is not tested. Nothing sets `bReceivingDamage` yet (that is AI1-03).

### Saved asset state (exported 2026-10-14, no dirty packages)

`BT_EnemyIA`, blackboard `BB_EnemyIA`. Root Selector, service `BTService_LocatePlayer` (interval 0.5 default). Children left to right:

1. `Sequence_0`. Decorator: Blackboard `bReceivingDamage` Is Set, Observer aborts Self. Child: `BTTask_HitSun`.
2. `Sequence_1`. Decorators: Blackboard `DistanceToTarget` <= 600 with abort Lower Priority, and Cooldown 6. Children: Rotate to face BB entry `TargetActor`, then `BTTask_Defend`.
3. `BTTask_Attack` (Target = `TargetActor`). Decorators: Cooldown 3, and Blackboard `DistanceToTarget` <= 220 with abort Lower Priority. No Force Success.
4. `Sequence_3`. Decorator: Blackboard `TargetActor` Is Set, abort Lower Priority. Children: Rotate to face `TargetActor`, then Move To `OrbitLocation`. Move To settings: Allow Strafe on, Observe Blackboard Value on, Reach Test Includes Agent Radius **off** (Step 0b, 2026-10-14), Acceptable Radius still the default 5, plus the service "Set default focus" with key `TargetActor`.
5. `Sequence_2`, no decorator. Children: `BTTask_Roam`, then Wait 3 ± 0.5.

`BB_EnemyIA` keys: `SelfActor`, `DetectionRadius` (float, default 1500), `TargetActor` (object), `bReceivingDamage` (bool), `DistanceToTarget` (float, default 100000), `OrbitLocation` (vector).

`BP_IAController`: BeginPlay → Run Behavior Tree `BT_EnemyIA` → Get Blackboard → Set Value as Float `DetectionRadius` = 1500.

`BTService_LocatePlayer` (correct, do not rework):
1. It sets `PlayerCharacter` to None.
2. It runs a Sphere Trace Multi for Objects at the pawn location with radius = BB `DetectionRadius` and object type Pawn, ignoring self.
3. For each hit, it casts to `BP_ThirdPersonCharacter` and stores the result in `PlayerCharacter`.
4. If `PlayerCharacter` is valid, it sets BB `TargetActor` and BB `DistanceToTarget`, then writes BB `OrbitLocation`:
   - Distance below 320 or above 480: player + Normalize(enemy − player) × 400.
   - Distance from 320 to 480: player + (enemy − player) rotated 18° around Z.
   - Saved values as of 2026-10-14 after Step 0: 150 / 210 / 180 / 40°. Export check passed (`=320`, `=480`, `=400`, `=18.` had no hits).
5. If it is not valid, it clears `TargetActor` and sets `DistanceToTarget` to 100000.

`BTTask_Defend`: Receive Execute AI → Print String `Enemigo: se está defendiendo` (2 s) → Delay 1.5 → Finish Execute (Success on). The owner added the accent on 2026-10-14. Not re-exported. The package was not dirty.

`BTTask_Attack`: Receive Execute AI → Print String `Enemigo: va a atacar` (2 s) → Is Valid (Get Blackboard Value as Actor, key `Target`).
- Is Valid → `BPI_Enemy` Attack (message) on the controlled pawn → Finish Execute (Success on).
- Is Not Valid → Finish Execute (Success off).

`BTTask_HitSun`: Receive Execute AI → Delay 0.6 → Set Value as Bool (target: Get Blackboard of Owner Controller, Key Name: Make Literal Name `bReceivingDamage`, value off) → Print String `Enemigo: ya no recibe daño` (2 s) → Finish Execute (Success on). That node is the only Set Value as Bool in the Event Graph node list, and it has no `ErrorType`. The owner moved it to about (880, −352) on 2026-10-14. Two old objects (`SetValueAsBool` with `ErrorType=1`, and an unwired `SetBlackboardValueAsBool`) are still in the asset text but are not in the Event Graph `Nodes` list, so they do not appear in the editor. Do not ask the owner to delete them.

`BTTask_Roam`: Receive Execute AI → AI MoveTo (pawn = Controlled Pawn, destination = Get Random Reachable Point In Radius around the pawn location, radius = variable `RoamRadius` 1000, acceptance radius 5).
- On Success → Finish Execute (Success on).
- On Fail → Finish Execute (Success off).
- The owner removed the debug prints and the orphan Branch on 2026-10-14. Not re-exported. The package was not dirty.

`BP_BaseEnemy` (death chain saved 2026-10-18, Reason `Dead`):
- Event BeginPlay → Bind Event to E_Dead. Target is `BPC_E_Health`. Event is custom event `Enemy_Death`.
- Event `Attack` (from `BPI_Enemy`, input `TargetActor`) goes straight to Sphere Trace Multi for Objects at its own location, radius 200, Pawn. The bind is no longer in this chain.
- For Each with Break. If Hit Actor == `TargetActor`, it calls Apply Damage 10 and then Play Montage (mesh `Mesh`). **Montage To Play is empty**, then the loop breaks.
- Custom event `Enemy_Death` → Set `bIsDead` true → Play Anim Montage `Enemy_Death_Montage` → Get Controller → Cast To AIController → Get Brain Component → Stop Logic (Reason `Dead`) → Disable Movement → Set Collision Enabled No Collision on the capsule → Set Life Span 3.
- Attack Play Montage still has Montage To Play empty. The mesh is `SK_SciFiWarrior02` (skeleton `UE4_Mannequin_Skeleton`). None of the 20 montages in the project use that skeleton, so Step 6 left the pin empty. `Enemy_Death_Montage` uses the SciFi trooper skeleton.
- Pawn defaults: capsule radius 34, half height 88. Max walk speed 600. Orient Rotation to Movement off. Use Controller Rotation Yaw on. Auto Possess AI = Placed in World or Spawned. AI Controller Class = `BP_IAController`.

`BPC_E_Health`: `E_Decrease_Health(Damage)` does these steps in order:
1. Branch: `E_Health` > 0. False ends. True continues. The greater-than B pin has no serialized number, which is the float default 0, same as the existing less-or-equal pin below.
2. `E_Health` −= Damage. `E_Health` defaults to 100.
3. Calls `E_Updated_Heatlh` (the typo is in the asset).
4. If `E_Health` <= 0, calls `E_Dead`.

`BP_ThirdPersonCharacter` (relevant parts):
- WeaponHitbox On Component Begin Overlap → Cast to `BP_BaseEnemy` → Print String `Hitbox detectada` → Branch on `bLightAttackActive`.
- The node `E_Decrease_Health` (target: the cast enemy's `BPC_E_Health`) runs from the hitbox Branch's True pin. Its Damage pin is the 15 / 15 / 19 Select. Its `then` pin goes to the object Cast To AIController.
- The light and heavy attack chains are separate copies. Light starts at event `IA_Light_Attack` (graph Y ≈ −2672). Heavy starts at `IA_Heavy_Attack` (Y ≈ −1760).
  - Light: Started → Branch → (False) Set `IsAttacking` → Set `bLightAttackActive` → Weapon to Hand → Play Montage `LightAttackCombo[AttackIndex]` at (4144, −2624). That node's white `then` goes to a Branch at (4416, −2160) which sets `AttackIndex` to `AttackIndex + 1`, or to 0 on the last swing. On Completed → `IsAttacking` false → `bLightAttackActive` false → `AttackIndex` 0 → Weapon to Back.
  - That same Play Montage's On Notify Begin feeds Switch on Name at (4672, −2896). `EnableHitbox` sets `WeaponHitbox` collision to Query Only. `DisableHitbox` sets it to No Collision. Saved 2026-10-18.
- `ResetState` → `SetState` (Nothing) → `AttackIndex` 0 → `bSaveLightAttack` false.
- `bLightAttackActive` exists (bool, default false). Light start sets it true, light On Completed and `ResetState` set it false. WeaponHitbox overlap → Cast to `BP_BaseEnemy` → Print String → Branch on `bLightAttackActive`. True calls `E_Decrease_Health`. Its Damage pin is a Select: Index = `LightSwingIndex`, Option 0 = 15, Option 1 = 15, Option 2 = 19. Then Cast To AIController (object) fed by Get Controller, then Get Blackboard → Set Value as Bool `bReceivingDamage` checked. Heavy attack was not changed.
- `LightSwingIndex` is set from `AttackIndex` on the live Play Montage's `then` pin, before the Branch that increments `AttackIndex`. `LightAttackCombo` order is `FA_1_Montage`, `FA_2_Montage`, `L_FA_3_Montage`.
- The player has Event AnyDamage (`ReceiveAnyDamage`). Its `then` calls `BPC_Health.Decrease_Health`, and the event's Damage pin feeds that node's Damage pin. Damage Type, Instigated By, and Damage Causer are empty. The debug key still calls Decrease Health with 25. Saved 2026-10-18. Enemy Apply Damage 10 now reaches the player.

Placed actors on `ThirdPersonMap`:

| Actor | Location |
| --- | --- |
| `BP_BaseEnemy` | (1140, 1970, 198) |
| `BP_BaseEnemy2` | (1490, 1980, 198) |
| `PlayerStart` | (1380, 5670, 212) |
| `NavMeshBoundsVolume` | origin (1330, 2300, 250), extent (1725, 1250, 250) |

Nav: `SupportedAgents` is empty, so every pawn uses `RecastNavMesh-Default` (height 144, radius 35). Do not change agent height. It is not a problem.

### Pending work, in order

**Playtest block.** Combo damage is saved: Select Option 0 = 15, Option 1 = 15, Option 2 = 19. All three light montages open the hitbox. Event AnyDamage is saved and forwards the incoming Damage pin to `BPC_Health.Decrease_Health`. The enemy still sends 10. AI1-T1 through AI1-T6 are ready for the owner. An export is not a pass.

**Next — Step 9, owner play.** No more Blueprint edits until the play result is written down. Open `ThirdPersonMap`, press Play, and check:

1. A light combo deals 15, then 15, then 19. About 0.6 seconds after each hit the screen shows `Enemigo: ya no recibe daño`. A heavy attack does not drop that health.
2. Two full light combos leave the enemy at 2 health. The next light hit kills it. It plays the death montage, stops moving, stops printing, and disappears after a few seconds.
3. While an enemy is in range, its attack lowers the player's health by 10. The debug key is still a separate 25.

If one swing removes 30 or 38, the hitbox overlapped twice. Record what was seen. Do not add a new number.

Each step: the owner (or an agent instructing the owner) makes the edit, presses **Compilar**, then **Guardar**. Then re-export with `Tools/UnrealPython/export_ai.py` and confirm the change in the summary before going to the next step. Spanish UI names are given in parentheses.

**Step 1 — Defend accent (AI1-04).** Done 2026-10-14. Owner edited the Print String and asked not to play-test it. Dirty packages were none. Original click: open `BTTask_Defend`, set `In String` to `Enemigo: se está defendiendo`, compile, save.

**Step 2 — Remove Roam debug nodes.** Done 2026-10-14. Owner removed both debug Print Strings and the orphan Branch, and wired AI MoveTo On Fail to Finish Execute with Success off. Asked not to play-test it. Dirty packages were none.

**Step 3 — Clear the HitSun error badge.** Done 2026-10-14. The node on the graph is wired Delay → Set Value as Bool → Print String → Finish Execute, with no `ErrorType`. A second export after the owner moved that node confirmed it is the only Set Value as Bool in the Event Graph `Nodes` list. An `ErrorType=1` object remains in the asset text and is not a graph node, so it is not visible and is not part of this step.

Original rewire, already applied on the live node:
  - exec in from Delay `then`, exec out to the Print String.
  - Target from Get Blackboard (whose Target is the event's Owner Controller).
  - Key Name from Make Literal Name `bReceivingDamage`.
  - Bool Value unchecked.
- Compile, save.

**Step 4 — Light-only damage (AI1-03).** Done 2026-10-18. Export confirms `bLightAttackActive`, Damage 25, and Set Value as Bool `bReceivingDamage` true on the object cast path. Original clicks, already applied:
1. My Blueprint → Variables → + → name `bLightAttackActive`, type Boolean, default unchecked. Compile once so the variable appears.
2. Find event `IA_Light_Attack` (Y ≈ −2672). Its Started pin goes into a Branch. That Branch's False output goes to Set `IsAttacking`. Alt+left click the wire from Set `IsAttacking` `then` to Weapon to Hand. Insert Set `bLightAttackActive` (checked) between them.
3. On that same chain, find the light Play Montage's On Completed path. Set `IsAttacking` false → Set `AttackIndex` 0 → Weapon to Back. Insert Set `bLightAttackActive` (unchecked) right after Set `IsAttacking` false.
4. Find custom event `ResetState`. Alt+click the wire from its `then` to `SetState`. Insert Set `bLightAttackActive` (unchecked) between them.
5. Find the WeaponHitbox overlap → Cast to `BP_BaseEnemy` → Print String `Hitbox detectada`. From that Print String's `then`, add a Branch (Rama). Condition = Get `bLightAttackActive`. Wire True → the existing `E_Decrease_Health` execute. **Change its Damage from 100 to 25** (decision B). Leave False empty.
6. From `E_Decrease_Health` `then`: Cast To AIController. Its Object input is the `BP_BaseEnemy` cast's As BP Base Enemy → Get Controller. From As AIController → Get Blackboard → Set Value as Bool. Key Name = Make Literal Name `bReceivingDamage`, Bool Value checked.
7. Compile, save.

Do not use `bSaveLightAttack` or `IsAttacking` as the gate. Those are a combo buffer and a shared state, and both are true for heavy attacks too. Do not touch the `IA_Heavy_Attack` chain.

Step 4 saved the flat 25. The owner replaced that on 2026-10-18 with 15 / 15 / 19, and that Select is saved. The enemy still stops for 0.6 s, then prints `Enemigo: ya no recibe daño`, after each hit that removes health. Two full combos leave 2 health. The next light hit kills.

**Step 5 — Enemy death (AI1 cleanup, needed before AI 2 counts living enemies).** Done 2026-10-18. Export confirms BeginPlay binds `E_Dead`, Attack goes to the sphere trace, `bIsDead` is set true, and Stop Logic Reason is `Dead`. Original clicks:
1. Add Event BeginPlay (Evento BeginPlay). Move the existing **Bind Event to E_Dead** node there: BeginPlay → Bind Event to E_Dead. Its Target stays `BPC_E_Health`, and its Event stays the `Enemy_Death` red pin.
2. In Event `Attack`, wire the event's `then` directly to the Sphere Trace node. The bind is no longer in this chain.
3. On `Enemy_Death`, after Play Anim Montage add these nodes in order:
   - Get Controller → Cast To AIController → Get Brain Component → Stop Logic (Reason: `Dead`).
   - Get Character Movement → Disable Movement.
   - Get Capsule Component → Set Collision Enabled (No Collision).
   - Set Life Span 3 on self.

   These are engine nodes. No new numbers are locked, except that the life span is a cleanup choice and not gameplay. Record it if you use a different value.
4. Add a boolean `bIsDead` on `BP_BaseEnemy`. Set it true at the start of `Enemy_Death`. AI 2 uses it to count living enemies.
5. Compile, save.

**Step 6 — Attack montage (cosmetic).** Closed 2026-10-18 with Montage To Play left empty. The enemy mesh `SK_SciFiWarrior02` uses `UE4_Mannequin_Skeleton`. No montage in the project uses that skeleton.

**Step 7 — Health component guard.** Done 2026-10-18. `E_Decrease_Health` starts with a Branch whose condition is Get `E_Health` > 0. True goes to the existing subtract. False is empty.

**Step 8 — Player receives enemy damage (needed for AI 3 and for AI 1's attack to matter).** Done 2026-10-18. Export: Event AnyDamage `then` calls `BPC_Health.Decrease_Health`, and the event Damage pin feeds that Damage pin. The debug key remains 25. The light Select remains 15 / 15 / 19. The number that arrives is the 10 `BP_BaseEnemy` already sends.

**Step 9 — Owner PIE checks.** Run the editor tests in `WORK_ITEMS.md` that say Ready. Write each result in the result log. Set an AI1 row to Done only after its checks pass.

### Owner decisions (resolved 2026-10-14)

The owner chose to shrink the orbit and lower the damage. `AI_REQUIREMENTS.md` already holds the new numbers, which are locked from now on.

- **A. Orbit vs attack range.** The old band 320–480 kept the enemy outside the attack distance of 220, so it almost never attacked. New values:
  - Preferred orbit radius: **180**.
  - Inner limit: **150**.
  - Outer limit: **210**.
  - Rotation step: **40°** per service tick. That is still the locked strafe of 250 units/s: 250 × 0.5 s = 125 units of arc, and 125 / 180 rad ≈ 40°.
  - Unchanged: attack distance 220, cooldown 3, defend 600, detection 1500.

  Result: while orbiting, the enemy is always inside attack range, so it attacks each time the 3 second cooldown is ready. Defend still has higher priority, so roughly every 7.5 s it defends instead. Spacing check: at 150 units between centers, the two capsules (34 + 35) leave about 80 units of gap, so it does not touch the player. `BP_BaseEnemy` Attack traces 200 from the enemy center, which reaches the player capsule at up to about 234, so attacks at 210 still connect.
- **B. One-hit kill.** The light damage on the player's `E_Decrease_Health` call changed from 100 to **25** on 2026-10-14. Enemy `E_Health` stays 100. On 2026-10-18 the owner replaced that flat 25 with combo damage **15 / 15 / 19** (the finisher was going to be 20; the owner set 19 so two combos do not kill). Two full combos leave 2 health. The next light hit kills. The 0.6 s hit stun still shows after each hit that removes health. The Select is saved.

**Step 0b — Let Move To reach the 180 point.** Done 2026-10-14. Export shows `bReachTestIncludesAgentRadius=(DefaultValue=False)` on `BTTask_MoveTo_0`. Agent PIE: at game time 98 s distances were 170 and 154; at 152 s they were 161 and 170, and both positions and `OrbitLocation` had changed. Attack lines continued. No `Accessed None`. Original click sequence, already applied:
1. Open `BT_EnemyIA`. Select the **Move To** whose Blackboard Key is `OrbitLocation` (orbit sequence, the fourth Selector child). Do not select the roam task.
2. In Details, uncheck **Reach Test Includes Agent Radius**. Leave Acceptable Radius at `5`. Leave Allow Strafe and Observe Blackboard Value on.
3. Compile, save.
4. Agent check: `export_ai.py`, then confirm `BT_EnemyIA.t3d` `BTTask_MoveTo_0` has `bReachTestIncludesAgentRadius` false (or the property serialized off). Then PIE with `teleport.flag` and `pie_sample.py`. `DistanceToTarget` should move into 150–210, and `OrbitLocation` should change between samples. `Enemigo: va a atacar` should still appear about every 3 s per enemy.

**Step 0 — Apply decision A (orbit numbers).** Done 2026-10-14. Export confirmed 150 / 210 / 180 / 40. PIE did not pass; see Step 0b. Original click sequence, already applied:
1. Open `BTService_LocatePlayer` (Content/ThirdPerson/Blueprints/EnemigoIA). In the Event Graph, find the orbit math after Set Blackboard Value as Float (`DistanceToTargetKey`).
2. On the **Less** node (`<`), where the distance is pin A, change pin B from `320` to `150`.
3. On the **Greater** node (`>`), where the distance is pin A, change pin B from `480` to `210`.
4. On the **Multiply** node (vector × float, after Normalize), change the float from `400` to `180`.
5. On the **Rotate Angle Axis** node, change Angle Deg from `18` to `40`. Leave Axis at (0, 0, 1).
6. Compile, save.
7. Agent check: run `export_ai.py`, then `summarize.py BTService_LocatePlayer`. Then confirm with `Select-String -Path Intermediate\inspect\live\_BTService_LocatePlayer.txt -Pattern "=150|=210|=180|=40"`: you should see each of the four new values. Search again for `=320|=480|=400|=18\.` and expect no hits.
8. PIE check: teleport the player with `teleport.flag`, then `pie_sample.py`. `DistanceToTarget` should settle around 150–210, with `Enemigo: va a atacar` in the log about every 3 s.

Decision B's flat 25 was replaced on 2026-10-18 by the Select 15 / 15 / 19.

If PIE shows the enemy pushing the player or jittering at 150–210, do not tune further. Record what you saw and escalate.

### After AI 1: AI 2 hostage build recipe

The specs and numbers are in `AI_REQUIREMENTS.md` → AI 2. Create all assets in `Content/ThirdPerson/Blueprints/Hostage/` (new folder).

1. `BB_Hostage` (Blackboard). Keys:
   - `SelfActor` (Object)
   - `PlayerActor` (Object, base class Actor)
   - `DistanceToPlayer` (Float)
   - `bMustFlee` (Bool)
   - `bWaiting` (Bool)
   - `bEnemyNear` (Bool)
   - `FleeLocation` (Vector)
2. `BP_HostageController` (parent AIController). BeginPlay → Run Behavior Tree `BT_Hostage`.
3. `BP_Hostage` (parent Character). Use any existing humanoid mesh from `Characters/` with the Mannequin anim blueprint.
   - Set AI Controller Class to `BP_HostageController` and Auto Possess AI to Placed in World or Spawned.
   - Turn on Orient Rotation to Movement.
   - Add a boolean `bAccompanying` (the zones read it). Also add the function `IsAccompanying` → returns `not bMustFlee and not bWaiting and DistanceToPlayer <= 600`. Read those keys from its own blackboard.
4. `BTService_HostageSense` (Blueprint, parent BTService_BlueprintBase). Variables: Blackboard Key Selectors `PlayerKey`, `DistanceKey`, `EnemyNearKey`, all Editable en instancia. On Receive Tick AI:
   1. Get Player Character 0 → set `PlayerKey`.
   2. Distance (pawn, player) → set `DistanceKey`.
   3. Get All Actors Of Class `BP_BaseEnemy` (and `BP_ChargerEnemy` once it exists). If any one is not `bIsDead` and within 800 of the pawn, set `EnemyNearKey` true; otherwise false.
5. `BT_Hostage`, a root Selector with `BTService_HostageSense`. Children left to right:
   1. Sequence [BB `bMustFlee` Is Set, abort Self]: Move To `FleeLocation` → `BTTask_HostageArrive`. That task sets `bMustFlee` false and `bWaiting` true, then Finish Execute success.
   2. Sequence [BB `bWaiting` Is Set, and BB `DistanceToPlayer` <= 400, abort Lower Priority]: `BTTask_ClearWaiting`. That task sets `bWaiting` false, then Finish Execute success.
   3. Sequence [BB `bWaiting` Is Set, abort Self]: Rotate to face `PlayerActor` → Wait 0.5. The hostage stays at the flee point until branch 2 fires.
   4. Sequence [BB `bEnemyNear` Is Set, abort Both]: Rotate to face `PlayerActor` → Wait 0.5.
   5. Sequence [BB `DistanceToPlayer` > 500, abort Lower Priority]: Move To `PlayerActor` with Acceptable Radius 300.
   6. Wait 0.5 (idle).

   Branch order matches the spec: flee, wait (branches 2 and 3), hold, follow, idle.

   **No Force Success under the Selector.** Every Blueprint task must call Finish Execute on every path.
6. `BP_CombatZone` (Actor). Components:
   - Box `Trigger`.
   - Box or static mesh `EntranceBlocker` with collision disabled at start.
   - Variable `FleePoint` (Target Point, instance editable).
   - Variable `LivingEnemies` (Integer).

   Behavior:
   - BeginPlay: count overlapping `BP_BaseEnemy` actors and store the count. Bind each enemy's `BPC_E_Health` `E_Dead` to a custom event that decrements the count. When the count reaches 0, disable the blocker and set the hostage's `bWaiting` true.
   - Player Begin Overlap with count > 0: enable the blocker collision. If the hostage `IsAccompanying`, set the hostage BB `FleeLocation` = `FleePoint` location and `bMustFlee` true.
7. `BP_HostageSpawnZone` (Actor). Components and variables:
   - Box `Trigger`.
   - `EnemyClass` (class of Character, default `BP_BaseEnemy`).
   - `SpawnCount` (int 2).
   - `bSpawned` (bool).
   - Optional `TargetZone` (`BP_CombatZone`) to register the spawned enemies.

   On player overlap, if not `bSpawned` and the hostage `IsAccompanying`: spawn `SpawnCount` enemies at points inside the box on the navmesh, then set `bSpawned`.
8. Place the actors inside the `NavMeshBoundsVolume` (origin 1330, 2300; extent 1725 × 1250): one hostage near `PlayerStart`, one `BP_CombatZone` with a Target Point outside it, and one `BP_HostageSpawnZone`. **Write their actor labels in this file.**
9. Add the new asset paths to `Intermediate/inspect/extra_paths.txt`, so `export_ai.py` exports them.

### After AI 2: AI 3 charger build recipe

The specs are in `AI_REQUIREMENTS.md` → AI 3. Put the assets in `Content/ThirdPerson/Blueprints/Charger/`.

1. `BB_Charger` keys:
   - `SelfActor`
   - `TargetActor` (Object)
   - `DistanceToTarget` (Float, default 100000)
   - `bCharging` (Bool)
   - `bRetreat` (Bool)
   - `RetreatLocation` (Vector)
   - `ChargeLocation` (Vector)
2. `BP_ChargerController`: BeginPlay → Run Behavior Tree `BT_Charger`.
3. `BP_ChargerEnemy`: a child Blueprint of `BP_BaseEnemy`, so it inherits health and death. Override AI Controller Class to `BP_ChargerController`. Its damage takes light **and** heavy hits, so the player hitbox needs a second cast. Escalate before editing the player again.
4. Service: reuse `BTService_LocatePlayer` with the radius key bound to a `DetectionRadius` key (1800), or copy it without the orbit math.
5. `BT_Charger` root Selector, left to right:
   1. Sequence [`bCharging` Is Set, abort Self]: `BTTask_Charge`. It sets max walk speed 900 and moves to `ChargeLocation` with acceptance 180. A time limit decorator of 1.0 s goes on this task. On end it restores speed 600, clears `bCharging`, sets `bRetreat`, then Finish Execute. Contact damage: during the charge, sphere trace 200 → Apply Damage to the player once per charge. The existing amount is 10, so use 10 and not 15.
   2. Sequence [`DistanceToTarget` in 250–700 (two Blackboard decorators: >= 250 and <= 700), Cooldown 2]: Rotate to face → Wait 0.8 → a task that sets `ChargeLocation` = player location and `bCharging` true.
   3. Sequence [`bRetreat` Is Set, abort Self]: a task that computes `RetreatLocation` = player + Normalize(self − player) × 1000 → Move To `RetreatLocation` → Wait 2 → a task that clears `bRetreat`.
   4. Sequence [`TargetActor` Is Set and `DistanceToTarget` > 700]: Move To `TargetActor` with Allow Strafe off.
   5. Roam: reuse `BTTask_Roam` → Wait 3.
6. Place one `BP_ChargerEnemy` in the navmesh area and record its label here.

### Files touched in this pass

- `Content/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA` (owner removed Force Success from Attack, 2026-10-14)
- Owner edits saved earlier on 2026-10-13/14:
  - `BTTask_Defend` (Delay + Finish Execute)
  - `BTTask_Attack` (Is Not Valid → Finish Execute false)
  - `BP_IAController` (1500)
  - `BTTask_Roam` (debug prints)
- `Tools/UnrealPython/*.py` (new; agent tooling, tracked because `Intermediate/` is git-ignored)
- `docs/GOVERNANCE.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/AI_REQUIREMENTS.md`
- `docs/WORK_ITEMS.md`
- `docs/HANDOFF.md`

## History

### 2026-10-21 — Partner menu widgets copied in

Copied `Content/Menu` (22 widgets) from the extracted UE 5.4 zip into this project so the `/Game/Menu/...` paths stay valid. Replaced `MainMenuLevel` with the zip's level, which creates `/Game/Menu/Menu_Inicio`. Added `GameInstanceClass` in `DefaultEngine.ini`. Did not replace `BP_ThirdPersonCharacter`, the game mode, the third-person map, or `BP_GameInstance`. Pause on P still has to be added on the current player Blueprint.

### 2026-10-21 — AI 1 playtests, death montage left to animation

Owner on `ThirdPersonMap`: T1–T4 passed. An enemy hit removes 10 health. On death the enemy stops and disappears; no death montage plays, and the owner accepted that as the 3D animation team's work. T5 is not a pass: the orbit comes in, but the motion does not flow naturally. AI1-02 stays open.

### 2026-10-21 — Weapon switch merged onto the AI player Blueprint

`main` `1545b36` is merged into `feat/ai`. `BP_ThirdPersonCharacter` keeps the light combo and AnyDamage wiring, and now has the hammer component on `HammerSocket` plus the two switch events. `Y` shows the hammer. `T` shows the sword. The hammer starts hidden.

### 2026-10-21 — Merge of main started, player Blueprint kept

`main` `1545b36` merged into `feat/ai`. The only conflict was `BP_ThirdPersonCharacter.uasset`. Resolved with the `feat/ai` asset. Hammer assets and input actions are staged. The weapon switch graph is not on the player Blueprint yet. The merge commit is still open.

### 2026-10-18 — Player AnyDamage saved

Export, dirty packages none. Event AnyDamage calls `BPC_Health.Decrease_Health`. The event's Damage pin is wired to that node's Damage pin. Damage Type, Instigated By, and Damage Causer are empty. The debug key is still 25. The light Select is still 15 / 15 / 19. Next step is the owner's play on `ThirdPersonMap`.

### 2026-10-18 — FA_1 hit window saved

Export, dirty packages none. `FA_1_Montage` Montage Notify `EnableHitbox` triggers at 0.08 s. `DisableHitbox` triggers at 0.34 s. EdAttack stays at 0.39 s and AttackFinished stays at the end. Swing 1 can now connect for 15 damage. Next decision is Step 8, player AnyDamage. Ask the owner before editing the player.

### 2026-10-18 — Combo damage saved as 15 / 15 / 19

Export, dirty packages none. Live Play Montage `then` sets `LightSwingIndex` from `AttackIndex`, then the Branch increments `AttackIndex`. Select Index is `LightSwingIndex`. Option 0 = 15, Option 1 = 15, Option 2 = 19. That return value is the Damage pin of `E_Decrease_Health`. The owner set 19 instead of 20 so two full combos leave the enemy at 2 health. `FA_1_Montage` still has no EnableHitbox. Next click is that montage.

### 2026-10-18 — Light hitbox enable saved, combo damage chosen

Export: the live light Play Montage On Notify Begin feeds Switch on Name at (4672, −2896). `EnableHitbox` sets `WeaponHitbox` to Query Only. `DisableHitbox` sets No Collision. Dirty packages were none. The owner chose light combo damage 15 / 15 / 20. `E_Decrease_Health` still has Damage 25. `FA_1_Montage` still has no EnableHitbox notify. Next click is `LightSwingIndex` plus Select on that Damage pin.

### 2026-10-18 — Light notify switch saved without the enable branch

Export: light Play Montage On Notify Begin and Notify Name feed a new Switch on Name at (4672, −2896) with pins `EnableHitbox` and `DisableHitbox`. `DisableHitbox` goes to Set Collision Enabled No Collision on `WeaponHitbox`. `EnableHitbox` has no wire and there is no Query Only node in that chain, so the hitbox still never turns on. Next click: add that node.

### 2026-10-18 — Light attack never enables the hitbox

`Weapon` is No Collision now and the owner still saw no `Hitbox detectada`. The light Play Montage's On Notify Begin is unwired. The old Switch on Name chain that enables `WeaponHitbox` has no exec input. `FA_1_Montage` has no EnableHitbox notify. `FA_2_Montage` and `L_FA_3_Montage` have one. No asset changed.

### 2026-10-18 — Sword mesh blocks the enemy

Playtest: the longsword pushes the enemy and the hit does not register. `Weapon` is Query and Physics, Block All Dynamic, Block on Pawn. `WeaponHitbox` is a 32-unit box, Overlap on Pawn, and No Collision until the `EnableHitbox` notify. The pasted `RigHierarchy.GetController` node has no wires and is not the hit path.

### 2026-10-18 — Health guard saved

`BPC_E_Health` export: `E_Decrease_Health` starts with a Branch on `E_Health` > 0. True continues to the subtract. False is empty. Next decision is whether to add Event AnyDamage on the player.

### 2026-10-18 — Death reason saved, attack montage left empty

Stop Logic Reason is `Dead`. Montage To Play stays empty: `SK_SciFiWarrior02` uses `UE4_Mannequin_Skeleton`, and no project montage uses that skeleton. Next click is the health guard on `BPC_E_Health`.

### 2026-10-18 — Enemy death chain saved, Reason empty

`BP_BaseEnemy` export: BeginPlay binds `E_Dead` to `Enemy_Death`. Attack goes straight to the sphere trace. `Enemy_Death` sets `bIsDead`, plays the death montage, stops the brain, disables movement, turns capsule collision off, and sets life span 3. Stop Logic's Reason pin has no text.

### 2026-10-18 — Light damage wire saved

`BP_ThirdPersonCharacter` export: light attack sets `bLightAttackActive`, the hitbox Branch calls `E_Decrease_Health` with Damage 25, then an object Cast To AIController (Get Controller from the enemy) writes blackboard `bReceivingDamage` true. Heavy attack is unchanged. Next click is Step 5.

### 2026-10-14 — HitSun error object is not on the graph

A fresh export after the owner moved Set Value as Bool to (880, −352) shows that node in the Event Graph `Nodes` list with no `ErrorType`. The `ErrorType=1` Set Value as Bool and the extra Set Blackboard Value as Bool are serialized objects that are absent from that list, which is why they are not behind the node in the editor. Step 3 is done. Next click is Step 4.

### 2026-10-14 — HitSun rewire is live, old error node remains

The owner added a new Set Value as Bool and wired Delay → that node → Print String → Finish Execute. Export shows no `ErrorType` on that node. The old Set Value as Bool is still in the graph with `ErrorType=1` and no wires, plus an unwired Set Blackboard Value as Bool. Next click is to delete those two nodes.

### 2026-10-14 — HitSun compile did not clear the badge

The owner compiled and saved `BTTask_HitSun`. Dirty packages were none. The export still has `ErrorType=1` on Set Value as Bool and no `ErrorMsg`. Wiring is unchanged. Next click is the Step 3 rewire.

### 2026-10-14 — Roam debug nodes removed, not play-tested

The owner cleaned `BTTask_Roam` and asked the agent not to test it. `ping.py` reported no dirty packages. Next click is Step 3.

### 2026-10-14 — Defend accent saved, not play-tested

The owner set `BTTask_Defend` Print String to `Enemigo: se está defendiendo` and asked the agent not to test it. `ping.py` reported no dirty packages. Next click is Step 2.

### 2026-10-14 — Step 0b: enemies enter the band and circle

The orbit Move To now has Reach Test Includes Agent Radius off. Agent PIE after teleport: both enemies stayed in 150–170, moved around the player, and the orbit point changed between samples 54 seconds apart. Attack and defend lines kept printing. No `Accessed None`. Next click is Step 1.

### 2026-10-14 — Step 0 saved, orbit does not enter the band

`BTService_LocatePlayer` export has Less 150, Greater 210, Multiply 180, Rotate Angle Axis 40. Old pins are gone. Dirty packages were none. Agent PIE with the player teleported 450 units from enemy 0: both enemies closed in, then froze. Samples at game time 87s and 133s were identical: distances 213 and 145, speeds 0, `OrbitLocation` on the 180 circle `(2265,3486)` and `(2246,3465)`. Attack and defend lines kept printing (about every 3 s per enemy). No `Accessed None`. The 40° branch never ran because Move To already counted them as arrived. Next edit is Step 0b, not a new radius.

### 2026-10-14 — Owner decisions A and B resolved

The owner chose a smaller orbit (radius 180, band 150–210, 40° step at the same 250 u/s strafe) so the enemy orbits inside the attack range of 220. The owner also chose light damage 25 against health 100, so it takes 4 hits and hit stun is visible. Only docs changed. The assets still hold the old values until Step 0 and Step 4 are done.

### 2026-10-14 — Root cause of "enemies do not walk" found and fixed

Comparing with `main`'s original tree showed the Force Success decorator on `BTTask_Attack` directly under the Selector. It ended every pass through the tree at Attack, so Orbit and Roam never ran. The owner removed it. Agent PIE then verified that roam, orbit, defend, and attack all work. Earlier the owner added Delay + Finish Execute to Defend, Finish Execute false on Attack's Is Not Valid path, and set the controller to 1500. The tooling scripts moved to `Tools/UnrealPython/`.

### 2026-10-13 — Full orbiter audit with agent-run PIE

Re-exported all orbiter assets and the player character. Ran short Play In Editor sessions from Python. Found that the Defend task never finishes. Agent height turned out not to be a blocker. No asset changed. (The claim "Roam never moves" from this audit was caused by Force Success, found on 2026-10-14.)

### 2026-10-13 — Orbiter tree saved, damage gate still open

Re-exported the Selector, the service, the three tasks, the health component, the enemy, and the player character. The five branches, the orbit math, and the three Spanish prints are in the assets. Player damage still does not execute. No Play In Editor test.

### 2026-10-11 — Enemy tree inspected, blackboard keys added

Connected to the open Terreno editor. Recorded the live `BT_EnemyIA` structure. Saved `bReceivingDamage`, `DistanceToTarget`, and `OrbitLocation` on `BB_EnemyIA`. No behavior-tree branches were rewired.

### 2026-10-11 — Decisions locked

The owner delegated the open choices and supplied `FE-OV 1.docx`. Locked Behavior Trees, the orbiter tuning, the hostage zone rules, and a second enemy (charger) required by the rubric. No Blueprint, map, or config asset was modified.

### 2026-10-11 — Governance created

Created the English agent docs from the owner brief and from files present in the repository. No Blueprint, map, or config asset was modified.
