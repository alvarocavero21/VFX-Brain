# Movie Render Graph y salida a Nuke
Tags: #unreal #render #mrg #nuke #aces #exr
Volver: [[00_MOC_Unreal]]

## Por qué MRG
En 5.8 **Movie Render Graph es Production Ready** y cubre todas las features del sistema legacy de Movie Render Queue. Es un grafo (me resulta natural viniendo de Houdini/Nuke): defines un preset reutilizable y lo aplicas a cualquier secuencia.

## Estructura conceptual
- **Globals**: resolución, frame range, output directory, nombre de archivos.
- **Renderer**: Deferred Renderer (Lumen) o **Path Tracer**.
- **Render Layers**: separar elementos con **Collections** (qué actores entran) y **Modifiers** (qué cambia en esa layer).
- **Light Modifier** (nuevo 5.8): override de propiedades de luces por layer → passes de luz para relighting en Nuke.
- **Outputs**: EXR (multicapa), PNG/JPG para previews, ProRes para dailies.
- **Console Variables**: subir calidad solo en render.

## Calidad: samples y anti-aliasing
- **Spatial samples**: más muestras por frame → menos ruido/aliasing.
- **Temporal samples**: subframes dentro del obturador → **motion blur real** (crucial en partículas).
- Con muchas muestras, poner Anti-Aliasing override en **None** y dejar que la acumulación limpie (si no, TSR + acumulación puede emborronar).
- Punto de partida: 1 spatial × 8–16 temporal para shots con movimiento; subir spatial si hay ruido de Lumen/MegaLights.
- **Warm-up frames** (render + engine warm-up): imprescindibles para que Niagara (lluvia, nieve, polvo) ya esté "llena" en el frame 1 y Lumen haya convergido.
- **Accumulation Depth of Field** (nuevo 5.8): DOF por acumulación de posiciones de apertura → bokeh más correcto, menos artefactos en bordes y partículas. Probarlo en shots con DOF fuerte.
- High-res tiling para stills de muy alta resolución.

## Cvars útiles en el nodo Console Variables (verificar en 5.8)
- `r.ScreenPercentage 100` (o >100 para supersampling)
- `r.DepthOfFieldQuality 4`
- `r.MotionBlurQuality 4`
- `r.Tonemapper.Quality 5`
- Calidad Lumen / MegaLights: mejor desde el Post Process Volume y documentar aquí qué funcionó.

## Color: ACES/OCIO y entrega a Nuke
Objetivo: **EXR lineal**, sin tonemapper "horneado", para gradear en Nuke igual que con Karma.
- Activar plugin **OpenColorIO** y configurar el config ACES igual que en Nuke (ver [[Version_Reference]] para versión de Nuke).
- En el output EXR: desactivar la tone curve / aplicar transform OCIO a ACEScg según convenga. Regla: lo que salga de UE y de Karma tiene que vivir en **el mismo espacio de trabajo** en Nuke.
- AOVs / passes útiles: Final Image, Scene Depth (Z para DOF/niebla en compo), World Normal, Base Color, Object ID/Cryptomatte (comprobar soporte en 5.8 MRG), y render layers por elemento (FG / BG / FX / atmósfera).

## Compo final en Nuke (donde se gana el "cine")
- Grade de referencia + LUT de visionado.
- **Grano de película** (sin grano UE se ve "CG limpio").
- Aberración cromática y viñeta MUY sutiles.
- Glow/halation en altas luces.
- Letterbox 2.39:1 si aplica.

## Pendiente (Fase 1)
- [ ] Crear y guardar preset MRG "Cine_Final" y "Cine_Preview" en el proyecto plantilla.
- [ ] Validar flujo EXR → Nuke 17 con ACES y documentar en [[06_Problemas_Resueltos]] lo que dé guerra.
