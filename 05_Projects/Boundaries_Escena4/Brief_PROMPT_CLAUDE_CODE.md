# Boundaries · Escena 4 · Concepts fotorrealistas con ComfyUI

Las imágenes base están en esta misma carpeta:
- `Concept_plano1_ventana.jpg`: plano 1. Kal y G, de espaldas, dentro de la estación, ven llegar por la ventana un transporte rojo en el espacio.
- `Concept_plano2_contraplano.jpg`: plano 2 (contraplano). Desde fuera, una ventana pequeña e iluminada en la roca de un asteroide gigante, con dos figuras dentro. Ya está recortada: no hay que recortar nada.

Son concepts de composición hechos a mano. El objetivo es que tengan aspecto fotorrealista sin perder el encuadre.

## Permiso para esta tarea
Para esta tarea SÍ puedes lanzar las generaciones tú mismo por la API de ComfyUI. Es una excepción puntual a mi preferencia habitual de que no lances renders; no la cambies en memoria.

## Paso 1: comprueba el entorno
- Busca la API de ComfyUI en http://127.0.0.1:8188 y, si no responde, en http://127.0.0.1:8000 (ComfyUI Desktop). Si no responde ninguna, para y dímelo.
- Lista los checkpoints, ControlNets, preprocesadores y upscalers instalados (GET /object_info). Prefiero FLUX.1-dev; si no está, SDXL. Para ControlNet, Union o Depth + Canny.
- Dime qué vas a usar y si falta algo. No descargues modelos sin preguntarme.

## Paso 2: workflow
Construye un workflow en formato API y guárdalo como JSON en `./workflows` para poder reutilizarlo:
- img2img desde la imagen base + ControlNet Depth y Canny, fuerza 0.6, que se desactive al 50 % de los pasos.
- Generación a 1536x640 (2.39:1), después upscale x2.
- Segunda pasada de inpaint sobre las personas. Crea tú la máscara a partir de la imagen: en el plano 1 son las dos siluetas oscuras en primer término; en el plano 2, la ventana iluminada del centro. Guarda las máscaras en `./masks`.
- Sampler: dpmpp_2m, scheduler karras, 30 pasos, CFG 3.5 (FLUX) o 6 (SDXL).

### Plano 1
Denoise general 0.6; inpaint de las siluetas a 0.8–0.85.

Prompt:
```
cinematic film still, dim industrial interior of a space station carved into an asteroid, two space marines seen from behind, a man and a woman with a ponytail, standing at a large panoramic window, outside deep space with stars and a blue nebula, a small boxy damaged red military escape transport with glowing orange thrusters approaching, edge of a gas giant, red thruster light rim-lighting their shoulders and hair, anamorphic 2.39:1, 35mm film grain, shallow depth of field, photorealistic
```

### Plano 2
Denoise general 0.4; inpaint de la ventana a 0.6.

Prompt:
```
cinematic wide shot, exterior of a huge dark rocky asteroid mining outpost in space, industrial modules embedded in the rock, one small warmly lit window carved into the rock face with two tiny human figures inside, lit hangar entrance nearby, mining facilities with smoke and orange work lights, gas giant planet in the background, starfield, photorealistic miniature photography, practical model effects look, film grain
```

### Negativo (los dos planos)
```
cartoon, illustration, cgi, 3d render, plastic, flat colors, text, watermark, deformed, extra people
```

## Paso 3: genera y filtra
- 4 variantes por plano (seeds distintas) en `./output/plano1` y `./output/plano2`.
- Revisa tú las imágenes y descarta las que tengan manos o caras deformadas, gente de más, la nave fuera de cuadro (plano 1) o la ventana sin las dos figuras (plano 2).
- Si ninguna pasa, ajusta el denoise o la fuerza de ControlNet y repite. Máximo 3 rondas por plano.
- Si en el plano 2 las figuras siguen saliendo mal tras 3 rondas, genera el asteroide sin personas (quítalas del prompt) y avísame: las meteré yo a mano.

## Paso 4: informe
Dime qué variante elegirías de cada plano y por qué, y con qué parámetros finales. No borres nada.
