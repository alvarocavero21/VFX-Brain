# Técnica: nave aterrizando — thrusters + polvo/humo de aterrizaje
Tags: #unreal #niagara #fx #thrusters #polvo #tecnica
Volver: [[00_MOC_Unreal]] · Relacionado: [[Puente_Houdini_Unreal]], [[Checklist_Critico_Realismo_UE]]

Notas de técnica (sin montar todavía). Material de partida en disco: proyecto `Unreal Projects\Landing` (Ship_baked.fbx, Camera_Landing.fbx, paisaje, Megaplants) y `Downloads\SpaceShip(HighDetail_NoUV).fbx`.

## Referencias reales a estudiar
Aterrizajes de **SpaceX Falcon 9 / Starship**, helicópteros sobre arena (*brownout*), Harrier/F-35B en vertical. Fijarse en: el polvo sale **radialmente a ras de suelo** y luego sube; el chorro casi no se ve de día; la distorsión por calor es lo que más vende.

## Capas del efecto (de dentro a fuera)
1. **Núcleo del chorro (exhaust plume)**
   - Malla cónica con material **emisivo + additive/translucent**, fresnel para que los bordes se desvanezcan, ruido panning a lo largo del eje. Diamantes de choque (*shock diamonds*) opcionales en escala de bandas.
   - Intensidad emisiva en valores físicos altos (con exposición manual, si no se "quema" o no se ve).
   - Animar intensidad/longitud con la potencia del motor (más fuerte al frenar cerca del suelo).
2. **Luz**: una **Point/Spot light** naranja-azulada por thruster iluminando el suelo; parpadeo sutil. Con **MegaLights** se pueden tener varias con sombras baratas.
3. **Distorsión por calor**: material de refracción/distorsión en sprites o malla alrededor del chorro (Niagara sprites con material de distorsión). Es lo que más realismo da de día.
4. **Polvo de impacto (ground effect)** — Niagara:
   - Emitir desde un **disco en el suelo debajo del chorro** (posición = proyección del thruster sobre el terreno; trace al suelo o Collision Query).
   - Velocidad **radial hacia fuera** + pequeña componente hacia arriba; drag alto para que frene.
   - **Spawn rate dependiente de la altura**: 0 a más de ~X m, máximo justo antes de tocar (parámetro de usuario `Altitude` que el BP/Sequencer actualiza).
   - Sprites grandes con textura de humo (flipbook), color tomado del terreno (arena/tierra), lit (que reciba luz del sol y del thruster), Volumetric Fog local si se quiere densidad.
   - Alternativa hero: **Niagara Fluids** (plugin `NiagaraFluids` instalado en 5.8) o sim de **pyro en Houdini → VDB → Heterogeneous Volume** (ver [[Puente_Houdini_Unreal]]).
5. **Secundarios**: piedrecitas/debris disparados radialmente (mesh particles con colisión), hierba/vegetación agitada (si hay Megaplants: wind actor local o Material Parameter Collection), ceniza/partículas finas que quedan flotando tras apagar motores.
6. **Después del toque**: motores bajan potencia → el polvo sigue expandiéndose y se asienta lentamente (no cortar de golpe). Tren de aterrizaje se comprime (suspensión) — la masa se vende ahí.

## Animación de la nave
- Curva de descenso: deceleración progresiva, **no lineal**; ligera oscilación/corrección lateral (los sistemas reales corrigen), pequeño "hover" antes de tocar.
- Shake de cámara sutil acoplado a la potencia de motores y al toque.
- Motion blur real (MRG temporal samples) para el chorro y el debris.

## Plan de montaje (cuando toque)
1. Importar nave + animación (o keys en Sequencer), cámara.
2. BP_Thruster: malla de chorro + luz + componente Niagara, parámetro `Power`.
3. NS_LandingDust con parámetros `Altitude`, `Power`, `DustColor`.
4. Sequencer: keys de `Power`; `Altitude` calculado en el BP cada tick (trace al suelo).
5. Pasar [[Checklist_Critico_Realismo_UE]] → render con `MRG_Cine_Final` ([[UE58_Cine_Template]]).

Montaje: lo hace Álvaro a mano en el editor, con Claude guiando paso a paso (el MCP está desconectado por decisión suya).
