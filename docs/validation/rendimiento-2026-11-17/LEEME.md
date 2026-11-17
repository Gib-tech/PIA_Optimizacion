# Condiciones de la muestra de render

UE 5.6, PIE en Windows 11 25H2, Ryzen 5 3600 y GeForce RTX 3060 Ti. Cámara preparada en (0, −1800, 90,15), yaw −90 y pitch −8, sin combate. Viewport 1014 × 550; la captura UI incluye la ventana del editor. Calidad distancia 1, AA 2, sombras 1 y texturas 2. No se presenta como una comparación de optimización antes/después ni como benchmark del ejecutable.

`muestra.json` registra 3 s de calentamiento y 5 s de callbacks de Slate con `t.MaxFPS 0`: media 12,47 ms y percentil 95 de 16 ms. Son intervalos del editor, no una promesa de FPS de la partida. La muestra anterior con grupos de calidad en cero se conserva en `muestra-baja.json`; no se comparan ambas como una mejora de código.

La lectura visible de `rhi-ui.png` muestra **DrawPrimitive calls: media 375,53; máximo 453; mínimo 344**, y triángulos dibujados: media 627.596,88. Son los valores de esa ventana de estadísticas; incluyen el contexto de render del editor. `stat RHI` y `stat SceneRendering` se activaron para inspección. `HighResShot` no captura la capa de estadísticas, por eso la evidencia del contador es `Shot showui` (`rhi-ui.png`); `rhi.png` sólo muestra el encuadre de gameplay.

La arquitectura usa Nanite donde corresponde, LOD clásico en modelos de demostración, materiales compartidos, radios/distancias de luces, culling de efectos y limpieza de restos. Repetir en el ejecutable y PC de exposición con la misma vista/calidad/resolución antes de comparar números. Las preferencias del usuario se restauran al terminar QA.
