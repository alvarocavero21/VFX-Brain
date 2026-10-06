# Puente Houdini → Unreal
Tags: #unreal #houdini #pipeline #vdb #usd #niagara
Volver: [[00_MOC_Unreal]]

Mi ventaja competitiva: sé hacer FX hero en Houdini. UE pone el entorno, la luz y el render rápido; Houdini pone la destrucción, el pyro y el agua.

## Opciones según el tipo de FX

| FX de Houdini | Cómo llevarlo a UE | Notas |
|---|---|---|
| Pyro / humo / explosión (VDB) | **Heterogeneous Volumes**: importar secuencia OpenVDB como Sparse Volume Texture y renderizar con el actor Heterogeneous Volume | Lo más fiel para cinemática. Pesado en VRAM: reducir resolución/campos (density, temperature, flame). Probar con Path Tracer y Lumen |
| RBD / destrucción | **Alembic (Geometry Cache)** o huesos (Labs RBD to FBX → skeletal mesh) | Alembic = fácil y fiel; huesos = más ligero. Piezas con Nanite si son muchas |
| Destrucción ligera / muchas piezas | **VAT (Vertex Animation Textures)** con SideFX Labs | Muy eficiente, ideal para debris secundario |
| Partículas (chispas, debris fino, polvo) | **Houdini Niagara plugin** (point cache → Niagara) | Combinar con EasyAtmos para el ambiente |
| FLIP / agua | Malla Alembic + material agua en UE, o render del agua en Karma y compo | Shading de agua realista en UE es exigente; evaluar caso a caso |
| Assets procedurales / terreno | **Houdini Engine for Unreal** (HDAs dentro de UE) o export a USD/FBX | Heightfield → mesh Nanite para terrenos hero |
| Escena / layout | **USD** (Solaris → UE, USD Stage / Interchange; asset import production ready en 5.8) | Útil para mantener layout sincronizado con Solaris |

## Reglas de oro
- **Escala**: Houdini metros, UE centímetros (×100). Revisar ejes (Y-up vs Z-up) al exportar.
- **Frame rate**: sim a 24 fps igual que la Sequence.
- **Motion blur**: en VDB/Alembic necesito velocidades (`v`) o subframes; comprobar que MRG genera blur real con temporal samples.
- **Iluminación coherente**: si el FX se renderiza en Karma y el fondo en UE, replicar sol/HDRI/cámara exactos (exportar cámara de UE a Houdini vía USD/FBX).
- Cada problema de importación que cueste >15 min → [[06_Problemas_Resueltos]].

## Alternativa híbrida (muchas veces la mejor para portfolio)
Entorno + cámara en UE → exportar cámara → FX renderizado en Karma XPU → integrar en Nuke. Así el FX mantiene la calidad Karma y el entorno el realismo/rapidez de UE.

## Pendiente (Fase 5 del roadmap)
- [ ] Probar un VDB de pyro (Shot 1 dragón) como Heterogeneous Volume en UE 5.8 y anotar VRAM/tiempos en laptop vs desktop.
- [ ] Probar Alembic del muro del Shot 2 ([[Shot2_Bullet_Wall]]) en UE.
