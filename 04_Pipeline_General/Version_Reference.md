# Referencia de versiones de software instaladas

## Houdini 22 (ambas máquinas)
- UI rediseñada (más limpia, nuevas opciones de personalización)
- Gaussian Splatting nativo: los splats son ciudadanos de primera clase, editables procedimentalmente en cualquier nodo (no solo visualización/render), se pueden crear, cargar y modificar como point clouds con atributos
- Solaris: mejoras grandes en layout, worldbuilding y set dressing, scattering procedural más rápido
- APEX Rig Pose Node: nuevo sistema central de rigging, gestiona posing/rest pose/animación, con Set Driven Key automatizado
- Neural Layer to Height: ML aplicado a generación de terrenos desde foto única (descarga modelo MOG 2 en background)
- Ramp catalog visual (sustituye presets de texto)
- Arquitectura de viewport en Vulkan (mejoras de rendimiento/estabilidad respecto a versiones anteriores)
- Evaluate Rig in Parallel: distribución de rigs en threads separados para playback fluido de personajes múltiples

## NukeX 17.0 v3
- Soporte nativo de 3D Gaussian Splats: importar (.ply/.splat), manipular, renderizar (nodo SplatRender con motion blur y depth output), aislar elementos con Field nodes
- Sistema 3D modernizado basado en USD: workflows no destructivos para proyecciones, iluminación real, materiales/shaders importables de otro software
- Path-based masking: cada elemento upstream sigue accesible en cualquier punto de la cadena, incluso al final del setup
- Sistema de anotaciones renovado (pinceles rediseñados, panel de comentarios dedicado)
- NukeX incluye BigCat (extensión de CopyCat para entrenar modelos de ML propios con datasets grandes)
- Compatible con VFX Reference Platform 2025, USD 25.08

## Unreal Engine 5.8 (junio 2026 — última versión mayor de UE5)
- Movie Render Graph **Production Ready** (Light Modifier por render layer, Accumulation DOF)
- MegaLights **Production Ready** (area lights con sombras suaves, IES en volumétricos, cloud shadows)
- Lumen Lite (Beta) — GI media ~2× más rápida, para viewport/juego
- Mesh Terrain, Procedural Vegetation Editor, FSSS (niebla), MetaHuman Crowd → Experimental
- PCG: edición manual no destructiva, atributos complejos, subgrafos embebidos
- X-Rite AxF → Substrate production ready
- MCP Server (Experimental) para conectar LLMs al editor
- Detalle completo: `07_Unreal_Engine/UE58_Novedades_Clave.md`
- ⚠️ Pendiente confirmar: ¿instalado en laptop, desktop o ambas?

## ComfyUI 0.37.0 (laptop, instalado con Pinokio) — verificado 2026-10-10
- PyTorch 2.7.0+cu128, Python 3.10.20, frontend 1.53.6. Custom nodes: ComfyUI-Manager, comfyui_controlnet_aux
- Modelos: FLUX.1-dev fp8 y FLUX.1-schnell fp8 (checkpoints todo en uno), ControlNet Union Pro 2.0 (FLUX), 4x-UltraSharp. **Sin SDXL ni FLUX Fill**
- Con FLUX: scheduler `simple`/`beta` (no karras) y CFG vía `FluxGuidance` con el CFG del KSampler a 1
- Detalle: `03_ComfyUI/GPU_Pipeline_Notes/ComfyUI_Pinokio_Setup_y_Modelos.md`
- ⚠️ Desktop: sin verificar qué hay instalado

## Regla de uso
Antes de sugerir un nodo, parámetro o workflow específico de versión, verificar contra este documento. Si hay duda sobre si una feature existe en la versión instalada, preguntar al usuario antes de asumir, en vez de dar por hecho comportamiento de versiones anteriores o posteriores.
