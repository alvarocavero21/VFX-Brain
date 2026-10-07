# Puente Houdini → Unreal (índice)
Tags: #unreal #houdini #pipeline #vdb #usd #niagara #moc
Volver: [[00_MOC_Unreal]]

Mi ventaja competitiva: sé hacer FX hero en Houdini. UE pone el entorno, la luz y el render rápido; Houdini pone la destrucción, el pyro y el agua.
Guía detallada (investigada y verificada contra Houdini 22.0.429 + UE 5.8.2 el 2026-10-07) en la carpeta `Houdini_a_UE/`:

1. [[HtoUE_00_Setup_Herramientas]] — qué instalar (Houdini Engine **v4.0.1**, SideFX Labs, plugin Interchange OpenVDB), unidades/ejes, reglas comunes
2. [[HtoUE_01_Pyro_VDB_Heterogeneous_Volumes]] — pyro/humo/fuego como volumen en UE: campos, material, actor, CVars cinemáticas, problemas conocidos
3. [[HtoUE_02_RBD_Destruccion]] — Alembic Geometry Cache (recomendado), Chaos Geometry Collection, VAT 3.0, RBD to FBX
4. [[HtoUE_03_Houdini_Engine_FLIP_Particulas_USD]] — HDAs en UE, agua FLIP, partículas → Niagara, USD y cámaras

## Resumen: qué método por tipo de FX
| FX de Houdini | Método principal | Alternativa |
|---|---|---|
| Pyro / humo / explosión | VDB → **Heterogeneous Volume** (experimental) | Render en **Karma** + compo Nuke |
| RBD / destrucción (cinemática) | **Alembic → Geometry Cache** con motion vectors | VAT rigid / RBD to FBX |
| Destrucción en tiempo real | Fractura Houdini → **Chaos Geometry Collection** (vía HDA) | Fractura de UE |
| Debris / chispas / ceniza | Puntos → **Niagara** o VAT Particle Sprites | Niagara puro en UE |
| FLIP / agua hero | Malla **Alembic** + material de agua | **Karma + compo** (mejor calidad) |
| Herramientas / terreno procedural | **Houdini Engine** (HDA) → bake | Export FBX/USD |
| Layout de escena / cámaras | **USD** / FBX de cámara | — |

## Reglas de oro
- **Escala y ejes**: Houdini m + Y-up → UE cm + Z-up. Test con cubo de 1 m antes de exportar nada gordo.
- **24 fps** en Houdini y en Sequencer.
- **Motion blur**: Alembic con `v` → motion vectors en el import; volúmenes: comprobar si interpolan en sub-frames (pendiente).
- **Iluminación coherente** si mezclo Karma y UE: mismo sol, misma cámara exportada.
- Atasco >15 min → [[06_Problemas_Resueltos]].

## Alternativa híbrida (muchas veces la mejor para portfolio)
Entorno + cámara en UE → exportar cámara → FX en Karma XPU con holdouts → integrar en Nuke. El FX conserva la calidad de Karma y el entorno la rapidez de UE.

## Pruebas pendientes (Fase 5 del roadmap)
- [ ] Instalar Houdini Engine v4.0.1 + SideFX Labs y comprobar la licencia de Engine.
- [ ] VDB de pyro de prueba → UE 5.8: confirmar escala/ejes, si `vel` sigue crasheando y si hay motion blur entre frames. Anotar VRAM/tiempos laptop vs desktop.
- [ ] Alembic del muro del Shot 2 ([[Shot2_Bullet_Wall]]) como Geometry Cache con motion vectors.
