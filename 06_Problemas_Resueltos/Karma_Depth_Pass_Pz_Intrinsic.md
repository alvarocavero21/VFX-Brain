# Extraer depth pass (Pz) correctamente en Karma XPU
Tags: #karma #depth-pass #xpu #renderVar #nuke

## Contexto
Al intentar extraer un depth pass de un render de Karma, el canal salía metido en el alpha (como si fuera el "extra" del EXR) en lugar de ser un canal flotante con valores de distancia reales. Esto pasaba al usar el checkbox estándar de "Depth (Camera Space)" en vez de un RenderVar manual. Resultado: en Nuke el canal aparecía negro/plano, sin info métrica usable.

## Solución
En `karmarendersettings`, sección **Extra Render Vars**, crear un RenderVar manual (no usar el checkbox de Depth):

- `Name`: `Pz`
- `VEX Variable`: `Pz`
- `VEX Type`: `float`
- `Precision`: `32 bit float`
- `Pixel Filter`: `minmax`
- `Filter Mode`: `zmin`
- `Source Name`: `z` (minúscula)
- `Source Type`: **Intrinsic** (en versiones de Karma que no tienen "Camera Space" como opción, Intrinsic es el equivalente para variables internas del renderer)

Pasos adicionales:
1. Desactivar el checkbox de "Depth (Camera Space)" original — si ambos están activos hay conflicto.
2. Para renders de depth puro, bajar `Path Traced Samples` a 1 en la pestaña Rendering (no se necesita path tracing real para un pase de distancia).
3. Renderizar un frame de prueba primero (frame range a 1 solo frame) antes de lanzar la secuencia completa.

## Por qué pasaba
El checkbox de Depth usa internamente el canal especial de EXR que Nuke trata como alpha — normalizado 0-1 sin info métrica real. El RenderVar manual con Source Type "Intrinsic" fuerza a Karma a escribir un canal flotante independiente con los valores reales de distancia en unidades de mundo.

## Nota importante
Si el render ya está hecho y NO se activó el AOV de depth antes de renderizar, **no se puede recuperar después** — hay que volver a renderizar. El depth pass se genera durante el render, no en post. Única alternativa sin re-renderizar: estimación con IA (Depth Anything v2, MiDaS, Marigold) — pero es depth relativo, no métrico real, sirve para DOF/compositing pero no para reconstrucción 3D precisa.

## Checklist de AOVs recomendados para futuros renders
Activar desde el principio en vez de descubrir la falta a mitad de proyecto:

| AOV | Canal | Uso |
|---|---|---|
| Depth | `Pz` | DOF, niebla, compositing |
| Normals | `N` | Relighting, efectos |
| Cryptomatte | — | Mattes por objeto |
| Diffuse / Specular | — | Grading por pass |

Guardar siempre como multi-part EXR para que cada canal quede como capa nombrada.
