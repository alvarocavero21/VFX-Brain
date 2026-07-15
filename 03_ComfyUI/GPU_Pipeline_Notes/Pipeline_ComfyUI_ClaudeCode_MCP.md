# Pipeline: Claude Code → MCP → ComfyUI para post-proceso de renders Karma
Tags: #comfyui #mcp #claude-code #img2img #controlnet #pipeline

## Contexto
Setup completo para post-procesar renders EXR de Karma (proyecto de referencia: Fire_Scene, un coche ardiendo + edificio abandonado) usando ComfyUI img2img con ControlNet (depth + normal) para conseguir texturizado e iluminación hiperrealista SIN alterar la geometría original.

## Setup de la integración MCP
Comando que funciona en Windows:
```
claude mcp add comfyui npx comfyui-mcp
```

**Importante**: esto escribe la configuración en `.claude.json` (no en `settings.json`). El enfoque de poner la config en `settings.json` no funcionó — Claude Code no lo detectaba. `.claude.json` es la ubicación correcta para este setup en Windows.

Puede aparecer un warning sobre necesitar un wrapper `cmd /c` en Windows — es normal, el MCP funciona igual. Confirmar conexión con `/mcp` dentro de Claude Code: debería mostrar `comfyui · ✓ connected`.

## Extracción de passes EXR multicanal de Karma XPU
Para extraer canales individuales (depth, normal, etc.) de un EXR multicapa renderizado con Karma XPU, usar:
- `hoiiotool.exe` (OpenImageIO tool que viene con Houdini)
- `hython` (para scripting si se necesita automatizar la extracción en batch)

## Problemas resueltos durante el setup

### Render oscuro/apagado tras el img2img
**Solución**: subir denoise a 0.65+ y CFG a 9. Con valores más bajos el resultado se quedaba demasiado apagado/oscuro respecto al render base.

### Procesado 4K con dual ControlNet demasiado lento
En el laptop (RTX 4090) el procesado a 4K con dos ControlNets (depth + normal) simultáneos era inviable en tiempos razonables.
**Solución**: renderizar/procesar a 1280x720 y luego hacer upscale con **UltimateSDUpscale** por tiles. Mucho más rápido y el resultado final en resolución alta mantiene la calidad.

## Estructura de carpetas de salida
```
C:\Users\<usuario>\ComfyUI\output\Renders_ComfyUI\
  └── [nombre_de_escena]\
```
Subcarpetas nombradas por escena para no mezclar proyectos.

## Modelo usado como base
RealVisXL V4.0 — buen punto de partida para fotorealismo en img2img sobre renders 3D.

## Aplicación al portfolio
Este pipeline es para POST-PROCESO estilístico, no para generar los shots del portfolio en sí — recordar que en el reel de portfolio se debe evitar meter IA generativa salvo que sea el punto explícito del shot, ya que lo que se evalúa es la capacidad de simulación real, no de generación con difusión.
