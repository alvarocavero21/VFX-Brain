# MOC — Unreal Engine 5.8 para escenas cinemáticas realistas
Tags: #unreal #moc #cinematica #roadmap

Mapa de contenido de todo lo relacionado con Unreal en el vault. Objetivo: llegar a producir **shots cinemáticos fotorrealistas en UE 5.8** que aguanten al lado de los renders de Karma del reel, y aprovechar UE como "segundo motor de render" para el portfolio.

## Notas de referencia
- [[UE58_Cine_Template]] — proyecto plantilla (settings, presets MRG, nivel lookdev, MCP)
- [[MCP_Unreal_ClaudeCode]] — servidor MCP de UE 5.8: qué puede y qué no (⛔ desconectado 2026-10-07: Claude guía, Álvaro ejecuta)
- [[UE58_Python_API_Aprendizajes]] — Python en el editor/headless, MRG por código, errores reales
- [[Niagara_Fundamentos_y_Cinematica]] — Niagara explicado desde Houdini, estado de features en 5.8, reglas para FX cinemáticos
- [[Cursos_Tutoriales_Niagara_Lighting_Render]] — cursos y tutoriales curados (Niagara, lighting, render) + plan de estudio
- [[Tecnica_Nave_Aterrizando_Thrusters_Polvo]] — técnica de thrusters + polvo de aterrizaje (pendiente de montar)
- [[UE58_Novedades_Clave]] — qué trae 5.8 y qué me importa como artista VFX
- [[Fab_Easy_Tools_William_Faucher]] — EasyFog, EasyRain, EasySnow, EasyAtmos, EasyMapper, EasyToolbag
- [[Fab_Otras_Herramientas_y_Assets]] — Megascans, packs gratis, plugins útiles
- [[Iluminacion_Cinematica_Realista]] — Lumen, MegaLights, exposición, atmósfera, path tracer
- [[Camara_Sequencer_Lenguaje_Cine]] — CineCamera, ópticas, DOF, motion blur, Sequencer
- [[Movie_Render_Graph_Salida_a_Nuke]] — render final, AA, EXR, ACES/OCIO, AOVs
- [[Materiales_Assets_Realismo]] — Substrate, Nanite, displacement, escala, imperfecciones
- [[Puente_Houdini_Unreal]] — índice de la guía Houdini → UE 5.8 (carpeta `Houdini_a_UE/`: setup, pyro VDB, RBD, Houdini Engine/FLIP/USD)
- [[Checklist_Critico_Realismo_UE]] — revisión antes de dar un shot por bueno

## Roadmap de aprendizaje (por fases, una por sesión)
Siguiendo la regla del vault: **una fase por sesión**. ⚠️ Desde 2026-10-07: **modo aprendizaje**, cada fase termina en notas y valores documentados, no en renders (salvo que Álvaro lo pida).

| Fase | Objetivo | Entregable | Estado |
|---|---|---|---|
| 0 | Base de conocimiento (estas notas) | Notas en `07_Unreal_Engine/` | ✅ 2026-10-06 |
| 1 | Proyecto plantilla cinemático (settings, MRG presets, nivel lookdev, MCP) | Proyecto `UE58_Cine_Template` reutilizable | ✅ 2026-10-07 (faltan checks manuales) |
| 2 | Lighting study: misma escena Megascans en 3 looks (golden hour / overcast / noche) | Valores y recetas documentados (sin render, decisión de Álvaro: solo aprender) | 📘 2026-10-07 |
| 3 | Cámara y lenguaje: 1 plano de 6–8 s con cámara "humana" (handheld sutil, rack focus) | Clip MRG | ⬜ |
| 4 | Clima con Easy tools: lluvia nocturna o nieve con acumulación | Clip MRG + breakdown | ⬜ |
| 5 | Integración Houdini → UE: sim (pyro VDB o RBD) dentro de escena UE | Shot con FX de Houdini | ⬜ |
| 6 | Shot de portfolio completo + compo Nuke | Shot para el reel | ⬜ |

## Principios que repito en cada shot
1. **Referencia real primero** (foto/fotograma de peli). Sin referencia no hay realismo, solo "bonito".
2. **Escala física correcta** (UE trabaja en cm: 1 uu = 1 cm).
3. **Exposición fija manual**, nunca auto-exposure en cinemática.
4. **La cámara cuenta la historia**: óptica real, sensor real, movimiento con peso.
5. **Imperfecciones y secundarios**: polvo, partículas en el aire, suciedad, variación.
6. **Lo último se gana en compo** (Nuke): grano, aberración leve, grade.

## Registro de sesiones
- [[Sesion_2026-10-06_Base_Conocimiento_UE]]: Fase 0
- [[Sesion_2026-10-07_Fase1_Plantilla]]: Fase 1
- [[Sesion_2026-10-07b_Fase2_Lighting_Aprendizaje]]: Fase 2, solo aprendizaje (sin renders)
