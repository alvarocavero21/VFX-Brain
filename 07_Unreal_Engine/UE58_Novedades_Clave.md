# Unreal Engine 5.8 — novedades clave para cinemática realista
Tags: #unreal #ue58 #referencia #version
Volver: [[00_MOC_Unreal]]

> Investigado el 2026-10-06 a partir de release notes oficiales y prensa. UE 5.8 salió en **junio 2026** y es la **última versión mayor planificada de UE5** (UE6 apunta a Early Access a finales de 2027) → versión estable para aprender y producir los próximos ~2 años.
> Antes de afirmar algo muy concreto de un nodo/cvar, comprobar en el editor: la documentación de 5.8 aún es nueva.

## Lo que más me importa (ordenado por impacto en mis shots)

### 1. Movie Render Graph (MRG) — Production Ready ✅
- Sustituye en la práctica a los presets "legacy" de Movie Render Queue: el grafo ya soporta todas las features importantes del sistema antiguo.
- **Render layers** ampliados y control de post-producción → pasar capas separadas a Nuke como en Karma.
- **Light Modifier**: override de propiedades de luces **por render layer** (ej. layer de solo luz de relleno, layer sin luz de clave). Ideal para relighting en compo.
- **Accumulation Depth of Field** (nuevo): DOF acumulando varias posiciones de apertura → bokeh físicamente más correcto, sin los artefactos del DOF post-proceso en bordes/partículas.
- Detalles de uso en [[Movie_Render_Graph_Salida_a_Nuke]].

### 2. MegaLights — Production Ready ✅
- Permite órdenes de magnitud más luces dinámicas con sombra, incluidas **area lights con sombras suaves** realistas.
- 5.8: mucho menos ruido, más rendimiento, soporte de transmisión, translucidez basada en froxels, **IES en volumétricos**, lighting channels y **sombras de nubes**.
- Para cinemática nocturna/urbana (farolas, neones, ventanas) cambia el juego: ya no hay que hacer trampas con pocas luces.
- Cvars mencionadas: `r.MegaLights.ScreenTraces.Quality`, `r.MegaLights.LightAttenuationFalloff`.

### 3. Lumen Lite — Beta
- GI de calidad media con irradiance fields, ~2× más rápido que Lumen High. Pensado para juego a 60 fps.
- **Para cinemática no lo uso en el render final** (Lumen High / Epic o path tracer), pero sí para trabajar fluido en el viewport del laptop si la escena es pesada.

### 4. Mesh Terrain — Experimental
- Terreno de nueva generación basado en malla: modelado 3D, capas, virtual texturing, teselación variable y Nanite. Permite voladizos/cuevas que el Landscape clásico (heightfield) no hace.
- Experimental → para portfolio aún prefiero Landscape o malla de Houdini (Heightfield → mesh → Nanite). Seguir de cerca.

### 5. PCG — mejoras grandes
- **Edición manual sobre contenido procedural** sin romper el procedimiento (antes era todo o nada).
- Atributos complejos (arrays, structs, sets, maps), subgrafos embebidos, scatter GPU en runtime al nivel del landscape grass.
- Nodos nuevos: operaciones de arrays de metadatos, Align Points, Scene Capture, Apply Spline to Component.
- Mentalidad: PCG ≈ "SOPs de scattering" dentro de UE. Mi experiencia en Houdini se transfiere bien.

### 6. Procedural Vegetation Editor — Experimental
- Crear/editar mallas de vegetación con soporte **Nanite Foliage** dentro de UE (nodos de crecimiento, semillas, injertos, evitar objetos).

### 7. Rendering de volumen / atmósfera
- **FSSS – Fog Screen Space Scattering** (Experimental): aproxima scattering múltiple en medios participantes → niebla más creíble alrededor de fuentes de luz.
- `r.Lumen.HeightFog` activado por defecto (la height fog recibe GI de Lumen).

### 8. Materiales
- **X-Rite AxF → Substrate** (Production Ready): importar materiales medidos (escaneados) reales. Muy útil para coches, tejidos, product shots.
- Substrate Toon/NPR (Experimental) — no relevante para realismo.

### 9. Personajes (si meto humanos en plano)
- **Mesh to MetaHuman** production ready (cualquier malla humana → MetaHuman riggeado, cabeza + cuerpo).
- **MetaHuman Crowd** (Experimental) con Mass: multitudes de fondo.
- MetaHuman Animator: captura de cuerpo con una sola cámara (Experimental).
- Control Rig: physics (Beta), dynamics (nuevo), direct mesh controls (Experimental).

### 10. Editor / productividad
- **Sequencer**: Simple View, AutoBaking, selección sincronizada viewport/Sequencer/Curve Editor.
- Gizmos nuevos con **preset estilo Maya** (Interaction presets: Default / Classic / Maya-style) → configurarlo el primer día.
- **Sandboxes**: espacios aislados para experimentar sin romper el proyecto.
- **MCP Server** (Experimental): plugin Model Context Protocol para conectar LLMs (Claude) al editor. Potencial: que Claude Code configure escenas/settings directamente → explorar en una fase futura, igual que hice con ComfyUI ([[Pipeline_ComfyUI_ClaudeCode_MCP]]).
- Import FBX más rápido (uFBX, Experimental); USD via Interchange production ready para assets.

## Qué NO tocar todavía (experimental, riesgo de perder tiempo)
Mesh Terrain, Procedural Vegetation Editor, FSSS, MetaHuman Crowd → probar en proyecto de pruebas, no en shot de portfolio.

## Fuentes
- [UE 5.8 Release Notes (Epic)](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US)
- [Anuncio oficial UE 5.8](https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available)
- [Tom Looman — UE 5.8 Performance Highlights](https://tomlooman.com/unreal-engine-5-8-performance-highlights/)
- [Ludus — UE 5.8 What's New](https://ludusengine.com/blog/unreal-engine-5-8-whats-new)
