# Con FLUX + scheduler karras, el img2img sale casi idéntico a la imagen base aunque el denoise sea alto
Tags: #comfyui #flux #img2img #scheduler #karras #denoise

## Contexto
Img2img con FLUX.1-dev fp8 en ComfyUI (proyecto [[05_Projects/Boundaries_Escena4/notes|Boundaries · Escena 4]]): dpmpp_2m + **karras**, 30 pasos, denoise 0.6, con un segundo inpaint a 0.82. El resultado era prácticamente el concept original: las siluetas seguían planas incluso en la zona inpainteada a 0.82.

## Solución
Cambiar el scheduler del KSampler a **`simple`** (o `beta`), que son los schedulers pensados para FLUX. El sampler `dpmpp_2m` puede quedarse. Con `simple`, denoise 0.6 transforma de verdad la imagen sin perder el encuadre (que lo sujetan los ControlNets).

## Por qué pasaba
FLUX es un modelo flow-matching con sigmas en [0, 1]. Karras (rho=7) concentra casi todos los pasos en sigmas muy bajos. Con denoise `d`, ComfyUI calcula un schedule de `pasos/d` pasos y se queda con los últimos `pasos`. Con karras, el primer sigma de esa cola es diminuto: con 30 pasos y d=0.6 (schedule de 50) arranca en sigma ≈ 0.17. Es decir, **un denoise 0.6 con karras equivale a ~0.17 de ruido real**. Con `simple` (más el shift de FLUX), el muestreo arranca cerca de lo que indica el denoise.

**Regla:** con FLUX (y otros modelos flow-matching como SD3 o Wan), no usar karras ni exponential en img2img o inpaint si quieres que el valor de denoise sea interpretable. En SDXL/SD1.5 karras sí es correcto.
