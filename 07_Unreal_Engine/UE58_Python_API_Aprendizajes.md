# Python en UE 5.8 — aprendizajes prácticos
Tags: #unreal #python #automatizacion #ue58 #mrg
Volver: [[00_MOC_Unreal]] · Relacionado: [[MCP_Unreal_ClaudeCode]], [[UE58_Cine_Template]]

Lo que aprendí escribiendo y depurando [[scripts/vfxbrain_setup.py]] (2026-10-07).

## Formas de ejecutar Python
| Forma | Cuándo |
|---|---|
| Editor → Tools → Execute Python Script | Puntual, viendo el resultado |
| Consola Python del Output Log (`import modulo; modulo.run()`) | `Content/Python/` está en el `sys.path` del proyecto |
| `UnrealEditor.exe proj.uproject -ExecutePythonScript="ruta"` | Abre el editor con ventana y ejecuta al arrancar |
| `UnrealEditor-Cmd.exe proj.uproject -run=pythonscript -script="ruta" -unattended` | **Headless**, sin ventana. Ideal para crear assets en lote. Tarda segundos si los shaders ya están compilados |

⚠️ **Rutas siempre con `/`**. Con `C:\...\UE58_Cine...` el `\U` se interpretó como escape y la ruta quedó corrupta (`Unreal Projects๘_Cine...`).
⚠️ Un script lanzado con `-ExecutePythonScript` también tiene `__name__ == "__main__"` cuando se ejecuta desde el menú → no cerrar el editor en `__main__` sin un flag explícito (yo uso `-VFXBrainQuit` leído de `unreal.SystemLibrary.get_command_line()`).

## Ejemplos oficiales que vienen con el engine (¡leerlos antes de inventar!)
`Engine/Plugins/MovieScene/MovieRenderPipeline/Content/Python/`
- `MovieGraphCreateConfigExample.py` — crear grafos de Movie Render Graph
- `MovieGraphEditorExample.py`, `MovieGraphQuickRenderExample.py`, `mrq_stills.py`…
Y el código fuente C++ (`Engine/Source`, `Engine/Plugins/**/Source`) es la referencia definitiva de nombres de propiedades y CVars.

## API: trucos y errores reales
- **`set_editor_property` acepta el nombre C++** (`bOverride_SpatialSampleCount`, `bEmulateMotionBlur`). Más fiable que adivinar el nombre "pythonizado" de los bitfields `bOverride_*`.
- **Structs se copian**: `s = obj.get_editor_property("settings")` → modificar → `obj.set_editor_property("settings", s)`. Si no se reasigna, no cambia nada (PostProcessSettings, filmback, focus_settings).
- `EditorLevelLibrary` está obsoleto → usar subsistemas: `unreal.get_editor_subsystem(unreal.EditorActorSubsystem)` (spawn, listar actores) y `LevelEditorSubsystem` (`new_level`, `load_level`, `save_current_level`).
- **Movilidad**: `actor.set_mobility()` NO existe en `DirectionalLight` → `light_component.set_mobility(unreal.ComponentMobility.MOVABLE)`.
- Niebla volumétrica: `ExponentialHeightFogComponent.enable_volumetric_fog` (no `volumetric_fog`).
- Crear assets: `unreal.AssetToolsHelpers.get_asset_tools().create_asset(nombre, carpeta, clase, factory)`; para secuencias `unreal.LevelSequenceFactoryNew()`.

## Movie Render Graph por Python (5.8)
- `graph.create_node_by_class(unreal.MovieGraphXxxNode)` y `graph.add_labeled_edge(a, "", b, "")` (pines sin nombre = `""`).
- Rama **Globals**: `input_node "Globals"` → nodos de settings → `output_node "Globals"`.
- Render layer: `graph.add_output()/add_input()` + `set_member_name("beauty")`, render pass → `MovieGraphRenderLayerNode` → output.
- Nodos clave y propiedades (nombre C++):
  - `MovieGraphGlobalOutputSettingNode`: `OutputResolution` (`MovieGraphLibrary.named_resolution_from_size(w,h)`), `OutputFrameRate`, `OutputDirectory`
  - `MovieGraphSamplingMethodNode`: `TemporalSampleCount`
  - `MovieGraphDeferredRenderPassNode`: `SpatialSampleCount`, `AntiAliasingMethod`, `bDisableToneCurve`, `bAllowOCIO`, high-res tiling
  - `MovieGraphPathTracerRenderPassNode` (¡el ejemplo oficial lo llama `PathTraced`, desactualizado!)
  - `MovieGraphWarmUpSettingNode`: `NumWarmUpFrames`, `bEmulateMotionBlur`
  - `MovieGraphCameraSettingNode`: `ShutterTiming` (FrameOpen / FrameCenter / FrameClose)
  - Outputs: `MovieGraphImageSequenceOutputNode_EXR / _MultiLayerEXR / _PNG / _JPG`, `FileNameFormat` con tokens `{sequence_name} {layer_name} {frame_number}`
- Cada propiedad necesita su `bOverride_X = True` o se ignora.

## CVars de proyecto verificadas en el código de 5.8
| CVar | Default 5.8 | Nota |
|---|---|---|
| `r.MegaLights.EnableForProject` | 0 | activar para MegaLights |
| `r.Substrate` | 0 | read-only en runtime → solo en `DefaultEngine.ini` + reinicio |
| `r.Nanite.Tessellation` | 1 | teselación Nanite ya activa |
| `r.HeterogeneousVolumes` | 1 | VDB/Sparse Volume Textures |
| `r.Lumen.HeightFog` | 1 | la niebla recibe GI de Lumen |
| `r.AntiAliasingMethod` | 4 | TSR |

## Aprendido el 2026-10-07 (estudio de iluminación, Fase 2)
### Migrar assets entre proyectos sin abrir el editor
- `unreal.AssetToolsHelpers.get_asset_tools().migrate_packages(paquetes, "C:/.../OtroProyecto/Content", opts)` con `opts = unreal.MigrationOptions()`, `prompt=False`, `ignore_dependencies=False`.
- Se ejecuta **en el proyecto origen** (headless con `-run=pythonscript`). Copia también todas las dependencias (master materials, texturas, physmats) y mantiene las rutas `/Game/...`, así que las referencias no se rompen. **No copiar `.uasset` a mano**: las MI de Megascans dependen de masters en `/Game/Custom/...` y `/Game/MSPresets`.
- Megascans locales: `ElectricDreamsEnv/Content/Megascans` (3D_Assets, 3D_Plants, Decals, Surfaces), todo en Nanite. Migrar 20 mallas con sus dependencias ocupó unos 2 GB.
- `StaticMesh.get_bounding_box()` da el tamaño en cm, útil para componer a ciegas.

### Logs en modo headless
- `unreal.log()` **no sale por stdout** en el commandlet. Para verlo, leer `<Proyecto>/Saved/Logs/<Proyecto>.log` y filtrar por un prefijo (`[VFXBrain]`).

### Render de Movie Render Graph por línea de comandos
- `-MoviePipelineConfig=` acepta **una Queue o una PrimaryConfig antigua, no un MovieGraphConfig** (verificado en `MovieRenderPipelineCommandLine.cpp`). Si el job lleva un graph preset, el executor cambia solo a `UMovieGraphPipeline`.
- Truco: crear la cola en Python (`unreal.new_object(unreal.MoviePipelineQueue)` → `allocate_new_job` → `job.map`, `job.sequence`, `job.set_graph_preset(graph)`), guardarla con `unreal.MoviePipelineEditorLibrary.save_queue_to_manifest_file(queue)` (escribe un `.utxt`) y lanzar:
  `UnrealEditor.exe <uproject> -game -MoviePipelineConfig="<ruta>.utxt" -windowed -resx=1280 -resy=720 -log -notexturestreaming`
- La primera vez compila shaders y crece la caché global `%LOCALAPPDATA%/UnrealEngine/Common/DerivedDataCache` (se puede borrar sin problema, solo se regenera).

### Nombres de propiedades verificados en 5.8
- Niebla: `fog_inscattering_luminance` (la antigua `FogInscatteringColor` está deprecated), `volumetric_fog_scattering_distribution`, `volumetric_fog_albedo` (**FColor**), `volumetric_fog_extinction_scale`.
- Luces: `use_temperature` + `temperature`, `diffuse_scale`, `specular_scale`. `light_color` es **FColor**: `unreal.Color(r=, g=, b=, a=255)` (`LinearColor` no tiene `to_fcolor` en Python).
- Point light en lúmenes: `intensity_units=unreal.LightUnits.LUMENS`.
- Material de cielo: `bIsSky` → `is_sky=True`. Con eso, una cúpula emisiva la captura la Sky Light en real-time capture (sirve para un overcast sin HDRI).
- Materiales por script: `MaterialEditingLibrary.create_material_expression` / `connect_material_property` / `recompile_material`. Las fábricas son `MaterialFactoryNew` y `MaterialInstanceConstantFactoryNew`.
