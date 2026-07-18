# Shot 2 — Tutorial paso a paso

Guía de ejecución nodo por nodo para reconstruir el grafo del Shot 2 (disparo en pared de cemento) en Houdini 22. Este documento es el **CÓMO**: nombres exactos de nodo, dónde colocarlo, qué parámetro tocar y con qué valor, código VEX completo, y qué debe verse en el viewport en cada paso. El **PORQUÉ** de cada decisión vive en `Shot2_Bullet_Wall_Guia_Maestra.md` — aquí solo se referencia en una línea cuando aporta claridad.

Convención: cada dato verificado contra la documentación oficial de SideFX lleva la nota *(verificado: URL)*. Cuando no se pudo confirmar con una fuente fiable, aparece explícitamente: **⚠️ No verificado — confirmar en Houdini al llegar a este paso.**

---

## FASE 1 — Blocking y fractura base

Contexto de red: todo dentro de un Geometry object, p.ej. `/obj/geo1`. Grafo: `wall_base → (crater_cone + tunnel → bullet_cutter) → entry_hole → fracture_points + fractured_wall`.

### Nodo: wall_base

1. **Nombre exacto en Tab menu**: `Box` (SOP).
2. **Dónde colocarlo**: primer nodo de la cadena, dentro de `/obj/geo1`. Sin inputs.
3. **Pestaña/parámetro/valor**: pestaña *Transform* → `Size` = `(4, 3, 0.25)`; `Center` = `(0, 1.5, 0)`.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: una caja rectangular vertical, 4m de ancho × 3m de alto × 0.25m de grosor, con su base inferior a Y=1.375 (porque el center está en Y=1.5 con altura 3, así que va de Y=0 a Y=3). Debe leer como un muro de carga visto de frente.

### Nodo: impact_point

1. **Nombre exacto en Tab menu**: `Null`.
2. **Dónde colocarlo**: nodo independiente en `/obj/geo1`, no necesita input geométrico (se posiciona a mano). Se referencia como input 2 en `fracture_points` más adelante.
3. **Pestaña/parámetro/valor**: pestaña *Transform* → `Translate` = `(0.35, 1.55, -0.125)`. Nota: Z=-0.125 corresponde a la cara frontal del muro (el muro tiene grosor 0.25 en Z centrado en Z=0, así que la cara -Z está exactamente en Z=-0.125).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: un icono de Null (ejes) apoyado justo sobre la cara frontal del muro, ligeramente a la derecha y por debajo del centro vertical.

### Nodo: crater_cone

1. **Nombre exacto en Tab menu**: `Tube`.
2. **Dónde colocarlo**: nodo independiente en `/obj/geo1`, sin input (geometría procedural). Alimenta el input 1 de `bullet_cutter`.
3. **Pestaña/parámetro/valor**: pestaña *Transform* → `Radius` (base) = `0.11`, `Radius` (top) = `0.02` (el Tube SOP tiene dos campos de radio, base y top); `Height` = `0.09`. Rotar 90° en X (pestaña *Transform* → `Rotate` = `(90, 0, 0)`) para que el eje del cono quede perpendicular a la cara del muro. Trasladarlo para que la boca ancha (radio 0.11) coincida con `impact_point`.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: un cono corto y ancho, como un embudo, con la boca grande apoyada en la cara frontal del muro sobre `impact_point` y el vértice metiéndose hacia el interior del muro.

### Nodo: tunnel

1. **Nombre exacto en Tab menu**: `Tube`.
2. **Dónde colocarlo**: segundo nodo independiente en `/obj/geo1`, sin input. Alimenta el input 2 de `bullet_cutter`.
3. **Pestaña/parámetro/valor**: pestaña *Transform* → `Radius` (base) = `0.02`, `Radius` (top) = `0.015`; `Height` = `0.13`. Posicionar/rotar para que continúe exactamente desde el vértice de `crater_cone` (mismo eje, mismo ángulo, arrancando donde termina el cono).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: un cilindro delgado y largo que se hunde más profundo en el muro, como la continuación del túnel de bala tras el cráter cónico.

### Nodo: bullet_cutter

1. **Nombre exacto en Tab menu**: `Boolean`. *(verificado: sidefx.com/docs/houdini/nodes/sop/boolean.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Input 1 (`Set A`) = `crater_cone`; Input 2 (`Set B`) = `tunnel`.
3. **Pestaña/parámetro/valor**: pestaña *Boolean* → `Operation` = `Union`. Los valores exactos del dropdown de `Operation` son `Union`, `Intersect`, `Subtract`, `Shatter`, `Seam`, `Custom`, `Detect`, `Resolve` *(verificado: sidefx.com/docs/houdini/nodes/sop/boolean.html)*.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: un único sólido cerrado que combina el cono ancho y el cilindro delgado en una sola forma continua tipo "bala fantasma" — sin costuras abiertas ni geometría duplicada.

### Nodo: entry_hole

1. **Nombre exacto en Tab menu**: `Boolean`.
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Input 1 (`Set A`) = `wall_base`; Input 2 (`Set B`) = `bullet_cutter`.
3. **Pestaña/parámetro/valor**: pestaña *Boolean* → `Operation` = `Subtract`. Si quieres además marcar la costura de corte como grupo (no imprescindible para el resto del grafo, es solo para QA visual), en la pestaña *Output* activa el checkbox `A-B seams` dentro de la sección **Output Edge Groups** *(verificado: sidefx.com/docs/houdini/nodes/sop/boolean.html — la sección se llama literalmente "Output Edge Groups" y el checkbox correspondiente a la intersección A∩B es "A-B seams")*.
   **Aclaración importante para no confundir**: el grupo `A-B seams` de este Boolean es solo el borde de corte del hueco de bala — **no tiene nada que ver** con el grupo `interior` que se usa en Fases 3 y 4. Ese grupo `interior` se genera después, en el nodo `fractured_wall` (Voronoi Fracture SOP, parámetro `Interior Group`, ver más abajo). Son dos grupos completamente distintos con propósitos distintos.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: el muro completo con un hueco tipo cráter+túnel excavado en la cara frontal, siguiendo la forma de `bullet_cutter`. El muro sigue siendo una sola pieza sólida, todavía sin fracturar.

### Nodo: fracture_points

1. **Nombre exacto en Tab menu**: `Voronoi Fracture Points`. *(verificado: sidefx.com/docs/houdini/nodes/sop/voronoifracturepoints.html — no existe ambigüedad de versión "2.0" para este SOP en la documentación consultada)*.
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Este nodo tiene **3 inputs** *(verificado en la doc oficial)*: Input 1 = *Geometry for Impact* (geometría alrededor de la cual generar puntos de fractura) → conectar `entry_hole`; Input 2 = *Impact Points and Metaballs* (puntos que representan "impactos") → conectar `impact_point`; Input 3 = *Optional SDF For Depth Sampling* (opcional, no se usa en este shot).
3. **Pestaña/parámetro/valor**:
   - No existe un parámetro literal llamado "Impact Point" — la posición de impacto se define puramente por la posición del punto conectado en el Input 2 *(verificado: sidefx.com/docs/houdini/nodes/sop/voronoifracturepoints.html)*. Es decir, `impact_point` (el Null) hace ese trabajo simplemente por estar conectado ahí.
   - `Impact Radius` ≈ `0.6` *(nombre de parámetro verificado; el valor 0.6 es el ya decidido en la guía maestra, coherente con `impact_radius` usado en Fase 2)*.
   - `Compute Number of Points` = ON *(verificado, nombre exacto)*.
   - Densidad por región: el nodo organiza los controles de densidad en tres bloques — **Surface**, **Interior**, **Exterior** — cada uno con su propio parámetro `Point Density` *(verificado: sidefx.com/docs/houdini/nodes/sop/voronoifracturepoints.html)*. Para lograr piezas pequeñas cerca del impacto y grandes hacia los bordes: sube `Point Density` en el bloque **Surface** (que es la región alrededor del punto de impacto/superficie de contacto) y baja `Point Density` en **Interior**/**Exterior** (a ojo, ajustar viendo el resultado — el material fuente no da valores numéricos exactos para este reparto, solo la intención de densidad no uniforme).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: una nube de puntos dispersos sobre y alrededor del hueco de bala — puntos muy juntos cerca de `impact_point` y cada vez más espaciados hacia los bordes del muro. Actívese `Visualize Points` para verlos coloreados por región (Surface/Interior/Exterior) si hace falta depurar.

### Nodo: fractured_wall

1. **Nombre exacto en Tab menu**: `Voronoi Fracture`. *(verificado: sidefx.com/docs/houdini/nodes/sop/voronoifracture.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Este nodo tiene **2 inputs** *(verificado)*: Input 1 = *Geometry to Fracture* → conectar `entry_hole`; Input 2 = *Points for Voronoi Cells* → conectar `fracture_points`.
3. **Pestaña/parámetro/valor**:
   - Sección **Cut** → `Cut Plane Offset` ≈ `0.002` *(nombre de parámetro verificado: "Offsets the cut plane between adjacent cell points before cutting", sidefx.com/docs/houdini/nodes/sop/voronoifracture.html)*.
   - Sección **Output Attributes** → `Interior Group` = deja el nombre por defecto o escribe `interior` explícitamente *(verificado: el parámetro se llama literalmente "Interior Group" y vive en la sección "Output Attributes")*. Este es el grupo real de caras interiores que se reutiliza en Fase 3 (`debris_source`) y Fase 4 (`rbd_interior_detail`, `chip_scatter`).
   - Sección **Pieces** → deja `Name Attribute` por defecto (crea el atributo `name` por pieza, usado en todo el resto del pipeline).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: el muro fracturado en múltiples piezas irregulares tipo Voronoi — piezas pequeñas y numerosas alrededor del hueco de bala, piezas grandes y pocas hacia los bordes del muro. Las piezas siguen encajadas en su posición original (todavía sin simular), como un rompecabezas 3D.

### Nodo: color_by_piece (opcional, solo QA)

1. **Nombre exacto en Tab menu**: `Color`.
2. **Dónde colocarlo**: dentro de `/obj/geo1`, después de `fractured_wall`. No forma parte del grafo de producción, solo para verificar visualmente la fractura.
3. **Pestaña/parámetro/valor**: pestaña *Color* → `Class` = `Primitive`, `Color Type` = algo tipo "Random from Attribute" apuntando a `name` (ajustar a ojo según la versión del Color SOP en pantalla — este nodo es puramente de inspección, no crítico).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: cada pieza de la fractura con un color aleatorio distinto — confirma visualmente que el atributo `name` está bien segmentado y que no hay piezas fusionadas por error.

### Nodo: cam1

1. **Nombre exacto en Tab menu**: `Camera` (se crea normalmente desde el menú *Object* del Tab menu, no dentro de `/obj/geo1` sino como hijo de `/obj`).
2. **Dónde colocarlo**: `/obj/cam1`, nodo de cámara independiente.
3. **Pestaña/parámetro/valor**: pestaña *Transform* → `Translate` ≈ `(0.9, 1.6, -3.2)`; orientar (look-at) hacia `impact_point`; pestaña *Projection* → `Focal Length` entre `35` y `50` mm (a ojo, ajustar en iteración según encuadre).
4. **VEX**: no aplica.
5. **Qué ver en el viewport de la cámara**: el muro fracturado encuadrado con el hueco de bala como punto focal, ligeramente descentrado en composición, con perspectiva creíble para un plano medio de impacto.

### Checkpoint de la Fase 1

Al completar la fase deberías ver en el viewport: un muro de hormigón (4×3×0.25m) con un hueco de entrada de bala en la cara frontal, fracturado en piezas Voronoi de densidad no uniforme — muchas piezas pequeñas concentradas alrededor del punto de impacto, pocas piezas grandes hacia los bordes del muro. Todas las piezas siguen en su posición de reposo (nada se ha movido todavía), encajadas como un rompecabezas. Con `color_by_piece` activado cada pieza tiene un color distinto y no hay fusiones erróneas entre piezas adyacentes. La cámara `cam1` encuadra el impacto desde un ángulo de plano medio.

---

## FASE 2 — RBD dinámico

Contexto de red: sigue dentro de `/obj/geo1`, encadenado después de `fractured_wall`.

### Nodo: piece_centroid

1. **Nombre exacto en Tab menu**: `Attribute Promote`. *(verificado: sidefx.com/docs/houdini/nodes/sop/attribpromote.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `fractured_wall`.
3. **Pestaña/parámetro/valor** *(todos los nombres verificados contra sidefx.com/docs/houdini/nodes/sop/attribpromote.html)*:
   - `Original Class` = `Point`.
   - `New Class` = `Point`.
   - `Piece Attribute` = ON, valor `name` (este toggle existe literalmente con ese nombre y sirve para indicar el atributo de partición por pieza).
   - `Original Name` = `P`.
   - Activar `Change New Name` = ON, y `New Name` = `centroid`.
   - `Promotion Method` = `Average` (el parámetro se llama literalmente "Promotion Method", no solo "Method" — ojo al buscarlo en la interfaz).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: geométricamente nada cambia respecto a `fractured_wall` (misma forma, mismas piezas). El cambio es solo de atributos: cada punto de cada pieza ahora carga un atributo vectorial `centroid` idéntico dentro de la misma pieza (posición promedio de esa pieza). Verificable en el spreadsheet de geometría, no a simple vista.

### Nodo: impact_kinematics

**Antes de pegar el código**: el material fuente original de este wrangle tiene una inconsistencia real — usa `@impact_point` en la línea de `dist` y `impact_pos` (sin `@`, sin declarar) en la línea de `toward`. Estas dos referencias deberían apuntar a la MISMA posición: la del Null `impact_point` creado en la Fase 1. Houdini no va a compilar el VEX tal cual porque `impact_pos` no existe como variable. La forma más simple y estándar de traer la posición de un Null externo a un Attribute Wrangle es conectando ese Null como **segundo input** del wrangle y leyendo su posición con `point(1, "P", 0, 0)` (input 1 en notación 0-indexed de VEX = segundo input del nodo). Con eso, el código queda funcional sustituyendo ambas referencias por una única variable local `impact_pos` calculada al principio del snippet. Este es el fix aplicado abajo — está señalado explícitamente, no es el código original sin tocar.

1. **Nombre exacto en Tab menu**: `Attribute Wrangle`.
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Input 1 = `piece_centroid`. Input 2 = `impact_point` (el Null de la Fase 1) — **hay que conectar este segundo input**, si no, `point(1, "P", 0, 0)` no tiene de dónde leer.
3. **Pestaña/parámetro/valor**: pestaña *Wrangle* → `Run Over` = `Points`.
4. **Código VEX** (versión corregida, con el fix de `impact_pos` aplicado y explicado arriba; pega esto, no el snippet roto):
```vex
vector impact_pos = point(1, "P", 0, 0);

float dist = distance(@centroid, impact_pos);
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
f@t = t;   // fix necesario: exportar t como atributo de punto para que constraint_strength pueda leerlo (ver más abajo)
```
   Nota sobre la última línea (`f@t = t;`): en el material fuente original, `t` se calcula como variable local (`float t = ...`) y nunca se exporta como atributo. El wrangle de más abajo (`constraint_strength`) necesita leer `t` con `point(0,"t",@primnum,0)`, lo cual solo funciona si `t` existe como atributo de punto float en la geometría de salida de este nodo. Por eso se añade `f@t = t;` al final — es un fix, no estaba en el snippet original tal cual.
5. **Qué ver en el viewport**: sin cambio de forma geométrica todavía (esto solo asigna atributos, no mueve nada — el movimiento lo aplica el solver más adelante). Para verificar que funcionó, revisa en el spreadsheet que las piezas cercanas a `impact_point` tengan `speed` alto (~60) y las piezas lejanas `speed` bajo (~4), y que `active` sea 1 dentro de un radio de 0.8m alrededor del impacto y 0 fuera de ese radio.

### Nodo: connect_adjacent_pieces

1. **Nombre exacto en Tab menu**: `Connect Adjacent Pieces`. *(verificado: sidefx.com/docs/houdini/nodes/sop/connectadjacentpieces.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `impact_kinematics`.
3. **Pestaña/parámetro/valor** *(nombres verificados en la doc oficial)*:
   - `Connection Type` = `Adjacent Pieces from Surface Points` (el dropdown tiene exactamente tres opciones: `Adjacent Pieces from Points`, `Adjacent Pieces from Surface Points`, `Adjacent Points` — la elegida es la segunda).
   - `Search Radius` ≈ 1.5–2× el tamaño medio de pieza — **valor a ojo, ajustar viendo el resultado en viewport**, el material fuente no da un número fijo.
   - `Max Connections` ≈ `6`.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: activa el modo *Guide* / visualización de constraints del nodo para ver líneas conectando los centroides de piezas vecinas — debería verse una especie de red/malla de líneas cubriendo todo el muro, más densa cerca del impacto (piezas pequeñas y numerosas) y más dispersa hacia los bordes (piezas grandes).

### Nodo: constraint_strength

**Nota de verificación importante sobre el atributo `constraint_name`**: la documentación conceptual oficial de constraints RBD *(verificado: sidefx.com/docs/houdini/destruction/constraints.html)* indica que el atributo de primitiva que define el tipo de constraint se llama literalmente `constraint_type` (no `constraint_name`), y que los valores estándar son minúsculas: `glue` y `soft` (no `Glue`). El material fuente de esta sesión usa `s@constraint_name = "Glue";`. Esto es una discrepancia real con la doc oficial — se mantiene el código EXACTO tal como está en el material fuente (instrucción explícita de no alterarlo), pero queda señalado aquí: **si el RBD Bullet Solver no reconoce el constraint como "Glue" en Fase 2, lo primero a revisar es cambiar `s@constraint_name` por `s@constraint_type` y el valor `"Glue"` por `"glue"` en minúsculas.**

1. **Nombre exacto en Tab menu**: `Attribute Wrangle`.
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `connect_adjacent_pieces`.
3. **Pestaña/parámetro/valor**: pestaña *Wrangle* → `Run Over` = `Primitives`.
4. **Código VEX** (exacto, tal cual el material fuente):
```vex
s@constraint_name = "Glue";
float t_avg = avg(point(0,"t",@primnum,0), point(0,"t",@primnum,1));
f@strength = (t_avg > 1.3) ? -1 : fit(t_avg, 0, 1, 50, 8000);
```
   Aclaración: `point(0,"t",@primnum,0)` y `point(0,"t",@primnum,1)` leen el atributo de punto `t` en los dos puntos extremo (punto 0 y punto 1) de cada línea de constraint generada por `connect_adjacent_pieces`. Esto solo funciona porque en el paso anterior (`impact_kinematics`) se añadió `f@t = t;` — sin ese fix, `point(0,"t",...)` devolvería 0 para todos los primitivos y todos los constraints tendrían la misma resistencia.
5. **Qué ver en el viewport**: sin cambio de forma. En el spreadsheet, las líneas de constraint cerca del impacto (`t_avg` bajo) deben tener `strength` bajo (cerca de 50, se rompen fácil) y las líneas lejanas (`t_avg` alto) deben tener `strength` alto (hasta 8000, casi irrompibles) o `-1` (irrompible del todo, si `t_avg > 1.3`).

### Nodo: ground_plane

1. **Nombre exacto en Tab menu**: `Grid`.
2. **Dónde colocarlo**: nodo independiente dentro de `/obj/geo1` (o en un objeto geo separado), sin input.
3. **Pestaña/parámetro/valor**: pestaña *Transform* → `Translate` = `(0, 0, 0)` (en Y=0, base del muro). Tamaño amplio para cubrir toda el área de caída de escombros (a ojo, p.ej. 20×20).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: un plano horizontal grande a la altura Y=0, justo en la base del muro.

### Nodo: rbd_bullet_solver

**Corrección importante respecto al material fuente sobre los inputs**: el material fuente asumía 5 inputs con Input4=`ground_plane`, pero la documentación oficial *(verificado: sidefx.com/docs/houdini/nodes/sop/rbdbulletsolver.html)* especifica que los 5 inputs son: **Input 1** = geometría de render/simulación (las piezas fracturadas — aquí, `constraint_strength`); **Input 2** = geometría de constraints (en este flujo de trabajo SOP-based, las líneas de constraint ya suelen venir mezcladas con la geometría de piezas en el mismo input, revisar en Houdini si hace falta separarlas en un input propio o si el nodo las detecta automáticamente por atributo — **⚠️ no verificado del todo, confirmar en Houdini al llegar a este paso**); **Input 3** = geometría proxy (simplificada, no se usa en este shot); **Input 4** = geometría de colisión; **Input 5** = geometría guía ("guiding geometry", no se usa en este shot).
El plano de suelo **no necesariamente va como geometría de colisión en un input** — el nodo tiene, dentro de la pestaña *Collision*, un parámetro `Ground Type` con las opciones `None` / `Ground Plane` / `Height Field` *(verificado)*. Para un suelo simple e infinito, lo más directo es poner `Ground Type` = `Ground Plane` y NO conectar `ground_plane` a ningún input. Si en cambio se quiere un suelo con forma/tamaño específico (el `Grid` ya modelado), hay que conectarlo como **Input 4** (Collision Geometry) y dejar `Ground Type` = `None`. Documenta ambas opciones aquí porque el material fuente no distingue cuál de las dos se pretendía — **decide en Houdini según lo que se vea mejor en el primer test de sim**.

1. **Nombre exacto en Tab menu**: `RBD Bullet Solver`. *(verificado: sidefx.com/docs/houdini/nodes/sop/rbdbulletsolver.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Input 1 = `constraint_strength`. Input 4 = `ground_plane` (solo si eliges la variante "Collision Geometry" de suelo explicada arriba; si no, deja Input 4 vacío y usa el toggle `Ground Type` = `Ground Plane`).
3. **Pestaña/parámetro/valor**:
   - Pestaña **General** (sección *Simulation*) → `Time Scale` = `1.0`; `Bullet Substeps` = `4` (probar primero con 4, subir a `6` si se ve penetración o rebote falso); `Constraint Iterations` = entre `6` y `10` (a ojo, según estabilidad).
   - Pestaña **Properties**, sección **Pieces** (subsección *Physical*) → `Density` = `2400`; `Bounce` = `0.1`; `Friction` = `0.7`; `Rotational Stiffness` = `0.3` *(este último ya confirmado en sesión previa como nombre literal correcto)*.
   - Pestaña **Collision**, sección *Collision Geometry* → `Collision Shape` = `Convex Hull`.
   - Pestaña **Constraints**: el material fuente pedía activar "Scale [Strength] by Attribute" con atributo `strength`, `Propagation Rate`=0.35, `Propagation Iterations`=2-3, `Half-Life`=0.15s directamente en este nodo. **Verificación con resultado importante**: la documentación oficial de RBD Bullet Solver SOP lista en su pestaña *Constraints* los parámetros de *Break Thresholds* (`Force Threshold`, `Distance Threshold`, `Angle Threshold`, etc.) pero **no** contiene, en el texto de la doc consultada, parámetros literales llamados `Propagation Rate`, `Propagation Iterations` o `Half-Life`. Esos tres SÍ existen, confirmados con nombre exacto, pero en un nodo distinto: **`RBD Constraint Properties`** (SOP; la versión actual en la documentación aparece etiquetada como "RBD Constraint Properties 2.0" — **⚠️ no verificado si el Tab menu en H22 muestra "RBD Constraint Properties" o "RBD Constraint Properties 2.0" literalmente, confirmar en Houdini**), y también en el nodo DOP `Glue Constraint Relationship` *(verificado ambos: sidefx.com/docs/houdini/nodes/sop/rbdconstraintproperties.html y sidefx.com/docs/houdini/nodes/dop/glueconrel.html)*.
     **Acción recomendada**: inserta un nodo `RBD Constraint Properties` entre `constraint_strength` y `rbd_bullet_solver` (input = `constraint_strength`), y en su sección de constraint tipo **Glue** configura: `Propagation Rate` = `0.35`, `Propagation Iterations` = `2` a `3`, `Half-Life` = `0.15` (segundos) — estos tres nombres sí están confirmados literalmente en ese nodo. Deja `Strength` sin tocar en este nodo (ya viene seteado por el wrangle `constraint_strength` vía atributo `strength`; si el nodo tiene un modo `Action`/`Edit` que permite tocar solo algunos campos sin sobrescribir otros, actívalo para no pisar el atributo `strength` ya calculado — **⚠️ confirmar en Houdini el comportamiento exacto del parámetro `Action`**).
     Sobre `Scale [Strength] by Attribute`: no se encontró ese nombre literal exacto en la documentación de RBD Bullet Solver ni de RBD Constraint Properties. Lo que sí es un mecanismo documentado y ya estás usando correctamente: si la geometría de constraints ya trae los atributos de primitiva `strength` (float) y `constraint_type`/`constraint_name` (string) seteados vía VEX —como hace `constraint_strength`—, el solver los lee de forma nativa sin necesidad de un toggle adicional. **⚠️ No verificado del todo si existe además un checkbox explícito llamado "Scale by Attribute" en la pestaña Constraints — confirmar en Houdini al llegar a este paso; si existe, actívalo y apunta `Force Attribute`/campo equivalente a `strength`.**
4. **VEX**: no aplica en este nodo.
5. **Qué ver en el viewport**: al reproducir la simulación desde frame 1, las piezas marcadas `active=1` cerca del impacto deben salir despedidas primero y más rápido (según `speed`/`v` de Fase 2), mientras las piezas con `strength` alto permanecen pegadas al resto del muro más tiempo antes de romperse (si es que llegan a romperse). Las piezas deben caer y colisionar con el suelo (`ground_plane` o el toggle `Ground Plane`) sin atravesarlo. Si ves penetración de piezas en el suelo o rebotes poco naturales, ese es el punto para subir `Bullet Substeps` a 6.

### Checkpoint de la Fase 2

Reproduciendo la simulación completa: el impacto debe leerse como una expulsión radial de piezas pequeñas cerca del punto de disparo, con las piezas más alejadas del impacto quedándose ancladas o desprendiéndose tarde y con menos energía. El muro no debe "explotar" de forma uniforme — la propagación de la rotura debe verse orgánica, siguiendo la red de constraints. Todas las piezas caen por gravedad y se asientan sobre el suelo sin atravesarlo ni vibrar de forma inestable.

---

## FASE 3 — Dust sourcing y debris fino

Contexto de red: a partir de la geometría ya simulada por `rbd_bullet_solver` (Fase 2). Como el RBD Bullet Solver usado aquí es la versión **SOP** (no el clásico flujo DOP), su output ya es geometría animada directamente en el contexto SOP, sin necesidad de un DOP Import adicional — se puede encadenar el resto de nodos SOP directamente a su salida.

### Nodo: debris_source

1. **Nombre exacto en Tab menu**: `Debris Source`. *(verificado: sidefx.com/docs/houdini/nodes/sop/debrissource.html — es un SOP standalone, encadenable directo en la red de geometría, no requiere una red DOP separada)*.
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = salida de `rbd_bullet_solver`.
3. **Pestaña/parámetro/valor** *(nombres verificados en la doc oficial)*:
   - `Interior Group` = `interior` (el grupo creado en Fase 1 por `fractured_wall` / Voronoi Fracture SOP).
   - `Speed Threshold` — valor a ojo, filtra piezas que se mueven rápido (candidatas a generar polvo/esquirlas); ajustar viendo el resultado.
   - `Volume Threshold` — valor a ojo, excluye piezas grandes/lentas que no deberían generar debris fino.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: puntos generados sobre las piezas que cumplen los criterios de velocidad y volumen — deberías ver puntos apareciendo principalmente en las piezas pequeñas y rápidas cerca del impacto, con atributos heredados como `age`, `density`, `v` (confirmados como salidas nativas del nodo: `Age Attribute`, `Released Attribute`, `Distance Attribute`, `Rest Position`, `Volume Attribute`, `Density Attribute` — *verificado: sidefx.com/docs/houdini/nodes/sop/debrissource.html*).

### Nodo: debris_popnet

1. **Nombre exacto en Tab menu**: `POP Network`.
2. **Dónde colocarlo**: dentro de `/obj/geo1` (el POP Network SOP encapsula una red DOP internamente pero se coloca como un nodo más en la red de geometría). Input = `debris_source`.
3. **Pestaña/parámetro/valor y estructura interna**: la documentación del shelf tool de debris *(verificado: sidefx.com/docs/houdini/shelf/debris.html)* confirma un patrón de 3 nodos a nivel de objeto (`Debris Source` → `Debris Sim` [red DOP con `POP Source` + `POP Replicate`] → `Import Debris`), pero **no detalla explícitamente** si dentro de esa red DOP se usa un nodo `Copy to Points` o `Copy and Transform` para la variación geométrica de esquirlas — la documentación consultada se queda en el nivel de flujo general, no en el detalle nodo-por-nodo dentro del POP Network. **⚠️ No verificado — confirmar en Houdini al llegar a este paso, revisando el contenido interno del shelf tool "Debris" (menú Shelf → FX → Debris) como referencia directa en la propia sesión de Houdini.**
   Dentro del POP Network (una vez dentro, en contexto DOP/POP), configura a mano, ajustando a ojo:
   - Un `POP Source` leyendo `debris_source`, heredando `v` (mantener activado el traspaso de velocidad inicial).
   - Un `POP Wind` o nodo de fuerza equivalente para añadir dispersión angular extra de ±10-15° sobre la dirección heredada — **valor a ojo**.
   - Un `POP Drag` con arrastre moderado — **valor a ojo**.
   - `Life Span` de las partículas ~1-2s (parámetro típico del `POP Source` o de un `POP Kill` por edad).
4. **VEX**: no aplica en este nodo directamente (la variación de escala/rotación de la geometría de esquirla se resuelve normalmente con un wrangle adicional sobre las partículas, ver más abajo el patrón usado en `chip_copy` de Fase 4 como referencia del mismo mecanismo).
5. **Qué ver en el viewport**: un chorro de partículas saliendo del punto de impacto, con dispersión angular visiblemente mayor que la dirección de eyección original de las piezas grandes (más "salpicadura" de polvo/esquirlas), y que se desvanecen o se eliminan tras 1-2 segundos.

### Nodo: dust_density_ramp

1. **Nombre exacto en Tab menu**: `Attribute Wrangle`.
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = salida de `debris_popnet` (se usa la salida del POP Network porque de ahí viene el atributo `age` acumulado por el tiempo de vida de la partícula, heredado desde `debris_source` pero incrementándose frame a frame dentro de la simulación de partículas — el `debris_source` por sí solo, sin pasar por el POP Network, no acumula `age` en el tiempo).
3. **Pestaña/parámetro/valor**: pestaña *Wrangle* → `Run Over` = `Points`.
4. **Código VEX** (versión sintácticamente corregida — el material fuente escribía `density = grow * @density` sin el prefijo de tipo, lo cual no es VEX válido; aquí con `f@density` explícito):
```vex
float grow = 1 - exp(-@age / 8);
f@density = grow * f@density;
```
   Nota: `@age` está confirmado como atributo nativo de salida de Debris Source SOP *(verificado: sidefx.com/docs/houdini/nodes/sop/debrissource.html, listado como "Age Attribute" — "stores increasing value from zero after release")*. `density` es igualmente un atributo nativo de Debris Source ("Density Attribute — decreases from 1 to zero during life span"), así que `f@density` en el lado derecho de la ecuación ya existe antes de este wrangle; este nodo solo lo multiplica por la curva de crecimiento `grow`.
5. **Qué ver en el viewport**: sin cambio geométrico (solo atributo). En el spreadsheet, `density` debe crecer suavemente desde 0 en el frame de liberación de cada partícula, siguiendo una curva exponencial de aproximación a 1 a medida que `age` aumenta — nunca saltar bruscamente a un valor alto de golpe.

### Nodo: dust_rasterize

1. **Nombre exacto en Tab menu**: `Volume Rasterize Attributes`. *(verificado: sidefx.com/docs/houdini/nodes/sop/volumerasterizeattributes.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `dust_density_ramp`.
3. **Pestaña/parámetro/valor** *(nombres verificados en la doc oficial)*: `Group` = grupo de puntos de `dust_density_ramp` (o vacío si se usa toda la geometría entrante); `Attributes` = `density`; ajustar `Voxel Size` a ojo según el detalle de humo/polvo deseado (valores más pequeños = más resolución, más coste).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: un volumen VDB (visible como caja/nube de voxels o iso-superficie según el modo de visualización) que sigue aproximadamente la nube de partículas de polvo, con densidad concentrada donde las partículas tienen `density` alto.

### Nodo: pyro_source_pack

1. **Nombre exacto en Tab menu**: `Pyro Source Pack`. *(verificado: sidefx.com/docs/houdini/pyro/packedrbd.html — es un nodo SOP standalone, se crea con el Tab menu como cualquier otro SOP, no es un shelf tool)*.
2. **Dónde colocarlo**: dentro de `/obj/geo1` (o en una red SOP separada dedicada a la colisión pyro). Input = geometría de Rigid Body Pieces desde `rbd_bullet_solver` (la salida ya simulada de Fase 2).
3. **Pestaña/parámetro/valor**: parámetro `Input` (o equivalente de modo de entrada) = `Rigid Body Pieces` (el nodo soporta dos modos: volúmenes o piezas de rigid body; aquí se usa el segundo) *(verificado: sidefx.com/docs/houdini/pyro/packedrbd.html)*. Además, según el flujo documentado, normalmente se combina con un `Merge` antes de una librería de colisión referenciada por el Pyro Solver (ver siguiente nodo).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: geometría empaquetada (packed primitives) representando las piezas de rigid body, lista para usarse como colisión en la sim de pyro — visualmente similar a las piezas fracturadas pero mostradas como cajas/puntos de "packed primitive" en el viewport según el modo de visualización de packed geo.

### Nodo: pyro_solver

1. **Nombre exacto en Tab menu**: `Pyro Solver`. *(verificado: sidefx.com/docs/houdini/nodes/sop/pyrosolver.html — es la versión SOP-based del solver de pyro, integrable directo en la red de geometría)*.
2. **Dónde colocarlo**: dentro de `/obj/geo1` (o red dedicada). Fuente de volumen = `dust_rasterize`. Colisión: según el flujo verificado, el Pyro Solver referencia una "librería de colisión" vía el parámetro `Collider Library` (pestaña *Collision*), apuntando a una ruta relativa a un nodo `Merge` que combina uno o más `pyro_source_pack` *(verificado: patrón de "Merge + Pyro Source Pack" confirmado como el workflow estándar en sidefx.com/docs/houdini/pyro/packedrbd.html)*.
3. **Pestaña/parámetro/valor** — estructura de tabs confirmada *(verificado: sidefx.com/docs/houdini/nodes/sop/pyrosolver.html)*:
   - Pestaña **Collision** → sección *Source Collision* → `Collision Type` = `SDF + Volume Velocity`, con un segundo menú/dropdown dependiente ajustado a `Packed Sets` *(verificado — nota importante: NO es un único valor de dropdown "SDF + Volume Velocity + Packed Sets" como sugería el material fuente; son dos controles encadenados: primero `Collision Type` = `SDF + Volume Velocity`, y luego un selector secundario = `Packed Sets`)*. En `Collider Library` escribe la ruta relativa al nodo `Merge` que combina los `Pyro Source Pack` (p.ej. `../pyro_collision_lib`, ajustar al nombre real del nodo en tu red).
   - Pestaña **Shape** → aquí viven, confirmados por tab: `Viscosity` (a nivel principal de la pestaña Shape), subsección **Buoyancy** → `Buoyancy Scale`, subsección **Turbulence** → `Turbulence`, subsección **Shredding** → `Shredding`, subsección **Disturbance** → `Disturbance`. Ajustar: Viscosity media-alta, Buoyancy Scale baja, Turbulence/Shredding/Disturbance bajos-moderados (todos a ojo, sin valores numéricos fijos en el material fuente).
   - Pestaña **Fields** → subsección **Density** → `Dissipation` (ajustar lenta) y, dentro de la misma subsección, `Clamp Below` (activar).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: humo/polvo denso emergiendo del punto de impacto, colisionando de forma creíble contra las piezas de escombro en movimiento (sin atravesarlas), con una disipación lenta que deja el polvo flotando varios frames antes de desvanecerse, y sin sacudidas de turbulencia excesivas.

### Checkpoint de la Fase 3

Reproduciendo la simulación: debe verse una nube de polvo fino naciendo en el punto de impacto, creciendo suavemente en densidad (sin aparecer de golpe), dispersa con un ángulo ligeramente mayor que la trayectoria de las piezas grandes, y colisionando correctamente contra las piezas de escombro simuladas en Fase 2 sin atravesarlas. El polvo debe disiparse lentamente, no desaparecer abruptamente.

---

## FASE 4 — Chipping estático de bordes

Contexto de red: dentro de `/obj/geo1`, esta fase trabaja en paralelo sobre la geometría de Fase 2 (no depende de Fase 3).

### Nodo: hires_active_pieces

1. **Nombre exacto en Tab menu**: `Blast` (opción más simple y estándar para filtrar por atributo, según lo pedido en el material fuente).
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `impact_kinematics` (de Fase 2, **no** la salida ya simulada del solver — se trabaja sobre la geometría de reposo con los atributos de kinemática ya calculados).
3. **Pestaña/parámetro/valor**: pestaña *Blast* → `Group` = expresión/grupo que seleccione `active==1` (por ejemplo, usando un grupo previo creado con Group SOP sobre la condición `@active==1`, o directamente escribiendo el patrón de selección por atributo si el Blast SOP en pantalla lo permite vía *Group Type* = `Points`/`Primitives` según corresponda). `Delete Non-Selected` = ON (para quedarte solo con las piezas activas, no con las inactivas).
4. **VEX**: no aplica directamente (si el Blast SOP no permite filtrar por expresión de atributo numérico directo, añade un `Group` SOP previo con una expresión VEX/regla `@active==1` y usa ese grupo en el Blast).
5. **Qué ver en el viewport**: solo quedan visibles las piezas pequeñas cercanas al punto de impacto (las que tenían `active=1` en Fase 2) — el resto del muro desaparece de este flujo de nodos (sigue existiendo en la rama de Fase 2, esta es una rama de trabajo aparte).

### Nodo: rbd_interior_detail

1. **Nombre exacto en Tab menu**: `RBD Interior Detail`. *(verificado: sidefx.com/docs/houdini/nodes/sop/rbdinteriordetail.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `hires_active_pieces`.
3. **Pestaña/parámetro/valor** *(todos los nombres verificados en la doc oficial, organizados en las secciones confirmadas)*:
   - Sección **Geometry** → `Interior Group` = `interior`; `Add Detail` = ON.
   - `Detail Size` — pequeño, a ojo.
   - Sección **Noise Settings** → `Noise Amplitude` — pequeña, a ojo; `Frequency` — media-alta, a ojo; `Fractal Type` = `Standard` (opciones confirmadas: `None`, `Standard`, `Terrain`, `Hybrid`).
   - Sección **Displacement Scaling** → `Depth Method` = `Minimum Distance to Exterior` (opciones confirmadas: `Minimum Distance to Exterior` o `SDF Volume`); `Clamp Displacement Amount to Depth` = ON *(nombre confirmado literal)*.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: las caras interiores (grupo `interior`) de las piezas activas muestran ahora un desplazamiento de ruido fino — bordes de fractura menos limpios/geométricos y más "chipped", sin que el desplazamiento sobrepase el grosor de la pieza en ningún punto (gracias al clamp por profundidad).

### Nodo: chip_scatter

1. **Nombre exacto en Tab menu**: `Scatter`.
2. **Dónde colocarlo**: dentro de `/obj/geo1`, input = `rbd_interior_detail` (o la geometría con el grupo `interior` disponible).
3. **Pestaña/parámetro/valor**: `Group` = `interior`. Densidad baja, escalada por área de pieza — **a ojo**, el material fuente no da un valor de `Density`/`Force Total Count` fijo.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: puntos dispersos únicamente sobre las caras interiores de fractura, en cantidad baja — no una alfombra densa de puntos, solo lo suficiente para sembrar unas pocas esquirlas por pieza.

### Nodo: chip_copy

1. **Nombre exacto en Tab menu**: `Copy to Points`. *(verificado: sidefx.com/docs/houdini/nodes/sop/copytopoints.html)*
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Input 1 = geometría fuente (3-4 variantes de esquirla low-poly, combinadas en un único input vía `Switch` o `Merge` — estas variantes hay que modelarlas/generarlas aparte, por ejemplo con un `Voronoi Fracture` pequeño sobre una caja simple, tal como indica el material fuente). Input 2 = `chip_scatter`.
3. **Pestaña/parámetro/valor**: `Copy to Points` **no tiene controles propios de randomización** — lee atributos de punto de instancia ya existentes en la geometría de destino: `pscale`, `trans`, `rot`, `scale`, y usa el toggle `Transform Using Point Orientations` si quieres orientar copias según normales (`N`) *(verificado: sidefx.com/docs/houdini/nodes/sop/copytopoints.html)*. Es decir: **hace falta un Attribute Wrangle previo** sobre `chip_scatter` que randomice `pscale` y `orient`/`rot` con `rand(@ptnum)` antes de llegar a `chip_copy` — el material fuente lo intuía correctamente, queda confirmado que sí es necesario, no es opcional.
4. **VEX** (wrangle previo necesario, sobre `chip_scatter`, `Run Over = Points` — no estaba en el material fuente como código explícito, se añade aquí para que el paso sea ejecutable):
```vex
f@pscale = fit(rand(@ptnum), 0, 1, 0.3, 1.0);
vector rotaxis = normalize(set(rand(@ptnum+1)-0.5, rand(@ptnum+2)-0.5, rand(@ptnum+3)-0.5));
float rotangle = rand(@ptnum+4) * 360;
p@orient = quaternion(radians(rotangle), rotaxis);
i@variant = int(fit01(rand(@ptnum+5), 0, 3.999));
```
   Nota: `variant` sirve para que el `Switch`/`Merge` de las 3-4 variantes de geometría elija una distinta por punto si se conecta correctamente (revisar en Houdini cómo tu setup concreto de variantes consume ese atributo — puede requerir un `Copy to Points` con `Piece Attribute` apuntando a `variant`, o resolverse antes con un `Switch` por punto).
5. **Qué ver en el viewport**: pequeñas esquirlas low-poly distribuidas sobre las caras interiores de fractura, con tamaño y rotación visiblemente variados entre sí — no todas idénticas ni alineadas.

### Nodo: transform_pieces

1. **Nombre exacto en Tab menu**: `Transform Pieces`. *(verificado: sidefx.com/docs/houdini/nodes/sop/xformpieces.html — el nombre interno del tipo de nodo es `xformpieces`, pero el nombre mostrado en el Tab menu es "Transform Pieces")*.
2. **Dónde colocarlo**: dentro de `/obj/geo1`. Este nodo tiene **3 inputs** *(verificado)*: Input 1 = *Geometry to Transform* → conectar un `Merge` de (`rbd_interior_detail`, `chip_copy`); Input 2 = *Template Points* → conectar la salida ya simulada de `rbd_bullet_solver` (la geometría animada de Fase 2, que aporta las transformaciones por pieza a lo largo del tiempo); Input 3 = *Rest Points* (opcional, no usado aquí).
3. **Pestaña/parámetro/valor**: parámetro `Attribute` = `name` *(nombre de parámetro confirmado: "The name of the attribute used for indexing or matching")*; `Attribute Mode` = `Match by Attribute` (ya que `name` es un atributo string, no un índice entero — las opciones confirmadas son `Index by Attribute` y `Match by Attribute`).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: las esquirlas de chipping (`chip_copy`) y el detalle de bordes rotos (`rbd_interior_detail`) ahora se mueven y rotan junto con su pieza correspondiente a lo largo de toda la animación de Fase 2 — es decir, el chipping estático "viaja" pegado a cada pieza en vuelo y en el suelo, no se queda flotando en la posición de reposo original.

### Checkpoint de la Fase 4

Con la simulación de Fase 2 reproduciéndose: cada pieza activa cerca del impacto debe mostrar, además de su forma Voronoi base, bordes interiores con detalle de chipping fino (ruido de desplazamiento) y pequeñas esquirlas sueltas pegadas a sus caras de fractura — y todo ese detalle debe seguir el movimiento y rotación de la pieza padre en todo momento, sin desfasarse ni quedarse atrás en el espacio.

---

## FASE 5 — Shading MaterialX / Karma XPU

Contexto de red: `/stage` (LOPs) → `/mat` conceptualmente, pero en Houdini 22 el shader se construye realmente dentro de una red interna de un nodo `Material Library` en `/stage`.

**Nota de ambigüedad de nombre encontrada**: la documentación oficial de SideFX usa dos formas distintas para referirse al mismo flujo — la página de la Karma User Guide (`solaris/kug/materials.html`) dice literalmente *"Dive inside of that node, create a **Karma Material Builder** via the Tab menu"*, mientras que la página *Using MaterialX in Solaris* (`solaris/materialx.html`) dice *"Inside of that node, create a **Karma MaterialX Builder**"*. Además, desde Houdini 20 existen varios subnets distintos disponibles en ese Tab menu filtrado: `Karma Material Builder`, `USD MaterialX Builder`, `VEX Material Builder`, `USD Preview Material Builder` *(verificado: sidefx.com/docs/houdini/nodes/lop/materiallibrary.html y sidefx.com/docs/houdini/solaris/kug/materials.html)*. Para este shot, el que corresponde es el orientado a Karma+MaterialX — **al escribir en el Tab menu dentro del Material Library, busca "Karma Material" y usa la entrada que aparezca (puede mostrarse como "Karma Material Builder"); si ves además una entrada "Karma MaterialX Builder" en tu versión concreta de H22, es la misma familia de nodo, usa esa** — ⚠️ confirmar el nombre exacto tal como aparece en tu instalación al llegar a este paso, la documentación no es 100% consistente entre páginas.

### Nodo: material_lib (Material Library)

1. **Nombre exacto en Tab menu**: `Material Library`.
2. **Dónde colocarlo**: en `/stage`, como LOP.
3. **Pestaña/parámetro/valor**: por defecto, sin cambios necesarios salvo el path de salida si tu jerarquía de `/stage` lo requiere.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: ningún cambio visual todavía en el viewport de Solaris — este nodo solo crea el contenedor.

### Nodo: karma_matx_builder (dentro de Material Library)

1. **Nombre exacto en Tab menu**: `Karma Material Builder` (ver nota de ambigüedad arriba).
2. **Dónde colocarlo**: dentro de la red interna de `material_lib` (doble clic para entrar).
3. **Pestaña/parámetro/valor**: sin parámetros iniciales relevantes, es un subnet contenedor.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: dentro de esta red, el Tab menu ahora está filtrado y solo ofrece nodos MaterialX/Karma/USD Preview compatibles — confirma que ves esa lista filtrada antes de seguir.

### Nodo: geompropvalue_interior

1. **Nombre exacto en Tab menu**: `MtlX Geometry Property Value`. *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxgeompropvalue.html)*
2. **Dónde colocarlo**: dentro de `karma_matx_builder`.
3. **Pestaña/parámetro/valor**: parámetro `Geomprop` = `interior` (el parámetro se llama literalmente "Geomprop": *"The name of the primvar to be read"*). Parámetro `Signature` = ajustar según el tipo de dato del grupo/atributo `interior` que llega desde SOPs — si `interior` se exporta como grupo (no como atributo numérico), tendrás que convertirlo antes a un atributo float/int en SOPs (p.ej. con un wrangle `f@interior = @group_interior;` o promoviendo el grupo) para poder leerlo aquí como primvar; si ya es un atributo numérico, `Signature` = `float`. **⚠️ No verificado el listado completo de valores del dropdown `Signature` — confirmar en Houdini al llegar a este paso.**
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: sin preview directo salvo que conectes esta salida temporalmente al color base para depurar — deberías ver una máscara blanco/negro clara diferenciando caras interiores (recién fracturadas) de caras exteriores (intemperie original).

### Nodo: mix_basecolor

1. **Nombre exacto en Tab menu**: `MtlX Mix`. *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxmix.html)*
2. **Dónde colocarlo**: dentro de `karma_matx_builder`.
3. **Pestaña/parámetro/valor**: inputs exactos del nodo confirmados: `fg`, `bg`, `mix` *(verificado)*. La fórmula documentada es `F*mask + B*(1-mask)`, es decir, cuando `mix=1` se ve 100% `fg`, y cuando `mix=0` se ve 100% `bg`. Conecta: `fg` = color "roto/fresco" (hormigón recién expuesto, más claro/gris), `bg` = color "intemperie" (superficie original, más sucia/oscura); `mix` = salida de `geompropvalue_interior` (así, donde `interior=1`, se ve el color fresco).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: el color base del muro debe mostrar dos tonos claramente diferenciados — gris más claro/fresco en las caras de fractura interior, tono más envejecido/sucio en el resto de la superficie exterior original.

### Nodo: noise3d_rough → range

1. **Nombre exacto en Tab menu**: `MtlX Noise3D` *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxnoise3d.html)* → `MtlX Range` *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxrange.html)*.
2. **Dónde colocarlo**: dentro de `karma_matx_builder`. `noise3d_rough` sin input especial (usa posición de shading internamente); su salida alimenta el input principal de `range`.
3. **Pestaña/parámetro/valor**: `MtlX Noise3D` genera ruido Perlin 3D con salida aproximada en el rango -1 a 1 (según amplitud/pivot, ambos con default 1.0/0.0). En `MtlX Range`, los parámetros de remapeo confirmados son `Inlow`/`Inhigh` (rango de entrada) e `Outlow`/`Outhigh` (rango de salida) *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxrange.html)* — configura `Inlow`=`-1`, `Inhigh`=`1`, `Outlow`=`0.6`, `Outhigh`=`0.85` para el remap pedido de rugosidad.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: la salida de `range` alimentando `specular_roughness` debe producir variación sutil de brillo/mate sobre la superficie del muro, sin zonas completamente especulares ni completamente mate.

### Nodo: mtlx_standard_surface

1. **Nombre exacto en Tab menu**: `MtlX Standard Surface`. *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxstandard_surface.html)*
2. **Dónde colocarlo**: dentro de `karma_matx_builder`.
3. **Pestaña/parámetro/valor**: `Base Color` = salida de `mix_basecolor`; `Specular Roughness` = salida de `range` (nombres de parámetro confirmados literalmente); `Metalness` = `0`.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: el muro renderiza con el look base combinando color mixto y rugosidad variable, sin reflejos metálicos.

### Nodo: mtlx_position → mtlx_multiply → mtlx_noise3d_disp → mtlx_displacement

1. **Nombre exacto en Tab menu**: `MtlX Position` *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxposition.html)* → `MtlX Multiply` *(nombre estándar de la familia MaterialX, patrón consistente con el resto de nodos `MtlX *` ya verificados — no se hizo fetch dedicado por ser un multiplicador genérico sin ambigüedad de nombre)* → `MtlX Noise3D` (segunda instancia, para desplazamiento) → `MtlX Displacement` *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxdisplacement.html)*.
2. **Dónde colocarlo**: dentro de `karma_matx_builder`, cadena independiente solo para la cara exterior.
3. **Pestaña/parámetro/valor**: `mtlx_multiply` escala la salida de `mtlx_position` para controlar el tamaño espacial del ruido (valor a ojo). `mtlx_displacement` tiene input `displacement` que acepta **Float** (escalar, a lo largo de la normal) — confirmado que Karma XPU soporta esta variante escalar (ya confirmado en sesión previa: "displacement solo escalar/float, no vectorial"), y un input `scale` para la magnitud *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxdisplacement.html)*. Para excluir esta rama en las caras interior/chip: multiplica la salida de ruido por `(1 - interior_mask)` antes de entrar a `mtlx_displacement` — usa un `MtlX Mix` adicional o un `MtlX Multiply` con la máscara invertida de `geompropvalue_interior` conectada.
4. **VEX**: no aplica.
5. **Qué ver en el viewport (requiere render Karma, el viewport OpenGL estándar no muestra True Displacement)**: superficie exterior del muro con micro-relieve de hormigón visible en el render, mientras que las caras interiores de fractura y las esquirlas de chipping quedan sin este desplazamiento adicional (ya tienen su propio detalle geométrico de Fase 4).

### Nodo: mtlx_surface_material

1. **Nombre exacto en Tab menu**: `MtlX Surface Material`. *(verificado: sidefx.com/docs/houdini/nodes/vop/mtlxsurfacematerial.html)*
2. **Dónde colocarlo**: dentro de `karma_matx_builder`, nodo de salida final.
3. **Pestaña/parámetro/valor**: inputs confirmados literalmente `surfaceshader` y `displacementshader` *(verificado)* — conectar `surfaceshader` = salida de `mtlx_standard_surface`; `displacementshader` = salida de `mtlx_displacement`.
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: este nodo no añade cambio visual nuevo, solo empaqueta ambas salidas en el material final que se asignará al muro.

### Nodo: assign_material

1. **Nombre exacto en Tab menu**: `Assign Material`. *(verificado: sidefx.com/docs/houdini/nodes/lop/assignmaterial.html — LOP dedicado, existe como nodo independiente en H22, no hace falta resolverlo solo desde el parámetro del Material Library)*.
2. **Dónde colocarlo**: en `/stage`, después de `material_lib`, encadenado en la jerarquía de LOPs.
3. **Pestaña/parámetro/valor**: selecciona el/los primitivos del muro en el stage (botón `Select`, o patrón de path) y apunta al material creado en `karma_matx_builder`.
4. **VEX**: no aplica (aunque el nodo soporta asignación programática vía VEX si se necesitara variar el material por primitivo — no es el caso aquí).
5. **Qué ver en el viewport**: el muro en el viewport de Solaris muestra ahora el shader de `karma_matx_builder` aplicado (visible en modo de render Karma o en el visor con shading activado).

### Nodo: render_geo_settings (Render Geometry Settings)

1. **Nombre exacto en Tab menu**: `Render Geometry Settings`.
2. **Dónde colocarlo**: en `/stage`, después de `assign_material`.
3. **Pestaña/parámetro/valor**: `Primitives` = path del prim del muro en `/stage`; pestaña **Karma** → sección **Dicing** → `Displacement Style` = `True Displacement` (las 4 opciones ya confirmadas en sesión previa: `Displacement as Bump`, `True Displacement`, `Disable Displacement Shader`, `Bump Added to Displacement`); `Dicing Quality` alta (valor a ojo, según presupuesto de render).
4. **VEX**: no aplica.
5. **Qué ver en el viewport**: al renderizar con Karma, el desplazamiento del hormigón debe leerse como geometría real (silueta afectada, no solo relieve de sombreado tipo bump) en los bordes del muro contra el fondo.

### Checkpoint de la Fase 5

Renderizando un frame con Karma (XPU): el muro debe mostrar dos zonas de color claramente diferenciadas (fractura reciente vs. superficie envejecida), variación sutil de rugosidad especular, y micro-desplazamiento real de superficie visible en la silueta de las caras exteriores — sin desplazamiento adicional no deseado sobre las caras interiores o las esquirlas de chipping, que ya traen su propio detalle geométrico de Fase 4.

---

## Fuentes verificadas en esta sesión

- https://www.sidefx.com/docs/houdini/nodes/sop/voronoifracturepoints.html
- https://www.sidefx.com/docs/houdini/nodes/sop/voronoifracture.html
- https://www.sidefx.com/docs/houdini/nodes/sop/boolean.html
- https://www.sidefx.com/docs/houdini/nodes/sop/attribpromote.html
- https://www.sidefx.com/docs/houdini/nodes/sop/connectadjacentpieces.html
- https://www.sidefx.com/docs/houdini/nodes/sop/rbdbulletsolver.html
- https://www.sidefx.com/docs/houdini/nodes/sop/debrissource.html
- https://www.sidefx.com/docs/houdini/shelf/debris.html
- https://www.sidefx.com/docs/houdini/nodes/sop/volumerasterizeattributes.html
- https://www.sidefx.com/docs/houdini/pyro/packedrbd.html
- https://www.sidefx.com/docs/houdini/nodes/sop/pyrosolver.html
- https://www.sidefx.com/docs/houdini/nodes/sop/rbdinteriordetail.html
- https://www.sidefx.com/docs/houdini/nodes/sop/xformpieces.html
- https://www.sidefx.com/docs/houdini/nodes/sop/copytopoints.html
- https://www.sidefx.com/docs/houdini/nodes/dop/glueconrel.html
- https://www.sidefx.com/docs/houdini/nodes/sop/rbdconstraintproperties.html
- https://www.sidefx.com/docs/houdini/destruction/constraints.html
- https://www.sidefx.com/docs/houdini/solaris/materialx.html
- https://www.sidefx.com/docs/houdini/solaris/kug/materials.html
- https://www.sidefx.com/docs/houdini/nodes/lop/materiallibrary.html
- https://www.sidefx.com/docs/houdini/nodes/lop/assignmaterial.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxgeompropvalue.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxmix.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxstandard_surface.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxdisplacement.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxposition.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxnoise3d.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxrange.html
- https://www.sidefx.com/docs/houdini/nodes/vop/mtlxsurfacematerial.html
