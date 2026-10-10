# Sesión: 2026-10-10
## Proyecto/Shot: [[05_Projects/Boundaries_Escena4/notes|Boundaries · Escena 4 · Concepts fotorrealistas]]
Tags: #boundaries #comfyui #flux #sesion

> Excepción puntual: en esta tarea Claude lanzó las generaciones por la API de ComfyUI a petición de Álvaro. Lo normal sigue siendo que Álvaro ejecute y Claude guíe.

### Qué se hizo hoy
1. **Arranque del entorno**: ComfyUI (instalado con Pinokio en `C:\pinokio\api\comfy.git`) no respondía en 8188 ni en 8000. Pinokio estaba cerrado: se abrió y ComfyUI se lanzó con `pterm run … --default start.js`. Detalle: [[ComfyUI_Pinokio_Setup_y_Modelos]].
2. **Inventario** (`GET /object_info`): solo había `flux1-schnell-fp8`, sin ControlNet, sin upscaler y sin preprocesadores de depth.
3. **Descargas aprobadas por Álvaro** (~22 GB): FLUX.1-dev fp8, ControlNet Union Pro 2.0, 4x-UltraSharp y los nodos `comfyui_controlnet_aux` (dependencias instaladas con torch y numpy fijados en sus versiones). Depth Anything V2 **vitb** (~390 MB) se baja solo la primera vez.
4. **Máscaras**: plano 1 por umbral de luminancia (siluetas L≈9.5 frente a suelo L≈15 → umbral 12, limpieza, dilatación de 25 px y blur), que pilla la coleta y el rim. Plano 2: primero el rectángulo de la ventana; en la ronda 3, una elipse con ventana + halo.
5. **Workflow API + script** `boundaries_run.py` (construye el JSON, sube imagen y máscara, lanza, espera y descarga). Técnica: [[FLUX_img2img_ControlNet_Inpaint_por_Recorte]].
6. **Prueba de humo**: con `karras` la imagen salía casi idéntica al concept → cambio a `simple` ([[FLUX_scheduler_karras_anula_denoise]]).
7. **Generación y filtrado** (4 seeds por ronda, ~95–130 s por variante en la 4090 laptop):
   - Plano 1, ronda 1 (0.6 / 0.82 / CN 0.6): pasan s202 y s303. Se descartan s101 (el hombre también con coleta) y s404 (moño raro en el hombre). No hizo falta otra ronda.
   - Plano 2, ronda 1 (0.4 / 0.6 / CN 0.6): s101, s202 y s404 pasan los criterios, pero la ventana es una pegatina con halo aerografiado. s303 se descarta por texto basura y gente de más.
   - Plano 2, ronda 2 (0.45 / 0.75 / CN 0.5): sin mejora clara. s101 sale con 3 figuras, s202 con criaturas raras, s303 con skyline y texto, y s404 con una ventana real pero vertical y un disco de roca con borde duro.
   - Plano 2, ronda 3 (0.4 / 0.75 / CN 0.5 + máscara de halo y prompt de luz sobre roca): la mejor es s101. s303 se descarta otra vez por texto y soldados.
8. Elegidas: **plano 1 `r1_s303`** y **plano 2 `r3_s101`**. Parámetros finales en [[05_Projects/Boundaries_Escena4/notes|notes]].

### Decisiones tomadas
- FLUX-dev frente a SDXL, por fotorrealismo (la 4090 laptop con 16 GB lo mueve en fp8).
- Scheduler `simple` en lugar del `karras` del brief.
- FluxGuidance 3.5 con CFG 1 → el negativo queda sin efecto (decisión consciente para no duplicar el tiempo).
- Inpaint por recorte con prompt específico de zona.
- Ronda 3 del plano 2 con una máscara ampliada al halo (la original se conserva).
- Las figuras salieron en las 3 rondas → no se activó el plan B de asteroide sin personas.

### Problemas encontrados
- `karras` + FLUX anula el denoise → [[FLUX_scheduler_karras_anula_denoise]].
- Pinokio cerrado y `pterm` con la IP vieja de un hotspot (`172.20.10.2`) → se arregla al abrir Pinokio, que reescribe `~/.pinokio/config.json`.
- `python` del sistema no existe (alias de la Microsoft Store) → usar `C:\pinokio\api\comfy.git\app\env\Scripts\python.exe` o `pterm which python`.
- El Canny del ControlNet en el inpaint mantiene el marco negro plano de la ventana del plano 2 (pendiente).

### Siguiente paso
- Plano 2: inpaint de la ventana sin ControlNet, o retoque a mano o en Nuke.
- Ver la lista completa en [[05_Projects/Boundaries_Escena4/notes#Siguiente paso|notes]].
