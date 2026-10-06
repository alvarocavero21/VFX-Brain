# Cámara, Sequencer y lenguaje de cine en UE
Tags: #unreal #camara #sequencer #cinematografia
Volver: [[00_MOC_Unreal]]

## CineCamera Actor — configurarla como una cámara real
- **Filmback**: elegir sensor real (p. ej. preset Super 35 / ARRI Alexa). El sensor define el FOV y la profundidad de campo para una focal dada.
- **Focales**: pensar en mm, no en FOV.
  - 18–24 mm: establishing, espacios grandes, sensación de escala.
  - 35 mm: "ojo humano" narrativo, plano medio/general.
  - 50 mm: neutral.
  - 85–135 mm: retratos, compresión de fondo, teleobjetivo de acción.
- **Aperture (f-stop)**: f/1.4–2.8 = DOF corta (aislar sujeto); f/5.6–11 = todo nítido (paisaje).
- **Focus**: Manual Focus Distance o **Tracking** a un actor. Activar *Draw Debug Focus Plane* mientras ajusto.
- **Escala**: si la DOF parece de "maqueta" (tilt-shift), la escala de la escena o del sensor está mal → revisar.

## Movimiento de cámara con peso
- Velocidades realistas: un dolly no acelera instantáneamente → **curvas suaves (ease in/out)** en el Curve Editor.
- **Camera Rig Rail / Rig Crane** para dollys y grúas creíbles.
- **Handheld sutil**: Camera Shake (Perlin/wave) con amplitud MUY baja, o importar un track de cámara real. Exagerado = videojuego.
- Evitar movimientos "imposibles" sin motivación (volar a través de todo).
- Rack focus: animar Focus Distance entre dos sujetos.

## Sequencer
- **24 fps** en la Level Sequence (Display Rate) para look de cine.
- Estructura: Master Sequence → shots (subsequences) → Camera Cuts track.
- 5.8: **Simple View** para timeline más limpio, **AutoBaking** a animation sequences, selección sincronizada viewport/Sequencer/Curve Editor.
- Keyframear también: exposición, Focus, intensidades de luz, parámetros de EasyAtmos/EasyRain (son keyframeables).

## Motion blur
- Angulo de obturador **180°** (shutter = 1/48 s a 24 fps) es el estándar de cine.
- En el render final el motion blur sale de **temporal samples** de MRG (ver [[Movie_Render_Graph_Salida_a_Nuke]]), no del motion blur de post del viewport.
- Partículas (lluvia/nieve) dependen mucho de esto: sin MB parecen puntos congelados.

## Composición
- Regla de tercios / líneas guía / encuadre dentro de encuadre (puertas, ventanas).
- Primer plano con algo desenfocado (foreground element) = profundidad instantánea.
- Activar **Composition Overlays** (grid de tercios) en el viewport de cámara.
- Aspect ratio: 2.39:1 (anamórfico) o 1.85:1 → configurar crop en filmback o letterbox en compo.

## Ejercicio (Fase 3 del roadmap)
1 plano de 6–8 s: dolly lento hacia sujeto, 35 mm, f/2.8, rack focus de primer plano a sujeto, handheld casi imperceptible, 24 fps, 180°.
