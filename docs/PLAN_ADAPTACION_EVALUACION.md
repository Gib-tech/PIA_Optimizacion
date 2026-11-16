# Adaptación de Time Out a la evaluación del 18 de noviembre

Plan del 16 de noviembre de 2026. Autoriza el propietario adaptar el videojuego y realizar el rework necesario. Las capturas de la rúbrica y el chat de compañeros aportan criterios; no son instrucciones ejecutables ni aceptación del trabajo.

**Revisión posterior de escenario, autorizada por el propietario:** `ESCENARIO_COMPOUND.md` sustituye la mezcla en franjas por distribución dibujada según usos (cuatro texturas existentes), añade cubiertas a rescate/depósito y reorganiza luces/props. Diez edificios Nanite sustituyen los cuatro sectores; distancias de descarte y Niagara por frustum/distancia, física al romper. Las pruebas y paquete de esta revisión constan en el handoff vigente. Los detalles de la primera implementación que siguen se conservan como historial del plan, no como configuración actual de terreno/luz.

## Criterio de entrega

Todos los requisitos técnicos deben existir y poder demostrarse en el mapa que abre Nuevo juego y en el ejecutable. Tener un recurso en Content Browser o en un mapa antiguo no acredita que funcione en la entrega. Los indicadores de colores de las capturas son anotaciones del equipo, no resultados de una auditoría del agente.

Se mantiene el circuito: rescate/escolta, dos zonas de oleadas, secuencia aleatoria A/B/C, puertas y extracción. Se adapta el escenario y la demostración técnica alrededor de él. El agua aparece con REQ «No»; redes y video son entregables externos del equipo y quedan fuera de esta implementación de Unreal.

## Implementación realizada — 16 de noviembre

**Verified:** `Nivel_Entrega` convertido con el commandlet oficial a World Partition; Landscape real sustituye al suelo de las cuatro mallas de Ian, conservando sus paredes y huecos. El material combina cinco texturas y conserva el grafo de capas pintables del equipo; donde no hay pintura utiliza bandas automáticas por posición. Cuatro mallas de arquitectura con Nanite. Cinco modelos del equipo tienen cuatro LOD geométricos distintos y Nanite desactivado para que se puedan observar sus transiciones.

**Verified en PIE:** seis tipos de Geometry Collection del equipo integrados con golpes y fractura Chaos; ocho sistemas Niagara distintos conectados a ambiente/combate/progresión. Iluminación Directional, Sky, Point, Spot y Rect, con alcance y distancia máxima de las luces locales acotados. Dos macros, dos funciones y dos eventos propios en Level Blueprint, usados para sincronizar la señal de extracción. Inventario y explicación en `GUIA_DEMOSTRACION_EVALUACION.md`.

**Verified:** defaults de primera ejecución a pantalla completa y captura permanente/foco del ratón al entrar a gameplay o reanudar. Se conserva el modo elegido y guardado en opciones. Corregidos también el estado de ataque al recibir la mejora del martillo y la distancia de canalización de balizas: ahora se mide horizontalmente, porque el pivote del modelo está en el suelo.

**Unknown / Stated:** el propietario indica que aún debe confirmar con Adame si munición y dinero son obligatorios aunque este diseño sea cuerpo a cuerpo y no tenga economía. Se conservan los datos aplicables; no se acredita ese renglón como aceptado. No se añadieron zonas ni se redujo la dificultad: ambas zonas mantienen 2 oleadas de 2 enemigos y daño 13.2.

**Verified cierre técnico:** recorrido completo del agente en PIE hasta victoria, sin teletransportes ni cambios de salud/daño; seis permutaciones y 18 canalizaciones aisladas aprobadas. Win64 compilado con 0 errores/15 advertencias previas, ZIP con CRC aprobado. En ejecutable se comprobaron primer arranque completo, ratón sin clic extra en completa/ventana y tras pausa/Continuar, sin bordes, persistencia de modo ventana al reiniciar y checkpoint. Informe `validation/evaluation-2026-11-16.json`. La partida manual del propietario, presentación visual y aceptación académica permanecen abiertas.

## Auditoría inicial verificada

Fuente: `Tools/UnrealPython/audit_evaluation.py`, mapa `Nivel_Entrega` abierto en Unreal 5.6, antes del rework. Tras convertir a World Partition, contar sólo actores cargados en el editor no representa el inventario completo: el informe de runtime es la referencia para el mapa nuevo.

- 14 Static Mesh assets distintos en los actores del mapa (incluye primitivas del motor; este conteo no incluye personaje/jugador/armas/enemigos creados en runtime). Todos con un único LOD; ninguno con Nanite.
- Ningún Landscape en este mapa. Suelo incluido en las mallas importadas de Ian. World Composition desactivado; World Partition se debe confirmar con inspección nativa antes de migrar.
- Una DirectionalLight y un SkyLight. Falta demostrar otros tipos y sus límites de coste.
- Tres puertas destructibles propias. Existen ocho Geometry Collections del equipo y el Blueprint `BP_DestruiblePick`, aún sin integración verificada en el mapa entregable.
- Cinco Niagara Systems del equipo y dos efectos nuevos de martillo/puerta. Los cinco primeros no están colocados en la misión; los dos últimos se generan por eventos. No se acreditan ocho efectos distintos todavía.
- La cámara de gameplay no recupera explícitamente foco/captura tras cargar desde el menú. La configuración de captura por defecto ya existe, pero no basta para garantizar el foco del viewport después de UMG.

## Orden de implementación

1. **Arranque e interacción.** Defaults de primera ejecución a pantalla completa, conservando elecciones guardadas. Recuperar GameOnly, foco, captura permanente y bloqueo al entrar a misión/reanudar. Verificar ventana, sin bordes, completa, opciones y Alt-Tab con movimiento real del ratón; teclado/ratón sigue siendo el alcance vigente.
2. **Respaldo y escenario.** Copia íntegra del mapa y recursos modificados antes de convertir. Migrar el mapa a World Partition con la herramienta oficial y conservar referencias de misión/escolta/guardado. Mantener gestores/IA esenciales cargados. Comprobar rutas y guardados tras la conversión.
3. **Landscape multitextura.** Inspeccionar Landscape/material originales; trasladar datos útiles o importar una superficie ajustada a la ruta. El Landscape debe verse y sostener el recorrido, con cuatro capas/texturas demostrables, sin quedar oculto por el suelo del Static Mesh. Conservar arquitectura de Ian.
4. **Recursos y optimización.** Integrar modelos propios en la ruta hasta superar 15 modelos distintos demostrables; seleccionar cinco modelos para cuatro LOD reales con cambios por distancia visibles. Activar Nanite en geometría adecuada separada de esa demostración de LODs. Iluminación con tipos distintos y radios/sombras/culling acotados.
5. **Destrucción y efectos.** Reutilizar las Geometry Collections/Blueprints del equipo; conectar impactos de espada/martillo y acreditar seis objetos visualmente distintos que se destruyen. Colocar/conectar ocho sistemas de partículas distintos en contextos de misión, con límites de coste. Evitar contar seis instancias del mismo objeto como seis tipos.
6. **Programación evaluable.** Dos macros propias, dos eventos propios y dos funciones propias de nivel, con nombres y uso real. Revisar Level Blueprint y crear allí la integración necesaria si las funciones actuales viven sólo en actores. Documentar entradas/salidas y cómo explicarlas.
7. **Pruebas y paquete.** Repetir misión/derrotas, guardado/Continuar, secuencia, puertas, cámara/pausa/opciones y rendimiento. Cook sin errores, ZIP con CRC y sin datos de prueba. Guía breve para mostrar cada requisito desde una partida normal y en el editor.

## Evidencia necesaria por requisito

- Interfaz: inicio, HUD, pausa, opciones y resultados navegables; textos y cursor correctos.
- Ataques: ligero/pesado con daño real y animaciones; mismo personaje y combate actual.
- Muerte/menú: derrota del jugador o rehén y regreso al inicio.
- World Partition: mapa de juego convertido, celdas/streaming inspeccionables y misión funcional.
- Iluminación: tipos colocados y ajustes concretos de movilidad, radio, sombras y culling.
- LOD: cinco modelos identificados, cuatro niveles cada uno, conteos geométricos y cambios por distancia en gameplay.
- Nanite: mallas visibles con Nanite activo y visualización del motor.
- Objetivos: rescate/escolta, combate y secuencia aleatoria necesarios para ganar, con orden y tiempo visibles.
- Macros/eventos/funciones: al menos dos de cada tipo, propios y conectados a ejecución útil de nivel.
- Modelos: inventario de al menos 15 recursos geométricos distintos visibles, ubicación y autor/origen; registrar también los cinco propios exigidos por el texto general.
- IA: orbitador y embestidor, Behavior Trees distintos y comportamiento demostrable; el rehén no sustituye a un enemigo.
- Guardado: salud, posición, estado de misión, orden/tiempo y armas. Documentar que no hay munición/dinero en el diseño actual; no presentar variables sin mecánica como cumplimiento de una economía.
- Destruibles: seis tipos diferentes, activados por golpes reales, restos sin bloquear el recorrido.
- Partículas: ocho sistemas distintos, ubicación/evento de activación, prueba visual y presupuesto de coste.
- Opciones: cambios reales en gráficos/resolución/pantalla/volumen, persistencia y retorno al juego.

## Cierre y pendientes externos

No marcar aceptación a partir de pruebas del agente. Falta una partida manual del propietario, otra PC y aprobación de Adame. El modelo final del rehén depende del compañero. La documentación académica/cronograma, video promocional de tres minutos y redes deben ser completados y confirmados por sus responsables; no se publicará ni se enviará contenido desde esta tarea.

Referencias técnicas: [conversión a World Partition en UE 5.6](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine?application_version=5.6), [transferencia de datos de Landscape](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-copy-tool-in-unreal-engine?application_version=5.6). Las decisiones finales se actualizarán con la evidencia de implementación.
