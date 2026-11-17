# Ciclo suave, luminarias y ataques a destruibles · 17/11/2026

Revisión vigente de `Nivel_Entrega`. Sustituye los valores históricos del cielo de ocho minutos y la indicación de usar sólo el pesado en props. El juego sigue ejecutando Blueprints; las herramientas de Python y el helper C++ se usan exclusivamente en el editor.

## Cielo y continuidad

`BP_SistemasComplementarios.DayCycleDuration` vale **1200 segundos (20 minutos)** tanto en la clase como en la instancia colocada. Es editable por instancia y se acota a un mínimo de 300 segundos. `WorldSeconds` conserva su unidad y campo de checkpoint; no se cambia el esquema del guardado. Un checkpoint anterior conserva sus segundos transcurridos, interpretados con el nuevo periodo, por lo que su hora visual puede diferir de la revisión anterior.

Ángulo = `35 + WorldSeconds × 360 / max(DayCycleDuration, 300)`. Se calcula elevación = seno del ángulo. La intensidad solar, la luna, el ambiente y las estrellas usan transiciones continuas `smoothstep(t) = t² × (3 − 2t)`, con pendiente cero en ambos extremos. El sol llega a 26 000 lux; la luna a 1,2 lux. El ambiente varía de 0,65 de día a 0,75 de noche. Las estrellas y la captura continua del SkyLight existentes se conservan. El crepúsculo de la mezcla nocturna abarca elevaciones −0,20 a +0,20, unos 77 segundos al cruzar cada horizonte con el periodo por defecto.

La fase avanza con DeltaSeconds del juego permitido. Pausa, revelación y resultados suspenden el reloj. Continuar restaura WorldSeconds; no comienza otra vuelta ni interpola desde una hora arbitraria. El periodo no cambia el cronómetro de misión, las ventanas de ataques ni la fabricación de BRUNO.

## Luminarias de pared

`BP_LuminariaPared` contiene anclaje, soporte metálico, carcasa, difusor emisivo cálido y un SpotLight dirigido hacia el recorrido. **41 instancias** cubren Rescate, Arena, Jardín, Depósito, Servicio, Patio Norte, Atrio, Ala Oeste, Ala Este y Salida. La receta traza contra las fachadas verticales reales `Compound_SM_Walls_*`, orienta el soporte según el normal y lo separa cinco centímetros de la superficie. El manifiesto `validation/ciclo-luces-ataques/luminarias.json` identifica pared, posición y orientación de cada instancia.

Cada foco aporta 3200 lúmenes, radio de 1450 cm, conos de 38°/78° y sombras para evitar atravesar muros. Se desvanece durante 500 cm antes de su distancia máxima de 2700 cm; la geometría se limita a 4000 cm. No tiene Tick, colisión ni efecto sobre navegación. Las instancias quedan residentes como el escenario de misión, manteniendo culling por luz/malla. Permanecen encendidas como iluminación de recorrido; no dependen de interruptores bruscos al anochecer.

## Todos los ataques contra los seis props

Caja, basurero, banca, barril, auto y fuente aceptan espada y martillo, ligeros o pesados, y pulso. No requieren la mejora del martillo. El contacto conserva WeaponHitbox y las ventanas de montaje; `HeavyHitActors` deduplica cada swing. Un barrido complementario de 220 cm y radio 30, situado unos 55 cm sobre el suelo, permite alcanzar props bajos cuando el arco de espada pasa por encima. Sólo se ejecuta con IsAttacking y WeaponHitbox en QueryOnly; el primer bloqueo Visibility corta el barrido. Comparte la deduplicación con el overlap y no aumenta daño a enemigos ni altera puertas. Daño de prop: **15 ligero, 25 pesado y 20 pulso**; vida inicial 50.

El pulso usa su traza visible existente de ocho metros. El primer enemigo o destruible bloqueante recibe un único daño; las paredes bloquean la traza. Consume una carga, respeta 0,8 s de recuperación y no dispara durante un ataque cuerpo a cuerpo. Su actor cian continúa siendo exclusivamente visual. El origen de ApplyDamage es el protagonista, no el actor de inventario.

`BP_DestruibleEntrega.ReceiveAnyDamage` valida origen, daño positivo y `bBroken`. Ya no exige IsAttacking, que sólo describe melee y rechazaba el pulso. Al agotar vida activa Chaos una vez, desactiva el proxy intacto, aplica efecto/impulso y elimina restos tras ocho segundos. Los restos ignoran Pawn y Camera. Los props se restablecen al cargar.

Las tres **puertas de misión** conservan desbloqueo por progresión y golpes pesados del martillo cargado, para mantener la secuencia de encuentros/balizas. La leyenda del HUD de los seis props ahora ofrece ligero, pesado y pulso.

## Regeneración y documentación interna

1. Con PIE detenido y helper de editor cargado, ejecutar `prepare_daynight_wall_lights.py`. Es reutilizable por etiqueta; no duplica las luminarias.
2. Generar exclusivamente `systems()`, `destructible()`, `player_camera()` y `generate_dialogue_hud.py`. Instalar con `install_daynight_attacks.py`; no reinstala menús ni cinemáticas.
3. Los cuatro Blueprints modificados y la luminaria incluyen recuadros explicativos en español dentro de EventGraph. El reloj, el receptor de daño, el contacto y el pulso incluyen comentarios sobre sus autoridades/guardas. El catálogo se regenera desde exportaciones reales y descripciones editoriales en `Tools/document_blueprints_es.py`.
4. Ejecutar la matriz de ataques, el muestreo solar y capturas; detener PIE antes de compilar/cook. Respaldar y restaurar partidas/preferencias del usuario.

## Evidencia de esta revisión

Los informes y capturas propios se guardan en `validation/ciclo-luces-ataques/`. Las pruebas preparan posición, arma o fase para aislar la condición; esto se declara en cada informe. No equivalen por sí solas a una partida completa natural ni a aceptación manual del propietario. La validación de mando físico y de rendimiento en otra PC continúa fuera de estas pruebas.

- `destruibles-*.json`: 30 combinaciones comprobadas (seis tipos × cinco ataques). Ligero 15, pesado 25 y pulso 20, sin daño duplicado y con eventos reales de Chaos. El martillo no está mejorado en estos fixtures. Se recoloca entre swings para compensar root motion; la fuente se prueba desde una cara visible, evitando su muro lateral.
- `ciclo-runtime.json`: 241 fases leídas de las luces reales durante una vuelta completa; coincide con la fórmula suave. Avance natural, congelación al pausar y reanudación sin reinicio comprobados.
- `guardado-y-guardas.json`: checkpoint nativo restaura hora nocturna con periodo de 1200 s. Pared y distancia bloquean daño; sin cargas no dispara; dos peticiones inmediatas consumen una carga y aplican un único impacto de 20.
- `capturas.json` y PNG: inspección de día, crepúsculos y noche. Comparación sin/con luminarias en el mismo punto. Se comprueba también que los componentes de las 41 instancias sigan al actor; esta verificación detectó y corrigió un anclaje sin raíz durante el desarrollo.
- `partida-nocturna.json`: misión completada por movimiento, ataques, curaciones consumibles e interacciones normales, sin teletransportes ni cambios de salud/daño. Única preparación adicional: fase inicial de noche (`WorldSeconds=783`). Incluye los tres encuentros, revelación, balizas y extracción conjunta; conserva la distinción respecto a aceptación manual.
- `paquete-final.json` y `paquete-*.png`: Win64 Development generado en 84,32 s; cook con 0 errores y una advertencia previa del pin Scale. Desde Continuar se comprueba noche visible, pulso de 3→2 cargas, caja fracturada después de pulso y dos ligeros de espada, pausa/reanudación y guardado por F5 con teclas/ratón reales. UserDir aislado y checkpoint preparado, sin helper de editor.
- `recarga-fria.json`: editor normal sin helper, 41 luminarias con jerarquía y sombras correctas, geometría sin colisión/navegación, periodo 1200 y lectura nativa del save del ejecutable. La fase guardada supera 783 y conserva dos cargas. `compilacion.json` comprueba siete Blueprints desde assets recién cargados; distingue mensajes activos del valor histórico ErrorType que Unreal puede conservar sin mensaje.
- `datos-usuario-restaurados.json`: partidas y preferencias originales restauradas y verificadas por SHA-256. El paquete/ZIP excluye los saves de QA. El editor queda abierto en Nivel_Entrega sin helper.
