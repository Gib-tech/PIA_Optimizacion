# IA, combate y escolta: contrato vigente

Esta guía en español resume la implementación actual. `AI_REQUIREMENTS.md` conserva decisiones e historial con valores anteriores: las secciones antiguas que dicen daño 6/10, rechazo de pesados o sólo dos encuentros no describen el balance vigente. El catálogo enlaza los grafos reales de cada actor, servicio, tarea, AnimNotify y componente.

## Quién decide y quién ejecuta

Las decisiones de IA pertenecen a Behavior Trees y sus Blackboards. Los servicios actualizan percepción/condiciones; las tareas ejecutan una acción y terminan o abortan; el actor reproduce montaje, orienta, comprueba contacto y aplica el resultado. El director de misión cuenta enemigos/oleadas y objetivos, sin sustituir al árbol. El Tick de una tarea activa no es un segundo árbol de decisiones en el enemigo.

**Orbitador:** `BP_BaseEnemy`, `BP_IAController`, `BB_EnemyIA`, `BT_EnemyIA`, `BTService_LocatePlayer`. Prioriza interrupción/recuperación, defensa/reposición, ataque cercano, órbita y patrulla según condiciones. Las tareas `BTTask_Attack`, `BTTask_Defend`, `BTTask_FaceCombatTarget`, `BTTask_HitSun` y `BTTask_Roam` encapsulan acciones. El nombre histórico HitSun significa aturdimiento; no es un sistema de luz solar.

**Embestidor:** `BP_ChargerEnemy`, `BP_ChargerController`, `BB_Charger`, `BT_Charger`, `BTService_ChargerSense`. Encadena anticipación, carga hacia un punto comprometido, golpe cercano, recuperación y retirada local. Sus tareas Windup/Charge/Recover/Retreat y su árbol son distintos del orbitador. Puede golpear cuando ya está cerca; no huye indefinidamente para intentar cargar otra vez.

Los dos pueden priorizar al rehén rescatado a menos de 6,5 m y conservar esa fijación aunque el jugador esté más cerca. Dejan de fijarse si el objetivo muere, deja de ser válido o se aleja más de 18 m. La víctima de una carga se conserva durante la acción para evitar un cambio instantáneo de dirección hacia otro actor.

## Contacto y daño

El inicio de un montaje no concede daño. Se comprueba objetivo vivo/válido, alcance, visibilidad, orientación, ventana temporal y que no se haya consumido el impacto. Un fallo no deja daño pendiente para después. Interrupción, aborto y fin de ataque cierran el contacto.

Los enemigos esperan al menos 3 s entre inicios. La aproximación pide el ataque al llegar cerca y alineado; el montaje de 1,3 s se reproduce a 1,25. La ventana efectiva está en posiciones 0,28–0,64, con distancia máxima 210 cm, línea de visión y cono frontal. El seguimiento de orientación termina pronto para permitir esquivar. La preparación de carga dura 0,65 s, carrera a 900 cm/s y predicción breve de 0,18 s; no se daña desde la pose de preparación.

El componente `BPC_E_Health` conserva el campo **`E_Health`**, máximo 100, y el evento `E_Decrease_Health`. No se llama Health a ese campo por analogía: `BPC_Health` del jugador sí tiene Health. El pulso llama al componente real porque el enemigo base no implementa una ruta AnyDamage de recepción.

Daños vigentes: espada ligera 15/15/19/22; martillo ligero 15/15; pesados 25; pulso 20; ataque enemigo 13,2. Ligeros tienen límite para no reiniciar aturdimiento indefinidamente; un pesado válido interrumpe. El pulso consume una carga incluso al fallar, alcanza 8 m y espera 0,8 s. La traza se detiene en paredes; las cápsulas enemigas bloquean Visibility. No confundir sonido de disparo con confirmación de daño real.

`LightSwingIndex` identifica el golpe que se está ejecutando. `AttackIndex` puede haberse adelantado para el siguiente combo. `bSaveLightAttack` es un búfer de entrada; **no** indica que el arma pueda dañar. `bLightAttackActive`, posición de montaje y `WeaponHitbox` delimitan la ventana. El conjunto de actores alcanzados impide repetición durante un golpe.

Los AnimNotifies SaveLightAttack/ResetState comunican búfer y recuperación al personaje. Los brazos FP usan copias sin notifies y sin colisión: nunca deben duplicar esos eventos ni aportar otro impacto. Tras cambiar montajes, comprobar los diez ataques, interrupción y recuperación antes de ajustar números.

## Rehén y navegación

`BP_HostageController` ejecuta `BT_Hostage` con `BB_Hostage`. El jugador no posee al rehén: E/RB solicita rescate o reanudación. `BTService_HostageSense` decide condiciones y refugios con ruta completa/local. El árbol hace seguimiento, huida, espera y canalización mediante sus tareas. La apariencia es `SK_RehenSuperviviente` con `ABP_RehenSuperviviente`; cambiarla no autoriza a eliminar el árbol o sustituirlo por movimiento directo.

Claves de flujo: `bRescued` identifica liberación; `bAccompanying`, seguimiento; `bMustFlee`, huida; `bWaiting`, espera a salvo. El aliado no vuelve a seguir sólo porque el jugador se acerque: requiere una interacción segura. Si no hay refugio válido, espera y vuelve a evaluar; no se teletransporta. Jugador/rehén no se atascan entre sí al moverse, pero conservan colisión con mundo y enemigos.

El rehén tiene salud 100 e intervalo de protección ante golpes repetidos inmediatos. `DamageNoticeSerial` sólo aumenta al aceptar daño hostil; no se serializa para que cargar salud no produzca una alerta falsa. Su muerte fija Paso 6; la del jugador, Paso 5. La cinemática presenta el desenlace ya decidido y luego pausa el mundo; no decide quién ganó.

## Encuentros y balizas

Tres instancias de `BP_CombatZone`: dos oleadas de dos orbitadores, dos oleadas de dos embestidores y dos oleadas mixtas. Las entradas requieren escolta cerca y requisitos del encuentro anterior. `Phase`: 0 espera, 1 combate, 2 intermedio, 3 despejado. `CurrentWave` cuenta oleada; `bCleared` confirma cierre. No volver a generar enemigos al restaurar un encuentro completado.

Las dos primeras zonas habilitan sus puertas. La tercera solicita la revelación del último guardián. El orden A/B/C se sortea por intento y permanece oculto hasta terminar u omitir la revelación. No mostrar la siguiente baliza antes, ni usar tres activaciones iguales como sustituto de objetivos distintos.

`BTTask_ActivateBeacon` exige aliado próximo, baliza correcta y ausencia de amenaza. Canaliza 3 s; abortar cancela sin conceder avance. Completar las tres habilita la puerta final. Paso 4 requiere extracción conjunta con ambos vivos; llegar solo sólo muestra una indicación.

## Validación y límites

`docs/validation/ataques-2026-11-17.json`: diez ataques, fixture de contacto con salud preparada. `rehen-superviviente.json`: locomoción/pies con ruta inicial comprobada. `rehen-combate-revision.json`: ataques reales de ambos árboles, protección inmediata y desenlace letal preparado. `pulso-controles-negativos.json`: pared, alcance, munición y bloqueo por escena/pausa. `partida-completa-2026-11-17.json`: recorrido con movimiento, armas, botiquines y pulso normales, sin teletransporte ni cambios de salud/daño. Los intentos fallidos se conservan en validation/intentos.

Estas pruebas del agente no sustituyen mando físico, PC de exposición ni aceptación estética/académica del equipo. Para modificar una IA, revisar primero su ficha, su Blackboard y consumidores, conservar finalización/aborto y repetir la prueba del comportamiento afectado.
