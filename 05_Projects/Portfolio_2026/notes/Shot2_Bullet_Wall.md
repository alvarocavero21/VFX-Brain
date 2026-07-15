# Shot: Disparo en pared de cemento
## Estado: En progreso — Fase 1 (blocking y fractura base) completada
## Última sesión: 2026-07-16

### Descripción
Fracturing (Voronoi/boolean), RBD de impacto, dust sourcing, debris fino con partículas. Rifle de alta velocidad (~800-900 m/s), impacto **sin perforación completa** (queda ~3cm de hormigón intacto en la cara trasera).

### Decisiones tomadas
- **Arma/velocidad de referencia**: rifle, ~800-900 m/s. Elegido por ser más dramático/vistoso para portfolio que una pistola (~350-450 m/s), y porque da mayor energía transferida a los fragmentos para la Fase 2.
- **Penetración**: NO perfora del todo (cráter + túnel profundo, ~3cm de muro intacto al fondo). Más realista para un muro de carga de 25cm de grosor que la penetración total.
- **Grosor del muro**: 0.25m (rango alto de un muro de carga real de hormigón armado, 20-30cm). Elegido deliberadamente alto para que un rifle no perfore de un solo disparo.
- **Dimensiones del muro**: Box SOP, size `(4, 3, 0.25)`, center `(0, 1.5, 0)`.
- **Punto de impacto**: Null en `(0.35, 1.55, -0.125)` — altura pecho/cabeza, desplazado del centro para encuadre menos estático. Es la única fuente de verdad que alimenta cutter, Voronoi Fracture Points y cámara.
- **Técnica de agujero de bala**: Boolean SOP (Subtract) manual con cutter propio, en vez de RBD Material Fracture SOP con custom cutter (4º input). Elegido por pedagogía — queríamos ver la mecánica nodo a nodo antes de saltar a la herramienta all-in-one. Ver sección "Fuentes consultadas" para el workflow alternativo con RBD Material Fracture SOP, más eficiente en producción una vez dominados los fundamentos.
- **Concentración de fragmentos cerca del impacto**: Voronoi Fracture Points SOP con input de impact point (`Impact Radius` ≈ 0.6m) y densidad por región (Surface > Interior/Exterior), en vez de la técnica manual antigua de pintar un atributo `density` con RBD Paint SOP + Scatter. Es el nodo dedicado que SideFX construyó para este caso exacto.
- **H22**: no se detectaron cambios de parámetros específicos de H22 en Voronoi Fracture SOP / Voronoi Fracture Points SOP / Boolean SOP / RBD Material Fracture SOP frente a versiones anteriores (H19-21). El único punto que SideFX destaca para H22 en esta área es genérico ("faster fracturing, tearing metal with the Bullet solver") y pertenece al Bullet solver (Fase 2), no cambia el grafo de esta fase.

### Setup de nodos — Fase 1
1. `wall_base` (Box SOP) — size `(4, 3, 0.25)`, center `(0, 1.5, 0)`.
2. `impact_point` (Null) — translate `(0.35, 1.55, -0.125)`, sobre la cara frontal del muro.
3. `crater_cone` (Tube SOP) — radio 0.11→0.02, height 0.09, rotado 90° en X, boca en impact_point.
4. `tunnel` (Tube SOP) — radio 0.02→0.015, height 0.13, continúa desde el final del cráter.
5. `bullet_cutter` (Boolean SOP, Union) — une crater_cone + tunnel en un sólido cerrado.
6. `entry_hole` (Boolean SOP, Subtract) — A=wall_base, B=bullet_cutter. "A-B seams" activado en Output Edge Groups (para detalle de borde en Fase 3).
7. `fracture_points` (Voronoi Fracture Points SOP) — input1=entry_hole, input2=impact_point. Impact Radius ≈0.6, Compute Number of Points ON, densidad Surface > Interior/Exterior.
8. `fractured_wall` (Voronoi Fracture SOP) — input1=entry_hole, input2=fracture_points. Cut Plane Offset ≈0.002.
9. `color_by_piece` (Color SOP, opcional) — color aleatorio por atributo `name`, solo QA visual de la distribución de densidad.
10. `cam1` (Camera) — translate ≈`(0.9, 1.6, -3.2)`, look-at impact_point, focal 35-50mm, encuadre con aire alrededor del impacto.

### Problemas resueltos
(ninguno todavía — fase de blocking inicial sin iteración)

### Siguiente paso
**Fase 2 (RBD dinámico)**: importar `fractured_wall` a DOPs (RBD Objects shelf tool o RBD Bullet Solver manual), configurar constraints de glue entre fragmentos, decidir tiempo real vs. cámara lenta (Time Scale del Bullet Solver) usando la referencia de velocidad de bala (~800-900 m/s → el impacto en sí ocurre en <1ms, no se anima; solo se simula la consecuencia). Revisar susteps/iteraciones de constraint según esa decisión.

### Fuentes consultadas
- [SideFX — Fracturing objects for simulation](https://www.sidefx.com/docs/houdini/dyno/fracturing.html) — workflow general de pre-fractura en SOPs.
- [SideFX — Voronoi Fracture SOP](https://www.sidefx.com/docs/houdini/nodes/sop/voronoifracture.html)
- [SideFX — Voronoi Fracture Points SOP](https://www.sidefx.com/docs/houdini/nodes/sop/voronoifracturepoints.html) — nodo usado para concentrar densidad cerca del impacto (Impact Radius, densidad por región).
- [SideFX — RBD Material Fracture SOP](https://www.sidefx.com/docs/houdini/nodes/sop/rbdmaterialfracture.html) — alternativa all-in-one, no usada en esta fase por pedagogía.
- [SideFX — Using custom cutters](https://www.sidefx.com/docs/houdini/destruction/custom.html) — workflow moderno de agujero de impacto coherente vía 4º input de RBD Material Fracture SOP; contrastado con el enfoque manual Boolean+Voronoi usado aquí.
- [SideFX — Boolean SOP](https://www.sidefx.com/docs/houdini/nodes/sop/boolean.html) — modo Subtract, Output Edge Groups (A-B seams).
- [SideFX — Voronoi Fracture Solver (DOP)](https://www.sidefx.com/docs/houdini/nodes/dop/voronoifracturesolver.html) — fractura dinámica en simulación, relevante para Fase 2.
- [SideFX — Debris Source SOP](https://www.sidefx.com/docs/houdini/nodes/sop/debrissource.html) — dust/debris sourcing desde fragmentos RBD, relevante Fase 2-3.
- [SideFX — Dust Pyro Smoke from Destruction Simulation (tutorial oficial)](https://www.sidefx.com/tutorials/dust-pyro-smoke-from-destruction-simulation-using-houdinis-shelf-tool/) — dust sourcing, relevante Fase 2-3.
- [SideFX — What's New in H22](https://www.sidefx.com/products/whats-new-in-h22/) — verificación de cambios específicos de versión (ninguno relevante a nodos de fractura de esta fase).
- Steven Knipping (TD de destrucción, ILM) — ["Boolean or not Boolean: Fun with Fracturing"](https://vimeo.com/228248086), Houdini HIVE SIGGRAPH — técnica clásica manual de Boolean+Voronoi, base del enfoque usado en esta fase.
- od|forum — [Bullet and Voronoi Fracturing](https://forums.odforce.net/topic/11396-bullet-and-voronoi-fracturing/), [Boolean and Voronoi Fracture problem](https://forums.odforce.net/topic/30442-boolean-and-voronoi-fracture-problem/) — revisados para gotchas prácticos, sin hallazgos aplicables directamente a esta fase.
