# Sesión: 2026-10-07
## Proyecto/Shot: Aprendizaje Unreal Engine 5.8 — Fase 1 (proyecto plantilla)

### Qué se hizo hoy
- Detectado UE **5.8.2** instalado en el laptop (+ Fab plugin y Quixel Bridge). Houdini 22.0.429 también.
- Creado `UE58_Cine_Template` a partir de la plantilla oficial Film/Video → Cinematic (`TP_ME_CineBP`).
- Config: MegaLights ON, Substrate ON, Heterogeneous Volumes ON, TSR. Plugins: Python, scripting, Cine Camera Rigs, Alembic, USD, MCP + toolsets.
- Script `vfxbrain_setup.py` (API verificada contra el ejemplo oficial de Epic `MovieGraphCreateConfigExample.py`) que creó: 3 presets MRG (Preview / Final EXR / PathTracer), nivel `LV_Lookdev` con luz y exposición físicas, secuencia `SEQ_Lookdev` 24 fps con CineCamera.
- Documentado todo en [[UE58_Cine_Template]].

### Decisiones tomadas
- Basar la plantilla en la de Epic en vez de partir de Blank: ya trae HW-RT, path tracer, auto-exposure OFF, alpha en post y presets de CVars.
- Substrate activado desde el principio (en 5.8 viene OFF; activarlo más tarde obliga a recompilar todo).
- EXR final **lineal sin tone curve ni OCIO** → la conversión a ACEScg se hace en Nuke. Más simple y robusto que montar OCIO en UE ahora.
- Exposición física: sol 100.000 lux ↔ cámara f/2.8, 1/4000, ISO 100 (EV100 ≈ 15).

### Problemas encontrados
- `-ExecutePythonScript` con ruta en barras invertidas: `\UE58` se convirtió en un carácter raro (escape `\U`). Solución: rutas con `/`.
- El editor con ventana se cerró a mitad (cierre limpio, probablemente manual) → se ejecutó todo en modo **headless** (`UnrealEditor-Cmd -run=pythonscript`), sin abrir ventana.
- API Python 5.8: `set_mobility` va en el componente (no en el actor); la niebla volumétrica es `enable_volumetric_fog`.
- MCP de UE escuchaba en `127.0.0.1:8000` pero la petición de prueba recibió "connection reset" (coincidió con el cierre del editor). **Sin verificar** que funcione.

### Continuación (misma sesión)
- MCP de Unreal **conectado a Claude Code** (`.mcp.json` del vault, servidor `unreal`). Verificado en vivo: sesión, list_toolsets, describe_toolset. Ver [[MCP_Unreal_ClaudeCode]].
- Encontrado proyecto previo `Unreal ProjectsLanding` (nave, cámara, paisaje). Se planteó montar una nave aterrizando → **abortado por decisión mía (Álvaro)**: de momento solo aprender y documentar. Técnica apuntada en [[Tecnica_Nave_Aterrizando_Thrusters_Polvo]].
- Aprendizajes de Python/MRG en [[UE58_Python_API_Aprendizajes]].

### Siguiente paso
- Checks manuales de [[UE58_Cine_Template]] (gizmo Maya, exposición, render de prueba con MRG_Cine_Final → Nuke).
- Decidir si conectar el MCP de UE a Claude Code.
- Fase 2: lighting study (golden hour / overcast / noche) con assets Megascans gratuitos.
