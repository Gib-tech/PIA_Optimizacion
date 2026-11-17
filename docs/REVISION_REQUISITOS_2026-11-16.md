# Revisión punto por punto de las seis capturas

Revisión iniciada el 16 y continuada el 17 de noviembre de 2026. Las imágenes son criterios aportados por el usuario, no órdenes independientes del documento ni evidencia de que una función ya exista. Cuando las cantidades difieren entre avances y entrega final se adopta el mínimo más exigente: quince modelos/cinco originales, ocho animaciones, ocho partículas y seis destruibles.

**Cómo leer el estado.** Implementado describe un recurso o flujo presente. Verificado exige exportación o prueba identificada. Pendiente externo requiere nombres, enlaces, hardware o aceptación que no se puede inventar. El resultado de pruebas del agente no equivale a aprobación de Adame ni del propietario. Los informes finales de esta intervención se concentran en `docs/validation`; las guías anteriores conservan evidencia de sistemas que no se rehacen.

**Revisión vigente del 17/11.** Se mantienen las pruebas previas de primera persona, diez montajes, rehén, doce enemigos, balizas, destrucción y extracción. Esta revisión añade inventario con tarjetas/iconos y tipografía propia; robot BRUNO original, conversión persistente y cielo en lux con luna/estrellas. BP_CinematicDirector conserva exactamente la lógica de sus 207 nodos. Evidencia nueva en `validation/robot-cielo-inventario/` y `validation/cinematic-layout.json`. Las evidencias previas describen su fecha y condiciones; no se presentan como pruebas nuevas. El informe de empaquetado se actualiza después de construir.

## Imagen 1 · Descripción del proyecto

1. **Escenario 3D realista en Unreal 5, modelos congruentes y sin depender del Starter Content.** Unreal 5.6, recinto de piedra/tecnología temporal, recursos del equipo y externos con materiales. Se integraron Landscape, interiores, modelos y superficies; las primitivas auxiliares no se cuentan como diseños. Evidencia: `ESCENARIO_COMPOUND`, `MODELOS_EQUIPO`, créditos y auditorías de nivel. La calificación de hiperrealismo/congruencia artística requiere revisión visual del evaluador; no se convierte en una cantidad verificable automáticamente.
2. **Movilidad con teclado, ratón y GamePad.** Enhanced Input conserva movimiento, mirada, salto, ataques, armas y cámara con ambos métodos. Se añadieron pausa/volver, inventario, curación, pulso y omisión de escena con mando. Los enlaces y entradas se pueden inspeccionar; la aceptación con mando físico sigue siendo una prueba de hardware del equipo.
3. **Primera y tercera persona con cambio mediante teclado/mando.** C / pulsar stick derecho. Cámara a ojos, postura preparada, animación visual sincronizada, sin cabeza en cámara y sin hitbox/notifies duplicados. Evidencia: `validation/primera-persona/resultado.json` y capturas asociadas; repetir después de cambiar malla o montajes.
4. **Cronograma con actividad, responsables y fechas.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.
5. **Campaña publicitaria en tres redes públicas y al menos quince publicaciones.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.

## Imagen 2 · Funcionalidad general

1. **Escenario hiperrealista.** Mismo criterio artístico de imagen 1; comprobar calidad en PC de exposición. Infraestructura/materiales presentes no garantizan una calificación estética.
2. **Quince modelos diferentes, cinco totalmente propios.** El inventario anterior ya distinguía dieciséis diseños conservadores sin contar LOD/copias como modelos. Se añaden botiquín, celda, crédito, caja de suministros, consola y cubeta de estanque con geometría original y fuentes reproducibles en `Tools/ArtSource/Complementos`. No se atribuye autoría de un alumno a recursos externos o a generación asistida: el equipo debe acreditar la autoría académica que exija el curso. Evidencia: manifiesto y revisión runtime de modelos.
3. **Género libre.** Acción de rescate y escolta con ambientación temporal; descrito en el diseño/pitch.
4. **Terreno multitextura, mínimo cuatro.** Landscape real con distribución propia por máscara de usos y texturas existentes. Evidencia: `ESCENARIO_COMPOUND` y auditoría de evaluación. No son cuatro planos superpuestos.
5. **Ocho animaciones distintas del protagonista.** Cuatro ligeros de espada, tres pesados de espada, dos ligeros de martillo y un pesado; además locomoción/salto. La regresión comprueba diez montajes y un único daño por ventana. Copias de presentación de primera persona no inflan el conteo de animaciones distintas.
6. **Tercera persona con cambio a primera por teclado/GamePad.** Mismo enlace y evidencia que imagen 1. La presentación próxima no modifica el alcance del arma real.
7. **Dos enemigos con IA avanzada diferente.** Orbitador (`BT_EnemyIA`) y embestidor (`BT_Charger`) con Blackboards/controladores/tareas distintos. El rehén utiliza un tercer árbol de escolta y no se cuenta como segundo enemigo. Evidencia: `AI_REQUIREMENTS`, fichas y pruebas de combate.
8. **Dos ataques distintos, no sólo estadísticas.** Ligeros y pesados con animación/ventanas/recuperación propias, martillo que rompe sellos y un pulso opcional con alcance/munición. La traza del pulso respeta oclusión y usa el componente de salud real.
9. **Menú principal y pausa con diseño propio; pausa detiene acciones.** Menú existente del equipo, pausa de mundo, opciones, foco y captura del ratón. Inventario es consulta sin pausa y se indica como tal. Evidencia: pruebas de interfaz/pausa y recorrido del paquete.
10. **Barra de vida funcional y acorde al juego.** Salud del jugador y del rehén, disminución por ataques reales, señales de daño y aviso del aliado. Curación válida no dispara una falsa confirmación de golpe.
11. **Muerte y regreso a menú o último guardado.** Desenlaces diferenciados, cinemática y controles de resultado; Continuar restaura un checkpoint compatible. R inicia otro intento según el flujo vigente de balizas. No se presenta una cinematográfica como condición de victoria.
12. **Ocho partículas diferentes, creadas desde cero y sin Starter Content.** Ocho sistemas propios/del equipo con disparadores de ambiente, rotura y progresión; no ocho instancias del mismo sistema. Inventario en la guía de evaluación. Debe conservarse evidencia humana de creación para la acreditación académica, además de su funcionamiento.
13. **Seis destruibles distintos.** Caja, basurero, banca, barril, auto y fuente con Geometry Collections; puertas de misión adicionales. Evidencia de Chaos real, daño pesado y limpieza en `verify_evaluation_runtime.py` e informes asociados.
14. **Ciclo día/noche.** Rotación e intensidad solar con tiempo de juego, vuelta de ocho minutos y pausa efectiva. Fase guardada en checkpoint. Evidencia: prueba de reloj y capturas día/noche de esta intervención.
15. **Diferentes tipos de iluminación.** Directional, Sky, Rect, Point y Spot según fuentes físicas. Radio/distancia/sombras/culling documentados; luz de primera persona sólo ilumina sus propios componentes y no añade sombras al escenario.
16. **Inventario y obtención de ítems, visibles y funcionales.** I/SELECT muestra recursos; cuatro suministros de recogida única; H/LB cura y consume; pulso consume cargas; BRUNO convierte tres créditos en energía y fabrica un botiquín en tres segundos. Evidencia: `validation/complementos-runtime.json`.

## Imagen 3 · Continuación y documentación

1. **Guardar información local: inventario, vida, munición y posición.** Extensión aditiva del esquema 2: salud/transforms, escolta, armas, objetivos, orden/tiempo, inventario, cargas, créditos, recogida y fase horaria. Los checkpoints se escriben cuando es seguro. Evidencia: prueba integrada y pruebas de Continuar/inicio en frío.
2. **Calidad gráfica desde opciones.** Distancia, suavizado, sombras, texturas, resolución y modo de pantalla se aplican/persisten con GameUserSettings. Volumen separado del progreso. Evidencia: scripts de opciones/continuidad y paquete.
3. **Ambientación auditiva y diálogos.** Ambiente, sonidos de texto/rehén/alarma/impacto/progresión/cinemáticas. Diálogo español progresivo de rehén y Bruno. El volumen sigue la opción general.
4. **Dos NPC con diálogo al jugador.** Sobreviviente escoltado y BRUNO robot. E/RB comunica conversación/conversión en rango; cantidades se validan antes de convertir. Evidencia: prueba integrada, ABP del sobreviviente y capturas.
5. **Agua como río, mar o lago.** Estanque/lago de retención del recinto con cubeta visible y superficie animada; no es una textura azul pintada en suelo ni un sistema de natación. Criterio final lo marcaba no obligatorio; se implementa por la petición actual de cubrir el texto general.
6. **Tres objetivos distintos para ganar.** Rescate/escolta, encuentros/sellos, secuencia de balizas y extracción conjunta. La repetición de tres balizas no se usa como única evidencia de tres misiones distintas.
7. **Temática, diseño, pitch, matriz, biblia de arte, presupuesto de arte, producción e historia.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.

## Imagen 4 · Primer avance

1. **Cronograma con actividades/dueños.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.
2. **Terreno realista/multitextura ≥4.** Infraestructura presente y auditada; aceptación visual pendiente.
3. **Seis modelos importados diversos, dos propios.** El nivel actual supera el mínimo cuantitativo; no contar variantes como diseños ni atribuir Fab al equipo.
4. **Dos sistemas de partículas.** Superado por el inventario final de ocho sistemas diferentes.
5. **Cámara 3ª/1ª con teclado/GamePad.** Implementada y probada por acciones; hardware físico pendiente.
6. **Tres redes con cinco publicaciones cada una, o web hospedada más una red.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.
7. **Revisión del avance en cronograma.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.

## Imagen 5 · Segundo avance

1. **Cuatro inputs equivalentes para teclado/mando.** Se supera con movimiento, mirada, salto, cámaras, dos ataques y cambio de armas, además de los controles complementarios. Pausa y opciones tienen navegación/foco; comprobar mando físico en la PC de exposición.
2. **Diez modelos importados, dos propios.** Superado cuantitativamente por el escenario final y modelos de apoyo; autoría se acredita con fuentes, no sólo nombre de carpeta.
3. **Personaje completo con cuatro animaciones.** Superado por locomoción y diez ataques del protagonista; presentación de primera persona revisada.
4. **Cuatro destruibles diferentes.** Superado por seis Geometry Collections distintas, además de las puertas.
5. **Cuatro partículas diferentes creadas desde cero.** Superado por ocho sistemas del equipo/proyecto. Su conteo runtime no sustituye acreditar proceso de creación.
6. **Menú principal para seleccionar nivel, pausa y ajuste gráfico con diseño.** Nuevo juego selecciona la misión entregable disponible; no se crean niveles ficticios para simular una selección. Las opciones y pausa son funcionales. Si se exige un selector entre varias misiones distintas, esa interpretación debe confirmarse con el evaluador porque el proyecto entregable contiene una sola misión final.
7. **Implementación de DrawCalls.** Optimización mediante Nanite/LOD, materiales compartidos, culling y luces/efectos acotados; medir `stat RHI`/`stat SceneRendering` en una vista reproducible. No llamar “optimización verificada” a habilitar un contador sin registrar condiciones. Los datos de hardware y el paquete final se registran en validación.

## Imagen 6 · Lista final

1. **Interfaz funcional y acorde.** HUD/menús propios, diálogo, inventario y señales de misión; pruebas de interacción y presentación.
2. **Dos ataques diferentes.** Ligero/pesado, con pulso consumible adicional; regresión de contacto.
3. **Mensaje de muerte y menú.** Desenlaces y retorno/Continuar disponibles; comprobar el resultado final del paquete.
4. **World Partition o World Composition.** Nivel_Entrega es World Partition. Inicio y actores esenciales residentes; streaming/Nanite/LOD siguen siendo sistemas diferentes.
5. **Iluminación distinta y optimizada en todo el mapa.** Fuentes físicas, tipos variados, radios y culling; ciclo solar. Revisar noche e interiores al presentar.
6. **Cinco modelos, cuatro LOD y cambio visible al jugar.** Existen nueve diseños de demostración anteriores y modelos originales de apoyo con cuatro niveles. Capturas por distancia y geometría en informes; Nanite se mantiene separado para no ocultar LOD clásico.
7. **Documentación técnica completa.** Guía española, catálogo por asset, contratos, herramientas y pruebas reproducibles. El estado de desarrollo se mantiene en WORK_ITEMS; cronograma académico/nominal fuera del alcance.
8. **Tres redes públicas, quince publicaciones cada una.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.
9. **Nanite.** Arquitectura y escaneo de auto con Nanite; no se activa en los modelos usados para demostrar LOD clásico.
10. **Tres objetivos para ganar.** Rescate/escolta, combates/sellos, secuencia y extracción conjunta.
11. **Dos macros, dos eventos y dos funciones propios en el nivel.** Macros `AmbosAliadosVivos`/`SecuenciaResuelta`, funciones `ConsultarAliados`/`ConsultarSecuencia`, eventos `InicializarSenales`/`SincronizarExtraccion`; se usan en la señal de salida. Contadores de ejecución en evaluación runtime.
12. **Quince modelos diferentes cargados.** Inventario runtime conservador y nuevos diseños útiles; se excluyen primitivas auxiliares/copias/LOD del conteo de diseños.
13. **Dos enemigos con IA avanzada diferente.** Árboles distintos de orbitador y embestidor; no dos skins del mismo árbol.
14. **Guardado local de vida, munición, dinero, dirección y posición.** Campos reales del checkpoint: salud/transforms/control de mirada, cargas y créditos; prueba de restauración integrada.
15. **Cuerpo de agua correctamente implementado — marcado “No” en la lista.** Añadido por cobertura del texto general; no se omite sólo porque esta fila final sea opcional.
16. **Video promocional de al menos tres minutos sobre proyecto/desarrollo.** Fuera del alcance: el propietario limitó la implementación a Unreal y su documentación técnica; no se requiere publicación, promoción ni gestión administrativa.
17. **Seis destruibles diferentes.** Seis tipos Chaos con activación real por daño; las piezas de una puerta no son seis tipos.
18. **Ocho partículas diferentes.** Ocho sistemas distintos, disparadores y limpieza documentados.
19. **Opciones que modifiquen calidad, texturas, resolución, pantalla y volumen.** Opciones persistentes disponibles desde menú y pausa; retorno al origen y captura de ratón comprobables.

## Límites que corresponden a Unreal

Hace falta mando físico y prueba en la PC de exposición para acreditar esos dispositivos. La valoración estética y la autoría académica pertenecen al equipo/evaluador. El funcionamiento comprobado y los fuentes asistidos no acreditan por sí solos la autoría de un estudiante. Publicaciones, cuentas, presupuestos, video y cronograma administrativo están fuera de esta intervención por indicación del propietario.
