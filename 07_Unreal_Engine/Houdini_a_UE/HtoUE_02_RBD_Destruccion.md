# Houdini → UE 5.8 · 02 · RBD / destrucción
Tags: #unreal #houdini #rbd #destruccion #alembic #chaos #vat
Volver: [[Puente_Houdini_Unreal]] · Setup: [[HtoUE_00_Setup_Herramientas]] · Relacionado: [[Shot2_Bullet_Wall]]

## Elegir método
| Método | Qué llega a UE | Pros | Contras | Uso ideal |
|---|---|---|---|---|
| **Alembic → Geometry Cache** | La sim tal cual, frame a frame | Fidelidad total, fácil, **motion vectors** | Ficheros grandes, no interactivo | ⭐ **Cinemática / portfolio** |
| **RBD to FBX (Labs) → Skeletal Mesh** | 1 hueso por pieza + animación | Ligero, se puede mezclar con Nanite (5.x) | Pierde deformación, setup Labs | Muchas piezas, rendimiento |
| **VAT 3.0 (Labs) Rigid mode** | Mesh + texturas de posición/rotación | Ligerísimo en GPU, miles de piezas | Precisión limitada por textura, más técnico | Debris secundario, repeticiones |
| **Fracturar en Houdini → Chaos Geometry Collection** | Piezas + clusters; **simula Chaos en UE** | Interactivo, tiempo real | La sim no es la de Houdini | Juego / destrucción en tiempo real |

Para mis shots (cinemática con cámara fija y look de Houdini) → **Alembic Geometry Cache**. Chaos solo si quiero aprender destrucción real-time.

## A. Alembic → Geometry Cache (recomendado)
### Houdini
1. Sim RBD (packed) → **Transform Pieces** / unpack → geometría final con `N`, `uv`, materiales por `shop_materialpath` o atributo de nombre.
2. Atributo `path` por pieza o grupo (`/wall/piece_*`) — o **un solo path** si quiero un único track (más ligero).
3. Mantener `v` (velocidad por punto) si quiero motion vectors desde Houdini.
4. ROP Alembic: rango de frames, **24 fps**, sin subframes (el motion blur lo hará MRG con temporal samples + motion vectors).
5. Interior de las piezas: material distinto (grupo `inside`) → en UE un material de cemento roto/chipping (ver [[Shot2_Bullet_Wall_Guia_Maestra]]).

### UE 5.8 — opciones del importador (verificadas en `AbcImportSettings.h`)
| Opción | Valor recomendado | Por qué |
|---|---|---|
| Import Type | **Geometry Cache** | (Static Mesh = solo frame 1; Skeletal = morph targets, no para RBD) |
| Conversion preset | Custom: Scale (100,100,100) si llega en metros, revisar Rotation | ejes/escala |
| **Motion Vectors** | **Import Abc Velocities As Motion Vectors** (si exporté `v`) o **Calculate Motion Vectors During Import** | motion blur correcto en TSR/MRG |
| Flatten Tracks | ON si no necesito piezas separadas | menos pistas, más rápido |
| Apply Constant Topology Optimizations | ON en RBD (topología constante) | menos memoria |
| Sampling | Per Frame, Frame Start/End | igual que Houdini |
| Recompute Normals | OFF si exporto `N` buenos | respetar normales de Houdini |
| Create/Find Materials | según el caso | asignar materiales por nombre |

Reproducción: arrastrar el Geometry Cache al nivel y añadirlo a **Sequencer** (pista de Geometry Cache) para que se sincronice con la cámara y el render.

## B. Chaos Geometry Collection (destrucción en tiempo real)
- Fracturar en Houdini (Voronoi/RBD Material Fracture) tiene más control que la fractura de UE; las piezas y clusters se convierten a **Geometry Collection**.
- Vía robusta: **HDA con Houdini Engine** que genera la Geometry Collection (soportado desde HE 3.0.7: "Geometry Collection property support").
- FBX "a pelo" no se reconoce como destructible: hay que convertir a Geometry Collection en UE (Fracture Mode).
- Secundarios: **ChaosNiagara** (Beta) lee los eventos de rotura → polvo/debris en Niagara ([[Niagara_Fundamentos_y_Cinematica]]).

## C. VAT 3.0 (SideFX Labs) — Rigid Body mode
- ROP *Labs Vertex Animation Textures* → modo **Rigid-Body Dynamics** → exporta mesh + texturas (posición, rotación) + material de UE incluido en Labs.
- Ideal para **debris secundario** o muchas copias. Precisión de textura limitada: cuidado con escenas muy grandes (usar HDR/16-bit).
- También tiene modos Soft-Body (tela, metal, vegetación), Fluid y Particle Sprites.

## D. RBD to FBX (Labs) → huesos
- Una pieza = un hueso; se importa como Skeletal Mesh + animación. Ligero; buena alternativa a Alembic si el Geometry Cache pesa demasiado.

## Checklist antes de exportar destrucción
- [ ] Escala real (muro de 3 m = 300 uu) y frame rate 24
- [ ] Interior con material/UVs propios
- [ ] Secundarios planificados (polvo VDB [[HtoUE_01_Pyro_VDB_Heterogeneous_Volumes]] o Niagara, debris VAT)
- [ ] Motion vectors activados en import
- [ ] Probado con 10 frames antes del cache completo

## Fuentes
- [Labs VAT 3.0 FAQs and Links (SideFX)](https://www.sidefx.com/forum/post/353541) · [VAT 3.0 Part 1](https://sidefxlabs.artstation.com/projects/zOyke6) · [VAT 3.0 Part 2: Soft-Body](https://sidefxlabs.artstation.com/projects/5XJZV8)
- [Realtime destruction techniques (SideFX)](https://www.sidefx.com/tutorials/realtime-destruction-techniques/)
- [RBD mesh in Niagara (foro SideFX)](https://sidefx.com/forum/topic/73733) · [Houdini real-time destruction to UE5 (RealtimeVFX)](https://realtimevfx.com/t/houdini-real-time-destruction-to-unreal-5/24618) · [WIP realtime VDBs and destruction in UE5](https://realtimevfx.com/t/wip-realtime-vdbs-and-destruction-in-unreal-engine-5/29696)
- [Houdini Engine for Unreal releases](https://github.com/sideeffects/HoudiniEngineForUnreal/releases)
