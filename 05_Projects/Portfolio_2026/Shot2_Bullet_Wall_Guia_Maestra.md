# Shot 2 — Disparo en pared de cemento
## Guía maestra paso a paso

Documento de referencia para seguir el shot en Houdini 22 y consultar dudas. Cada fase indica qué está hecho, qué falta, y el porqué de las decisiones clave — para que puedas retomarlo en cualquier momento sin perder el hilo.

---

## Estado general

| Fase | Estado |
|---|---|
| 1. Blocking y fractura base | ✅ Completa |
| 2. RBD dinámico | ✅ Completa |
| 3. Dust sourcing + debris fino | ✅ Completa |
| 4. Chipping estático de bordes | ✅ Completa |
| 5. Shading hormigón + render Karma XPU | ✅ Completa |
| 6. Shading del volumen de polvo (Pyro density/color) | ⏭️ Pendiente |

---

## Fase 1 — Blocking y fractura base

**Objetivo**: geometría del muro, punto de impacto, y fractura Voronoi concentrada cerca del disparo.

### Grafo de nodos
```
Box (muro 4×3×0.25m)
  → Cutter (cráter + túnel de entrada, sin perforar completamente)
  → Boolean Subtract
  → Voronoi Fracture Points (densidad concentrada en impact_point)
  → Voronoi Fracture (fragmentación final)
```

### Decisiones clave
- **Muro**: 4m × 3m × 0.25m — proporción realista de un muro de carga.
- **Punto de impacto**: definido como punto de referencia (`impact_point`) reutilizado en todas las fases siguientes.
- **Cráter + túnel sin perforar**: el muro es grueso, la bala no lo atraviesa — decisión artística coherente con "muro que aguanta".
- **Densidad de fractura no uniforme**: piezas pequeñas cerca del impacto, grandes hacia los bordes — evita el error típico de fractura uniforme que se ve "de kit".
- **Cámara**: posicionada con referencia a la velocidad de bala real, preparando el timing de la Fase 2.

---

## Fase 2 — RBD dinámico

**Objetivo**: que la fractura se propague de forma físicamente creíble desde el punto de impacto, no toda a la vez.

### Grafo de nodos
```
fractured_wall (de Fase 1)
  → piece_centroid (Attribute Promote SOP)
  → impact_kinematics (Attribute Wrangle, over Points)
  → connect_adjacent_pieces (Connect Adjacent Pieces SOP)
  → constraint_strength (Attribute Wrangle, sobre primitivas)
  → rbd_bullet_solver (RBD Bullet Solver SOP)
```

### 0. Anclaje del muro
`piece_centroid`: promedia `P` por pieza (`name`) → `centroid`. Necesario para que cada pieza tenga una velocidad rígida coherente en vez de una por punto.

### 1. Cinemática de impacto (`impact_kinematics`, VEX)
```vex
float dist = distance(@centroid, @impact_point);
float impact_radius = 0.6;
float active_radius = 0.8;
float t = clamp(dist / impact_radius, 0, 1);

vector bulletdir = {0,0,1};
vector toward = normalize(@centroid - impact_pos);
vector radial = normalize(toward - bulletdir * dot(toward, bulletdir));
vector dir = normalize(lerp(-bulletdir, radial, fit(t, 0, 1, 0.15, 0.85)));

f@speed = fit(t, 0, 1, 60, 4);   // m/s
v@v = dir * @speed;
i@active = (dist < active_radius) ? 1 : 0;
```
- Rango de velocidad (0–118 m/s) basado en estudio de eyección en hormigón (UHPFRC penetration study).
- Ángulo de cono de eyección 25-50° (pico ~30°) según estudio de Ejecta Cone Angle.
- `active`: piezas dentro de 0.8m son dinámicas; el resto queda kinemático (ancla fija).

### 2. Constraints (glue)
`connect_adjacent_pieces`: Connection Type = Adjacent Pieces from Surface Points, Search Radius ≈ 1.5-2× tamaño medio de pieza, Max Connections ≈ 6.

`constraint_strength` (VEX sobre primitivas):
```vex
s@constraint_name = "Glue";
float t_avg = avg(point(0,"t",@primnum,0), point(0,"t",@primnum,1));
f@strength = (t_avg > 1.3) ? -1 : fit(t_avg, 0, 1, 50, 8000);
```
Cerca del impacto el glue rompe con poca fuerza; en el anillo ancla (t>1.3) nunca rompe.

### 3. Parámetros del RBD Bullet Solver

| Parámetro | Valor | Por qué |
|---|---|---|
| Time Scale | 1.0 | Física real; cámara lenta se hace en compo, no aquí |
| Bullet Substeps | 4-6 | Bullet detecta colisión antes que el glue rompe; reduce rebote falso, necesario para piezas rápidas |
| Constraint Iterations | 6-10 | Red de constraints más estable ante impulso fuerte |
| Density | 2400 kg/m³ | Densidad real del hormigón |
| Bounce | 0.1 | Hormigón absorbe energía, no rebota |
| Friction | 0.7 | Piezas grandes se frenan y asientan — se leen "pesadas" |
| Rotational Stiffness | 0.3 | Evita giros exagerados por roce lateral (confirmado con 2 fuentes oficiales) |
| Collision Shape | Convex Hull | Piezas angulares Voronoi encajan/apilan de forma creíble |
| Scale [Strength] by Attribute | strength | Activa el atributo de `constraint_strength` |
| Propagation Rate | 0.35 | Ni fractura puramente local ni instantánea a toda la red — 2-3 anillos por step |
| Propagation Iterations | 2-3 | Limita saltos del impulso por step, mantiene timing escalonado |
| Half-Life | 0.15s | El impulso decae; evita que siga rompiendo cosas mucho después del impacto |

**Resultado emergente**: las piezas centrales se mueven desde el frame 1 (velocidad inicial alta). Las del siguiente anillo solo se mueven cuando el impulso propagado + contacto físico supera su `strength` — el delay sale de la física, no de keyframes manuales.

---

## Fase 3 — Dust sourcing y debris fino

**Objetivo**: polvo con volumen real (no partículas sueltas) y esquirlas finas coherentes con el cono de eyección ya definido.

- **Fuente del polvo**: POP/Pyro Source desde piezas RBD activas (`@active`, `@v` de Fase 2 como driver de emisión).
- **Debris fino**: sistema de partículas separado del RBD grueso — velocidad y spread heredan el cono de 25-50° ya usado en Fase 2.
- **Timing**: el polvo no aparece instantáneo y limpio — tiene masa, se expande con delay respecto al impacto.

---

## Fase 4 — Chipping estático de bordes

Geometría de esquirlas finas añadida sobre los bordes de fractura de las piezas RBD activas — detalle estático (no sim), aplicado sobre el resultado final de fases 2/3. Evita que los bordes de fractura se vean "limpios" o recién cortados.

---

## Fase 5 — Shading y render (hormigón)

- **MaterialX** para el hormigón: base color, roughness, displacement.
- **Render**: Karma XPU.
- Pendiente explícito: esta fase cubrió solo el hormigón, no el shading del volumen de polvo.

---

## Fase 6 — Shading del volumen de polvo (pendiente)

Por hacer: shading de densidad y color del Pyro del polvo generado en Fase 3 — distinto del shading de superficie, necesita su propia sesión de look dev de volumen.

---

## Cómo usar este documento

1. Antes de cada sesión con Claude Code, dile en qué fase estás y qué duda tienes concreta.
2. Si algo de Houdini no se comporta como aquí se describe, dilo explícitamente — puede haber diferencia de versión o un parámetro mal nombrado (ya pasó una vez con "Rotational Stiffness", se verificó y era correcto).
3. Cuando cierres la Fase 6, este documento pasa a ser el making-of técnico completo, reutilizable para la sección de portfolio o LinkedIn.

## Fuentes técnicas consultadas
- Attribute Promote SOP — docs SideFX
- Connect Adjacent Pieces SOP — docs SideFX
- RBD Constraint Properties — docs SideFX
- Glue Constraint Relationship — docs SideFX
- Bullet Solver and Glue — foro SideFX (od|forum)
- Penetration and perforation of UHPFRC — ScienceDirect
- Ejecta Cone Angle study — ScienceDirect
