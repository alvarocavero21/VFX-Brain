# Iluminación cinemática realista en UE 5.8
Tags: #unreal #lighting #lumen #megalights #exposicion #atmosfera
Volver: [[00_MOC_Unreal]]

## Mentalidad
En Karma pienso "path tracer físico". En UE pienso igual pero sabiendo que **Lumen es una aproximación** con trucos de caché/pantalla. Reglas:
- Trabajar en **unidades físicas** (lux, candelas, nits) y **exposición manual**. Si la exposición es automática, cualquier ajuste de luz "se compensa solo" y nunca aprendes nada.
- Primero **luz clave + cielo**; añadir rebotes/fill solo si la referencia lo pide.
- Validar look con el **Path Tracer** como "verdad física" y comparar con Lumen.

## 1. Setup base de exterior (lo que monta el Environment Light Mixer / EasyToolbag)
- **Directional Light** (sol): Atmosphere Sun Light ON. Valores orientativos: sol directo ~75.000–120.000 lux; golden hour bastante menos.
  - Source Angle: ~0.5° (sol real) → sombras con penumbra correcta. Subir para cielos con bruma.
- **Sky Atmosphere**: da el color del cielo y la perspectiva aérea reales según el ángulo del sol.
- **Sky Light**: Real Time Capture ON (captura el Sky Atmosphere + nubes).
- **Volumetric Clouds**: nubes que proyectan sombra (en 5.8 MegaLights también soporta cloud shadows).
- **Exponential Height Fog** con **Volumetric Fog** ON → god rays y profundidad. En 5.8 `r.Lumen.HeightFog` (la niebla recibe GI) viene activado.
- **Local Fog Volumes** / EasyFog para niebla localizada.

## 2. Exposición (lo más importante para que "parezca cámara")
Post Process Volume (Unbound) → Exposure:
- **Metering Mode: Manual**.
- Opción A (fotográfica): activar **Apply Physical Camera Exposure** → la exposición sale de ISO / shutter / f-stop de la CineCamera. Mismo razonamiento que una cámara real (sunny 16 ≈ EV100 15 en exterior soleado).
- Opción B (rápida): Exposure Compensation a mano y dejar la cámara fuera.
- Project Settings → "Extend default luminance range in Auto Exposure settings" debe estar ON (default en UE5) para trabajar en EV100.
- Herramienta: viewport → **Show > Visualize > HDR (Eye Adaptation)** y **Pixel Inspector** para leer luminancias.

## 3. Lumen para cinemática (laptop 4090 / desktop 5080)
- Project Settings: **Hardware Ray Tracing ON** (Support Hardware Ray Tracing + Use Hardware Ray Tracing when available). Con RTX tiene sentido: reflejos y GI más estables.
- Post Process → Global Illumination:
  - Lumen Scene Lighting Quality ↑ (2–4 en render final).
  - Final Gather Quality ↑ (2–4) → menos ruido/manchas.
  - Max Trace Distance acorde a la escena (interiores grandes).
- Reflections: método Lumen, quality ↑; Ray Lighting Mode "Hit Lighting" para reflejos más correctos (más caro).
- **Lumen Lite** (5.8, Beta) solo para trabajar fluido en viewport, no para el final.
- Problemas típicos: light leaking en interiores (paredes demasiado finas → engrosar a ≥10 cm), GI que "tarda" en converger en cortes de cámara (usar warm-up frames en MRG).

## 4. MegaLights (5.8 Production Ready)
- Cuándo: muchas luces con sombra (ciudad nocturna, interiores con prácticas, neones, faros).
- Permite **area lights (Rect Lights) con sombras suaves** reales → iluminación de estudio creíble.
- 5.8 añade IES en volumétricos (conos de farola en niebla), lighting channels, transmisión, translucidez.
- Activar por proyecto y comprobar ruido en movimiento. Cvars de calidad: `r.MegaLights.ScreenTraces.Quality`.

## 5. Path Tracer
- Viewport → View Mode → Path Tracing, o nodo Path Tracer en MRG.
- Usos: **ground truth** para comparar Lumen; frames hero; product shots.
- Limitaciones: más lento, algunos efectos de post/Niagara/volúmenes se comportan distinto → probar antes de comprometer un shot entero.

## 6. Recetas de look (para la Fase 2 del roadmap)
- **Golden hour**: sol a 3–8° sobre el horizonte, Source Angle algo mayor, niebla con inscattering cálido, contraluz para siluetas y rim. Exposición pensada para las altas luces del cielo.
- **Overcast**: sol oculto/muy suave, la Sky Light hace todo, contraste bajo, sombras de contacto (AO) importantes. Lo que vende es la **humedad y los materiales** (roughness).
- **Noche**: luna fría con poca intensidad + **luces prácticas cálidas** (farolas, ventanas) → contraste de temperatura. Con lluvia: contraluz obligatorio (ver EasyRain en [[Fab_Easy_Tools_William_Faucher]]).
- **Interior**: luz entrando por ventana (sol + skylight), resto rebote. Rect lights invisibles en ventanas para ayudar a Lumen si hace falta.

### Valores de partida concretos (estudio del 2026-10-07, sin validar con render)
Para los tres casos: cámara f/2.8 fija (no cambia la DOF) y exposición con ISO/obturador. Regla rápida: gris medio ≈ 0,125 · 2^EV nits; iluminancia ≈ 2,5 · 2^EV lux.
| Look | Key | Cielo / ambiente | Niebla | Cámara (EV100) |
|---|---|---|---|---|
| Golden hour | Sol 100.000 lux *atmosphere sun light* (la atmósfera lo atenúa y calienta sola), elevación 5°, contraluz lateral justo fuera de cuadro, source angle 1° | Sky Atmosphere + Sky Light real-time | Volumétrica, scattering 0,7 hacia delante (halo a contraluz), inscattering cálido ~250 nits | ISO 100, 1/500 (EV ≈ 11,9) |
| Overcast | Key de 1.500 lux muy suave (source angle 20°), 6.800 K, sin atmósfera | Cúpula emisiva gris ~2.000 nits con `is_sky`, capturada por la Sky Light (≈ 6.000 lux de ambiente) | Densa (0,06), gris frío ~1.200 nits | ISO 100, 1/250 (EV ≈ 10,9) |
| Noche | "Luna de cine": 15 lux azulada (la real son ~0,3 lux; en rodaje se usa un HMI con gel azul) | Cúpula azul oscuro ~0,4 nits | Ligera, azul ~0,3 nits | ISO 3200, 1/50 (EV ≈ 3,6) |
| Práctica nocturna | Farol de 800 lm a 2.700 K (~64 lux a 1 m) más una esfera emisiva visible (la point light no se ve en cámara) | — | Volumetric scattering ×2 en la luz para el halo | — |

## 7. Lenguaje de luz (lo que separa "bonito" de "cine")
- Ratio key/fill definido (dramático 4:1–8:1).
- Motivar cada luz: toda fuente debe tener una justificación en el mundo.
- Separar sujeto de fondo: rim/contraluz, o fondo más brillante/oscuro que el sujeto.
- Guiar el ojo: el punto más brillante y con más contraste = donde quiero que mire.
- Mucho del "look de peli" se gana en **post/grading** (lo dice el propio Faucher) → ver [[Movie_Render_Graph_Salida_a_Nuke]].

## Fuentes
- [William Faucher — Lighting in UE5 for Beginners (CGTricks)](https://cgtricks.com/lighting-in-unreal-engine-5-for-beginners-william-faucher)
- [Rebusfarm — How to give your renderings a cinematic look](https://rebusfarm.net/news/how-to-give-your-renderings-a-cinematic-look)
- [UE 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US)
