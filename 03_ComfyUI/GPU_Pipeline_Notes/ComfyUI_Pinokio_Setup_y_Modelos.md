# ComfyUI en Pinokio (laptop): arranque, modelos instalados y rutas
Tags: #comfyui #pinokio #setup #modelos #laptop
Actualizado: 2026-10-10

## Instalación
- ComfyUI instalado con **Pinokio** en `C:\pinokio\api\comfy.git` (app en `app\`, venv en `app\env\`).
- Versión: **ComfyUI 0.37.0**, Python 3.10.20, PyTorch 2.7.0+cu128 y frontend 1.53.6. Avisos al arrancar: pide PyTorch cu130 para ops optimizadas y avisa de que Python 3.10 llega a EOL el 31/10/2026. **No actualizado** (decisión pendiente).
- GPU: RTX 4090 Laptop, 16 GB VRAM. API en `http://127.0.0.1:8188`.
- Las carpetas de modelos (`checkpoints`, `controlnet`, `upscale_models`, `loras`, `vae`…) son **symlinks** a `C:\pinokio\drive\drives\peers\d1790676688024\…`, compartidas entre apps de Pinokio.
- Custom nodes: `ComfyUI-Manager`, `comfyui_controlnet_aux` (añadido el 2026-10-10).

## Arrancar ComfyUI desde terminal (o desde Claude Code)
1. **Pinokio tiene que estar abierto** (`%LOCALAPPDATA%\Programs\Pinokio\Pinokio.exe`). Si no, el panel de control `127.0.0.1:42000` no responde.
2. `pterm` está en `C:\pinokio\bin\npm\pterm.cmd`:
   ```
   pterm run "C:\pinokio\api\comfy.git" --default start.js
   pterm status comfy.git      # esperar state=online, ready=true
   pterm stop comfy.git        # parar (necesario tras instalar custom nodes)
   pterm logs comfy.git --tail 200
   ```
3. **Problema visto**: `pterm` daba `ETIMEDOUT 172.20.10.2:42000` porque `~/.pinokio/config.json` → `access.host` guardaba la IP de un hotspot antiguo. Al abrir Pinokio se reescribe con la IP actual y se arregla.
4. Python: el `python` del sistema es el alias de la Microsoft Store (no existe). Usa el del venv: `C:\pinokio\api\comfy.git\app\env\Scripts\python.exe`.
5. Para instalar dependencias de custom nodes sin romper torch: `pip install -r req.txt -c constraints.txt`, con torch, torchvision, torchaudio, numpy y pillow fijados a su versión actual (`pip freeze`), y quitando `torch`/`torchvision` del requirements.

## Modelos instalados
| Carpeta | Archivo | Tamaño | Origen |
|---|---|---|---|
| checkpoints | `flux1-schnell-fp8.safetensors` | 17 GB | (previo) |
| checkpoints | `flux1-dev-fp8.safetensors` | 17,2 GB | HF `Comfy-Org/flux1-dev` (2026-10-10) |
| controlnet | `FLUX.1-dev-ControlNet-Union-Pro-2.0.safetensors` | 4,3 GB | HF `Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro-2.0` (renombrado de `diffusion_pytorch_model.safetensors`) |
| upscale_models | `4x-UltraSharp.pth` | 67 MB | HF `lokCX/4x-Ultrasharp` |
| controlnet_aux/ckpts | `depth_anything_v2_vitb.pth` | ~390 MB | autodescarga en el primer uso |

- No hay SDXL, ni LoRAs, ni VAE suelto, ni modelos de inpaint (FLUX Fill).
- Licencia de FLUX.1-dev: **no comercial**. Para trabajo pagado: schnell (Apache 2.0) o licencia comercial de BFL.
- Notas relacionadas: [[FLUX_img2img_ControlNet_Inpaint_por_Recorte]] · [[Pipeline_ComfyUI_ClaudeCode_MCP]] (setup antiguo con MCP y RealVisXL; ahora no hay MCP de ComfyUI configurado).
