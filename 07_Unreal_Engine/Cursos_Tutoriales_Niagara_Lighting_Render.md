# Cursos y tutoriales — Niagara, lighting y render en UE
Tags: #unreal #aprendizaje #cursos #niagara #lighting #render
Volver: [[00_MOC_Unreal]] · Relacionado: [[Niagara_Fundamentos_y_Cinematica]], [[Iluminacion_Cinematica_Realista]], [[Movie_Render_Graph_Salida_a_Nuke]]

> Recopilado el 2026-10-07. Precios y contenidos cambian: comprobar antes de pagar. Criterio de selección: **realismo cinemático + útil para un artista de Houdini/Nuke**, no FX estilizado de juego.

## ⭐ Prioridad (mi top para empezar)
1. **William Faucher (YouTube, gratis)** — lighting cinemático realista, cómo funciona la luz real y cómo trasladarlo a UE; grading. Ex-VFX (*Black Panther*, *Watchmen*). Autor de las Easy tools ([[Fab_Easy_Tools_William_Faucher]]). → Fundamentos de lighting.
2. **Udemy — "Unreal Generalist: Cinematic Rendering Pipeline"** (actualizado abril 2026) — MRQ de producción, Path Tracer, Lumen para cinemática, **render por pases (beauty, fog, VFX) y compo en Nuke**, herramientas BP de render en 1 clic. → Es literalmente mi pipeline UE→Nuke.
3. **Contenido oficial de Epic (gratis)** — Niagara Tutorials, Content Examples, +50 sistemas Niagara gratuitos de 5.7. → Base de Niagara.
4. **The Gnomon Workshop — "Cinematic Lighting in Unreal Engine 5" (Ted Mebratu, lighting artist de Naughty Dog)** — 2 h avanzadas: lightmaps vs Lumen, niebla/atmósfera, multi-cámara en Sequencer, composición dramática. Suscripción ~49 $/mes → 1 mes y exprimirlo.

## Niagara
### Gratis
- **Epic — Tutorials for Niagara Effects** (docs oficiales): ejemplos paso a paso desde ambiente a interacciones complejas. [link](https://dev.epicgames.com/documentation/unreal-engine/tutorials-for-niagara-effects-in-unreal-engine)
- **Epic — +50 sistemas Niagara gratuitos listos para 5.7** (explosiones, chispas, humo…): diseccionarlos es la mejor escuela. [link](https://www.unrealengine.com/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7)
- **Epic — Content Examples** (proyecto gratuito en Fab/launcher): mapas de Niagara con cada feature aislada.
- **Niagara Fluids Quick Start** (docs oficiales). [link](https://dev.epicgames.com/documentation/unreal-engine/niagara-fluids-quick-start-guide-for-unreal-engine)
- **Niagara Data Channels intro** (foro Epic). [link](https://forums.unrealengine.com/t/tutorial-niagara-data-channels-intro/1338576)
- **CGHOW** — colección de **1000+ tutoriales de VFX en Niagara** (más orientado a juego, pero cubre todos los módulos). [link](https://forums.unrealengine.com/t/1000-unreal-engine-vfx-tutorials-collection/2733843)
- **Epic Learning (dev.epicgames.com/community)** — cursos de VFX periódicos. [link](https://www.unrealengine.com/learning/februarys-epic-learning-content-vfx-2d-animation-and-digital-twins)

### De pago
- **Coursera — "Unreal Engine: Master Advanced FX & Gameplay Design"** — reseñas muy buenas sobre la parte de Niagara. [link](https://www.coursera.org/learn/unreal-engine-master-advanced-fx-gameplay-design/reviews)
- Udemy "Stylized Game VFX: Hit Impact" (UE 5.7) — **estilizado**, solo si quiero dominar módulos básicos rápido; no es mi objetivo de realismo. [link](https://www.udemy.com/course/learn-stylized-game-vfx-in-unreal-engine-5-hit-impact/)

## Lighting cinemático
- **William Faucher** — "Lighting in UE5 for Beginners" (día y overcast desde cero) y "cómo hacer que Unreal se vea más cinemático" (incluye grading en Resolve). [CGTricks](https://cgtricks.com/lighting-in-unreal-engine-5-for-beginners-william-faucher) · [Evermotion](https://evermotion.org/tutorials/show/12491/how-to-make-unreal-look-more-cinematic)
- **Gnomon — Cinematic Lighting in UE5 (Ted Mebratu)**. [link](https://origin.thegnomonworkshop.com/blog/cinematic-lighting-in-unreal-engine-5)
- **Gnomon — Lighting for Games & Cinematics Using UE5 (Eric Roin)** — personajes + entornos, 3 shots con distintas horas del día, interior y exterior. [link](https://gnomon.thegnomonworkshop.com/blog/real-time-character-environment-lighting)
- **JSFILMZ (YouTube)** — fotorrealismo con assets de marketplace y **path tracing**.
- **CG Spectrum — Realtime Technical Artist / Virtual Production** (Faucher como mentor): formación larga con mentor, cara. [link](https://cgspectrum.com/mentors/william-faucher)

## Render / Sequencer / MRQ-MRG
- **Udemy — Unreal Generalist: Cinematic Rendering Pipeline** ⭐ (ver arriba). [link](https://www.udemy.com/course/unreal-generalist-cinematic-rendering-pipeline/)
- Udemy — UE5 Master Cinematics: Sequencer & Animation (luz direccional, HDRI, niebla volumétrica, MRQ). [link](https://www.udemy.com/course/unreal-engine-5-master-cinematics-sequencer-animation/)
- Udemy — Unreal Cinematic Mastery (workflow de lighting en Sequencer + MRQ). [link](https://www.udemy.com/course/unreal-cinematic-mastery-from-beginner-to-cinematic-creator/)
- Udemy — UE5 Complete Beginners Cinematic Course (básico: EXR, deferred, AA). [link](https://www.udemy.com/course/unreal-engine-5-the-complete-beginners-cinematic-course/)
- **Escape Studios — Unreal Engine for Film and TV** (online, curso estructurado; la edición de junio 2026 ya empezó, mirar próximas). [link](https://author.escapestudios.ac.uk/courses/short-courses/unreal-engine-for-film-and-tv-evening-online/)
- Foro Epic — UE5 Beginner Tutorial Day 9: Movie Render Queue. [link](https://forums.unrealengine.com/t/2524290)

> ⚠️ Casi todo el material de pago habla de **Movie Render Queue**; en 5.8 lo actual es **Movie Render Graph** (production ready). Los conceptos (samples, warm-up, EXR, pases) son los mismos → traducir a MRG con [[Movie_Render_Graph_Salida_a_Nuke]] y [[UE58_Python_API_Aprendizajes]].

## Plan de estudio sugerido (encaja con el roadmap de [[00_MOC_Unreal]])
| Bloque | Material | Encaja con |
|---|---|---|
| Lighting base | Faucher (gratis) → Gnomon Mebratu | Fase 2 (lighting study) |
| Cámara/Sequencer | Udemy Master Cinematics (secciones de cámara) | Fase 3 |
| Niagara base | Docs Epic + Content Examples + pack 50 sistemas | Fase 4 |
| Render UE→Nuke | Udemy Unreal Generalist Rendering Pipeline | Fases 2–6 |
| Niagara avanzado | Niagara Fluids + Heterogeneous Volumes + Sim Cache | Fase 5 |

## Por verificar
- [ ] Canales de YouTube adicionales que me recomienden (añadir aquí solo tras ver 1–2 vídeos y juzgar calidad).
- [ ] Si Faucher tiene curso de pago propio actualizado a 5.7/5.8.
