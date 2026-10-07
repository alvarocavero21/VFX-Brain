# Houdini → UE 5.8 · 03 · Houdini Engine, FLIP, partículas y USD
Tags: #unreal #houdini #houdini-engine #hda #flip #niagara #usd
Volver: [[Puente_Houdini_Unreal]] · Setup: [[HtoUE_00_Setup_Herramientas]]

## Houdini Engine for Unreal (HDAs dentro de UE)
- **Versión para mí: v4.0.1** (Houdini 22.0.429 / HAPI 9.0, UE 5.8 Windows). v4.0.1 añade API `GetHoudiniAssetInfo()`, exportación de atributos de splines, tags por actor, propiedades de material y botón de reset de parámetros en grafos **PCG**.
- Qué permite: cargar un `.hda` en UE, cambiar sus parámetros en el Details panel y que Houdini (en segundo plano, vía licencia Engine) recalcule y devuelva la geometría como Static Mesh/Instancias/Landscape/Geometry Collection.
- Usos que me interesan:
  - **Herramientas de entorno**: generador de rocas/escombros, cables, vallas sobre spline, scatter con reglas propias.
  - **Terreno**: Heightfield de Houdini → Landscape de UE (o malla Nanite).
  - **Fractura**: HDA que fractura y entrega Geometry Collection ([[HtoUE_02_RBD_Destruccion]]).
  - Integración con **PCG** (HE 4.x tiene soporte en grafos PCG).
- Flujo: el HDA es "procedural en editor" → al final **bake** a assets normales de UE (Static Mesh) para no depender de Houdini al renderizar ni al abrir el proyecto en otra máquina.
- No sirve para simulaciones pesadas en vivo: las sims se cachean en Houdini y se exportan (VDB/Alembic/VAT).

## FLIP / agua
| Opción | Cómo | Notas |
|---|---|---|
| **Malla Alembic** (Geometry Cache) | Particle Fluid Surface → mesh → Alembic con `v` | Lo más fiel. Material de agua en UE (Substrate: refracción, absorción por profundidad). Motion vectors en import |
| **VAT 3.0 Fluid mode** | Labs VAT → mesh con topología variable en textura | Ligero; resolución limitada |
| **Espuma/spray/burbujas** | Puntos → Niagara (Houdini Niagara / point cache) o VAT Particle Sprites | Secundarios con look de partícula |
| **Render en Karma + compo** | Cámara UE → Houdini, render del agua en Karma, integrar en Nuke | Mejor calidad de agua, más trabajo de integración |
- El shading de agua realista en UE es difícil (refracción en translucidez, cáusticas) → para un hero de agua tipo [[Simulacion_Cascada_FLIP_Universidad]], considerar **Karma + compo** como opción principal.

## Partículas → Niagara
- Exportar puntos con atributos (`P`, `v`, `pscale`, `Cd`, `age`, `id`) → leerlos en Niagara (Houdini Niagara data interface / point cache) para chispas, debris fino, ceniza.
- Alternativa sin plugin: **VAT 3.0 Particle Sprites** o Alembic de puntos.
- Ventaja: los secundarios se iluminan y colisionan en la escena de UE.

## USD (Solaris ↔ UE)
- UE 5.8: importación USD vía Interchange **production ready para assets**; importación de nivel completo aún experimental.
- Útil para: llevar **layout/set dressing de Solaris** a UE o viceversa, **cámaras**, y mantener una sola fuente de verdad de la escena.
- Houdini 22 mejoró mucho layout/worldbuilding en Solaris ([[Version_Reference]]) → combinar con USD Stage en UE.
- Precaución: materiales MaterialX/Karma no se traducen 1:1 a UE → rehacer materiales en UE.

## Cámaras
- UE → Houdini: exportar CineCamera como FBX o USD (focal, filmback, foco) → simular "a cámara".
- Houdini → UE: FBX de cámara (ya lo tengo hecho en el proyecto `Landing`: `Camera_Landing.fbx`). Revisar que la focal y el sensor coinciden (sensor de UE en mm).

## Fuentes
- [Houdini Engine for Unreal — Releases](https://github.com/sideeffects/HoudiniEngineForUnreal/releases) · [Intro HE for Unreal](https://www.sidefx.com/docs/houdini/unreal/intro.html)
- [Labs VAT 3.0 FAQs](https://www.sidefx.com/forum/post/353541) · [UE 5.8 Release Notes (USD/Interchange)](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes)
