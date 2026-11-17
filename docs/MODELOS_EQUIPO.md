# Integración visual del checklist del equipo

16 de noviembre de 2026. Solicitud del propietario: integrar los recursos compartidos y mejorar su aspecto. La conversación/captura son contexto del checklist, no una aceptación de requisitos ni prueba de autoría.

Se incorporan cinco diseños distintos en `/Game/ThirdPerson/Environment/TeamModels`: edificio, farol, escombros, auto destruido y árbol Fab. Ocho instancias dan función visual a los accesos, jardín y zona de servicio: torre como referencia de orientación, faroles en pasos, auto abandonado y residuos junto a los recintos, y árboles para acompañar los bordes. `Tools/ArtSource/TeamModels/placements.json` conserva la colocación. No se añaden obstáculos a la secuencia ni se cambian objetivos/combate.

El edificio no incluía sus cuatro texturas externas; se mantienen las regiones del modelo con fachada mate, vidrio oscuro y cubierta metálica. El farol conserva sólo el vidrio luminoso; su poste es metálico oscuro. Dos Point Lights de1600lm, radio4.5m, distancia22m/fundido4m, sin sombras ni volumétricos, aportan luz local. El Landscape jugable permanece; una superficie de fondo de dos triángulos a1m por debajo rellena el horizonte negro, sin colisión ni sombras.

Los escombros se reducen de876677a45000triángulos, con un nuevo atlas de color horneado. El auto conserva sus2499999triángulos y UV originales con Nanite para preservar la superficie del escaneo; su colisión es simple y su malla de fallback es reducida. Se orienta por su eje largo y mide4.5m; los escombros ocupan3.5m. Las colisiones de poste/tronco no abarcan brazos/copas. Edificio, farol, escombros y árbol conservan cuatro LOD geométricos diferentes, con Nanite desactivado para esa demostración. Los diez edificios Nanite anteriores y los cinco LOD anteriores se conservan; el auto añade otro ejemplo de Nanite.

Los modelos usan LOD automático o streaming Nanite y no tienen un recorte duro por distancia. Las ocho instancias son residentes de World Partition para evitar desapariciones visibles, con geometría adaptativa y texturas mipmapped/streaming. No se promete coste cero fuera de cámara ni se usa esta revisión como benchmark de la PC de presentación.

Créditos: `CREDITOS_MODELOS.md`. Edificio/farol: autores por confirmar por indicación del propietario. Escaneos/árbol: externos con atribución; cinco modelos nuevos no equivale a cinco modelos propios.

## Reproducción

1. Blender3.6: `Tools/Blender/prepare_team_models.py`, `bake_optimized_scans.py`, `finish_team_collisions.py` y `prepare_nanite_wreck.py`. Leen los archivos originales proporcionados; el árbol se obtiene con `Tools/inspect_fab_tree.py`. La metadata/firma de las fuentes se conserva. El FBX intermedio pesado del auto queda en Intermediate; el asset de Unreal sí se versiona.
2. Editor con helper de autoría BPB3 y PIE detenido: `import_team_models.py`, luego `place_team_models.py`. Guardar umap y paquetes externos; los scripts lo hacen explícitamente. No reconstruir el escenario entero ni tocar árboles/gameplay.
3. `start_team_models_qa.py`, `verify_team_models_runtime.py`; esperar marcador de finalización antes de detener PIE. Las pruebas son de cámara/navegación preparadas. Restaurar guardados/preferencias con `finish_team_models_qa.py`.
4. Validar assets y guardar/cerrar editor; `Tools/Build-Delivery.ps1`, `Tools/Archive-Delivery.py`. El juego no depende de Blender, Python ni del helper.

## Estado del checklist

Ya implementados y documentados: muerte/menú, World Partition, Nanite, luces variadas, cinco modelos con cuatro LOD anteriores (más cuatro nuevos), programación del nivel con2macros/2funciones/2eventos, guardado local, seis destruibles, ocho efectos y cuatro cinemáticas. La última revelación amplía las tres escenas inicialmente pedidas. No se duplican sistemas para cubrir casillas de una captura anterior.

El agua figura como opcional y no se añade por inferencia. Siguen requiriendo información/aceptación del equipo la autoría de cinco modelos propios, documentación académica y cronograma con responsables reales, video/redes y validación final en la PC de presentación. La documentación técnica de esta integración queda aquí y en el handoff; no se inventa evidencia externa.

## Evidencia de esta revisión

**Verified:** doce rutas completas con los objetos colocados y dieciséis capturas de los cuatro LOD convencionales por distancia, con colores blanco/rojo/verde/azul comprobados sin forzar LOD. Auto/edificio/farol observados en el ejecutable mediante checkpoint preparado con UserDir aislado; ataque/pausa/reanudar y salida limpia. Recarga fría sin helper, sin PIE ni paquetes sucios. Originales de guardado restaurados y hash verificado. Son pruebas preparadas del agente, no una nueva partida natural ni aceptación manual.

Win64 Development:0errores;30registros que repiten los mismos15avisos anteriores (Scale y posesManny), sin tipos nuevos. ZIP674655940bytes, CRC aprobado y créditos incluidos. `validation/team-models-2026-11-16.json` reúne la evidencia. [Auto integrado](validation/team-models-auto-2026-11-16.png), [farol integrado](validation/team-models-farol-2026-11-16.png).
