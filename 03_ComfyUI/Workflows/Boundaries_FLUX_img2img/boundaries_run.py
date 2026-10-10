"""Boundaries · Escena 4 — concepts fotorrealistas con FLUX.1-dev + ControlNet Union Pro 2.0.

Construye el workflow en formato API, lo guarda en ./workflows y (opcionalmente) lo lanza
contra ComfyUI, descargando los resultados en ./output/planoN.

Uso:
  python boundaries_run.py --plano 1 --round 1 --seeds 101 202 303 404 [--url http://127.0.0.1:8188]
  python boundaries_run.py --plano 2 --denoise 0.35 --cn 0.7 --save-only
"""
import argparse, json, os, sys, time, uuid, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEG = "cartoon, illustration, cgi, 3d render, plastic, flat colors, text, watermark, deformed, extra people"

PLANOS = {
    1: dict(
        image="Concept_plano1_ventana.jpg",
        mask="masks/plano1_siluetas_mask.png",
        denoise=0.6, inpaint_denoise=0.82,
        # Recorte (en espacio 3072x1280) alrededor de las siluetas y resolución a la que se inpaintea
        crop=(1408, 512, 1664, 768), crop_res=(1664, 768),
        prompt=("cinematic film still, dim industrial interior of a space station carved into an asteroid, "
                "two space marines seen from behind, a man and a woman with a ponytail, standing at a large "
                "panoramic window, outside deep space with stars and a blue nebula, a small boxy damaged red "
                "military escape transport with glowing orange thrusters approaching, edge of a gas giant, red "
                "thruster light rim-lighting their shoulders and hair, anamorphic 2.39:1, 35mm film grain, "
                "shallow depth of field, photorealistic"),
        inpaint_prompt=("cinematic film still, two space marines seen from behind, a man and a woman with a ponytail, "
                        "wearing worn dark tactical armor, standing at a large panoramic window looking out into space, "
                        "red-orange thruster light rim-lighting their shoulders and hair, dim industrial space station "
                        "interior, 35mm film grain, shallow depth of field, photorealistic"),
    ),
    2: dict(
        image="Concept_plano2_contraplano.jpg",
        mask="masks/plano2_ventana_mask.png",
        denoise=0.4, inpaint_denoise=0.6,
        crop=(1344, 562, 384, 288), crop_res=(1024, 768),
        prompt=("cinematic wide shot, exterior of a huge dark rocky asteroid mining outpost in space, industrial "
                "modules embedded in the rock, one small warmly lit window carved into the rock face with two tiny "
                "human figures inside, lit hangar entrance nearby, mining facilities with smoke and orange work "
                "lights, gas giant planet in the background, starfield, photorealistic miniature photography, "
                "practical model effects look, film grain"),
        inpaint_prompt=("close-up of a small warmly lit rectangular window carved into dark rough asteroid rock, two "
                        "human figures standing inside the window, a man and a woman with a ponytail, silhouetted "
                        "against warm orange interior light, photorealistic miniature photography, practical model "
                        "effects look, film grain"),
    ),
}

HALO_PROMPT = ("small horizontal rectangular window carved into dark rough asteroid rock, warm orange interior light "
               "spilling out and softly lighting the surrounding rock face, two small human figures standing inside the "
               "window looking out, a man and a woman with a ponytail, backlit, photorealistic miniature photography, "
               "practical model effects look, film grain")

W, H = 1536, 640          # generación 2.39:1
UW, UH = W * 2, H * 2     # tras upscale x2


def build(p, seed, denoise, cn, cn_end, inpaint_denoise, image_name, mask_name, prefix, figures=True):
    cx, cy, cw, ch = p["crop"]
    sw, sh = p["crop_res"]
    prompt, inprompt = p["prompt"], p["inpaint_prompt"]
    if not figures:  # plan B plano 2: asteroide sin personas
        prompt = prompt.replace(" with two tiny human figures inside", "")
        inprompt = ("close-up of a small warmly lit empty rectangular window carved into dark rough asteroid rock, "
                    "warm orange interior light, photorealistic miniature photography, film grain")
    sampler = dict(steps=30, cfg=1.0, sampler_name="dpmpp_2m", scheduler="simple")
    g = {
        "1": ("CheckpointLoaderSimple", {"ckpt_name": "flux1-dev-fp8.safetensors"}),
        "2": ("LoadImage", {"image": image_name}),
        "3": ("ImageScale", {"image": ["2", 0], "upscale_method": "lanczos", "width": W, "height": H, "crop": "disabled"}),
        "4": ("CLIPTextEncode", {"clip": ["1", 1], "text": prompt}),
        "5": ("CLIPTextEncode", {"clip": ["1", 1], "text": NEG}),
        "6": ("FluxGuidance", {"conditioning": ["4", 0], "guidance": 3.5}),
        "7": ("ControlNetLoader", {"control_net_name": "FLUX.1-dev-ControlNet-Union-Pro-2.0.safetensors"}),
        "8": ("DepthAnythingV2Preprocessor", {"image": ["3", 0], "ckpt_name": "depth_anything_v2_vitb.pth", "resolution": 1024}),
        "9": ("Canny", {"image": ["3", 0], "low_threshold": 0.2, "high_threshold": 0.5}),
        "10": ("ControlNetApplyAdvanced", {"positive": ["6", 0], "negative": ["5", 0], "control_net": ["7", 0], "image": ["8", 0],
                                           "strength": cn, "start_percent": 0.0, "end_percent": cn_end, "vae": ["1", 2]}),
        "11": ("ControlNetApplyAdvanced", {"positive": ["10", 0], "negative": ["10", 1], "control_net": ["7", 0], "image": ["9", 0],
                                           "strength": cn, "start_percent": 0.0, "end_percent": cn_end, "vae": ["1", 2]}),
        "12": ("VAEEncode", {"pixels": ["3", 0], "vae": ["1", 2]}),
        "13": ("KSampler", {"model": ["1", 0], "seed": seed, **sampler, "positive": ["11", 0], "negative": ["11", 1],
                            "latent_image": ["12", 0], "denoise": denoise}),
        "14": ("VAEDecode", {"samples": ["13", 0], "vae": ["1", 2]}),
        # Upscale x2: 4x-UltraSharp y bajada a 3072x1280
        "16": ("UpscaleModelLoader", {"model_name": "4x-UltraSharp.pth"}),
        "17": ("ImageUpscaleWithModel", {"upscale_model": ["16", 0], "image": ["14", 0]}),
        "18": ("ImageScale", {"image": ["17", 0], "upscale_method": "lanczos", "width": UW, "height": UH, "crop": "disabled"}),
        "19": ("SaveImage", {"images": ["18", 0], "filename_prefix": prefix + "_A_preinpaint"}),
        # Inpaint por recorte: máscara -> 3072x1280 -> crop -> escala de trabajo
        "20": ("LoadImageMask", {"image": mask_name, "channel": "red"}),
        "21": ("MaskToImage", {"mask": ["20", 0]}),
        "22": ("ImageScale", {"image": ["21", 0], "upscale_method": "bilinear", "width": UW, "height": UH, "crop": "disabled"}),
        "23": ("ImageToMask", {"image": ["22", 0], "channel": "red"}),
        "24": ("ImageCrop", {"image": ["18", 0], "x": cx, "y": cy, "width": cw, "height": ch}),
        "25": ("CropMask", {"mask": ["23", 0], "x": cx, "y": cy, "width": cw, "height": ch}),
        "26": ("ImageScale", {"image": ["24", 0], "upscale_method": "lanczos", "width": sw, "height": sh, "crop": "disabled"}),
        "27": ("MaskToImage", {"mask": ["25", 0]}),
        "28": ("ImageScale", {"image": ["27", 0], "upscale_method": "bilinear", "width": sw, "height": sh, "crop": "disabled"}),
        "29": ("ImageToMask", {"image": ["28", 0], "channel": "red"}),
        "30": ("CLIPTextEncode", {"clip": ["1", 1], "text": inprompt}),
        "31": ("FluxGuidance", {"conditioning": ["30", 0], "guidance": 3.5}),
        "32": ("DepthAnythingV2Preprocessor", {"image": ["26", 0], "ckpt_name": "depth_anything_v2_vitb.pth", "resolution": 1024}),
        "33": ("Canny", {"image": ["26", 0], "low_threshold": 0.2, "high_threshold": 0.5}),
        "34": ("ControlNetApplyAdvanced", {"positive": ["31", 0], "negative": ["5", 0], "control_net": ["7", 0], "image": ["32", 0],
                                           "strength": cn, "start_percent": 0.0, "end_percent": cn_end, "vae": ["1", 2]}),
        "35": ("ControlNetApplyAdvanced", {"positive": ["34", 0], "negative": ["34", 1], "control_net": ["7", 0], "image": ["33", 0],
                                           "strength": cn, "start_percent": 0.0, "end_percent": cn_end, "vae": ["1", 2]}),
        "36": ("InpaintModelConditioning", {"positive": ["35", 0], "negative": ["35", 1], "vae": ["1", 2], "pixels": ["26", 0],
                                            "mask": ["29", 0], "noise_mask": True}),
        "37": ("DifferentialDiffusion", {"model": ["1", 0], "strength": 1.0}),
        "38": ("KSampler", {"model": ["37", 0], "seed": seed + 1, **sampler, "positive": ["36", 0], "negative": ["36", 1],
                            "latent_image": ["36", 2], "denoise": inpaint_denoise}),
        "39": ("VAEDecode", {"samples": ["38", 0], "vae": ["1", 2]}),
        "40": ("ImageScale", {"image": ["39", 0], "upscale_method": "lanczos", "width": cw, "height": ch, "crop": "disabled"}),
        "41": ("ImageCompositeMasked", {"destination": ["18", 0], "source": ["40", 0], "x": cx, "y": cy,
                                        "resize_source": False, "mask": ["25", 0]}),
        "42": ("SaveImage", {"images": ["41", 0], "filename_prefix": prefix + "_B_final"}),
    }
    return {k: {"class_type": c, "inputs": i} for k, (c, i) in g.items()}


def http(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def upload(base, path, name):
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + open(path, "rb").read() + \
           f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n".encode()
    r = json.loads(http(base + "/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    return r["name"]


def run(base, wf, out_dir, tag):
    pid = json.loads(http(base + "/prompt", json.dumps({"prompt": wf, "client_id": "boundaries"}).encode(),
                          {"Content-Type": "application/json"}))["prompt_id"]
    t0 = time.time()
    while True:
        time.sleep(3)
        h = json.loads(http(f"{base}/history/{pid}"))
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                raise RuntimeError(json.dumps(st.get("messages", [])[-1:], indent=1)[:2000])
            if st.get("completed"):
                break
    saved = []
    for node in h[pid]["outputs"].values():
        for im in node.get("images", []):
            q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
            kind = "final" if "_B_final" in im["filename"] else "preinpaint"
            dst = os.path.join(out_dir, f"{tag}_{kind}.png")
            open(dst, "wb").write(http(f"{base}/view?{q}"))
            saved.append(dst)
    print(f"{tag}: {time.time() - t0:.0f}s -> {', '.join(os.path.basename(s) for s in saved)}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plano", type=int, required=True, choices=[1, 2])
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--seeds", type=int, nargs="+", default=[101, 202, 303, 404])
    ap.add_argument("--denoise", type=float)
    ap.add_argument("--inpaint-denoise", type=float)
    ap.add_argument("--cn", type=float, default=0.6)
    ap.add_argument("--cn-end", type=float, default=0.5)
    ap.add_argument("--no-figures", action="store_true")
    ap.add_argument("--url", default="http://127.0.0.1:8188")
    ap.add_argument("--save-only", action="store_true")
    ap.add_argument("--mask", help="máscara alternativa (ruta relativa a la carpeta del proyecto)")
    ap.add_argument("--crop", type=int, nargs=4, metavar=("X", "Y", "W", "H"), help="recorte de inpaint en espacio 3072x1280")
    ap.add_argument("--crop-res", type=int, nargs=2, metavar=("W", "H"))
    ap.add_argument("--halo", action="store_true", help="plano 2: prompt de inpaint para ventana + halo de luz sobre la roca")
    a = ap.parse_args()
    p = dict(PLANOS[a.plano])
    if a.mask: p["mask"] = a.mask
    if a.crop: p["crop"] = tuple(a.crop)
    if a.crop_res: p["crop_res"] = tuple(a.crop_res)
    if a.halo: p["inpaint_prompt"] = HALO_PROMPT
    den = a.denoise if a.denoise is not None else p["denoise"]
    iden = a.inpaint_denoise if a.inpaint_denoise is not None else p["inpaint_denoise"]

    img_name, mask_name = f"boundaries_{p['image']}", f"boundaries_plano{a.plano}_mask.png"
    wf = build(p, a.seeds[0], den, a.cn, a.cn_end, iden, img_name, mask_name,
               f"boundaries/plano{a.plano}/r{a.round}", figures=not a.no_figures)
    wf_path = os.path.join(ROOT, "workflows", f"plano{a.plano}_api.json")
    json.dump(wf, open(wf_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("workflow ->", wf_path)
    if a.save_only:
        return
    upload(a.url, os.path.join(ROOT, p["image"]), img_name)
    upload(a.url, os.path.join(ROOT, p["mask"]), mask_name)
    out_dir = os.path.join(ROOT, "output", f"plano{a.plano}")
    os.makedirs(out_dir, exist_ok=True)
    print(f"plano {a.plano} r{a.round}: denoise={den} inpaint={iden} cn={a.cn}@{a.cn_end} figures={not a.no_figures}", flush=True)
    for s in a.seeds:
        wf = build(p, s, den, a.cn, a.cn_end, iden, img_name, mask_name,
                   f"boundaries/plano{a.plano}/r{a.round}_s{s}", figures=not a.no_figures)
        run(a.url, wf, out_dir, f"r{a.round}_s{s}")


if __name__ == "__main__":
    main()
