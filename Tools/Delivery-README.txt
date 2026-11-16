TIME OUT - Entrega del 18 de noviembre de 2026

Abrir Windows/Terreno.exe. Conservar la carpeta Windows completa; el ejecutable
necesita los archivos y subcarpetas que lo acompañan.

MISION
1. Nuevo juego abre el escenario de Ian.
2. Acercarse al rehen. El recuadro inferior indica [E / RB] Rescatar. Pulsar E.
3. Entrar con el aliado cerca a la primera zona. Aparecen dos oleadas de dos
   orbitadores. El aliado huye a un refugio; no hace falta traerlo entre oleadas.
4. Al eliminar al ultimo enemigo, recuperar al aliado con E en el refugio y
   llevarlo a la baliza 1. Solo el rehen puede activarla: se acerca y tarda 3 s.
   Una amenaza interrumpe el proceso. El jugador no activa balizas con E.
5. La baliza equipa automaticamente el martillo, que emite particulas de mejora.
   El primer pesado (clic derecho) deja grietas geometricas;
   el segundo hace trizas la puerta habilitada siguiendo esas mismas divisiones.
   Las otras puertas siguen selladas hasta activar su propia baliza.
6. Llevar al aliado a la segunda zona. Completar otras dos oleadas de dos
   embestidores, recuperar al aliado, escoltarlo a la baliza 2 y romper su puerta.
7. Escoltar al rehen a la baliza 3 y romper la ultima puerta con el martillo.
   Llevar al aliado a la zona azul de extraccion.
   Llegar solo no completa la mision.

El aliado no vuelve a seguir automaticamente al acercarse. Hay que despejar
las amenazas cercanas y pulsar E. Las zonas se activan una sola vez por partida.
El recuadro inferior avisa al acercarse a una zona: entrar con el aliado
siguiendote a no mas de 6 metros inicia sus oleadas. Los mensajes cambian con
el combate, el intermedio y la zona despejada. El rehen tiene una senal E / RB.
Hay unos tres segundos entre sus oleadas. Las primeras dos balizas requieren
despejar su zona y las tres se activan en orden.
El rehen tiene 100 de vida, visible en la barra superior izquierda. Ambos tipos
de enemigo pueden atacarlo. Al verlo a menos de 6.5 metros, se fijan en el rehen
y lo priorizan aunque el jugador este mas cerca. Protege su retirada atacandolos.
Si muere, termina el intento. La barra se vuelve roja si queda poca vida.
La fijacion se libera si deja de ser un objetivo valido o se aleja mas de 18 m.

COMBATE
Orbitador: se mueve alrededor del jugador. Embestidor: prepara una carga,
avanza en linea, se separa unos metros y vuelve al combate.
Ambos reciben golpes ligeros y pesados. Aprovechar preparacion y recuperacion.
Espada ligera: 15 / 15 / 19 / 22. Martillo ligero: 15 / 15.
Todos los pesados: 25 contra ambos enemigos. Golpe enemigo: 13.2 (+120% sobre 6).
Cada ataque alcanza una sola vez a cada enemigo y requiere linea de vision.
La recuperacion del pesado de espada cede la pose a locomocion al volver a moverse.
Recibir dano produce una punzada roja tenue en las esquinas durante 0.38 s.
El rehen elige refugios cercanos con rutas de hasta 18 metros, sin rodear sectores.
Las puertas producen 42 / 56 / 72 fragmentos irregulares de su propia malla.
Los escombros giran y caen, no bloquean al jugador/rehen/camara y duran 4 s.
Los ataques enemigos pueden interrumpirse al causarles dano. Ambos enemigos
conservan la malla Warrior y sus materiales originales, sin armadura naranja.

DIALOGO Y AUDIO
Recuadro negro con borde blanco y texto progresivo. ENTER completa la frase;
un segundo ENTER cierra ese mensaje. Los avisos informativos se ocultan solos.
No pausan el juego. Las interacciones siguen siendo E / RB.
Sobre el rehen aparece E / RB cuando espera a salvo para rescatarlo o llamarlo.
La voz del rehen usa tres silabas sinteticas propias, distintas al sonido narrativo.
Audio propio para texto, avisos, rescate, zona despejada, dano, victoria y derrota;
ambiente tenue en bucle. El audio se limpia al reiniciar o volver al menu.
Las puertas tienen sonido de impacto y rotura; la mejora tiene su propia senal.

CONTROLES
WASD / flechas: moverse. Raton: camara. Espacio: saltar.
Clic izquierdo: ligero. Clic derecho: pesado.
E: interactuar. Mando: RB/R1 para interactuar; X/cuadrado ligero, Y/triangulo pesado.
F5: guardar un punto de control cuando estes a salvo.
Tras derrota: R recupera el ultimo punto de control; Enter vuelve al menu.
Tras victoria: R inicia un nuevo intento; Enter vuelve al menu.
No se ha probado con mando fisico en esta computadora.

GUARDADO Y CONTINUAR
El juego guarda automaticamente al rescatar al rehen, despejar una zona,
activar una baliza o cambiar el estado de una puerta, cuando termina el peligro.
F5 permite guardar manualmente estando a salvo. No guarda durante oleadas,
intermedios, ataques, canalizacion, huida o derrota: conserva el punto anterior.
El HUD confirma el guardado o indica que debes esperar a estar a salvo.
Continuar carga vida y posicion de jugador/rehen, escolta, arma/mejora,
balizas, puertas y zonas. Los enemigos ya eliminados no reaparecen.
Cerrar y abrir el juego conserva el punto de control local.
Nuevo juego inicia desde cero y reemplaza el punto anterior.
Continuar se deshabilita si no hay un guardado compatible y legible.
El ZIP no incluye partidas de las pruebas del equipo.

PENDIENTES DEL EQUIPO
Modelo definitivo de baliza y modelo final del aliado (ambos son provisionales).
Coordinacion de particulas/notifies con Dany; no se editaron sus efectos.
Falta aceptacion del propietario y recorrido manual del paquete definitivo.
Una prueba automatizada completo el recorrido sin teletransportes ni cambios
de vida/dano. Las pruebas aisladas de guardado usan estados de prueba en PIE.

Proyecto fuente: Terreno.uproject, Unreal Engine 5.6.
Detalles y evidencia: docs/HANDOFF.md y docs/validation/fracture-difficulty-2026-11-15.json.
