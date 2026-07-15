# Pipeline: bandera ardiendo (Vellum + Pyro + brasas + shading)
Tags: #vellum #pyro #materialx #blackbody #vex #pipeline-completo

## Contexto
Proyecto de referencia: efecto hiperrealista de una bandera de tela ardiendo, desde desgarro de tela hasta render final en Karma XPU. Pipeline completo de 7 fases, útil como plantilla para futuros efectos de "combustión de sólidos" (madera, ropa, papel, etc.) — aplicable al Shot 1 del portfolio (llamas de dragón + elemento sólido secundario ardiendo).

## Pipeline por fases

### Fase 1 — Geometría base (SOPs)
Malla base de la bandera → puntos fijos del asta (para el pin constraint) → pre-fractura de la tela (permite que se desgarre de forma creíble en vez de estirarse indefinidamente) → dos atributos procedurales iniciales que controlarán cómo se quema cada fibra.

### Fase 2 — Ignición procedural (Wrangle)
Ignición desde una esquina/punto de origen usando combinación de:
- `time_gate` (cuándo empieza a arder cada zona)
- factor espacial (distancia al punto de ignición)
- `(1 - @fire_resist)` — resistencia al fuego por punto, permite zonas que tardan más en prender

Genera los atributos: `@fuelmask`, `@heat`, `@burn`.

### Fase 3 — Vellum Cloth Solver
Constraints recomendados:
- Stretch: 1e5
- Bend: 1e3
- Breaking: ON (permite desgarro real de la tela)
- Pin del asta: 1e8 (prácticamente rígido en el punto de sujeción)
- Substeps ≥3, Iterations ≥60 para estabilidad

Wrangle interno dentro del solver: samplea el volumen de Pyro para traer `@heat`, `@burn`, `@burn_edge` de vuelta a los puntos de tela — así la simulación de tela "sabe" dónde está ardiendo en tiempo real.

Desde aquí la señal se bifurca en dos direcciones:
- `@fuel` + `@temp` → alimenta la Fase 4 (Pyro)
- `@burn_edge` → alimenta la generación de brasas (POPs)

### Fase 4 — Pyro (fuego)
El fuego se genera usando el fuel/temperature que vienen de los puntos Vellum activos (el frente de quemado).

### Fase 5 — Brasas (POPs)
Partículas generadas específicamente en el `@burn_edge` (el frente activo de combustión), no en toda la superficie — así las brasas solo salen del borde que está ardiendo ahora mismo, no de zonas ya quemadas o aún no alcanzadas.

### Fase 6 — Shading (MaterialX)
Primvars usados como input del shader: `burn`, `heat`, `burn_edge` → controlan:
- BaseColor (transición a ceniza conforme `burn` sube)
- Roughness
- Opacity (para simular consumición del material)

Emisión: Blackbody 700–2200 K. Las brasas usan **pura emisión sin diffuse** (no reciben luz, solo la emiten).

### Fase 7 — Render (Karma XPU)
- Dome HDRI oscuro (para que la emisión del fuego sea el contraste dominante)
- Pyro Shader LOP
- Geometry Light sobre el volumen de fuego (para que el fuego ilumine su entorno correctamente)
- Path Traced

## Atributos clave que atraviesan todo el pipeline
| Atributo | Comportamiento |
|---|---|
| `@burn` | 0→1, nunca baja (combustión es irreversible) |
| `@heat` | instantáneo, sube y baja según proximidad al fuego activo |
| `@burn_edge` | marca el frente activo de combustión |
| `@noise_fray` | variación procedural para que el borde quemado no sea uniforme |
| `@fire_resist` | resistencia al fuego por punto/zona |
| `@fuel` / `@temperature` | fuente que alimenta el Pyro |

## Aplicación al portfolio
Este pipeline es la base para el Shot 1 (dragón) si se añade un elemento sólido secundario ardiendo (madera, tela, hierba) además del char/scorch progresivo en el suelo — reutilizar la lógica de `@burn`/`@burn_edge`/Blackbody en vez de partir de cero.
