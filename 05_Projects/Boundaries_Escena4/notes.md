# Shot: Boundaries · Escena 4 · Concepts fotorrealistas (planos 1 y 2)
Tags: #boundaries #comfyui #flux #controlnet #pitch #concept

## Estado: Concepts generados. Plano 1 usable; plano 2 pendiente de retoque en la ventana.
## Última sesión: [[Sesion_2026-10-10_Concepts_ComfyUI]]

Corto **Boundaries** (UTAD / GiantVFX), escena 4. Contexto y presupuesto: [[00_MOC_Presupuesto_Boundaries]] · [[2026-10-01 - Desglose VFX del guion y presupuesto escena 4]].

Objetivo: pasar dos concepts de composición hechos a mano a imágenes fotorrealistas para el pitch, **sin perder el encuadre**. Brief original: [[Brief_PROMPT_CLAUDE_CODE]].

| Plano | Qué es | Concept | Elegida |
|---|---|---|---|
| 1 | Kal y G de espaldas, dentro de la estación, ven llegar el transporte rojo por la ventana | ![[plano1_concept.jpg]] | ![[plano1_elegida_r1_s303.jpg]] |
| 2 | Contraplano: ventana pequeña iluminada en la roca del asteroide, con las dos figuras dentro | ![[plano2_concept.jpg]] | ![[plano2_elegida_r3_s101.jpg]] |

**Archivos** (fuera del vault, en `C:\Users\alvar\Downloads\Boundaries_concepts\`):
- `output/plano1` y `output/plano2`: 39 PNG a 3072x1280; de cada variante hay versión `_preinpaint` y `_final`.
- `workflows/`, `masks/`: copia de referencia en el vault en `03_ComfyUI/Workflows/Boundaries_FLUX_img2img/`.
- Técnica reutilizable: [[FLUX_img2img_ControlNet_Inpaint_por_Recorte]] · [[FLUX_Union_Pro_2_Depth_Canny]] · [[ComfyUI_Pinokio_Setup_y_Modelos]].

### Decisiones tomadas
- **Modelo: FLUX.1-dev fp8** (checkpoint todo en uno) + **ControlNet Union Pro 2.0** (Depth Anything V2 vitb + Canny), fuerza 0.6, del 0 al 50 % de los pasos. Upscale x2 con 4x-UltraSharp. Se eligió frente a SDXL por fotorrealismo. La licencia de FLUX-dev es no comercial: vale para el pitch, pero hay que revisarla si se usa en producción.
- **Scheduler `simple`, no `karras`.** Con FLUX, karras hace que el denoise no signifique lo que pone → [[FLUX_scheduler_karras_anula_denoise]].
- **CFG 3.5 = FluxGuidance**, con el CFG del KSampler a 1.0. Por eso el **prompt negativo no tiene efecto**; para activarlo hay que subir el CFG del KSampler a ~1.5 (cada imagen tarda el doble).
- **Inpaint por recorte**: se recorta la zona de las personas de la imagen ya escalada, se inpaintea a ~1 MP con DifferentialDiffusion y se vuelve a componer con la máscara. Imprescindible en el plano 2, donde la ventana mide ~110x60 px en el concept.
- Prompt de inpaint específico de la zona (personas o ventana) en vez del prompt general, para que no meta naves ni elementos dentro del recorte.
- **Plano 1 → `r1_s303`**: personas correctas (él con pelo corto, ella con coleta), nave en cuadro, la orientación y el gas giant más fieles al concept, algo de rim naranja en hombros y sin texto basura.
- **Plano 2 → `r3_s101`**: la coleta se lee, hay dos figuras y la textura de roca se ve a través del halo. Alternativa más fiel al concept, aunque más "pegatina": `r1_s202` ![[plano2_r1_s202.jpg]]

### Parámetros finales
| | Plano 1 (r1_s303) | Plano 2 (r3_s101) |
|---|---|---|
| Denoise general | 0.6 | 0.4 |
| Inpaint | 0.82 (máscara de siluetas) | 0.75 (máscara de ventana + halo) |
| ControlNet | 0.6, end 0.5 | 0.5, end 0.5 |
| Recorte de inpaint (espacio 3072x1280) | 1408,512 · 1664x768 → 1664x768 | 1152,418 · 768x576 → 1024x768 |
| Seed general / seed de inpaint | 303 / 304 | 101 / 102 |
| Común | dpmpp_2m · simple · 30 pasos · FluxGuidance 3.5 · 1536x640 → 3072x1280 | |

### Crítica técnica (antes de seguir)
- **Plano 1**: se parece más a un render 3D limpio que a una foto. La nave ha perdido el daño del concept y parece de juguete. No hay rim rojo real en el pelo. Las manos quedan casi fuera de cuadro (bien).
- **Plano 2**: la miniatura y el humo funcionan, pero **la ventana sigue leyéndose como gráfica** (marco negro grueso, siluetas recortadas) y el halo naranja queda como un blob suave. Algunas seeds meten texto basura ("GUMITB") y soldaditos de más.

### Problemas resueltos
- [[FLUX_scheduler_karras_anula_denoise]]
- ComfyUI no arrancaba porque Pinokio estaba cerrado y `pterm` apuntaba a una IP de red vieja → [[ComfyUI_Pinokio_Setup_y_Modelos]]

### Siguiente paso
- [ ] Plano 2: probar el inpaint de la ventana **sin ControlNet** (el Canny es lo que fija el marco negro plano), o retocar la ventana a mano o en Nuke.
- [ ] Plano 1: si hace falta más foto y menos CG, probar denoise 0.65–0.7 o activar el negativo (CFG del KSampler a 1.5), y añadir el daño a la nave en el prompt.
- [ ] Decidir si se rehace el halo del plano 2 en compo (glow real sobre la roca).
