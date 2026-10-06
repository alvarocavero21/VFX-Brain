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
