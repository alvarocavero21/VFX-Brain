# Easy Tools de William Faucher (Fab)
Tags: #unreal #fab #plugins #clima #atmosfera #faucher
Volver: [[00_MOC_Unreal]]

**William Faucher**: artista 3D/VFX (Canadá, vive en Oslo), créditos en *Black Panther* y *Watchmen*. Su canal de YouTube es de las mejores referencias para lighting cinemático realista en UE. Sus "Easy" tools son Blueprints + Niagara + Material Functions controlados desde **un único Blueprint**, pensados para cinemática con MRG/MRQ (motion blur correcto).

> ⚠️ Compatibilidad: EasyToolbag se anunció para 5.1–5.6 (luego 5.6+). **Comprobar en la página de Fab que cada tool tiene build para 5.8** antes de comprar. Precios: mirar en Fab (cambian con rebajas).

## Resumen rápido

| Tool | Qué hace | Cuándo usarla |
|---|---|---|
| **EasyToolbag** | Menú in-engine que convierte setups de muchos clics en 1 clic | Siempre, desde el día 1 |
| **EasyFog** | Niebla, nubes bajas y "mood" localizado | Profundidad atmosférica, separar planos |
| **EasyRain** | Lluvia realista (Niagara) + charcos + goteos | Noche lluviosa, urbano, drama |
| **EasySnow** | Nieve (copos 3D) + acumulación en materiales | Invierno, ventisca |
| **EasyAtmos** | Partículas ambientales: hojas, bichos, humo, chispas, polvo, niebla densa local, rocas que caen | Secundarios: "aire vivo" |
| **EasyMapper** | Master material triplanar + Nanite displacement + vertex paint | Texturizar kitbash/escaneos rápido y sin UVs |

## EasyToolbag
Construido sobre Editor Utilities de Epic. Funciones:
- Crear **Post Process Volume** con valores por defecto sensatos (unbound).
- Crear **Level Sequence con CineCamera** ya enganchada → navegar escena desde la cámara.
- **Environment Light Mixer**: genera Sky Atmosphere + Volumetric Clouds + Exponential Height Fog + Directional Light + Sky Light de golpe.
- Helpers de viewport: limitar FPS, screen percentage, exposición, cambiar anti-aliasing.
- Botones dedicados que **spawnean EasyFog/Rain/Atmos/Snow delante de la cámara**.
- Uso: es la base de mi proyecto plantilla (Fase 1 del roadmap).

## EasyFog
- Herramienta para añadir niebla, nubes y ambiente a entornos.
- Útil para lo que el Exponential Height Fog global no hace bien: **bancos de niebla locales**, niebla que se arrastra por el suelo, capas entre planos.
- Truco de composición: niebla entre primer plano y fondo = separación de profundidad (aerial perspective) → la escena "lee" como grande.

## EasyRain
- Rain Blueprint con Niagara: de llovizna a tormenta.
- Cada gota usa una **textura animada basada en estudios reales usados en VFX** → con motion blur de MRG queda creíble.
- **Cortinas de lluvia fina** a distancia para dar profundidad.
- **Backlighting/refracción**: la lluvia solo se ve de verdad a contraluz → poner una luz detrás (farola, luna, rim) es obligatorio en lluvia nocturna.
- Material Functions:
  - **Puddles**: charcos controlados por BP (tamaño, forma, color, humedad), funcionan con landscape.
  - **Droplets/Leaks**: goteos animados en superficies.
- Parámetros: color, opacidad, escala de movimiento, intensidad de backlight/refracción, densidad, splashes.
- Rinde bien incluso en GPUs modestas.

## EasySnow
- Niagara + Material Function, un solo BP.
- **Cada copo es un modelo 3D basado en clumps reales** → se ilumina y sombrea de verdad.
- De ligeras rachas a ventisca, motion blur correcto con MRQ/MRG.
- **Acumulación**: Material Function que se conecta al master material → nieve acumulada en todos los modelos del nivel, con **Nanite Tessellation/Displacement**, brillo (glimmer) y parámetros de cantidad, falloff y breakup.
- Implica tener master materials propios (o EasyMapper) para inyectar la función.

## EasyAtmos
- Un único BP controla: hojas a la deriva, enjambres de bichos, humo, chispas, polvo, niebla localizada densa, rocas que se desmoronan (con **mallas propias**).
- Todo **keyframeable** en Sequencer.
- Es exactamente el tipo de "secundarios" que el rol de crítico técnico pide (ver [[Checklist_Critico_Realismo_UE]]): sin partículas en el aire los planos se ven estériles.

## EasyMapper
- Master material: proyección **world-aligned (triplanar)** + **Nanite displacement** + **vertex painting avanzado** (mezcla de capas: suciedad, musgo, desgaste).
- Ideal para kitbash, bloqueos o mallas de Houdini sin UVs buenas.

## Cómo encajan en mi pipeline
- Clima/atmósfera "de fondo" → Easy tools (rápido, cinemático).
- FX hero (fuego del dragón, destrucción, agua) → **Houdini** y traer a UE ([[Puente_Houdini_Unreal]]). Las Easy tools complementan, no sustituyen.

## Fuentes
- [EasyToolbag en Fab](https://www.fab.com/listings/b6d9b879-1b66-4b47-b8f3-572a3b038e7f) · [Infinite Detail sobre EasyToolbag](https://www.infinitedetail.xyz/newsletters/william-faucher-s-easytoolbag-is-the-ue5-time-saver-you-didn-t-know-you-needed) · [Digital Production](https://digitalproduction.com/2025/10/16/one-toolbag-to-rule-your-clicks/)
- [EasyFog en Fab](https://www.fab.com/listings/0a1c0c21-ff23-4fb7-9dc5-7beb6e16ce64) · [EasyFog Gumroad](https://williamfaucher.gumroad.com/l/easyfog)
- [80.lv — EasyRain](https://80.lv/articles/william-faucher-on-easyrain-a-new-unreal-engine-5-add-on) · [80.lv — EasySnow](https://80.lv/articles/get-this-powerful-ue5-tool-for-realistic-snow-effects) · [80.lv — EasyAtmos](https://80.lv/articles/add-atmosphere-depth-to-your-ue5-project-in-just-few-clicks)
- [Foro UE — EasyMapper](https://forums.unrealengine.com/t/2424047)
