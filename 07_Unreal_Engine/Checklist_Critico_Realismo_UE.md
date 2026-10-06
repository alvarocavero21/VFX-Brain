# Checklist del crítico técnico — realismo en UE
Tags: #unreal #checklist #critica #portfolio
Volver: [[00_MOC_Unreal]]

Pasar esta lista **antes de pasar a render final** (equivalente al paso "simulación → shading" del CLAUDE.md). Problemas típicos de portfolio amateur en UE:

## Escala y física
- [ ] Escala real verificada con maniquí de 180 cm.
- [ ] DOF coherente con focal + sensor + distancia (sin efecto maqueta).
- [ ] Velocidad de cámara y de objetos creíble para su tamaño.

## Luz
- [ ] Exposición **manual**, nada de auto exposure.
- [ ] Cada luz está motivada por algo del mundo.
- [ ] Hay un punto de interés claro (más brillo/contraste donde quiero el ojo).
- [ ] Comparado con el Path Tracer al menos en un frame.
- [ ] Sin light leaking, sin manchas de GI que parpadean entre frames.

## Atmósfera y secundarios
- [ ] Perspectiva aérea: el fondo pierde contraste y se tiñe con la atmósfera.
- [ ] Partículas en el aire (polvo, insectos, hojas, ceniza) → EasyAtmos.
- [ ] En clima: interacción con superficies (charcos, goteo, acumulación), no solo partículas cayendo.
- [ ] Timing no plano: algo cambia a lo largo del plano (viento, nube, luz parpadeante, rack focus).

## Materiales
- [ ] Roughness con variación; nada "plástico".
- [ ] Bordes con desgaste/bevel; base de paredes y suelos con suciedad.
- [ ] Sin repetición evidente de texturas ni de assets.

## Cámara
- [ ] Focal y sensor reales, 24 fps, obturador 180°.
- [ ] Movimiento con ease in/out; handheld sutil si aplica.
- [ ] Composición pensada (tercios, foreground, líneas guía).

## Render y compo
- [ ] Motion blur real (temporal samples), sin ghosting de TSR.
- [ ] Warm-up frames → partículas llenas en frame 1.
- [ ] EXR en espacio de color correcto para Nuke.
- [ ] Grano, grade y lente sutil en compo.

## La prueba final
- [ ] Puesto al lado de la **referencia real**, en blanco y negro: ¿los valores (luces/sombras) coinciden?
- [ ] ¿Un no-artista diría "es un videojuego"? Si sí → volver a Luz o Cámara.
