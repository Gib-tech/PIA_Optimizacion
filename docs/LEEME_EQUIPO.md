# Guía del equipo · Time Out

El HUD de partida agrupa los recursos en columna y se oculta durante las cinemáticas. El estanque está junto al refugio de rescate. [Controles, cambios y pruebas](REVISION_JUGABLE.md).

> **Versión actual.** Ciclo de 8 min desde la tarde, BRUNO por proximidad y diez objetos rompibles de un golpe. La revisión de jugabilidad reúne los valores y pruebas actuales. [Ver controles y cambios](REVISION_JUGABLE.md).

> **Revisión anterior, 17/11 — cielo, luces y ataques.** El ciclo dura 20 minutos, con mezcla gradual de sol/luna/ambiente. Se añaden 41 luminarias de pared. Los seis props aceptan ligero/pesado con espada o martillo y pulso, sin mejora obligatoria. Las puertas conservan sus reglas de misión. Ver [CICLO_LUCES_Y_ATAQUES.md](CICLO_LUCES_Y_ATAQUES.md); prevalece sobre los valores históricos siguientes.

> **Estado vigente, 17/11 — ítems, colisiones y seis destruibles comprobados.** Ver [ITEMS_Y_DESTRUIBLES.md](ITEMS_Y_DESTRUIBLES.md). La curación actualiza salud y barra; los tres objetos de la mesa son recogibles persistentes. Alcance: requisitos de Unreal y documentación técnica en español. Redes, campaña, video promocional y documentos administrativos quedan fuera por indicación expresa del propietario. Se conserva el diseño de los menús; se rediseña el inventario. BRUNO usa modelo mecánico original, convierte 3 créditos en energía y fabrica 1 botiquín en 3 s. Ver [ROBOT_CIELO_INVENTARIO.md](ROBOT_CIELO_INVENTARIO.md). El texto posterior conserva historial cuando describe otra revisión.

Esta es la entrada a la documentación técnica vigente en español. Las notas de `HANDOFF`, `PROJECT_CONTEXT`, `GOVERNANCE` y `WORK_ITEMS` conservan decisiones e historial; cuando una sección antigua contradiga una actualización fechada, prevalece la actualización y su evidencia. La petición actual amplía el trabajo a todos los requisitos de las seis imágenes, al rehén, a primera persona y a documentar los Blueprints.

## Abrir y reconocer la versión correcta

Usar Unreal Engine 5.6 y abrir `Terreno.uproject`. El mapa de trabajo es `/Game/ThirdPerson/Maps/Nivel_Entrega`. El menú del ejecutable es `/Game/LevelMenu/MainMenuLevel`. El nivel final sobrescribe el modo global con `BP_GameMode_Entrega`, que selecciona `BP_PlayerEntrega` y `BP_HUD_Entrega`. No demostrar la entrega desde el antiguo ThirdPersonMap.

El proyecto conserva packs y prototipos. Que un asset exista no significa que participe en la misión. El [catálogo](CATALOGO_BLUEPRINTS.md) identifica cada ruta, su padre, responsabilidad, entradas y referencias exportadas; es importante consultar la ruta completa porque hay menús con nombres repetidos.

## Flujo de una partida

1. **Nuevo juego.** El menú fija la intención en `BP_GameInstance`, abre Nivel_Entrega y reproduce la introducción. Continuar valida un checkpoint y abre la misión sin repetirla.
2. **Rescate.** El jugador se acerca al sobreviviente y usa E/RB. `BP_Hostage.Interactuar` escribe el estado de rescate/seguimiento. `BT_Hostage` decide seguir; no se controla al aliado como un segundo jugador.
3. **Primer encuentro.** Entrar con el aliado cerca activa dos oleadas de dos orbitadores. El servicio del rehén detecta peligro y el árbol elige huir a un refugio local. Al limpiar, hay que acercarse y llamarlo de nuevo.
4. **Primer sello.** Despejar carga/equipa el martillo. Dos pesados rompen la puerta: primer golpe deja grietas geométricas y el segundo desprende las piezas correspondientes.
5. **Segundo encuentro.** Dos oleadas de dos embestidores. Tienen árbol y patrón propios: preparación, carrera, golpe cercano y retirada. Recuperar al aliado y romper la segunda puerta.
6. **Guardia final.** Dos oleadas mixtas antes del patio. El último guardián revela la permutación real de A/B/C mediante `LS_Revelacion`. Hasta terminar u omitir, el orden permanece oculto. El reloj y la escolta se suspenden durante esa escena.
7. **Balizas.** A/B/C son lugares fijos; su orden cambia por intento. Sólo el rehén canaliza tres segundos la siguiente baliza válida, sin amenaza. Un enemigo interrumpe; visitar una fuera de orden no concede progreso.
8. **Extracción conjunta.** Completar las tres habilita la última puerta. Romperla y llegar con el aliado a la salida azul. Llegar solo no gana. La muerte de cualquiera pierde la misión y presenta su cinemática correspondiente.

Son objetivos distintos: rescatar/escoltar, superar encuentros y abrir paso, resolver una secuencia y extraer a ambos. Las balizas son parte de la secuencia; no se presentan como tres misiones distintas sólo por repetir una interacción.

## Qué Blueprint manda en cada sistema

`BP_DirectorEntrega` coordina misión, secuencia, tiempo y resultado. Las instancias de `BP_CombatZone` gestionan sus propias oleadas y comunican su finalización. `BP_BeaconEntrega` valida la canalización y `BP_DestructibleDoor` valida el martillo/estado de carga. El director no calcula daño de armas ni decide los movimientos de la IA.

`BP_ThirdPersonCharacter` es la base del jugador: Enhanced Input, locomoción, salto, combos y montajes. `BP_PlayerEntrega` añade contactos seguros, recuperación, daño a puertas/Chaos y presentación de primera persona. `BPC_Health` posee su salud. Conservar los nombres de eventos llamados por AnimNotifies; renombrarlos sin actualizar los notifies rompe la recuperación del combo.

`BP_BaseEnemy` ejecuta acciones comunes y el orbitador. `BP_ChargerEnemy` especializa al embestidor. Cada uno tiene controlador, Behavior Tree y Blackboard propios. Los servicios escriben percepción/objetivos; las tareas hacen una acción y terminan/abortan. El Tick del actor enemigo no reemplaza el árbol.

`BP_Hostage` conserva salud, interacción y eventos de escolta. `BP_HostageController`, `BT_Hostage`, `BB_Hostage`, su servicio y sus tareas deciden seguimiento, huida, espera y canalización. La apariencia se puede reemplazar sin rehacer el árbol.

`BP_SistemasComplementarios` lleva suministros recogidos, botiquines, cargas, créditos, inventario, conversión con el robot y fase del día. `BP_TecnicoTemporal` representa a Bruno, un NPC inmóvil de apoyo. El rehén y Bruno son los dos NPC con diálogo; Bruno no cuenta como enemigo avanzado.

`BP_DeliveryInterface` administra pausa/opciones/foco; los widgets presentan botones y delegan. `BP_DeliverySaveManager` es el único escritor del checkpoint final. `BP_HUD_Entrega` dibuja estados, señales y textos; dibujar una señal no concede objetivos. `BP_CinematicDirector` suspende/restaura presentación sin alterar reglas de victoria/daño.

## Estados que no deben confundirse

- `Paso`: 0–3 avance de la secuencia, 4 victoria, 5 derrota del jugador, 6 derrota del rehén.
- `Phase` de cada zona: 0 espera, 1 combate, 2 intermedio, 3 completada. `CurrentWave` identifica la oleada; `bCleared` es la confirmación del encuentro.
- `bRescued`, `bAccompanying`, `bWaiting`, `bMustFlee` del Blackboard del rehén distinguen rescate, seguimiento, espera y amenaza. Esperar a salvo requiere E/RB para continuar.
- `IsAttacking`/`CurrentState` gobiernan la acción del jugador. `bLightAttackActive`, montaje/posición y `WeaponHitbox` delimitan daño; una malla visible no significa que el golpe esté activo.
- `bActivated` de una baliza no equivale a `bUnlocked` de una puerta. Las dos primeras se habilitan por sus encuentros; la última por la secuencia resuelta.
- `bNarrativePaused` suspende misión durante la revelación. Pausa de menú detiene el mundo completo. Inventario es una consulta y no pausa la partida.

## Primera persona y animaciones

La cámara FPC sigue la cápsula a altura de ojos y orientación del control, sin seguir los giros de la cabeza de un montaje. La tercera persona conserva brazo con colisión. `BrazosFP` es una malla ligera extraída del personaje del proyecto; conserva esqueleto/pesos y excluye torso/cabeza/piernas. Muestrea copias de secuencias sin notificaciones: mantiene una postura preparada en reposo y sigue la posición temporal del montaje real al atacar. Las copias se mezclan desde la guardia durante 0,12 s y recuperan la guardia durante los últimos 0,18 s del tramo efectivo; las secuencias originales no cambian. La espada FP compensa el pivote del modelo para sujetarla en la mano. Las copias no avanzan solas y el muestreo no dispara notifies; no aportan una hitbox.

`EspadaFP`, `MartilloFP` y la luz acotada de canal exclusivo son presentación para el propietario de la cámara. Las armas originales, su alcance y sus ventanas permanecen como autoridad de daño. Cambiar de vista o restaurar un checkpoint sincroniza visibilidad. Los desplazamientos visuales por velocidad son pequeños; la cámara no gira por la animación de ataque.

No modificar los tiempos de contacto para compensar un error visual. Primero comprobar socket, escala, pose y encuadre. Mantener interrupción, fin de montaje y cambio de arma con hitbox desactivada fuera de la ventana.

El rehén usa `SK_RehenSuperviviente`, copia de `Survival_Character/Meshes/SK_Survival_Character`, un recurso que ya existía. `SKEL_RehenSuperviviente` y `ABP_RehenSuperviviente` conservan la compatibilidad con las animaciones Manny de la escolta. El pack original no se reemplaza ni se acredita como modelo propio del equipo. Probar pies, reposo, caminar, correr/huir, canalización, daño y muerte cada vez que cambie apariencia.

## Controles y suministros

- Mover: WASD/flechas / stick izquierdo. Mirar: ratón / stick derecho. Saltar: Espacio / A.
- Ligero: clic izquierdo / X. Pesado: clic derecho / Y. Cámara: C / pulsar stick derecho.
- Espada: T / cruceta izquierda. Martillo: Y / cruceta derecha. Interacción: E / RB.
- Pausa: P/Esc / START. En menús, B vuelve a la pantalla anterior; botones se seleccionan con foco y navegación estándar de UMG.
- Inventario: I / SELECT. Botiquín: H / LB; consume una unidad y recupera hasta 35, con máximo 100. No consume si ya tienes vida completa.
- Pulso: clic central / RT; consume una carga, tiene recuperación y sólo daña al enemigo alcanzado por una traza visible dentro de ocho metros. No sustituye los dos ataques cuerpo a cuerpo.
- F5 o Guardar desde pausa: checkpoint seguro. Enter / cruceta arriba: completar/cerrar diálogo. Espacio / A: omitir cinemática.
- En desenlace: R / A inicia otro intento y Enter / cruceta abajo vuelve al menú. Los alias de mando y su verificación concreta se registran en la revisión de requisitos; no confundir inspección de enlaces con una prueba de mando físico.

Cuatro cajas de suministros se recogen una sola vez: +1 botiquín, +3 cargas y +3 créditos. El inventario muestra cantidades. Apuntando a BRUNO dentro de 270 cm, E/RB explica que es un robot anclado a la red. Repetir convierte tres créditos en energía y fabrica un botiquín en tres segundos. Un trabajo activo no admite otro consumo. La pausa detiene proceso y animación; el checkpoint conserva energía y progreso. No cobra por ayudar ni puede abandonar su pedestal. El estado de recogida y cantidades se guarda con la misión para evitar duplicación al continuar.

La instancia colocada de `BP_SistemasComplementarios` debe tener Auto Receive Input Player 0 y prioridad 5. La inicialización también llama EnableInput cuando ya existe PlayerController. Cambiar sólo el CDO no actualiza necesariamente una instancia antigua: la prueba del paquete detectó esa diferencia y se corrigió. Verificar una tecla real además de llamar directamente al evento.

## Guardado y compatibilidad

`TimeOut_Delivery_v1.sav` usa esquema 2. Guarda salud/transforms de aliados, escolta, arma/mejora, cámara, zonas/oleadas, puertas, balizas, permutación, tiempo e inventario/recogida/fase horaria. Las revisiones aditivas evitan invalidar por completo checkpoints anteriores. Campos nuevos de un archivo antiguo toman valores iniciales; no se inventa munición previamente recogida.

Un cambio de hito o recurso pendiente se guarda cuando es seguro. No se serializa una oleada a mitad. La posición guardada corresponde al momento seguro del checkpoint, no necesariamente al último fotograma antes de cerrar. Los objetos decorativos Chaos reaparecen al cargar; las puertas de misión conservan destrucción/grietas.

Gráficos y pantalla están en GameUserSettings; volumen en `TimeOut_Options_v1`. Son independientes del progreso. En pruebas se respaldan las partidas del usuario y se restauran al terminar. No distribuir saves de QA con el ejecutable.

## Escenario, agua y optimización

El nivel usa Landscape multitextura y World Partition. Actores de misión y props que requieren continuidad permanecen residentes; eso no desactiva culling, oclusión, LOD ni Nanite. Arquitectura y escaneo de auto usan Nanite; los modelos de demostración de LOD clásico conservan cuatro niveles diferentes.

Las luces locales están junto a sus fuentes y tienen radios/distancias propios. El ciclo solar usa tiempo de juego y se detiene al pausar. La superficie de agua del estanque tiene normal desplazada y material propio; la cubeta visible explica su contención. No se presenta como sistema de natación.

Niagara ambiental tiene límites de visibilidad y reanudación. Chaos se activa al romper, no en todos los props desde el inicio. Las piezas ignoran peones/cámara y expiran. Para medir draw calls, comparar el mismo punto/calidad/resolución con `stat RHI` y `stat SceneRendering`; registrar hardware y condiciones, no sólo un número aislado.

## Modificar, regenerar y probar

1. Consultar ficha del asset y generador que lo crea. Cambiar sólo la responsabilidad correspondiente; conservar contratos de eventos, Blackboard y guardado.
2. Los scripts locales `generate_*.py` producen texto revisable en `Intermediate/inspect/delivery_graphs`. Los scripts `prepare_*` crean recursos/campos; `install_*` instalan gráficos mediante el helper editor-only. Algunos preparadores son migraciones de una sola ejecución: leerlos antes de repetirlos.
3. El helper se carga con `Tools/UnrealPython/launch_cinematic_editor.ps1`. Nunca incorporarlo como módulo de gameplay. Instalar grafos sólo con PIE detenido y todo guardado.
4. Compilar consumidores tras cambiar una clase compartida. `compile_project_blueprints.py` registra los estados exportados. Después ejecutar las pruebas de comportamiento relacionadas.
5. `audit_project_blueprints.py` exporta todos los Blueprints; `Tools/document_blueprints_es.py` regenera catálogo/fichas. No editar a mano los listados extraídos y esperar que sobrevivan a regeneración: ampliar el diccionario editorial del generador.
6. Usar `Tools/Build-Delivery.ps1` con editor cerrado para cook/build/stage. Confirmar menú, Nueva partida, Continuar, opciones y misión en el paquete final. El resultado actual está en los informes de validación, no implícito en esta receta.

Las pruebas preparadas pueden mover actores o preparar salud para aislar una condición y lo declaran en su informe. Una partida de aceptación debe recorrer la misión mediante movimiento/interacciones/ataques normales, sin teletransporte, invulnerabilidad ni modificación de daño. Las pruebas del agente no son aprobación del propietario ni de Adame.

## Lectura por área

Programación: esta guía, catálogo, `AI_REQUIREMENTS` y esquema de guardado. Animación: primera persona/rehén, fichas de ABP y notifies, ventanas de ataque en `AI_REQUIREMENTS`. Arte: `MODELOS_EQUIPO`, `ESCENARIO_COMPOUND`, créditos y manifiestos de `Tools/ArtSource`. Coordinación: WORK_ITEMS, requisitos de Unreal, estado técnico y pendientes de pruebas de hardware. QA: `docs/validation`, guía de demostración y scripts `verify_*`/`playthrough_*`.
