TIME OUT · Unreal Engine 5.6 · Revisión del 17 de noviembre de 2026

Abrir Windows/Terreno.exe y conservar toda la carpeta Windows.
El juego ejecuta Blueprints; no necesita Unreal Editor, Python ni el helper.

MISIÓN
Rescatar al sobreviviente con E/RB. Escoltarlo a tres encuentros de dos oleadas:
orbitadores, embestidores y guardia mixta. Proteger su retirada y recuperarlo
con E/RB cuando espere a salvo. Los primeros encuentros cargan el martillo y
habilitan sus puertas: dos pesados las rompen. El último guardián revela el
orden de balizas; el rehén canaliza 3 segundos en cada una. Resolver las tres,
romper el último sello y llegar juntos a la extracción. Llegar solo no gana.

CONTROLES
WASD/flechas o stick izquierdo: mover. Ratón/stick derecho: mirar.
Espacio/A: saltar. Clic izquierdo/X: ligero. Clic derecho/Y: pesado.
C/pulsar stick derecho: primera/tercera persona.
T/cruceta izquierda: espada. Y/cruceta derecha: martillo.
E/RB: rescatar/reanudar; apuntar para recoger piezas o hablar con BRUNO.
I/SELECT: inventario con tarjetas, cantidades y controles. No pausa.
H/LB: botiquín, cura hasta 35 sin superar 100. No consume a vida completa.
Clic central/RT: pulso de 8 metros, gasta carga, recuperación 0,8 segundos.
P/Esc/START: pausa. B: volver desde opciones/pausa.
Enter/cruceta arriba: leer/cerrar diálogo. Espacio/A: omitir cinemática.
F5 o Guardar en pausa: checkpoint seguro.
Resultado: R/A nuevo intento. Enter/cruceta abajo menú.

BRUNO Y RECURSOS
Cuatro cajas conceden una sola vez +1 botiquín, +3 cargas y +3 créditos.
BRUNO es un robot anclado a la red: no puede salir con los viajeros.
Apuntar a BRUNO y usar E/RB abre su diálogo; repetir convierte 3 créditos en energía y fabrica
1 botiquín en 3 segundos. No es un pago. No consume dos veces mientras
trabaja. Pausa detiene el proceso; checkpoint conserva energía y progreso.

La mesa contiene un botiquín (+1), una celda (+3 cargas) y créditos (+3).
Apuntar y usar E/RB recoge una pieza una sola vez; se conserva al continuar.

DESTRUIBLES
Caja, basurero, banca, barril, auto y fuente. Seis tipos distintos.
Atacar con clic derecho/Y; el martillo mejorado llega con el primer encuentro.
Los sellos de misión son adicionales. Nombre visible al apuntar de cerca.

NOVEDADES
Curación sincronizada con barra. Robot y mesa bloquean al personaje.
Objetos apoyados en el tablero. Pulso con trazo visual y consumo real.
Animaciones sincronizadas con brazos/armas y recuperación en primera persona.
Sobreviviente del proyecto integrado con locomoción y desenlace.
Inventario rediseñado; menús con su diseño existente. Robot BRUNO original.
Sol corregido en lux, luna, estrellas y captura continua del cielo.
Ciclo solar de 8 minutos, guardado y detenido en pausa. Estanque animado.
Se conservan dos IA diferentes, World Partition, Landscape multitextura,
Nanite, modelos de cuatro LOD, seis destruibles y ocho partículas.
BP_CinematicDirector reorganizado visualmente sin alterar su lógica.

GUARDADO Y OPCIONES
Continuar restaura el checkpoint seguro del intento. Incluye salud, poses,
mirada, escolta, cámara, armas, encuentros, puertas, balizas, orden, tiempo,
inventario, recogida, fase solar y fabricación. En peligro conserva el anterior.
R comienza desde cero. Los destruibles decorativos se reconstruyen al cargar.
Opciones aplica distancia, AA, sombras, texturas, resolución, pantalla y volumen.
Las preferencias son independientes del progreso. No se incluyen saves de QA.

DOCUMENTACIÓN EN ESPAÑOL
README.md y docs/LEEME_EQUIPO.md: flujo, controles y lectura por área.
docs/CATALOGO_BLUEPRINTS.md: 102 fichas, incluido el Blueprint del nivel.
docs/ITEMS_Y_DESTRUIBLES.md: efectos, recogida, colisiones y ubicación de los seis.
docs/ROBOT_CIELO_INVENTARIO.md: explicación y reproducción de esta revisión.
docs/REVISION_REQUISITOS_2026-11-16.md: seis capturas, alcance sólo Unreal.
docs/validation: distingue pruebas preparadas de la partida natural completa.
docs/CREDITOS_MODELOS.md: procedencia. Fuentes originales asistidos en el
repositorio, sin atribuir autoría manual ni académica a otro integrante.

LÍMITES
Falta prueba con mando físico y PC de exposición. Los enlaces para mando
están implementados; las pruebas por API no equivalen a pulsaciones físicas.
La valoración artística y la autoría académica corresponden al equipo.
Redes, campañas y promoción quedan fuera del alcance solicitado.
