# FLUX.1-dev img2img + ControlNet Depth/Canny + inpaint por recorte
Tags: #comfyui #flux #controlnet #img2img #inpaint #workflow #concept-to-photo

Técnica para convertir un **concept de composición** en una imagen fotorrealista sin perder el encuadre, y rehacer después una zona concreta (personas, ventana…) a más resolución. Usada en [[05_Projects/Boundaries_Escena4/notes|Boundaries · Escena 4]].

**Archivos** en `03_ComfyUI/Workflows/Boundaries_FLUX_img2img/`:
- `plano1_api.json` y `plano2_api.json`: workflows en **formato API** (se cargan arrastrándolos a ComfyUI o se envían a `POST /prompt`). Esperan en `input/` la imagen base `boundaries_<concept>.jpg` y la máscara `boundaries_planoN_mask.png`.
- `boundaries_run.py`: construye el JSON, sube imagen y máscara (`/upload/image`), lanza, espera en `/history` y descarga en `output/planoN`. Espera la estructura `proyecto/{concepts, masks/, workflows/, output/}` (la original está en `Downloads/Boundaries_concepts`).
  ```
  python boundaries_run.py --plano 1 --round 1 --seeds 101 202 303 404
  python boundaries_run.py --plano 2 --round 3 --seeds 101 --denoise 0.4 --inpaint-denoise 0.75 --cn 0.5 \
      --mask masks/plano2_ventana_halo_mask.png --crop 1152 418 768 576 --crop-res 1024 768 --halo
  ```
  Opciones: `--denoise --inpaint-denoise --cn --cn-end --mask --crop X Y W H --crop-res W H --halo --no-figures --save-only --url`.
- Máscaras `.png` de los dos planos.

## Modelos (ver [[ComfyUI_Pinokio_Setup_y_Modelos]])
- `checkpoints/flux1-dev-fp8.safetensors` (todo en uno: MODEL + CLIP + VAE)
- `controlnet/FLUX.1-dev-ControlNet-Union-Pro-2.0.safetensors`: la versión Pro 2.0 **no necesita** `SetUnionControlNetType`.
- `upscale_models/4x-UltraSharp.pth`
- Nodos `comfyui_controlnet_aux`: `DepthAnythingV2Preprocessor` (vitb). Canny es nodo nativo.

## Estructura del grafo (41 nodos)
**1. Pasada general (1536x640, 2.39:1)**
- `LoadImage` → `ImageScale` (lanczos, 1536x640, crop disabled; estira para que la máscara cuadre 1:1)
- `CLIPTextEncode` (positivo) → `FluxGuidance 3.5` · `CLIPTextEncode` (negativo)
- `DepthAnythingV2Preprocessor` (vitb, res 1024) y `Canny` (0.2 / 0.5) sobre la imagen escalada
- 2 × `ControlNetApplyAdvanced` encadenados (depth y luego canny): strength 0.6, start 0, **end 0.5**, con la entrada `vae` conectada (necesaria en FLUX)
- `VAEEncode` → `KSampler` (dpmpp_2m, **simple**, 30 pasos, **cfg 1.0**, denoise 0.6) → `VAEDecode`

**2. Upscale x2**: `UpscaleModelLoader` + `ImageUpscaleWithModel` (4x) → `ImageScale` a 3072x1280 → `SaveImage` (`_A_preinpaint`)

**3. Inpaint por recorte**
- `LoadImageMask` (canal red) → `MaskToImage` → `ImageScale` 3072x1280 → `ImageToMask`
- `ImageCrop` + `CropMask` con la misma caja → `ImageScale` de imagen y máscara a la resolución de trabajo (~1 MP)
- Prompt de zona → `FluxGuidance` → los mismos 2 ControlNets sobre el recorte
- `InpaintModelConditioning` (noise_mask true) + `DifferentialDiffusion` en el modelo → `KSampler` (denoise 0.75–0.85, seed+1)
- `VAEDecode` → `ImageScale` de vuelta al tamaño del recorte → `ImageCompositeMasked` sobre la imagen 3072x1280 con la máscara recortada → `SaveImage` (`_B_final`)

## Claves aprendidas
- **Scheduler `simple`/`beta` con FLUX, nunca karras** si el denoise importa → [[FLUX_scheduler_karras_anula_denoise]].
- **CFG en FLUX-dev = `FluxGuidance`**; el CFG del KSampler va a 1.0. Con 1.0 **el negativo se ignora**. Si se necesita, subir el CFG del KSampler a 1.5–2 (el doble de tiempo, y FLUX-dev no está entrenado para ello).
- **Inpaint por recorte** cuando la zona es pequeña en el frame: inpaintear a la resolución completa deja las figuras como manchas. Hay que ampliar el recorte para que la zona ocupe ~200–400 px.
- **Prompt de zona** en el inpaint: con el prompt general, FLUX intenta meter elementos de la escena (la nave) dentro del recorte.
- **Máscara por luminancia** para siluetas oscuras: umbral entre siluetas y fondo, mediana + apertura (Min/Max filter 9) y dilatación generosa (25 px a 2400 px de ancho) para cubrir el rim, más blur de 6 px.
- **El ControlNet en el inpaint fija la forma del concept.** Es bueno para mantener poses, pero si el concept tiene un elemento gráfico (marco negro grueso, halo aerografiado), el Canny lo conserva. En ese caso hay que bajar o quitar el ControlNet solo del inpaint y ampliar la máscara para que cubra el halo.
- FLUX mete **texto basura** cuando ve formas tipo cartel ("GUMITB"); el negativo no ayuda con CFG 1. Hay que filtrar por seed.
- Tiempos en la 4090 laptop (16 GB): ~95–130 s por variante (pasada general + upscale + inpaint). La primera ejecución tarda +60 s por la carga de modelos.
