# Proyecto plantilla: UE58_Cine_Template
Tags: #unreal #plantilla #setup #mrg #fase1
Volver: [[00_MOC_Unreal]]

Ruta: `C:\Users\alvar\Documents\Unreal Projects\UE58_Cine_Template\UE58_Cine_Template.uproject`
Máquina: laptop (RTX 4090 Laptop 16 GB, UE **5.8.2**). Pendiente replicar en desktop.

## Cómo usarla
Para cada shot/proyecto nuevo: **copiar la carpeta entera** (sin `Saved/`, `Intermediate/`, `DerivedDataCache/`) y renombrar el `.uproject`. No trabajar dentro de la plantilla.

## Base
Copia de la plantilla oficial de Epic **Film/Video → Cinematic** (`TP_ME_CineBP`), que ya trae:
- Lumen GI + reflexiones con **Hardware Ray Tracing**, Virtual Shadow Maps, Path Tracer habilitado
- Auto-exposure, motion blur y bloom **desactivados por defecto** (`r.DefaultFeature.*=False`)
- Alpha en post-proceso (`r.PostProcessing.PropagateAlpha`) → holdouts para compo
- Plugins: Movie Render Pipeline, OpenColorIO, Accumulation DOF, Niagara MRQ, Mask Render Pass (cryptomatte), Cinematic Assembly Tools (producciones a 24 fps), Console Variables Editor, MetaHuman, Virtual Camera
- Presets de CVars en `/Game/CinematicTemplate/CVARPresets/` (Lumen, Raytracing, VolumeFog, VSM, PostProcess…)

## Lo que añadí (Fase 1)
### Config (`Config/DefaultEngine.ini`)
| Setting | Valor | Por qué |
|---|---|---|
| `r.MegaLights.EnableForProject` | 1 | Production Ready en 5.8, muchas luces con sombra |
| `r.Substrate` | 1 | Materiales por capas + AxF. Activarlo de inicio evita recompilar todo luego (en 5.8 viene a 0 por defecto) |
| `r.HeterogeneousVolumes` | 1 | VDB de Houdini en UE (ya es default, explícito) |
| `r.AntiAliasingMethod` | 4 (TSR) | Viewport; en render final manda la acumulación de MRG |

### Plugins extra (`.uproject`)
Python Editor Script, Editor Scripting Utilities, Sequencer Scripting, Cine Camera Rigs (rail/crane), Camera Shake Previewer, Alembic Importer, USD Importer, **Model Context Protocol** + toolsets (Editor, ConfigSettings, Niagara, PCG).

### Servidor MCP (Experimental)
`Config/DefaultEditorPerProjectUserSettings.ini` → `bAutoStartServer=True`, puerto 8000.
Al abrir el editor queda escuchando en `http://localhost:8000/mcp`. Con `bEnableToolSearch` (default) expone `list_toolsets`, `describe_toolset` y `call_tool`. **Aún no conectado a Claude Code** (pendiente de decidir).

### Assets creados por script (`Content/Python/vfxbrain_setup.py`, copia en [[scripts/vfxbrain_setup.py]])
Se puede relanzar sin miedo: no sobrescribe assets que ya existan. Headless:
`UnrealEditor-Cmd.exe <uproject> -run=pythonscript -script="C:/.../vfxbrain_setup.py" -unattended` (**rutas con barras normales `/`**: con `` el `U` de `UE58...` se interpreta como escape y falla).
| Asset | Qué es |
|---|---|
| `/Game/VFXBrain/Render/MRG_Cine_Preview` | 1280×720, 24 fps, TSR, 1 sample, warm-up 8, PNG. Dailies rápidos |
| `/Game/VFXBrain/Render/MRG_Cine_Final` | 1920×1080, 24 fps, AA **None** + 16 temporal samples, warm-up 32 (emulando motion blur), shutter FrameCenter, **EXR multicapa lineal** (tone curve OFF, sin OCIO) |
| `/Game/VFXBrain/Render/MRG_Cine_PathTracer` | 1920×1080, path tracer 64 spp, EXR lineal. Ground truth |
| `/Game/VFXBrain/Maps/LV_Lookdev` | Sol 100.000 lux (source angle 0.5°), Sky Atmosphere, Sky Light real-time, Volumetric Clouds, Height Fog volumétrica, PPV unbound con **exposición manual física**, suelo, bola chrome, bola gris, maniquí 180 cm |
| `/Game/VFXBrain/Cinematic/SEQ_Lookdev` | Level Sequence 24 fps, 120 frames, Camera Cut → `CineCam_Main` |

Salida de render: `{project_dir}/Saved/MovieRenders/{sequence_name}/{layer_name}/{sequence_name}.{layer_name}.{frame_number}`

### CineCam_Main
Sensor 16:9 Digital Film (23.76 × 13.365 mm), 35 mm, f/2.8, foco manual 600 cm, ISO 100, 1/4000 s → **EV100 ≈ 15** (regla sunny 16), coherente con el sol de 100.000 lux. Si cambio la luz, ajusto la exposición **como una cámara real**: ISO/obturador/diafragma, no el sol.

## EXR → Nuke
- MRG_Cine_Final escribe **lineal scene-referred en Rec.709/sRGB primaries** (tone curve desactivada).
- En Nuke (ACES): Read con colorspace `Linear Rec.709 (sRGB)` (nombre exacto según config OCIO) → working space ACEScg. Así conviven con los EXR de Karma.
- Alternativa futura: crear un asset OCIO config en UE con el mismo config que Nuke y renderizar ya en ACEScg (`bAllowOCIO`).

## Pasos manuales pendientes (1 vez)
- [ ] Editor Preferences → Gizmos → Interaction preset **Maya-Style Interaction**.
- [ ] Abrir `SEQ_Lookdev` y confirmar que el Camera Cut apunta a `CineCam_Main` (el script lo enlaza, no pude verificarlo visualmente).
- [ ] Comprobar en `LV_Lookdev` la exposición (bola gris ≈ gris medio) y ajustar si hace falta.
- [ ] Movie Render Queue → añadir `SEQ_Lookdev` → elegir `MRG_Cine_Final` → render de prueba → abrir en Nuke.
- [ ] Instalar EasyToolbag cuando lo compre (Fab → Install to Engine 5.8) y añadir al proyecto.
- [ ] Decidir si conectar el MCP de UE a Claude Code.
