# AI requirements

## Compatibilidad con cinemáticas — 16 noviembre 2026

**Stated / Decision:** introducción18s, derrota8s y victoria14s por libertad creativa del propietario; son tiempos de presentación, no de combate. Durante la introducción se bloquean las entradas y la pausa; no avanza el cronómetro previo al rescate. Al terminar u omitir se restituyen vista, cámara elegida, visibilidad y entrada. Continuar omite la escena. Sólo después del resultado existente se detienen árboles/movimiento y daño tardío para presentar el desenlace; al cerrar queda pausado con R/Enter. Se conservan los Behavior Trees, sus decisiones y ContactDamage13.2. La pose física del rehén muerto y el ajuste visual de la malla del jugador caído pertenecen al desenlace, sin alterar salud ni combate. Diseño y evidencia: `CINEMATICAS.md` y handoff vigente.

## Refinamiento vigente de fluidez — 16 noviembre 2026

Esta sección sustituye los tiempos/distancias de ataque de la revisión anterior. **Decision / Verified en gráficos:** el melee se aproxima hasta150cm, alinea progresivamente y solicita Attack, que exige objetivo válido, LOS, <=160cm y recuperación cumplida. Cada enemigo espera al menos3s entre inicios de golpes. El montaje1.3s se reproduce a1.25; contacto único en posiciones0.28..0.64, distancia<=210cm, LOS y cono frontal (dot>=0.4). Sigue al objetivo sólo antes de0.26; después el jugador puede esquivar. Se evalúa en el Tick de la tarea activa mediante UpdateStrike, conservando Actor Tick desactivado. EndAttack/Abort cancelan el golpe.

**Decision / Verified en gráficos:** giro limitado420–480grados/s y DeltaTime<=0.033 por paso para evitar el salto de entrada por tiempo acumulado del BT. Orbitador: desplazamiento cercano230, aproximación560, arco28grados, defensa con reposición0.65s. Embestidor: preparación0.65s, carrera900, predicción0.18s y correcciones sólo durante sus primeros0.45s; al llegar se planta y golpea. Aproximación/carga cancelan a1.5s si no alcanzan su objetivo. La rama cercana del segundo árbol ahora golpea y recupera en lugar de huir continuamente; retirada más corta y dirigida a su CombatTarget real.

**Decision / Verified en gráficos:** los ligeros no pueden reiniciar indefinidamente el aturdimiento (cooldown1s orbitador /1.2s embestidor); un pesado25 siempre interrumpe. Conservan daño del jugador15/15/19/22 y25, audio/confirmación de pérdida real y aviso de daño al rehén. Las cápsulas jugador/rehén se ignoran mutuamente sólo al moverse para evitar un atasco entre aliado y marco de puerta; mantienen colisión con mundo/enemigos. HUD cuenta bActivated de las tres balizas, evitando mostrar3/3 al perder antes de activarlas.

La evidencia de esta revisión se documenta en el handoff vigente. Pruebas aisladas y partidas del agente se distinguen de la aceptación del propietario.

## Corrección vigente de ataque y señales — 16 noviembre 2026

**Stated:** corregir el golpe lejano seguido de carrera, avisar del daño al rehén y confirmar daño a rivales. **Verified:** Attack rechaza solicitudes sin objetivo visible a220cm o menos. El embestidor sostiene preparación0.8s sin ejecutar el golpe, corre a900 hasta1s y al alcanzar180cm se detiene y ejecuta el montaje1.3s; impacto a0.45s. ResolveAttack exige montaje activo y posición0.30..0.70s y consume un único intento, aunque se falle por distancia/visibilidad. Abort/interrupción cancela el golpe. Se conservan ambos árboles, daño13.2 y daño del jugador15/15/19/22 y pesado25.

**Verified:** el rehén incrementa DamageNoticeSerial sólo al aceptar daño hostil; HUD renueva un aviso2.4s, con alerta sonora separada por1.2s. El serial no se guarda, evitando avisos al restaurar salud/checkpoint. Enemigos confirman pérdida real de vida (incluida letal) con impacto2D del audio existente y X/cifra central0.18s; curación y contactos repetidos sin daño no confirman golpe. Pruebas actuales: `validation/combat-timing-2026-11-16.json`, `combat-misses-2026-11-16.json`, `combat-feedback-2026-11-16.json`. Son pruebas del agente, no aceptación manual.

## Compatibilidad con el rework de evaluación — 2026-11-16

**Verified:** las dos IA y el BT del rehén se conservan en el mapa convertido a World Partition; navegación dinámica convencional reconstruida al cargar. CompleteActivation mide distancia horizontal al pivote de suelo de la baliza, conservando límite220cm y guardas de canalización. GrantHammerUpgrade limpia el ataque y ResetState para evitar un bloqueo al recibir recompensa durante un golpe. Recorrido completo del agente y seis permutaciones aprobados; daño13.2 y zonas2×2 intactos. No sustituye aceptación manual.

## Criterios vigentes de balizas — 2026-11-16

**Stated:** condiciones de Adame transmitidas por el propietario: nombres, orden aleatorio por intento, temporizador y orden/tiempo visibles. El propietario elige orden real aleatorio en una zona accesible.

**Decision / Verified en PIE:** identidades A/B/C estables; permutación de las tres, con exclusión del intento previo en la misma sesión. Se muestran secuencia, siguiente, 0–3 activadas y tiempo de misión MM:SS. El cronómetro comienza al rescatar, se congela durante pausa y al terminar. Sin tiempo máximo impuesto. El rehén canaliza 3 s mediante el árbol existente; una amenaza aborta y una baliza fuera de turno rechaza la activación.

**Decision / Verified en PIE:** completar cada una de las dos zonas carga su puerta y equipa martillo; las tres balizas se encuentran después de la segunda puerta. La tercera puerta requiere completar la secuencia. Se mantienen dos impactos pesados y la extracción con ambos personajes. R inicia desde cero con otra secuencia; Continuar restaura la secuencia y tiempo del checkpoint (esquema 2, incompatible con archivos de esquema 1). Esta actualización sustituye las asociaciones históricas baliza 1/2 → zona 1/2.

**Unknown:** aceptación de Adame/propietario, conveniencia de una zona enemiga adicional y tiempo objetivo de evaluación. Las pruebas del agente no son aceptación manual.

## Pausa, opciones y cámara — 2026-11-15

**Stated:** continuar FIN-03 y FIN-04, hacer commits y dejar el mando pendiente. **Decision / Verified:** interfaz común `BP_DeliveryInterface` en ambos mapas, entrada P/Esc consumida por encima del P heredado, pausa de mundo y bloqueo de movimiento/mirada. Opciones conserva el widget de origen; volver desde opciones durante pausa mantiene el mundo detenido. Reanudar restaura cursor y entrada de juego. Ir al menú descarga la misión. El botón de guardar usa el gestor seguro vigente; E no ejecuta interacción durante la pausa.

**Decision / Verified:** gráficos y pantalla persisten con GameUserSettings; resolución 1280×720, 1600×900, 1920×1080 o 2560×1440; ventana/sin bordes/completa. Volumen general 0/25/50/100% con SoundMix propio y archivo `TimeOut_Options_v1`, separado del checkpoint. Los cambios se aplican al elegirlos. El menú conserva el arte existente y permite consultar los controles en pausa.

**Verified en PIE:** C usa la acción de cámara existente; primera persona en cápsula Z64, FOV90, rotación de control y malla propia oculta; tercera restaura su visibilidad y conserva brazo 350/sonda24. Y equipa martillo y T espada. Pruebas de acciones mediante Enhanced Input sobre fotogramas reales, movimiento/ataque después de reanudar y diez montajes con daño conservado. Árboles/Blackboards y balance 13.2 sin cambios. **Pendiente:** aceptación manual, mando y otra PC.

## Guardado de misión y reintento — 2026-11-15

**Stated:** comenzar FIN-01 y FIN-02. **Decision de implementación:** puntos de control en momentos seguros, automáticos al rescatar, despejar zona, activar baliza o cambiar salud de puerta; F5 permite un guardado manual seguro. No se sobrescribe el punto anterior durante oleadas/intermedios, ataque, canalización, huida, amenaza cercana, caída o derrota. No se serializa un combate a mitad de una oleada.

**Verified en PIE:** `BP_DeliverySave` y `BP_DeliverySaveManager` guardan vida/transform del jugador y rehén, cámara, arma/mejora, estado de escolta, paso, balizas, puertas (incluidas grietas/colisión) y zonas/oleadas completadas. Ranura separada `TimeOut_Delivery_v1`, esquema 1; sin referencias a actores del mapa en el archivo. Menú habilita Continuar sólo con datos legibles, compatibles y vivos. Nuevo juego reemplaza el punto por el comienzo; R tras derrota carga el último punto y R tras victoria empieza de cero. Los árboles de IA no se modificaron.

**Verified / límite:** recorrido completo automatizado mediante movimiento y ataques, sin teletransportes ni cambios de salud/daño, terminado en victoria. Pruebas del agente, no aceptación manual del propietario. Evidencia de FIN-01/02 y verificación del paquete en el handoff actual.

## Dificultad y fractura — 2026-11-15

**Stated / Decision:** aumento de daño enemigo del 120% sobre 6: **ContactDamage=13.2**, tanto orbitador como embestidor, contra jugador y rehén. Los valores históricos 6 quedan sustituidos. Mantener las ventanas de ataque, interrupción y gracia del rehén de 0.8 s.

**Decision / Verified en PIE:** primer pesado de martillo energizado contra puerta habilitada: 50→25 y malla con fracturas geométricas. Segundo: las mismas piezas se desprenden y giran; 42/56/72 fragmentos irregulares según puerta, juntas de 0.7 cm, duración 4 s. Ignoran Pawn/Camera y no afectan navegación. El marco permanece. Se conservan los controles de baliza, arma y tipo de ataque. Evidencia y límites en el handoff actual.

## Señal, fijación y feedback — 2026-11-15

**Stated / Decision:** señal E/RB segura hasta 1200 cm, interacción existente 400; voz sintética propia exclusiva del speaker REHÉN. Ambos enemigos fijan al rehén visible/rescatado/vivo a ≤650 cm y retienen prioridad hasta 1800 cm, incluso con jugador cercano o pérdida temporal de visión. Liberan objetivo inválido/muerto/no rescatado/fuera de límite; carga comprometida no cambia víctima a mitad. Recuperación pesada de espada con corte 1.18/1.05/1.70 s, mezcla 0.12 s. Primer pesado energizado contra puerta habilitada: grietas/25 de vida; segundo: rotura. Valores de daño conservados. Esta prioridad sustituye la intercepción histórica por proximidad.

## Refinamiento de IA y daño completo — 2026-11-15

**Stated:** ambas IA deben mantener el encuentro local; el rehén no debe rodear el mapa y los enemigos no deben abandonar el combate caminando de espaldas. Todos los ataques deben causar daño, con balance delegado.

**Decision:** espada ligera 15/15/19/22, martillo ligero 15/15, todos los pesados 25 contra ambos enemigos; una aplicación por ataque/enemigo, visión y alcance ≤300. Contacto enemigo 6. Refugio con ruta completa ≤1800, distancia al rehén ≤1600, al jugador 600–1800 y a enemigos ≥950. Retirada del embestidor 420 cm, ruta ≤650, timeout 1.4 s y recuperación 0.8 s; prioridades/carga conservadas. Punzada roja de esquinas 0.38 s, pico alfa 0.30. El detalle de ventanas y evidencia está en el handoff actual. Estos ajustes sustituyen los valores históricos incompatibles de este documento; aceptación del propietario pendiente.

## Actualización del propietario — 2026-11-15

**Stated, progresión posterior:** sólo el rehén activa las balizas tras vencer a la horda. Añadir su indicador de vida, puertas destruibles ajustadas al escenario y mejora del martillo con equipamiento automático y partículas después de cada baliza. Esta petición sustituye la activación directa por E y la apertura automática de barreras al limpiar una zona.

**Decision de implementación:** vida del rehén 100, gracia de daño 0.8 s; canalización de baliza 3 s. Cada puerta tiene 50 de vida, recibe 25 por golpe pesado del martillo mejorado y sólo se habilita con su baliza. La tercera baliza sigue a las dos hordas existentes. Detalles y pruebas en el handoff actual; aceptación del propietario pendiente.

**Stated:** para la entrega del miércoles 18 se prioriza el nuevo nivel con el escenario de Ian y la IA del rehén: seguir al jugador, huir al ver enemigos hacia una zona segura lejos del jugador y esperar una nueva interacción para seguirlo. El propietario pidió implementación autónoma. La reanudación automática descrita más abajo es histórica y queda sustituida por interacción manual.

**Stated, ampliación del 2026-11-15:** el propietario pidió priorizar el segundo enemigo y las oleadas, refinar las IA y las animaciones, y guardar el trabajo en una rama nueva mediante commits.

**Stated, refinamiento posterior:** recuperar la apariencia anterior de los enemigos, mejorar camara/paredes, impedir que el jugador quede atrapado, senalar el rescate dentro del mundo, explicar activacion y reducir dano enemigo.

**Stated, presentación posterior:** el propietario rechazó el texto flotante y pidió recuadros tipo Undertale para señales/alertas y agregar audio. La presentación nueva sustituye los TextRender anteriores; no altera las reglas de activación de las IA.

**Verified:** escolta en `BT_Hostage`/`BB_Hostage`; segundo enemigo en `BT_Charger`/`BB_Charger`; encuentros finitos en `BP_CombatZone`, colocados en `Nivel_Entrega`. Pruebas del agente y límites en el handoff actual. La aceptación del propietario sigue pendiente.

**Decision de implementación:** una misma zona combina la condición de escolta y el control de oleadas: no se crea un segundo volumen `BP_HostageSpawnZone` superpuesto. Cada zona activa dos oleadas de dos enemigos, con intermedio de 3 s, y no repite al reentrar. La primera y segunda baliza exigen despejar sus respectivas zonas; la puerta permanece cerrada hasta su destrucción con martillo. No es la supervivencia posterior a la extracción descrita en el documento histórico.

**Decision de ajuste:** pesado del embestidor 25; ligero conserva 15/15/19 y el orbitador mantiene inmunidad al pesado. El ataque del orbitador aplica 6 a los 0.45 s y finaliza a los 1.3 s; recibir daño lo interrumpe. En el embestidor la preparación dura 0.8 s, la carga hasta 1 s, la retirada tiene límite de 4 s si la navegación se atasca y después espera 2 s. Persecución con aceptación 450 cm para entrar con margen en su rango 250–700. Las decisiones de cada personaje siguen en su árbol.

Distances are Unreal units (centimeters). Every numeric value in "Locked decisions" is a **Decision** the owner delegated on 2026-10-11. Expose each one as an editable variable on the Blackboard or the actor, initialized to the value below.

Existing enemy assets are listed in `PROJECT_CONTEXT.md`. What is already saved is in `HANDOFF.md`, which was exported on 2026-10-14. The numbers below stay the target.

Agent PIE showed the orbiter's movement branches working, but the owner has not run the acceptance checks, so none is done yet. Inspect the current graph before adding a second damage path or a second task that does the same job.

On 2026-10-14 the owner changed two orbiter values. Both are **Decisions** now (see `HANDOFF.md` → Owner decisions):
- Orbit: radius 180, band 150–210 (was 400, band 320–480). The old band kept the enemy outside the attack distance of 220.
- Light damage: combo **15 / 15 / 19** (owner choice 2026-10-18; the finisher was drafted as 20, then set to 19 so two combos do not kill). Was a flat 25, and before that 100. With health 100, one full combo leaves 51. Two full combos leave 2. The next light hit kills.

Current owner balance request: AI 3 and orbiter contact damage is 6, exposed as `BP_BaseEnemy.ContactDamage` (previously 10). The 15 fallback below does not apply.

The professor's rule: each AI is a Behavior Tree, not a pile of conditionals. Tree shape is specified under each AI.

## AI 1 — Orbiter

Asset base: `BP_BaseEnemy`, `BP_IAController`, `BB_EnemyIA`, `BT_EnemyIA`.

Board status stated by the owner: Done. The integrations below stay open until an editor test checks them off.

This is enemy one of the two required by the rubric. It orbits at melee range and takes damage only from light attacks.

### Tree

`BT_EnemyIA`, highest priority first:

1. Hit stun, while Blackboard `bReceivingDamage` is true. Task lasts 0.6 seconds. On finish, print the damage-end line and clear the key.
2. Defend, when the player is within 600 units, the enemy is not attacking, and at least 6 seconds passed since the last defend. Task lasts 1.5 seconds.
3. Attack, when the player is within 220 units and the attack cooldown of 3 seconds is ready.
4. Orbit, when the player is detected inside 1500 units.
5. Roam, using the existing `BTTask_Roam` if it already wanders. If it does something else, keep that task and add a new orbit task. Do not delete roam until the editor shows what it does.

`BTService_LocatePlayer` writes the player actor and the distance. It does not choose the branch.

### Orbit

- Preferred radius: 180. (Owner decision 2026-10-14; was 400.)
- Inner limit: 150. Closer than this, strafe outward. (Was 320.)
- Outer limit: 210. Farther than this, and still detected, move inward. (Was 480.)
- The whole band sits inside the attack distance of 220, so the orbiter attacks whenever the cooldown allows.
- Strafe speed while inside the band: 250 units per second. With the service's 0.5 s tick, this is a 40° rotation step at radius 180 (it was 18° at radius 400).
- Face the player while orbiting.
- Do not stop on the player's capsule.

No defend animation was found. The defend task faces the player and does not move. If a defend montage is added later, play it from that task only.

### Damage

Only a player light attack reduces this enemy's health. Heavy attacks and any other damage source are ignored.

Use the existing path. `SaveLightAttack_AN` calls `SaveLightAttack` on `BP_ThirdPersonCharacter`. `bSaveLightAttack` is a combo-input buffer, not a light-hit window. `ResetState_AN` calls `ResetState`, and that event currently goes to `SetState`. `BPC_E_Health.E_Decrease_Health` subtracts its Damage argument and fires `E_Dead` when health reaches 0 or less. The light-attack window uses `bLightAttackActive`, set when the light attack starts and cleared from the light montage's On Completed and from `ResetState`. Do not add a second health system. `BP_BaseEnemy` Attack applies 10 damage with a sphere of radius 200. That is this enemy hitting another actor. AI 3 contact damage reuses 10. Do not change it while building the orbiter.

Light combo damage (owner choice 2026-10-18), by the swing that is playing, not by the already-incremented `AttackIndex`:

| Swing | `LightSwingIndex` | Damage |
| --- | --- | --- |
| 1 | 0 | 15 |
| 2 | 1 | 15 |
| 3 | 2 | 19 |

One full combo removes 49. Two full combos remove 98 and leave 2 health. The next light hit kills. A heavy hit is still ignored.

A light hit that actually removes health sets `bReceivingDamage` for the hit-stun branch. A rejected heavy hit does not.

Do not change max health (100). Do not invent a damage number other than 15, 15, and 19.

### Print String

Print String nodes, 2 second duration, in Spanish:

| Moment | Text |
| --- | --- |
| Attack task starts | `Enemigo: va a atacar` |
| Defend task starts | `Enemigo: se está defendiendo` |
| Hit-stun task finishes | `Enemigo: ya no recibe daño` |

These three lines are required. Do not add more required lines on this enemy.

## AI 2 — Hostage escort

No hostage asset was found by file name. Create `BP_Hostage`, `BB_Hostage`, `BT_Hostage`, and an AI controller that runs that tree only.

The hostage is not the rubric's second enemy.

### Tree

`BT_Hostage`, highest priority first:

1. Flee, while `bMustFlee` is true. Move to the zone's flee point, then stay there and set `bWaiting`.
2. Wait, while `bWaiting` is true. Clear it when the player comes within 400 units, then go back to follow.
3. Hold, when any living enemy is within 800 units of the hostage. Stay put and face the player. Do not follow into the fight.
4. Follow, when the player is farther than 500 units. Move until within 300 units, then stop.
5. Idle, while the player stays between 300 and 500 units and no higher branch is active.

### Zones

Create `BP_CombatZone` as a box trigger. A zone is populated while its living enemy count is greater than 0. Count enemies that start inside it and enemies spawned for it.

When the player begins overlap and the zone is populated, enable that zone's entrance blocker so the player cannot leave. Disable the blocker when the living count reaches 0.

If the hostage is accompanying at that moment, set `bMustFlee`. Accompanying means the escort is not already fleeing or waiting, and the hostage is within 600 units of the player.

The flee point is a Target Point referenced by the zone, placed outside the volume. There is no named landmark yet. Place at least one `BP_CombatZone` in reachable space on `ThirdPersonMap` and record its label in `HANDOFF.md`.

### Conditional spawn

Create `BP_HostageSpawnZone` as a box trigger.

On player begin overlap, spawn only when the hostage is accompanying. Spawn once per zone. Default count is 2, using the enemy class set on the zone.

- First zone class: `BP_BaseEnemy`.
- Second zone class, if a second volume is placed: `BP_ChargerEnemy`.

If the player enters without the hostage, spawn nothing. Place at least the first zone and record its label.

## AI 3 — Charger

Course requirement: two enemies with different advanced AI. This is the second enemy. New assets: `BP_ChargerEnemy`, `BB_Charger`, `BT_Charger`, and a controller that runs that tree only.

It does not orbit. It takes both light and heavy damage, so the player's two attack types both matter. It does not use the three orbiter Print Strings.

### Tree

`BT_Charger`, highest priority first:

1. Charge, while `bCharging` is true. Move at 900 units per second for at most 1 second, or until within 180 units. On arrival stop and execute the 1.3-second close strike, resolving its single impact at 0.45 seconds, then clear the charge and set retreat. A missed approach retreats without a remote strike.
2. Windup, when the player is between 250 and 700 units and the 2 second cooldown is ready. Face the player and wait 0.8 seconds, then set `bCharging`.
3. Retreat, while `bRetreat` is true. Move away until the player is at least 1000 units away, then clear retreat and wait 2 seconds before another chase.
4. Chase, when the player is detected inside 1800 units and farther than 700 units. Run straight at the player. No strafe orbit.
5. Roam, when the player is outside detection.

Contact during the charge applies damage to the player. Use the damage amount this project already uses for an enemy hit. If no such amount exists, use 15 and record that in the handoff.

## Out of this AI assignment

Do not implement these unless a work item is added:

- Hammer pickup and the gate that requires it.
- Character progression.
- The post-escape survival timer and the formula that turns remaining enemies into waves.
- Dialogue NPCs, menus, save games, and the other non-AI rubric rows.
- Player combat animations, except the light-attack flag the orbiter must read.

## Acceptance checks

An item is done only after Play In Editor on `ThirdPersonMap` shows the behavior. Updating a document is not acceptance. Partial checks while a slice is still open are in `WORK_ITEMS.md` under Editor tests. A pass there does not set Done.

| Check | Pass condition |
| --- | --- |
| Tree | Stopping the Behavior Tree stops the decision. The character Blueprint has no Tick branch that chooses orbit, attack, defend, chase, flee, or follow. |
| Orbit | After detection, the orbiter stays near 180 units (150–210) and circles. It does not overlap the player capsule. It attacks about every 3 seconds while orbiting. |
| Light damage | A light attack reduces orbiter health. A heavy attack does not. |
| Prints | The three Spanish lines appear on attack start, defend start, and hit-stun end. |
| Calm follow | With no enemy inside 800 units, the hostage stops around 300 units from the player. |
| Zone | Entering a populated `BP_CombatZone` turns on the entrance blocker, and the hostage runs to that zone's flee point. |
| Return | After the zone count hits 0, the blocker turns off. The hostage waits until the player is within 400 units, then follows again. |
| Spawn | The hostage spawn zone spawns only while the hostage is accompanying. A pass without the hostage spawns nothing. |
| Second enemy | The charger uses `BT_Charger`, rushes in a line, retreats, and still takes heavy-attack damage. |
