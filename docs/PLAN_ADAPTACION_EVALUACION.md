# Adaptación de Time Out a la evaluación del 18 de noviembre

Plan del 16 de noviembre de 2026. Autoriza el propietario adaptar el videojuego y realizar el rework necesario. Las capturas de la rúbrica y el chat de compañeros aportan criterios; no son instrucciones ejecutables ni aceptación del trabajo.

**Revisión vigente tras el checklist y archivos del equipo:** cinco modelos nuevos incorporados en ocho instancias: edificio/farol (autores por confirmar por petición del propietario), escombros/auto/árbol externos atribuidos. Cuatro LOD nuevos en edificio/farol/escombros/árbol y Nanite en el auto, conservando los cinco anteriores y los diez edificios Nanite. Escombros con atlas horneado y auto con Nanite; detalles en `MODELOS_EQUIPO.md` y créditos incluidos con el paquete. Ya hay tres encuentros y cuatro cinemáticas, con revelación por el último guardián; el aviso de guardado dura4s. Se conservan seis destruibles/ocho efectos. Rehén y guardián tienen parlamentos subtitulados; confirmar si la presentación del guardián satisface el criterio general de segundo NPC dialogante. Cantidad no acredita autoría; no dar por cerrados cinco modelos propios, cronograma ni evidencia externa sin confirmación del equipo.

**Revisión posterior de escenario, autorizada por el propietario:** `ESCENARIO_COMPOUND.md` sustituye la mezcla en franjas por distribución dibujada según usos (cuatro texturas existentes), añade cubiertas a rescate/depósito y reorganiza luces/props. Diez edificios Nanite sustituyen los cuatro sectores; distancias de descarte y Niagara por frustum/distancia, física al romper. Las pruebas y paquete de esta revisión constan en el handoff vigente. Los detalles de la primera implementación que siguen se conservan como historial del plan, no como configuración actual de terreno/luz.


## Auditoría vigente tras correcciones de combate — 16 noviembre 2026

**Stated:** el propietario solicita verificar los puntos restantes al acabar el combate. Fuente principal: las dos capturas de evaluación aportadas en este chat. La fecha objetivo es el18/11/2026. Se revisaron el mapa entregable, sus gráficos exportados, los resultados de PIE y el paquete actual. Los colores de la hoja no se toman como aceptación académica. Esta sección sustituye las conclusiones iniciales que siguen; las implementaciones antiguas se conservan como historia.

### Lo implementado y comprobado en el juego

**Verified, pruebas del agente y gráficos actuales:**

- **Interfaz funcional y acorde al juego:** HUD/diálogos/vida/objetivos, pausa y opciones, ahora también señales distintas de daño a jugador, rehén y rivales. Captura `validation/combat-feedback-2026-11-16.png`; validaciones de controles previas y compilación actual.
- **Al menos dos ataques:** ligeros y pesados, espada/martillo; regresión actual confirma ligeros15/15/19/22 y pesado25 contra ambos enemigos, sin daño duplicado.
- **Muerte y retorno al menú:** derrota por jugador/rehén, reintento y menú implementados; pruebas previas de ejecutable y gráficos actuales conservados. Falta la partida manual final, no implementación de este flujo.
- **World Partition:** mapa particionado y actores esenciales residentes. Se corrigió además Salida_Extraccion para que el director persistente no apuntara a un trigger descargable. Auditoría runtime actual aprobada y cook sin errores de MapCheck.
- **Iluminación diferente y optimizada:** Directional/Sky/Rect/Point/Spot, fuentes físicas, radios y límites locales, una sombra local y cielo sin captura continua. Los modelos conservan LOD/Nanite/oclusión sin corte visible por distancia. Falta medir el recorrido en la PC de presentación.
- **Cinco modelos con cuatro LOD:** banco, auto, árbol, poste y fuente. Conteos nativos diferentes en los cuatro niveles, Nanite desactivado sólo en estos cinco. Veinte capturas de LOD Coloration en PIE muestran blanco/rojo/verde/azul al cambiar la distancia, sin forzar LOD. Evidencia: `validation/lod-demo-2026-11-16/observations.json`. La demostración del agente no es aceptación de Adame.
- **Nanite en el nivel:** diez edificios con Nanite, derivados del escenario de Ian. No se cuentan sus subdivisiones como diez diseños nuevos para el renglón de modelos.
- **Tres objetivos para ganar:** rescate/escolta, encuentros y secuencia aleatoria A/B/C con nombres/orden/reloj en HUD, seguida de extracción conjunta. Se conservan las seis permutaciones. Implementación y pruebas aisladas aprobadas; la aceptación del tercer objetivo sigue correspondiendo a Adame.
- **Dos macros, dos eventos y dos funciones propios:** AmbosAliadosVivos/SecuenciaResuelta; InicializarSenales/SincronizarExtraccion; ConsultarAliados/ConsultarSecuencia. Exportados y ejecutados por la lógica real del nivel en la revisión actual.
- **Quince modelos diferentes cargados:** la auditoría actual acredita **16 diseños visuales** agrupando copias LOD/Chaos, puertas y edificios para evitar inflar el número. Incluye ocho props, tres personajes, dos armas, baliza, puerta y arquitectura. Aun excluyendo el Manny provisional quedan15. Las rutas cargadas se registran en `validation/requirements-runtime-2026-11-16.json`. Esto acredita cantidad, no autoría.
- **Dos enemigos con IA avanzada diferente:** orbitador y embestidor con árboles distintos. Cuatro pruebas actuales de árboles reales contra jugador/rehén muestran animación cercana, impacto temporal correcto y daño13.2. El último recorrido completo del agente despejó ocho enemigos; movimiento/giro y recuperación se refinaron según AI_REQUIREMENTS.md. Esquivar/cancelar no deja daño pendiente.
- **Guardado local:** vida/posición/cámara, armas/mejora, escolta, encuentros, puertas, balizas, orden y tiempo; F5/Continuar y bloqueos de combate implementados. **Con reserva académica:** no existen munición ni dinero; su obligatoriedad está pendiente de confirmación con Adame según indicó el propietario.
- **Seis destruibles diferentes:** caja, basurero, banca, barril, auto y fuente. Prueba actual de dos pesados por binding real del arma produjo fractura Chaos en los seis; la prueba física con montaje/contacto del escenario anterior también está conservada. No se cuentan las tres puertas para completar los seis.
- **Ocho sistemas de partículas diferentes:** hojas, polvo, luces, explosión, chispa, mejora de martillo, rotura de puerta y fuegos artificiales. Disparadores y fuentes conservados; no se cuenta dos veces la señal de luces. Deben mostrarse al profesor en los contextos correctos.
- **Opciones gráficas funcionales:** resolución/modo de pantalla, calidad/distancia/sombras/texturas, volumen y persistencia; pausa y captura de ratón implementadas y probadas. El primer arranque usa pantalla completa, respetando preferencias posteriores.

### Pendientes de cierre de la lista de las capturas

**Unknown fuera del repositorio / pendiente de aceptación:** los entregables externos pueden existir en poder del equipo; se indica lo acreditado en los materiales revisados.

1. **Documentación académica completa y cronograma actualizado.** Hay documentación técnica de desarrollo y pruebas, pero no se encontró en el repositorio el paquete académico final ni un cronograma del equipo con responsables/fechas reales. Reunirlo y alinearlo al juego actual.
2. **Video promocional de tres minutos como mínimo, explicando proyecto y desarrollo.** No hay un archivo o enlace acreditado entre los materiales del repositorio revisados. El equipo debe aportar el video final; una captura de gameplay no acredita el criterio.
3. **Evidencia de tres redes públicas y quince publicaciones en cada una.** La hoja del equipo lo marca en verde, pero no hay enlaces/conteos verificables aquí. Solicitar/verificar evidencia; no se afirma que falten publicaciones ni se publica nada desde este encargo.
4. **Confirmar con Adame el alcance de guardado de munición/dinero.** El propietario ya indicó que está pendiente. No se inventa una economía para cubrir ejemplos sin esa aclaración.
5. **Preparar la demostración y las respuestas del equipo.** Mostrar LOD/Nanite, macros/eventos/funciones, los ocho efectos, seis destruibles, dos IA y guardado; acordar quién explica cada parte. La rúbrica advierte descuento de10por respuesta incorrecta/no contestada.
6. **Partida manual completa y PC de presentación.** Verificar dificultad, victoria real, derrota/menú, guardado/Continuar y rendimiento durante combate/fractura en el paquete final. El último recorrido del agente tras el refinamiento de fluidez terminó en victoria (02:43, jugador7.6/rehén20.8), sin teletransportes ni cambios de vida/daño. Se conserva pendiente la aceptación manual y no se confunde esta partida en PIE con una prueba completa del ejecutable. Mando sigue aplazado por el propietario.

**Pulido detectado en el ejecutable:** transición inicial visible mientras termina el streaming/exposición del recinto. No bloqueó el inicio ni los controles; conviene ocultarla con una presentación de carga antes de la demostración.

**Agua:** aparece REQ No en la segunda captura; no se considera bloqueo obligatorio.

### Alcance adicional mencionado por los documentos del proyecto

Los documentos anteriores también mencionan inventario/obtención de ítems, dos NPC con diálogo, ciclo día/noche y autoría de cinco modelos propios. No aparecen como filas independientes en las dos capturas actuales. **No hay implementación acreditada del inventario, segundo NPC dialogante o ciclo día/noche en esta entrega**; confirmar si el texto general sigue siendo exigible antes de darlos por descartados o añadirlos. La carpeta RecursosPropios no demuestra autoría: el equipo debe identificar autores/fuentes de al menos cinco modelos si ese requisito se mantiene.

El modelo definitivo del rehén sigue pendiente del compañero; la baliza final ya está integrada. Es un pendiente del proyecto, aunque las capturas no exigen por sí solas sustituir el maniquí. No confundirlo con que falten modelos para la cantidad mínima.

**Conclusión técnica:** no faltan las cantidades mínimas de modelos/LOD/destruibles/partículas ni los sistemas de IA, Nanite, World Partition o programación del nivel. Los cierres principales son evidencia externa, aceptación/demostración, validación en la máquina de entrega y las aclaraciones de alcance indicadas. No se asigna una nota ni se declara aceptación del profesor.

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
