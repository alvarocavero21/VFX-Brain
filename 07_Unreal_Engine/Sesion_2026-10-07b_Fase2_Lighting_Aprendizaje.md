# Sesión: 2026-10-07 (mañana)
## Proyecto/Shot: Aprendizaje Unreal Engine 5.8, Fase 2 (lighting study)

### Qué se hizo hoy
- Encontrada una librería Megascans completa en `ElectricDreamsEnv/Content/Megascans`, que se puede reutilizar sin descargar nada de Fab.
- Probada la migración headless de assets entre proyectos y el render de MRG por línea de comandos. Lo aprendido está en [[UE58_Python_API_Aprendizajes]].
- Definidos valores físicos de partida para golden hour, overcast y noche. Están en [[Iluminacion_Cinematica_Realista]] §6.

### Decisiones tomadas
- **Álvaro: no quiere renders ni escenas montadas, solo que Claude aprenda y lo documente.** Se borró el proyecto de prueba `UE58_LightStudy` (2,7 GB con los renders) y los scripts que lo generaban.
- Limpieza de disco:
  - `UE58_Cine_Template`: borradas sus cachés (Intermediate, DerivedDataCache, Saved; unos 615 MB). Queda el proyecto, que ocupa 1,3 MB.
  - Caché global de shaders: borrado lo generado hoy (~0,67 GB).

### Problemas encontrados
- `unreal.log()` no aparece en stdout en modo headless: hay que leer `Saved/Logs`.
- `-MoviePipelineConfig` no acepta un MovieGraphConfig directamente, solo una cola `.utxt`.
- `LinearColor` no tiene `to_fcolor` en Python, y `light_color` es FColor.

### Siguiente paso
- **MCP de Unreal desconectado** (Claude ya no controla UE). Nuevo modo de trabajo: Álvaro ejecuta en el editor y Claude le guía paso a paso y le da tips.
- Fase 3 del roadmap (cámara y lenguaje) en ese modo.
