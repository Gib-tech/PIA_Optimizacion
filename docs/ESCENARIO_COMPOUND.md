# Escenario: distribución e iluminación con función

Revisión del 16 de noviembre de 2026. **Stated:** el propietario rechaza la distribución del terreno en franjas y los objetos/luces sin relación con el espacio. Autoriza modificar terreno y estructuras reutilizando los recursos disponibles y reducir trabajo fuera de vista.

## Diseño implementado

**Decision:** recinto de rescate cubierto, depósito cubierto, patios abiertos y caminos de piedra que conectan accesos y balizas. Se mantienen coordenadas de objetivos, huecos originales, puertas y ambos encuentros. Los techos tienen 4.2 m de altura libre. Las prolongaciones de pared derivan de las caras superiores del modelo de Ian; no cierran los pasos a nivel del suelo.

El material `Environment/Atmosphere/M_TerrenoRecorrido` sustituye las franjas por un mapa de uso dibujado para este recorrido. `Tools/ArtSource/Atmosphere/terrain_layout.json` contiene polígonos y anchos de senderos; `build_terrain_control_map.py` produce la máscara RGBA de datos. Reutiliza cuatro texturas de superficie existentes: suelo con vegetación, adoquines, grava y roca. El pavimento cambia de escala/tono entre senderos e interiores. No se usan texturas ornamentales de pared como camino. La mezcla no corresponde a pintura manual de capas Landscape; el Landscape real se conserva y el material anterior queda disponible.

Los objetos se agrupan: caja en rescate; árbol, banca y basurero en espera junto al acceso de la primera arena; vehículos/barril en depósito y estacionamiento; fuente/banca en patio lateral y fuente en atrio. Los cinco modelos con cuatro LOD y los seis tipos de destruibles se conservan. Se retiró el efecto ambiental redundante de luces en mitad del patio; la señal de extracción conserva ese sistema cuando tiene utilidad.

Los dos vehículos quedan en el estacionamiento sur, fuera de las rutas de refugio. Dos puntos de refugio próximos al acceso del depósito, detrás de sus paredes, evitan exigir cruzar toda la arena durante la retirada. Se conservan el árbol del rehén y sus límites; no se cambia vida/daño ni se añade combate por cantidad. El bot de regresión logró cruzar accesos y combatir, pero perdió en la segunda zona: su resultado no acredita victoria natural de esta revisión. La dificultad/experiencia final debe probarla el propietario.

## Luz y coste

Tres luces locales con una fuente visible: panel Rect en rescate, lámpara Point dentro del depósito y Spot asociado al poste del acceso al patio. Sus radios son 10/7/11 m; distancia máxima24 m, fade3.5 m. Sólo el panel de rescate proyecta sombras locales. Sin contribución volumétrica local. Sol móvil de15000lux, cielo móvil con captura única, sombras del cielo y Lumen en el volumen de nivel para separar interiores/exteriores. Exposición bias-.75 y adaptación4/2. No ejecutar `fix_delivery_lighting.py`: corresponde al arreglo histórico de los sectores grandes y desactiva la GI de esta revisión.

Las rotaciones se crean con **pitch/yaw/roll por nombre**. El constructor posicional de Python usa otro orden; las pruebas verifican el vector hacia abajo del panel y del foco. En World Partition, modificar actores/componentes exige Modify y guardar también sus paquetes externos: guardar sólo el umap no garantiza que PIE/cook lean las últimas transformaciones.

La arquitectura se divide en diez edificios con pivotes y bounds locales y Nanite. Techos y prolongaciones son geometría sencilla. La revisión posterior elimina los límites duros de distancia de todos los modelos colocados: los cortes anteriores de 38/60/180 m producían desapariciones visibles. Los once props LOD/destruibles se mantienen residentes en World Partition; arquitectura conserva su partición. Los cinco modelos siguen con cuatro LOD; frustum/occlusion y Nanite siguen activos. No hay un Tick que apague actores según un rayo de cámara.

Las 104 paredes texturizadas (edificios, límites, marcos y módulos) usan tres materiales M_WallMetric_ con las texturas existentes y WorldAlignedTexture XYZ a 400 cm. La escala deja de depender de UV o escala del actor; no cambia geometría, colisión ni navegación. Once texturas de superficies/props usan compresión de mundo, mipmaps y streaming, con máximos de 1024 o 2048 según detalle. Los dos archivos no POT de madera/metal se remuestrean a POT al construir, conservando sus fuentes. No se modifican recursos Fab.

Los efectos ambientales usan copias de los sistemas del equipo con `NET_CompoundAmbient`: límite24m, comprobación1s y descarte fuera de frustum o sin renderizar durante1s. DeactivateImmediateResume detiene la simulación y la permite volver al entrar en rango/vista. Bounds finitos conservadores; una cámara dentro de su esfera puede seguir considerándolos visibles. Los efectos de golpes son eventos breves. Los destruibles intactos no simulan física; al llegar a cero salud se activa la simulación y la fractura Chaos, y los restos expiran tras8s. La IA y los gestores de misión siguen funcionando fuera de vista.

No se promete coste cero fuera de pantalla: una luz o sombra puede afectar una superficie que sí ve el jugador, y las decisiones de misión deben continuar. No se atribuye una ganancia de FPS sin comparación medida en el mismo hardware y condiciones. La validación de la PC de presentación sigue pendiente.

La colisión intacta usa el BoxComponent `Colision` ya existente, ajustado al volumen visible: QueryOnly, Destructible, solapamientos activos, bloqueo de Pawn y cámara ignorada. Al romper se desactiva ese proxy y se activa colisión/simulación de la GC. Esto evita depender de cuerpos Chaos inactivos para detectar el arma. La prueba final usa dos ataques pesados animados, no llamadas directas al binding de colisión: salud50→25→0 y20 eventos físicos. Las pruebas anteriores que llamaban al binding sólo acreditaban la recepción de daño, no el contacto real.

Referencia del mapeado: [WorldAlignedTexture](https://dev.epicgames.com/documentation/unreal-engine/texturing-material-functions-in-unreal-engine?application_version=5.6).

Referencia: [visibilidad y oclusión de Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/visibility-and-occlusion-culling-in-unreal-engine?application_version=5.6), además del código instalado de UE5.6 consultado para Niagara y rotaciones.

## Reproducción

Editor cerrado para compilar helper `Tools/Build-EditorBridge.ps1`; abrir con -PLUGIN a BPB3. Helper editor-only incluye LoadEditorRegion; no forma parte del juego. Cargar región (-6500,-12500,-1000)..(6500,1000,3000). Con PIE detenido: `export_compound_sources.py` → Blender `build_compound_shelters.py` → `build_terrain_control_map.py` local → `prepare_compound_terrain.py` → `prepare_compound_scene.py` → `prepare_compound_fx.py` → `optimize_delivery_surface_textures.py` → **`fix_wall_mapping_and_model_visibility.py` al final**. Esta última pasada debe repetirse si se regeneran las paredes o la escena, porque la preparación asigna los materiales originales. Después ejecutar `validate_wall_visibility_fix.py` y `verify_compound_editor.py`. El Blender hornea **escala2 en XYZ**, incluyendo la altura ya corregida del escenario anterior, y marca reimport de paredes. Generar `generate_evaluation_graphs.py` y ejecutar `install_compound_logic.py` para física bajo demanda. Respaldos de umap/actores externos anteriores en Intermediate/inspect/atmosphere-backup.

Pruebas del agente y resultados finales se registran en el handoff actual y `docs/validation/compound-2026-11-16.json`; no sustituyen aceptación visual del propietario. La comprobación visual del ejecutable precede al último ajuste de colliders, que no cambia materiales/luz/distribución: éste se verificó en PIE con contacto físico real y se incluyó en el cook final. La captura estática del interior mostró aproximadamente78FPS en RTX3060Ti/Ryzen53600, salida1920×1080 con resolución interna1400×788; no es una medición comparativa ni representa el combate o la PC de presentación.

La evidencia vigente de paredes, texturas, visibilidad y paquete está en `docs/validation/walls-visibility-2026-11-16.json`. Los reportes compound anteriores conservan su contexto histórico y sus valores de distancia ya sustituidos.
