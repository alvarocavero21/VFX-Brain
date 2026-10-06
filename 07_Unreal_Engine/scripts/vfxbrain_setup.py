# VFX-Brain - Fase 1: setup del proyecto plantilla cinematico (UE 5.8)
#
# Crea (sin borrar nada existente):
#   /Game/VFXBrain/Render/MRG_Cine_Preview      -> 720p, TSR, PNG, rapido para dailies
#   /Game/VFXBrain/Render/MRG_Cine_Final        -> 1080p, 24fps, AA por acumulacion, EXR multicapa lineal para Nuke
#   /Game/VFXBrain/Render/MRG_Cine_PathTracer   -> 1080p, path tracer, EXR lineal (ground truth)
#   /Game/VFXBrain/Maps/LV_Lookdev               -> sol fisico + cielo + nubes + niebla + PPV exposicion manual
#                                                 + CineCamera + bolas chrome/gris + maniqui 180 cm
#   /Game/VFXBrain/Cinematic/SEQ_Lookdev         -> Level Sequence 24 fps con Camera Cut
#
# Uso dentro del editor: Tools > Execute Python Script... > este archivo
#   o en la consola Python:  import vfxbrain_setup; vfxbrain_setup.run()
# Desde linea de comandos: -ExecutePythonScript=<ruta> -VFXBrainQuit (cierra el editor al terminar).

import unreal

ROOT = "/Game/VFXBrain"
RENDER_DIR = ROOT + "/Render"
MAP_PATH = ROOT + "/Maps/LV_Lookdev"
SEQ_DIR = ROOT + "/Cinematic"
SEQ_NAME = "SEQ_Lookdev"

FPS = 24
SEQ_FRAMES = 120  # 5 s
OUTPUT_DIR = "{project_dir}/Saved/MovieRenders/"
FILE_FORMAT = "{sequence_name}/{layer_name}/{sequence_name}.{layer_name}.{frame_number}"

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary


def log(msg):
    unreal.log("[VFXBrain] " + msg)


def warn(msg):
    unreal.log_warning("[VFXBrain] " + msg)


def set_props(obj, **props):
    """set_editor_property acepta los nombres C++ (bOverride_X), mas fiable que el nombre python de los bitfields."""
    for k, v in props.items():
        try:
            obj.set_editor_property(k, v)
        except Exception as e:
            warn("No se pudo poner %s.%s: %s" % (obj.get_class().get_name(), k, e))


# ---------------------------------------------------------------- Movie Render Graph

def new_graph(name):
    path = RENDER_DIR + "/" + name
    if eal.does_asset_exist(path):
        warn(path + " ya existe, no lo toco")
        return None
    # factory None = grafo vacio (no copia la plantilla de Project Settings)
    return asset_tools.create_asset(name, RENDER_DIR, unreal.MovieGraphConfig, None)


def chain(graph, nodes):
    for a, b in zip(nodes, nodes[1:]):
        graph.add_labeled_edge(a, "", b, "")


def globals_branch(graph, width, height, extra_nodes):
    out = graph.create_node_by_class(unreal.MovieGraphGlobalOutputSettingNode)
    set_props(out,
              bOverride_OutputResolution=True,
              OutputResolution=unreal.MovieGraphLibrary.named_resolution_from_size(width, height),
              bOverride_OutputFrameRate=True,
              OutputFrameRate=unreal.FrameRate(FPS, 1),
              bOverride_OutputDirectory=True,
              OutputDirectory=unreal.DirectoryPath(OUTPUT_DIR))
    nodes = [out] + extra_nodes
    chain(graph, nodes)
    graph.add_labeled_edge(graph.get_input_node(), "Globals", nodes[0], "")
    graph.add_labeled_edge(nodes[-1], "", graph.get_output_node(), "Globals")


def layer_branch(graph, branch, renderer_node, layer_name):
    graph.add_output().set_member_name(branch)
    graph.add_input().set_member_name(branch)
    layer = graph.create_node_by_class(unreal.MovieGraphRenderLayerNode)
    set_props(layer, bOverride_LayerName=True, LayerName=layer_name)
    graph.add_labeled_edge(graph.get_input_node(), branch, renderer_node, "")
    graph.add_labeled_edge(renderer_node, "", layer, "")
    graph.add_labeled_edge(layer, "", graph.get_output_node(), branch)


def output_node(graph, cls):
    node = graph.create_node_by_class(cls)
    set_props(node, bOverride_FileNameFormat=True, FileNameFormat=FILE_FORMAT)
    return node


def sampling_nodes(graph, temporal, warmup):
    sampling = graph.create_node_by_class(unreal.MovieGraphSamplingMethodNode)
    set_props(sampling, bOverride_TemporalSampleCount=True, TemporalSampleCount=temporal)
    warm = graph.create_node_by_class(unreal.MovieGraphWarmUpSettingNode)
    # emulate motion blur: el primer frame ya tiene velocidades/motion blur correctos
    set_props(warm, bOverride_NumWarmUpFrames=True, NumWarmUpFrames=warmup,
              bOverride_bEmulateMotionBlur=True, bEmulateMotionBlur=True)
    cam = graph.create_node_by_class(unreal.MovieGraphCameraSettingNode)
    # obturador centrado en el frame (como una camara real, 180 grados lo da la CineCamera/PPV)
    set_props(cam, bOverride_ShutterTiming=True, ShutterTiming=unreal.MoviePipelineShutterTiming.FRAME_CENTER)
    return [sampling, warm, cam]


def build_preview():
    g = new_graph("MRG_Cine_Preview")
    if not g:
        return
    png = output_node(g, unreal.MovieGraphImageSequenceOutputNode_PNG)
    globals_branch(g, 1280, 720, sampling_nodes(g, temporal=1, warmup=8) + [png])
    deferred = g.create_node_by_class(unreal.MovieGraphDeferredRenderPassNode)
    set_props(deferred, bOverride_AntiAliasingMethod=True, AntiAliasingMethod=unreal.AntiAliasingMethod.AAM_TSR)
    layer_branch(g, "beauty", deferred, "beauty")
    eal.save_loaded_asset(g)
    log("MRG_Cine_Preview creado")


def build_final():
    g = new_graph("MRG_Cine_Final")
    if not g:
        return
    exr = output_node(g, unreal.MovieGraphImageSequenceOutputNode_MultiLayerEXR)
    # 16 subframes temporales: limpian aliasing, ruido de Lumen/MegaLights y dan motion blur real
    globals_branch(g, 1920, 1080, sampling_nodes(g, temporal=16, warmup=32) + [exr])
    deferred = g.create_node_by_class(unreal.MovieGraphDeferredRenderPassNode)
    set_props(deferred,
              bOverride_SpatialSampleCount=True, SpatialSampleCount=1,
              # con acumulacion de samples el AA temporal sobra y emborrona
              bOverride_AntiAliasingMethod=True, AntiAliasingMethod=unreal.AntiAliasingMethod.AAM_NONE,
              # EXR lineal (scene-referred) para gradear en Nuke igual que los EXR de Karma
              bOverride_bDisableToneCurve=True, bDisableToneCurve=True,
              bOverride_bAllowOCIO=True, bAllowOCIO=False)
    layer_branch(g, "beauty", deferred, "beauty")
    eal.save_loaded_asset(g)
    log("MRG_Cine_Final creado")


def build_pathtracer():
    g = new_graph("MRG_Cine_PathTracer")
    if not g:
        return
    exr = output_node(g, unreal.MovieGraphImageSequenceOutputNode_MultiLayerEXR)
    globals_branch(g, 1920, 1080, sampling_nodes(g, temporal=1, warmup=8) + [exr])
    cls = getattr(unreal, "MovieGraphPathTracerRenderPassNode", None) or getattr(unreal, "MovieGraphPathTracedRenderPassNode")
    pt = g.create_node_by_class(cls)
    set_props(pt,
              bOverride_SpatialSampleCount=True, SpatialSampleCount=64,
              bOverride_bDisableToneCurve=True, bDisableToneCurve=True)
    layer_branch(g, "pathtracer", pt, "pathtracer")
    eal.save_loaded_asset(g)
    log("MRG_Cine_PathTracer creado")


# ---------------------------------------------------------------- Nivel de lookdev

def spawn(cls, loc=(0, 0, 0), rot=(0, 0, 0), label=None):
    actor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_class(
        cls, unreal.Vector(*loc), unreal.Rotator(roll=rot[0], pitch=rot[1], yaw=rot[2]))
    if label:
        actor.set_actor_label(label)
    return actor


def spawn_mesh(mesh_path, loc, scale, label, material_path=None):
    actor = spawn(unreal.StaticMeshActor, loc, label=label)
    comp = actor.static_mesh_component
    comp.set_static_mesh(unreal.load_asset(mesh_path))
    actor.set_actor_scale3d(unreal.Vector(*scale))
    if material_path and eal.does_asset_exist(material_path):
        comp.set_material(0, unreal.load_asset(material_path))
    return actor


def build_level():
    if eal.does_asset_exist(MAP_PATH):
        warn(MAP_PATH + " ya existe, no lo toco")
        return None
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.new_level(MAP_PATH)

    # Sol: ~100.000 lux (dia soleado). Source angle 0.5 = disco solar real -> penumbra correcta
    sun = spawn(unreal.DirectionalLight, (0, 0, 500), rot=(0, -35, -40), label="Sun")
    lc = sun.light_component
    set_props(lc, intensity=100000.0, atmosphere_sun_light=True, light_source_angle=0.5)
    lc.set_mobility(unreal.ComponentMobility.MOVABLE)

    spawn(unreal.SkyAtmosphere, label="SkyAtmosphere")
    sky = spawn(unreal.SkyLight, (0, 0, 300), label="SkyLight")
    set_props(sky.light_component, real_time_capture=True)
    sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    spawn(unreal.VolumetricCloud, label="VolumetricClouds")
    fog = spawn(unreal.ExponentialHeightFog, label="HeightFog")
    set_props(fog.component, enable_volumetric_fog=True, fog_density=0.01)

    # Post Process: exposicion MANUAL con camara fisica (ISO / obturador / f-stop de la CineCamera)
    ppv = spawn(unreal.PostProcessVolume, label="PPV_Global")
    ppv.set_editor_property("unbound", True)
    s = ppv.get_editor_property("settings")
    s.set_editor_property("override_auto_exposure_method", True)
    s.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
    s.set_editor_property("override_auto_exposure_apply_physical_camera_exposure", True)
    s.set_editor_property("auto_exposure_apply_physical_camera_exposure", True)
    s.set_editor_property("override_auto_exposure_bias", True)
    s.set_editor_property("auto_exposure_bias", 0.0)
    ppv.set_editor_property("settings", s)

    # Referencias de lookdev
    spawn_mesh("/Engine/BasicShapes/Plane", (0, 0, 0), (40, 40, 1), "Floor")
    spawn_mesh("/Engine/BasicShapes/Sphere", (-60, 0, 25), (0.5, 0.5, 0.5), "Ball_Chrome",
               "/Game/CinematicTemplate/Materials/MI_Chrome")
    spawn_mesh("/Engine/BasicShapes/Sphere", (60, 0, 25), (0.5, 0.5, 0.5), "Ball_Grey")
    # Maniqui de escala: cilindro de 180 cm (Plane/Cylinder del engine miden 100 uu = 100 cm)
    spawn_mesh("/Engine/BasicShapes/Cylinder", (0, 150, 90), (0.45, 0.3, 1.8), "Scale_Human_180cm")

    # CineCamera: sensor 16:9 Digital Film, 35 mm, f/2.8, enfoque manual a las bolas
    # Exposicion fisica: f/2.8, 1/4000 s, ISO 100  ~= EV100 15 (sunny 16)
    cam = spawn(unreal.CineCameraActor, (-600, 0, 120), rot=(0, -5, 0), label="CineCam_Main")
    cc = cam.get_cine_camera_component()
    fb = cc.get_editor_property("filmback")
    fb.set_editor_property("sensor_width", 23.76)
    fb.set_editor_property("sensor_height", 13.365)
    cc.set_editor_property("filmback", fb)
    cc.set_editor_property("current_focal_length", 35.0)
    cc.set_editor_property("current_aperture", 2.8)
    focus = cc.get_editor_property("focus_settings")
    focus.set_editor_property("focus_method", unreal.CameraFocusMethod.MANUAL)
    focus.set_editor_property("manual_focus_distance", 600.0)
    cc.set_editor_property("focus_settings", focus)
    pp = cc.get_editor_property("post_process_settings")
    pp.set_editor_property("override_camera_iso", True)
    pp.set_editor_property("camera_iso", 100.0)
    pp.set_editor_property("override_camera_shutter_speed", True)
    pp.set_editor_property("camera_shutter_speed", 4000.0)
    cc.set_editor_property("post_process_settings", pp)

    les.save_current_level()
    log("LV_Lookdev creado")
    return cam


# ---------------------------------------------------------------- Level Sequence

def build_sequence(cam):
    path = SEQ_DIR + "/" + SEQ_NAME
    if eal.does_asset_exist(path):
        warn(path + " ya existe, no lo toco")
        return
    seq = asset_tools.create_asset(SEQ_NAME, SEQ_DIR, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(FPS, 1))
    seq.set_tick_resolution(unreal.FrameRate(24000, 1))
    seq.set_playback_start(0)
    seq.set_playback_end(SEQ_FRAMES)
    if cam:
        binding = seq.add_possessable(cam)
        track = seq.add_track(unreal.MovieSceneCameraCutTrack)
        section = track.add_section()
        section.set_range(0, SEQ_FRAMES)
        try:
            section.set_camera_binding_id(seq.get_binding_id(binding))
        except Exception as e:
            warn("Camera cut: enlaza la camara a mano (%s)" % e)
    eal.save_loaded_asset(seq)
    log("SEQ_Lookdev creado")


def run(quit_after=False):
    for step in (build_preview, build_final, build_pathtracer):
        try:
            step()
        except Exception as e:
            unreal.log_error("[VFXBrain] %s fallo: %s" % (step.__name__, e))
    cam = None
    try:
        cam = build_level()
    except Exception as e:
        unreal.log_error("[VFXBrain] build_level fallo: %s" % e)
    try:
        build_sequence(cam)
        unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    except Exception as e:
        unreal.log_error("[VFXBrain] build_sequence fallo: %s" % e)
    log("SETUP TERMINADO")
    if quit_after:
        unreal.SystemLibrary.quit_editor()


if __name__ == "__main__":
    # Solo cierra el editor si se lanzo desde linea de comandos con -VFXBrainQuit
    run(quit_after="-vfxbrainquit" in unreal.SystemLibrary.get_command_line().lower())
