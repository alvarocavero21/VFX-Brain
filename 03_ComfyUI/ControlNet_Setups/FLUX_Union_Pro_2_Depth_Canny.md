# ControlNet para FLUX: Union Pro 2.0 con Depth + Canny
Tags: #comfyui #controlnet #flux #depth #canny

- **Modelo**: `FLUX.1-dev-ControlNet-Union-Pro-2.0` (Shakker-Labs). Un solo archivo sirve para depth, canny, pose, gray y soft edge. En la Pro 2.0 **no hace falta `SetUnionControlNetType`**: el modo se deduce de la imagen de control.
- **Preprocesadores**: `DepthAnythingV2Preprocessor` (de `comfyui_controlnet_aux`; vitb es un buen equilibrio, vitl pesa 1,3 GB) y `Canny` nativo (umbrales 0.2 / 0.5 para concepts con zonas planas oscuras; los 0.4 / 0.8 por defecto pierden bordes en interiores oscuros).
- **Aplicación**: dos `ControlNetApplyAdvanced` encadenados, cargando el modelo una sola vez y **conectando la entrada `vae`** (FLUX la necesita).
- **Valores probados (concept → foto)**: strength 0.5–0.6 y end_percent 0.5. Mantienen el encuadre y dejan que la segunda mitad de los pasos invente detalle fotográfico. Shakker recomienda strength ~0.7 y end ~0.8 para fidelidad máxima.
- **Ojo en inpaint**: el Canny conserva los elementos gráficos del concept (marcos negros, halos pintados). Si la zona es "gráfica", bajar o quitar el CN solo en el inpaint.
- Workflow completo: [[FLUX_img2img_ControlNet_Inpaint_por_Recorte]].
