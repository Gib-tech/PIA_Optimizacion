# Revisión jugable del ciclo, impactos y recorrido

## Hora del mundo

El ciclo anterior empezaba a 35° y duraba 20 minutos. En una partida nueva el sol tardaba 8 min 03 s de juego activo en cruzar el horizonte. Una misión corta podía terminar de día.

Ahora el nivel arranca por la tarde. El atardecer empieza a los **31 s**, el sol cruza el horizonte a los **47 s** y el HUD marca **Noche** a **1 min 02 s**. El primer amanecer comienza a **4 min 31 s**, con salida del sol a **4 min 47 s**. La vuelta completa dura **8 minutos**. Continuar recupera los segundos del checkpoint, así que una partida guardada puede empezar en otra fase.

En `BP_SistemasComplementarios`, el ángulo es `145 + WorldSeconds × 360 / max(DayCycleDuration, 300)`. El reloj integra DeltaSeconds durante el juego activo. Las luces, estrellas y fase se actualizan cada 0,12 s con las curvas suaves del cielo. Pausa, revelación y resultado suspenden el avance. Los focos locales iluminan el refugio también de noche. Desde dentro se aprecia mejor el cambio mirando al exterior.

## Controles y señales

- **Pulso.** Apunta la mira al enemigo o al objeto a menos de 8 m y pulsa la rueda del ratón o RT. Consume una celda cian por disparo, tiene 0,8 s de recuperación y causa 20 de daño. La mira sirve en ambas cámaras. El HUD indica impacto, fallo o falta de celdas. Puedes recogerlas en la mesa del inicio o en las cajas de suministros.
- **BRUNO.** Acércate a menos de 3,2 m con línea de visión. Pulsa E/RB para hablar y vuelve a pulsar mientras está abierto el diálogo para convertir tres créditos en un botiquín. Tarda 3 s. Si estás apuntando directamente a un objeto recogible de la mesa, E recoge primero ese objeto.
- **HUD.** Botiquines, celdas y créditos comparten una fila con sus iconos y cantidades `xN`. I/SELECT abre las fichas. F5 mantiene el guardado seguro en silencio cuando tiene éxito. El HUD conserva la indicación de guardado pendiente o fallido. La alerta de daño del rehén aparece junto al margen derecho, debajo del panel de misión.

## Objetos y efectos

Caja, basurero, banca, barril, auto y fuente tienen **15 de vida**. Un contacto válido de ligero (15), pesado (25) o pulso (20) los rompe de un golpe. Las diez instancias incluyen la banca, el auto y la fuente de demostración LOD y el auto abandonado. Estas cuatro mallas eran estáticas. Conservan sus materiales y geometría hasta el impacto, entonces el Blueprint oculta el modelo intacto y revela una colección Chaos ajustada a sus dimensiones. El auto abandonado reutiliza los fragmentos de la familia de autos.

El arma combina su overlap con un barrido de 220 cm y radio 52 cm durante la ventana activa. Ambos comparten el registro de contactos por ataque. La traza del pulso parte de la cámara y comprueba la distancia del impacto al héroe. El trazo visible sale del personaje. Las puertas conservan los dos pesados de martillo cargado y el desbloqueo de misión. Las cajas de suministros conservan su función de recogida.

Las chispas acompañan el metal del barril, del auto y del basurero. Una ráfaga corta acompaña los fragmentos de caja, banca y fuente. El efecto nace en el centro del volumen roto a escala 0,4. El polvo ambiental tiene un corte de dibujo a 14 m y las hojas a 18 m.

## Agua y recursos

La bajante del edificio de control alimenta la cubeta por un colector y una boquilla. El agua retorna a la superficie por un chorro corto. El borde usa la geometría real de su anillo para que se pueda pisar el interior. La textura normal se desplaza y la boquilla genera anillos continuos. Entrar en el agua produce otra onda en los pies. Caminar dentro renueva la onda cada 0,65 s. Salir o saltar por encima suspende las pisadas. Las posiciones de contacto y los tiempos se envían a una instancia dinámica del material.

Los 41 focos conservan sus sombras y su radio de 14,5 m. La distancia máxima de dibujo baja de 27 a 23 m, con 5 m de desvanecimiento. La escala de resolución de sombra baja de 0,5 a 0,35 y se desactiva la dispersión volumétrica local. Los faroles y escombros pequeños salen del dibujo a 65 m. La fuente LOD usa el material de la fuente fracturable. La banca conserva su textura de concreto con máximo de 1024 px y los escombros usan un máximo de 512 px, ambos con mips y streaming. Se inspeccionaron los materiales de 13 mallas colocadas. Doce tienen cuatro LOD. El auto abandonado conserva su representación de un LOD. No se reexportaron modelos con Blender.

## Reproducción y verificación

Desde la raíz, con `Tools/UnrealPython` en PYTHONPATH, generar `generate_rubric_systems.systems()`, `generate_evaluation_graphs.destructible()`, `generate_delivery_controls.player_camera()`, `generate_delivery_save.manager()` y ejecutar `generate_dialogue_hud.py`. En el editor 5.6 con el helper BPB3 y Nivel_Entrega cargado, ejecutar `install_playability_revision.py` y `prepare_retention_water.py`. Los grafos instalados tienen comentarios en español. Las herramientas de autoría se quedan en el editor.

- **Impactos.** En PIE se probaron 50 combinaciones en tercera persona. Cada una usa una pulsación inyectada por Enhanced Input, sin llamar a ApplyDamage. Se preparan posición, arma y munición. En cada caso se verifica vida de 15 a 0 y eventos de fractura. Para los martillos, originales y copias se probaron en sesiones independientes porque un swing también puede alcanzar al objeto contiguo. Los modos de `verify_playability_attacks.py` se leen de `Intermediate/inspect/revision-jugable/mode`: espada_ligero, espada_pesado, martillo_ligero-originales, martillo_ligero-copias, martillo_pesado-originales, martillo_pesado-copias y pulso.
- **Mecánicas.** `verify_playability_systems.py` comprueba diálogo/conversión con E, entrada, movimiento y salida del agua, y F5 sin aviso de éxito. Con fase inicial preparada en cero, el reloj avanzó a velocidad natural. El HUD cambió a atardecer a 31,30 s y a noche a 62,12 s. El sol llegó a 0 lux. [Resultados](validation/revision-jugable/sistemas.json).
- **Ejecutable.** Desde Continuar, en un perfil aislado junto a BRUNO, dos E convirtieron los tres créditos, el clic central bajó las cargas de tres a dos y F5 guardó. La lectura posterior del archivo confirmó dos botiquines, dos cargas y cero créditos. Se observó la transición natural sin preparar la hora durante la partida. Para verificar la ubicación de la alerta se activó únicamente su temporizador visual en otra sesión. [BRUNO](validation/revision-jugable/paquete-bruno.png) · [Atardecer](validation/revision-jugable/paquete-atardecer.png) · [Noche](validation/revision-jugable/paquete-noche.png) · [Alerta del rehén](validation/revision-jugable/paquete-alerta-derecha.png).
- **Rendimiento.** Win64 Development a 1280 × 720 sobre Ryzen 5 3600 y RTX 3060 Ti. La captura de 1201 fotogramas en la escena inicial registró una mediana de 13,92 ms y un percentil 95 de 17,06 ms. Es una medición local del inicio del nivel. El empaquetado terminó en 178,29 s con cero errores y la advertencia previa de Scale en Spawn System Attached. [Medición y guardado](validation/revision-jugable/ejecutable.json) · [Luces, mallas, texturas y partículas](validation/revision-jugable/recursos.json).
