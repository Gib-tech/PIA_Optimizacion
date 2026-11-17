# Demostración de Time Out — evaluación Unreal

**Modelos nuevos del equipo,16/11:** en la carpeta de actores `Escenario/ModelosEquipo`, mostrar torre de control, dos faroles, auto abandonado, escombros y árboles. Cinco diseños adicionales, cuatro LOD en cuatro de ellos y Nanite en el auto, junto a los cinco LOD anteriores. Abrir `SM_Escombros` en `/Game/ThirdPerson/Environment/TeamModels` para revisar cuatro conteos geométricos; dejar Forced LOD en Auto al jugar. Los escombros usan un atlas horneado; el auto conserva la geometría y UV originales con Nanite. Explicar colisiones simples y luces acotadas. `CREDITOS_MODELOS.md` diferencia recursos externos de autores de edificio/farol por confirmar. La misión vigente tiene tres encuentros y cuatro cinemáticas, incluida la revelación por el último enemigo; mostrar el avisoF5 de4s. Consultar el handoff actual para evidencia/paquete; las cantidades antiguas de esta guía son historial.

Estado del 16 de noviembre de 2026. Pruebas del agente, pendientes de aceptación del propietario y Adame. Mapa de juego: `/Game/ThirdPerson/Maps/Nivel_Entrega`. Abrir desde Nuevo juego; para inspeccionar arquitectura en editor, cargar la región del mapa desde World Partition cuando esté descargada.

**Revisión artística posterior:** `ESCENARIO_COMPOUND.md` sustituye la distribución inicial en franjas y las luces locales anteriores. Ahora hay cuatro texturas de superficie distribuidas por una máscara propia del recorrido, rescate y depósito cubiertos, diez edificios Nanite separados y props reorganizados. Los requisitos de gameplay/LOD/macros se conservan. Ubicaciones y sistema de descarte actuales en ese documento; las posiciones de props de la auditoría inicial que siguen son referencia anterior a esta reorganización.

## Recorrido y requisitos de gameplay

Rescatar con E, defender al rehén en las dos zonas, despejar sus dos oleadas, recuperarlo con E y romper cada puerta con dos golpes pesados. Las tres balizas están en el patio accesible; seguir el orden aleatorio del HUD. Sólo el rehén canaliza durante 3 s. Completar la secuencia permite romper la última puerta y extraer a ambos. El HUD muestra orden, siguiente, progreso y tiempo; R en resultados comienza otro intento. Continuar recupera el intento guardado.

Mostrar ligero y pesado; orbitador y embestidor utilizan árboles distintos, no reemplazados durante este rework. Mostrar pausa, opciones, derrota por jugador o rehén y retorno al menú. F5 guarda sólo a salvo; guardado incluye vida, posición/orientación, arma, escolta, zonas, puertas, secuencia y tiempo. **Pendiente con Adame:** si exige agregar munición/economía. No existen en este diseño.

## Landscape, World Partition y Nanite

El suelo es un Landscape de cuatro componentes; usa `Environment/Atmosphere/M_TerrenoRecorrido` y una máscara de uso espacial propia. Cuatro texturas existentes cubren suelo con vegetación, caminos, grava y roca; el pavimento se reutiliza con otra escala en interiores/patios. No hay franjas por World Y ni se afirma pintura manual de capas Landscape. El material anterior `/Game/Landscape` se conserva como recurso histórico, no es el terreno activo.

Abrir World Settings/World Partition y mostrar celdas/actores externos. Actores esenciales residentes, navegación dinámica convencional sin navchunks particionados. Diez mallas `Environment/Atmosphere/SM_Walls_*` con Nanite sustituyen los cuatro sectores grandes conservando geometría/UV. Mostrar visualización Nanite. Cubiertas sencillas en rescate y depósito justifican la luz interior.

## Cinco modelos con cuatro LOD

Recursos en `/Game/ThirdPerson/Environment/Evaluation/`. Son copias de modelos existentes del equipo, con cuatro LOD reales y Nanite desactivado. Screen sizes: 1, .45, .20, .07. En Static Mesh Editor mostrar LOD0..3; en gameplay acercarse/alejarse y usar la visualización LOD Coloration de PIE para acreditar cambios por distancia. La comprobación geométrica se complementó con veinte capturas actuales de LOD Coloration en PIE (cuatro distancias por modelo, sin forzar LOD): `validation/lod-demo-2026-11-16/observations.json`. Falta presentarlas/demostrarlo ante el profesor.

- `SM_LOD_Banco`, (1100,-1900): 158592 / 87226 / 39648 / 12687 triángulos.
- `SM_LOD_Car`, (-4500,-7050): 2548 / 1402 / 636 / 204.
- `SM_LOD_Tree1`, (1450,-1750): 210176 / 115597 / 52544 / 16815.
- `SM_LOD_Light_Pole`, (1900,-8050): 708 / 390 / 176 / 64.
- `SM_LOD_fuente`, (0,-7300): 11644 / 6404 / 2910 / 932.

## Seis destruibles y ocho efectos

`BP_DestruibleEntrega` adapta el Blueprint del equipo, conserva sus colecciones y recibe daño desde el overlap real del arma. Salud 50: dos pesados o varios ligeros. La fractura usa CrumbleActiveClusters e impulso; el contador ChaosBreakCount recibe los eventos físicos. Restos sin bloquear personajes/cámara, vida 8 s. Los objetos decorativos no se guardan en el checkpoint.

- Caja: (520,-900), `GC_box`.
- Basurero: (900,-1900), `GC_Trash`.
- Banca: (2900,-3350), `GC_Banco`.
- Barril: (-4500,-5300), `GC_Barril`.
- Auto: (-3200,-7050), `GC_Car2`.
- Fuente: (3200,-3800), `GC_fuente`.

Ocho sistemas diferentes: `NS_Hojas` junto al árbol; `NS_Polvo` en la primera zona; `NS_Luces` en patio y extracción; `NS_Explocion` al romper barril; `NS_ChispaImpacto` en otros destruibles; `NS_HammerUpgrade` al recibir mejora; `NS_DoorBreak` al romper puertas; `NS_FuegArtificiales` al completar la secuencia. Dos instancias de NS_Luces cuentan como un solo sistema.

## Level Blueprint e iluminación

Level Blueprint contiene macros `AmbosAliadosVivos`, `SecuenciaResuelta`; funciones `ConsultarAliados`, `ConsultarSecuencia`; eventos `InicializarSenales`, `SincronizarExtraccion`. BeginPlay agenda inicialización una vez y sincronización cada .2 s mediante delegados de timer. Las funciones llaman a las macros y deciden la visibilidad de `FX_Extraccion`. Contadores Inicializaciones/Sincronizaciones permiten inspeccionar su ejecución.

DirectionalLight y SkyLight móviles, cielo sin captura continua; Rect en rescate, Point en depósito y Spot junto al poste de acceso al patio, con fuentes visibles. Radios10/7/11m, máximo24m y fade3.5m, sólo Rect con sombras locales. Niagara ambiental se suspende por distancia/frustum y vuelve al entrar; física de destruibles sólo al romper. Ver `ESCENARIO_COMPOUND.md`. Esto no acredita una ganancia de FPS ni rendimiento en otra PC.

## Inventario y pendientes

La auditoría actual agrupa16 diseños visuales cargados (15si se excluye al Manny provisional), sin contar variantes como diseños adicionales: `validation/requirements-runtime-2026-11-16.json`. Esto acredita cantidad, no autoría. El inventario de la primera auditoría enumeró30 rutas geométricas; la división posterior por edificios añade recursos derivados del mismo escenario. No contar esas divisiones, primitivas o mallas auxiliares como diseños nuevos para inflar la rúbrica. Los recursos usados incluyen arquitectura de Ian, puertas/marcos, baliza, cinco modelos LOD, seis colecciones, jugador, enemigo, espada y martillo. Varios derivan de un mismo modelo: el equipo debe confirmar con Adame el criterio de quince modelos distintos y acreditar autoría de los cinco propios; no atribuir modelos Fab al equipo. El informe `compound-runtime-2026-11-16.json` es histórico; el inventario vigente está en `requirements-runtime-2026-11-16.json`.

Pendientes externos: documentación académica y cronograma actualizado, redes, video de tres minutos, modelo final del rehén, aceptación manual, otra PC y mando. Agua marcada REQ No en la captura. No dar por aceptados los colores de la rúbrica ni las pruebas automáticas.
