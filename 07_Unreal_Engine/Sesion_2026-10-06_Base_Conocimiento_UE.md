# Sesión: 2026-10-06
## Proyecto/Shot: Aprendizaje Unreal Engine 5.8 — Fase 0 (base de conocimiento)

### Qué se hizo hoy
- Investigación de novedades de UE 5.8 (release notes oficiales + prensa).
- Investigación de las Easy tools de William Faucher en Fab (EasyToolbag, EasyFog, EasyRain, EasySnow, EasyAtmos, EasyMapper) y estado de Megascans en Fab.
- Creada la carpeta `07_Unreal_Engine/` con MOC, roadmap por fases y notas de iluminación, cámara, render (MRG → Nuke), materiales, puente Houdini → UE y checklist de crítico técnico.
- Añadido UE 5.8 a `04_Pipeline_General/Version_Reference.md`.

### Decisiones tomadas
- FX hero siguen en Houdini; UE para entorno, luz, cámara y render rápido. Easy tools para clima/atmósfera de fondo.
- Evitar features Experimental de 5.8 en shots de portfolio (Mesh Terrain, PVE, FSSS, MetaHuman Crowd).
- Render final con Movie Render Graph → EXR → Nuke en el mismo espacio ACES que Karma.

### Problemas encontrados
- Fab y la web de Epic bloquean lectura automática (403): precios y compatibilidad exacta 5.8 de cada Easy tool sin confirmar.

### Siguiente paso
Fase 1: crear proyecto plantilla `UE58_Cine_Template` (settings de proyecto, HW ray tracing, OCIO/ACES, presets MRG Cine_Final/Cine_Preview, gizmos estilo Maya, EasyToolbag si está comprado).
