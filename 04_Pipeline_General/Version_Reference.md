# Referencia de versiones de software instaladas

## Houdini 22 (ambas máquinas)
- UI rediseñada (más limpia, nuevas opciones de personalización)
- Gaussian Splatting nativo: los splats son ciudadanos de primera clase, editables procedimentalmente en cualquier nodo (no solo visualización/render), se pueden crear, cargar y modificar como point clouds con atributos
- Solaris: mejoras grandes en layout, worldbuilding y set dressing, scattering procedural más rápido
- APEX Rig Pose Node: nuevo sistema central de rigging, gestiona posing/rest pose/animación, con Set Driven Key automatizado
- Neural Layer to Height: ML aplicado a generación de terrenos desde foto única (descarga modelo MOG 2 en background)
- Ramp catalog visual (sustituye presets de texto)
- Arquitectura de viewport en Vulkan (mejoras de rendimiento/estabilidad respecto a versiones anteriores)
- Evaluate Rig in Parallel: distribución de rigs en threads separados para playback fluido de personajes múltiples

## NukeX 17.0 v3
- Soporte nativo de 3D Gaussian Splats: importar (.ply/.splat), manipular, renderizar (nodo SplatRender con motion blur y depth output), aislar elementos con Field nodes
- Sistema 3D modernizado basado en USD: workflows no destructivos para proyecciones, iluminación real, materiales/shaders importables de otro software
- Path-based masking: cada elemento upstream sigue accesible en cualquier punto de la cadena, incluso al final del setup
- Sistema de anotaciones renovado (pinceles rediseñados, panel de comentarios dedicado)
- NukeX incluye BigCat (extensión de CopyCat para entrenar modelos de ML propios con datasets grandes)
- Compatible con VFX Reference Platform 2025, USD 25.08

## Regla de uso
Antes de sugerir un nodo, parámetro o workflow específico de versión, verificar contra este documento. Si hay duda sobre si una feature existe en la versión instalada, preguntar al usuario antes de asumir, en vez de dar por hecho comportamiento de versiones anteriores o posteriores.
