# Time Out · Proyecto de Unreal Engine 5.6

Juego de acción y rescate temporal, desarrollado con Blueprints. Abrir `Terreno.uproject`. El editor inicia en `Nivel_Entrega`; el ejecutable inicia en el menú principal.

En una partida nueva el primer ocaso cruza el horizonte a los 47 segundos. BRUNO responde a E/RB por proximidad, el HUD muestra los objetos en columna durante el juego y los diez objetos rompibles aceptan cualquier ataque. [Mecánicas, controles y pruebas](docs/REVISION_JUGABLE.md).

La documentación vigente para todo el equipo está en [LEEME_EQUIPO](docs/LEEME_EQUIPO.md). Contiene el flujo de la misión, responsabilidades, controles, guardado, animaciones, pruebas y orden recomendado de lectura.

- [Catálogo completo de Blueprints](docs/CATALOGO_BLUEPRINTS.md): una ficha por ruta, incluidas interfaces, widgets, AnimBlueprints y recursos de ejemplo.
- [Requisitos de las seis capturas](docs/REVISION_REQUISITOS_2026-11-16.md): criterios, implementación y evidencia; no confunde funcionamiento con aprobación académica.
- [Guía de demostración](docs/GUIA_DEMOSTRACION_EVALUACION.md), [créditos](docs/CREDITOS_MODELOS.md) y [evidencias](docs/validation/).
- [IA y combate en español](docs/IA_Y_COMBATE.md): decisiones de árboles, contacto, escolta, encuentros y contratos que no deben romperse.

El código de `Tools/UnrealPython` y `Tools/Blender` sirve para crear, inspeccionar y verificar assets. El juego empaquetado ejecuta Blueprints; no necesita Python ni el helper de editor.

La revisión actual conserva los menús y mejora el inventario. BRUNO es un robot original con conversión de energía y fabricación persistente. El ciclo solar corrige las unidades de intensidad y añade noche estrellada/luna. [Cambios, flujo y pruebas](docs/ROBOT_CIELO_INVENTARIO.md). Los requisitos ajenos a Unreal quedan fuera del alcance solicitado.

La revisión de [ítems, colisiones y destruibles](docs/ITEMS_Y_DESTRUIBLES.md) corrige la barra de curación, convierte las piezas de la mesa en recursos recogibles persistentes, bloquea el paso por robot/mesa y comprueba los seis tipos mediante ataques físicos.
