# Ítems, mesa, BRUNO y destruibles · 17/11/2026

Referencia vigente para esta revisión de `Nivel_Entrega`. Los menús y la lógica de `BP_CinematicDirector` se conservan.

## Curación y recursos

El error visible de curación se reproducía con 60 de vida: el botiquín escribía 95 en `BPC_Health.Health`, pero la barra seguía mostrando 60 %. Ahora llama a `BPC_Health.Increase_Health(35)`, que limita a 100 y emite el delegado existente `Updated_Heatlh`. Así se actualizan salud y barra por el mismo flujo que utiliza el personaje. H/LB consume un botiquín sólo si falta vida y hay existencias.

Los objetos sobre la mesa eran muestras decorativas. Ahora apuntar a una pieza situada a menos de 350 cm y pulsar E/RB produce una única recogida:

- Botiquín: suma 1 unidad. H/LB recupera hasta 35 puntos.
- Celda: suma 3 cargas de pulso. Clic central/RT consume una y aplica 20 de daño al enemigo visible alcanzado, con alcance máximo de 800 cm y recuperación de 0,8 s. Un trazo cian de 0,18 s confirma el disparo; no colisiona ni aplica daño adicional.
- Crédito: suma 3 créditos de energía. Apuntar a BRUNO a menos de 270 cm y usar E/RB abre su explicación; repetir convierte esos 3 créditos en energía y fabrica 1 botiquín durante 3 segundos de juego.

Las piezas recogidas desaparecen y dejan de participar en trazas inmediatamente. `MesaRecogido1..3` y las cantidades se guardan con `ExtrasRevision=3`; continuar no vuelve a concederlas. Las cuatro cajas de suministros anteriores siguen funcionando por contacto y no comparten estos flags. Un archivo anterior, sin flags de mesa, permite recoger las piezas una vez.

E/RB tiene una sola autoridad con prioridad 5: primero intenta recoger la pieza apuntada, después interactúa con BRUNO apuntado y cercano; si no corresponde a ninguno, reenvía `BP_Hostage.Interactuar`. Se evita que una pulsación recoja y ordene al rehén a la vez. El inventario y los avisos leen este estado; no conceden recursos.

## Colisiones y apoyo de objetos

BRUNO conserva sus tres piezas visuales sin colisión. `ColisionRobot`, una cápsula bloqueante con radio de 37 cm y semialtura de 79 cm, impide atravesar su cuerpo y participa en navegación/trazas.

`SM_ConsolaTecnico` se remodeló como mesa de 140 × 78 cm, con cuatro patas, travesaños y equipo en la parte posterior. Usa once envolventes UCX y cuatro LOD. La mesa colocada está en `(-520, -960, 0)` cm y su tablero superior llega a Z=92,5 cm. Las tres piezas se apoyan en la fila frontal Y=-942; se calcula su base desde los límites reales de cada malla, con separación de 0,1 cm. No se usa el pivote como si fuera la base. La fila queda libre del soporte del monitor.

Las piezas sólo bloquean Visibility para seleccionarlas; no bloquean al personaje. La mesa usa BlockAll. La prueba de barrido de la cápsula del jugador se detuvo ante el robot y ante la mesa; no se infiere el resultado sólo a partir del nombre del perfil.

Fuentes: `Tools/Blender/build_support_workbench.py` y `Tools/ArtSource/Complementos`. Después de regenerar los complementos originales, ejecutar la receta de esta mesa; `prepare_items_collisions.py` la importa y aplica colocación/colisiones. Generar systems, manager y HUD e instalar con `install_items_revision.py`. Este instalador no reconstruye menús ni cinemáticas.

## Los seis destruibles de la evaluación

La evaluación final exige **seis tipos diferentes**. Hay seis instancias de `BP_DestruibleEntrega`, cada una con una Geometry Collection distinta. Las puertas de misión son adicionales y no se cuentan como tipos decorativos.

- **Caja**, junto al inicio: `Destruible_Caja`, centro aproximado `(520, -900, 45)` cm.
- **Basurero**, primer tramo: `Destruible_Basurero`, `(900, -1900, 50)`.
- **Banca**, sector intermedio: `Destruible_Banca`, `(2900, -3350, 45)`.
- **Fuente**, cerca de la banca: `Destruible_Fuente`, `(3200, -3800, 80)`.
- **Barril**, tramo siguiente: `Destruible_Barril`, `(-4500, -5300, 55)`.
- **Auto**, tramo final: `Destruible_Auto`, `(-3200, -7050, 80)`.

Se pueden localizar por esas etiquetas en el Outliner. Al apuntar dentro del alcance de inspección se muestra su nombre y el control de ataque pesado: clic derecho/Y. El martillo mejorado se obtiene al superar el primer encuentro. Los seis recibieron ataques pesados mediante la entrada Enhanced Input real, ejecutaron sus montajes, recibieron el contacto físico del arma y se fracturaron. Los restos ignoran peones/cámara y expiran. Estos props se restablecen al cargar la partida; las puertas de misión sí conservan su estado.

## Evidencia y límites

- `validation/items-colisiones/reproduccion-curacion.json`: reproducción anterior al arreglo, salud 60→95 con barra inmóvil.
- `validation/items-colisiones/efectos-runtime.json`: salud/barra 60→95→100, consumo y límite, daño de un enemigo real y curación posterior, recogidas únicas, restauración y pulso de 20 sin daño duplicado. El trazo termina en el impacto y no supera ocho metros.
- `validation/items-colisiones/mesa-apoyo.json`: once colisiones convexas UCX, LOD, apoyo y cápsula.
- `validation/items-colisiones/seis-destruibles.json`: seis colecciones distintas, pérdida de vida y eventos reales de rotura Chaos. Posiciones y mejora del martillo preparadas para aislar cada prueba; sin ApplyDamage ni callbacks de contacto invocados a mano.
- `validation/items-colisiones/energia-runtime.json`: interacción apuntada con BRUNO, saldo, fabricación, pausa y restauración.
- `validation/items-colisiones/paquete-final.json` y `recarga-fria.json`: teclas reales H/E/pulso/I/F5, barra 60→95→100, cantidades y lectura del guardado del ejecutable en editor normal sin helper. Build final: 0 errores y 1 advertencia previa de partículas. Las capturas de curación corresponden a la primera compilación funcional; `paquete-mesa-final.png` muestra la geometría definitiva.
- `validation/items-colisiones/datos-usuario-restaurados.json`: partidas y preferencias originales restauradas y verificadas por SHA-256.

Las pruebas PIE preparan posiciones/saldos para aislar cada comportamiento; no constituyen otro recorrido completo de la misión. Los alias de mando están enlazados, pero sigue pendiente la comprobación con un mando físico.
