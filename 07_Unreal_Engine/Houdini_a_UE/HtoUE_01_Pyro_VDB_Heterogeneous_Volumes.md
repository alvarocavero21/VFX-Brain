# Houdini → UE 5.8 · 01 · Pyro (VDB) como Heterogeneous Volume
Tags: #unreal #houdini #pyro #vdb #volumen #heterogeneous-volumes
Volver: [[Puente_Houdini_Unreal]] · Setup: [[HtoUE_00_Setup_Herramientas]]

**Caso de uso**: humo, fuego, explosiones, polvo volumétrico hero de Houdini renderizado dentro de UE con la luz de la escena (sombras, MegaLights, path tracer).
**Estado**: la doc oficial de 5.8 sigue marcando Heterogeneous Volumes como **Experimental** (la release de 5.7 lo llamaba Beta para Niagara). El importador VDB (Interchange OpenVDB) también es experimental. → Válido para portfolio, con pruebas previas.

## Flujo
`Pyro Solver → limpiar campos → File Cache (.vdb secuencia) → UE: Import → Sparse Volume Texture (SVT) → Material Volume (SparseVolumeMaterial) → Heterogeneous Volume Actor → Sequencer → MRG`

## 1. Houdini: preparar el cache
- Campos a exportar: **`density`** + como mucho **`temperature`** y **`flame`** (o `heat`). Nada más.
- **Borrar `vel`** antes de cachear: en UE 5.4 los VDB con velocidad crasheaban (reportado por la comunidad). *Verificar si sigue pasando en 5.8.* El motion blur no lo va a usar de todas formas (ver límites).
- Por qué ≤ 2–4 campos extra: el importador de UE 5.8 (código `SparseVolumeTextureFactory.cpp`) guarda **`density` en 8 bits (Attributes A)** y el resto de campos en **16 bits float (Attributes B, máx. 4 componentes)**. Esa es la "asignación optimizada"; con 3 campos extra los rellena a 4 igualmente.
- **Limpiar densidad baja** (evita el humo "punteado/pixelado" en colas finas, ver problemas):
  ```c
  // Volume Wrangle post-solver
  float cutoff = 0.02, soft = 0.03;
  @density *= smooth(cutoff, cutoff + soft, @density);
  ```
- Resolución: empezar con voxel grande y bajar solo si hace falta. La **VRAM** es el límite (la caché interna de iluminación es densa, máx. 1024×1024×512).
- Escala: dejar la sim en metros; corregir en UE (×100) o escalar ×100 en Houdini antes de exportar (decidir uno y documentarlo).

## 2. UE: importar
1. Activar plugin **Interchange OpenVDB** (Experimental) en el proyecto y reiniciar.
2. Arrastrar **un** `.vdb` de la secuencia al Content Browser → detecta la secuencia numerada completa.
3. En el diálogo: comprobar el mapeo de grids (density → A 8-bit unorm, temperature/flame → B 16-bit float). "Pivot at Centroid" centra el pivote pero rompe la posición original de Houdini → **desactivar** si quiero que coincida con la cámara/escena.

## 3. Material
- Duplicar `Engine Content > EngineMaterials > SparseVolumeMaterial` (material de dominio **Volume** con nodo *Sparse Volume Texture Sample*).
- Material Instance → asignar el SVT en *Global Texture Parameters*. Parámetros: Albedo Color/Scale, Density Scale.
- Para **fuego**: emisión a partir de `temperature`/`flame` con una rampa de blackbody (igual que mi shader de Karma en [[Pipeline_Bandera_Ardiendo_Vellum_Pyro]]). Hacerlo en una copia del material: Extinction ← density, Emissive ← ramp(temperature) × intensidad.

## 4. Actor Heterogeneous Volume
Place Actors → *Heterogeneous Volume* → asignar el Material Instance. Propiedades:
| Propiedad | Uso |
|---|---|
| Frame / Frame Rate (24) / Start–End Frame / Playing / Looping | Animación del cache. **Keyframear `Frame` en Sequencer** para render controlado |
| Step Factor | Paso de ray marching (múltiplo de la resolución). Bajar (0.5–0.25) = más calidad |
| Shadow Step Factor / Shadow Bias Factor | Calidad de sombras propias / reducir auto-sombreado |
| Lighting Downsample Factor | Resolución de la caché de luz (más bajo = más calidad, más VRAM) |
| **Issue Blocking Requests** | **ON para cinemática**: espera a que el streaming cargue todo |
| Streaming Mip Bias | Negativo (-1/-2) = forzar más detalle |

## 5. CVars para render cinemático (doc oficial 5.8)
Ponerlas en el nodo Console Variables de MRG ([[Movie_Render_Graph_Salida_a_Nuke]]):
```
r.HeterogeneousVolumes.IndirectLighting 1          ; GI en el volumen (off por defecto)
r.HeterogeneousVolumes.OrthoGrid.MaxBottomLevelMemoryInMegabytes 512   ; default 128
r.HeterogeneousVolumes.OrthoGridShadingRate 1      ; default 4
r.HeterogeneousVolumes.FrustumGrid.MaxBottomLevelMemoryInMegabytes 512
r.HeterogeneousVolumes.FrustumGrid.ShadingRate 1   ; default 4
r.HeterogeneousVolumes.FrustumGrid.DepthSliceCount 1024
r.PathTracing.HeterogeneousVolumes 1               ; si renderizo con path tracer
```
Comunidad (5.4): `r.HeterogeneousVolumes.MaxTraceDistance 1000000` si el volumen no se ve a distancia.
⚠️ Shading rate 1 sin subir la memoria → **faltan vóxeles**.

## 6. Iluminación
- Recibe luz direccional con sombras en cascada y proyecta sombras sobre el entorno (5.7: Beer Shadow Maps, mucho más rápido).
- Path tracer: soporte más completo, con GI real del volumen (requiere DX12 + HW ray tracing + path tracing activados → ya lo están en la plantilla).
- MegaLights soporta Heterogeneous Volumes desde 5.7 (luces de fuego dentro del humo).

## Límites y problemas conocidos
- **Humo de baja densidad punteado/pixelado/parpadeante**: mitigado (no resuelto del todo) con Issue Blocking Requests ON, Streaming Mip Bias -1/-2, Step Factor 0.5–0.25, Lighting Downsample bajo, más temporal samples, y limpiando densidad baja en Houdini. Sospecha: cuantización del SVT.
- **Volúmenes solapados** se ven a bloques → evitar solapar dos HV; mejor un VDB combinado.
- **Path tracer**: el actor no invalida la acumulación al animarse → pausar la animación / controlar por Sequencer.
- **Motion blur del volumen**: el actor reproduce frames del cache; no está claro que interpole entre frames en sub-frames de MRG → *probarlo* (si sale "stepped", alternativa: render del pyro en Karma con motion blur real e integrar en Nuke).
- Experimental: puede cambiar en hotfixes.

## Plan B (calidad garantizada)
Cámara UE → Houdini, pyro renderizado en **Karma XPU** con holdouts de la geometría de UE ([[Karma_Holdout_Matte_Render_Layers]]) → compo en Nuke. Más trabajo de integración, pero motion blur y shading perfectos.

## Fuentes
- [Heterogeneous Volumes in UE (doc oficial)](https://dev.epicgames.com/documentation/unreal-engine/heterogeneous-volumes-in-unreal-engine)
- [How to use VDBs in Unreal Engine — Versluis](https://www.versluis.com/2025/03/how-to-use-vdbs-in-unreal-engine/)
- [VDB volumes and Render Layers in UE 5.4 — Slick3D](https://slick3d.substack.com/p/volumes-and-render-layers-ue5)
- [Low-density VDB smoke dotted/pixelated — RealtimeVFX](https://realtimevfx.com/t/ue5-heterogeneous-volume-low-density-houdini-vdb-smoke-becomes-dotted-pixelated/31286)
- [UE 5.7 Release Notes (HV Beta, Beer Shadow Maps)](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-7-release-notes)
