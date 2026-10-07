# Niagara — fundamentos y uso cinemático (UE 5.8)
Tags: #unreal #niagara #fx #particulas #ue58
Volver: [[00_MOC_Unreal]] · Relacionado: [[Tecnica_Nave_Aterrizando_Thrusters_Polvo]], [[Puente_Houdini_Unreal]], [[Cursos_Tutoriales_Niagara_Lighting_Render]]

> Investigado el 2026-10-07. Estado de plugins **verificado en mi instalación de UE 5.8.2** (ficheros `.uplugin`), no solo en webs.

## Traducción mental desde Houdini
| Houdini | Niagara |
|---|---|
| DOP network / POP network | **Niagara System** (asset que se coloca en el nivel) |
| Un POP source + sus fuerzas | **Emitter** (dentro del System) |
| POP nodes (force, drag, wrangle…) | **Modules** apilados en el *stack* |
| Atributos `@P`, `@v`, `@age`, `@life`, `@Cd`, `@pscale` | `Particles.Position`, `Velocity`, `Age`, `Lifetime`, `Color`, `SpriteSize` |
| Wrangle VEX | **Scratch Pad module** (grafo de nodos) o HLSL custom |
| Ejecución por frame / substeps | Etapas: Spawn / Update (+ **Simulation Stages** para iterar en GPU) |
| Volumen / campos | **Grid 2D / Grid 3D** (data interfaces) |
| Instance / Copy to points | **Mesh Renderer** |
| Parámetros de HDA promovidos | **User Parameters** (`User.X`), editables por instancia, BP o Sequencer |
| Cache a disco (`.bgeo.sc`) | **Niagara Sim Cache** (grabar y reproducir en Sequencer) |

## Arquitectura (lo esencial)
- **Namespaces**: `System.` (global del sistema), `Emitter.` (por emisor), `Particles.` (por partícula), `User.` (expuesto hacia fuera), `Engine.` (tiempo, owner…).
- **Stacks**: System Spawn/Update → Emitter Spawn/Update → Particle Spawn/Update → Event Handlers / Simulation Stages → **Renderers**.
- **Sim target**: **CPU** (pocas partículas, colisión con escena por raycast, eventos) vs **GPU** (miles/millones, colisión con depth buffer o distance fields, simulation stages, grids).
- **Renderers**: Sprite, Mesh, Ribbon (estelas), Light (luces por partícula — con MegaLights en 5.7+ salen baratas), Component, **Heterogeneous Volumes** (volúmenes, Beta desde 5.7), **Nanite** (Experimental en 5.8, plugin `NiagaraNanite`).
- **Data Interfaces**: leer el mundo — Static/Skeletal Mesh (emitir desde superficie), Spline, Collision Query, Grid, Texture/Render Target, Curve, Audio, Chaos destruction…
- **Fixed bounds**: siempre fijar bounds en cinemática (si no, el sistema se puede *cullear* al salir de cámara).

## Funciones modernas y su estado en 5.8
| Feature | Estado | Para qué |
|---|---|---|
| **Lightweight (stateless) emitters** | Beta desde 5.5 | Emisores sin compilar ni tick: ambiente, polvo, chispas simples. Muy baratos |
| **Niagara Data Channels** | Production Ready desde 5.5 | Pasar datos entre sistemas/gameplay (ej. un único sistema gestiona todos los impactos) |
| **Heterogeneous Volumes renderer** | Beta (5.7) | Humo/fuego volumétrico real, sombras, compatible con MegaLights |
| **Niagara Fluids** (Grid 2D/3D Gas, FLIP, Shallow Water) | **Beta** (plugin `NiagaraFluids`) | Fuego/humo/agua simulados en tiempo real. 3D = caro → hero/cinemática. Se puede hornear a flipbook |
| **Niagara Sim Caching** | Estable (plugin) | Grabar la sim y reproducirla en Sequencer → **determinista y scrubbeable**, clave para render |
| **NiagaraMRQ** | Beta | Data interface que lee info de Movie Render Queue/Graph dentro de Niagara (sub-frames, etc.) |
| **ChaosNiagara** | Beta | Leer datos de destrucción Chaos → polvo/debris secundario al romperse |
| **PCGNiagaraInterop** | Experimental | PCG ↔ Niagara |
| **Cascade→Niagara converter** | Beta | Migrar sistemas viejos de Cascade |
| **NiagaraToolsets** (MCP) | Experimental | Existe, pero no se usa: el MCP está desconectado ([[MCP_Unreal_ClaudeCode]]) |

Plantillas incluidas en el engine (`Niagara/Content/DefaultAssets/Templates/Systems`): DirectionalBurst, RadialBurst, SimpleExplosion, Fountain/Minimal **Lightweight**, AttributeReaderTrails… + emisores y "BehaviorExamples".

## Reglas para FX cinemáticos realistas en Niagara
1. **Determinismo**: activar *Deterministic* + seed fija en emisores → cada render sale igual. Mejor aún: **Sim Cache** y reproducir desde Sequencer.
2. **Warm-up**: el sistema tiene que estar "lleno" en el frame 1 → warm-up en el System o en MRG ([[Movie_Render_Graph_Salida_a_Nuke]]).
3. **Motion blur**: los sprites no tienen vectores de velocidad por defecto como la geometría — usar temporal samples de MRG (sub-frames reales) y/o *motion vector settings* del renderer. Revisar que no haya "stepping".
4. **Iluminación**: humo/polvo **lit** (no unlit): material translúcido con *Translucency Lighting Mode* volumétrico, o directamente **Heterogeneous Volumes** para humo hero. El humo unlit es lo que más delata un FX amateur.
5. **Escala y velocidad física**: gravedad 980 cm/s², drag realista, tamaño de chispa ~0.5–2 cm. Mismo criterio que en Houdini.
6. **Texturas de humo de calidad**: flipbooks de sims reales (hornear desde Houdini/EmberGen o Niagara Fluids a flipbook) con normales/motion vectors para interpolar frames (*sub-UV blending*).
7. **Capas**: núcleo + secundarios + residuos (ej. explosión = flash + fuego + humo + debris + chispas + polvo que se asienta + scorch decal). Una sola capa = amateur.
8. **Fixed bounds + scalability "Cinematic"** para que nada se reduzca por distancia.

## Cuándo Niagara y cuándo Houdini (mi criterio)
- **Niagara**: ambiente (polvo, partículas en el aire, lluvia, nieve, chispas, embers), secundarios que reaccionan a la escena, iteración rápida en contexto, muchas instancias.
- **Houdini → VDB / Alembic / VAT**: hero pyro, destrucción, agua FLIP, cualquier cosa que tenga que aguantar un primer plano → ver [[Puente_Houdini_Unreal]].
- **Mixto (lo más habitual)**: hero en Houdini + secundarios Niagara que leen la geometría/destrucción (ChaosNiagara, mesh data interfaces).

## Ruta de aprendizaje Niagara (por sesiones)
1. Abrir el **Content Examples** de Epic (mapas de Niagara) y los **+50 sistemas Niagara gratuitos de 5.7**: diseccionar 3–4 (humo, chispas, explosión, lluvia).
2. Emisor de **chispas** CPU con colisión y luz por partícula (Light renderer) → cubre módulos básicos.
3. **Polvo ambiente** con lightweight emitter (barato, cinemático).
4. **Humo lit** con flipbook + sub-UV blending, después versión **Heterogeneous Volumes**.
5. Scratch Pad: un módulo propio (ej. fuerza radial dependiente de altura, la base del polvo de aterrizaje).
6. **Niagara Fluids Grid 3D Gas**: fuego cinemático + comparar con pyro de Houdini en coste y look.
7. **Sim Cache + Sequencer + MRG**: render determinista.

## Fuentes
- [UE 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes) · [UE 5.7 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-7-release-notes) · [Tom Looman — 5.5 highlights](https://tomlooman.com/unreal-engine-5-5-performance-highlights/)
- [Niagara Lightweight Emitters Overview](https://dev.epicgames.com/documentation/unreal-engine/niagara-lightweight-emitters-overview) · [Roadmap: Lightweight Emitters](https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/1687-niagara-lightweight-emitters-beta) · [Tutorial Niagara Data Channels](https://forums.unrealengine.com/t/tutorial-niagara-data-channels-intro/1338576)
- [Niagara Fluids](https://dev.epicgames.com/documentation/unreal-engine/niagara-fluids-in-unreal-engine) · [Fluid Simulation Overview](https://dev.epicgames.com/documentation/unreal-engine/fluid-simulation-in-unreal-engine---overview) · [Niagara Fluids Reference](https://dev.epicgames.com/documentation/unreal-engine/niagara-fluids-reference-in-unreal-engine)
- [+50 sistemas Niagara gratis (5.7)](https://www.unrealengine.com/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7)
