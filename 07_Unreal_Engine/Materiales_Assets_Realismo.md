# Materiales y assets para realismo
Tags: #unreal #materiales #substrate #nanite #megascans
Volver: [[00_MOC_Unreal]]

## Substrate
- Sistema de materiales modular (slabs) de UE5: mezcla real de capas (metal + clear coat, piel, tela, suciedad sobre pintura).
- 5.8: importación de materiales medidos **X-Rite AxF → Substrate** (Production Ready).
- Comprobar en Project Settings si Substrate está activo en el proyecto (cambiarlo en un proyecto ya avanzado recompila todos los shaders).

## Nanite
- Geometría densa sin LODs manuales: escaneos, kitbash, mallas de fractura de Houdini.
- **Nanite Tessellation/Displacement**: displacement real desde textura (lo usan EasySnow y EasyMapper). Requiere habilitarlo en el proyecto; caro en sombras (5.8 añade cvars de escalabilidad de VSM con teselación).
- **Nanite Foliage** (5.7 experimental) / Procedural Vegetation Editor (5.8 experimental) para vegetación densa.

## Las 6 reglas de material realista
1. **Roughness es el canal más importante**: nunca valor plano; variación con manchas, huellas, polvo.
2. **Albedo dentro de rango físico** (nada 100% negro ni 100% blanco; ~0.04–0.9).
3. **Escala de textura correcta**: un ladrillo debe medir lo que mide un ladrillo. Usar referencia de 180 cm (maniquí) en escena.
4. **Bordes**: desgaste en aristas (curvature/AO) — en el mundo real no hay aristas perfectas (bevels!).
5. **Decals de imperfección** (Megascans): manchas de agua, grietas, hojas, suciedad en la base de las paredes.
6. **Variación por instancia**: Per Instance Random / world position para que 50 rocas iguales no parezcan copias.

## Assets
- Megascans: superficies + decals primero (ver [[Fab_Otras_Herramientas_y_Assets]]).
- Mallas propias desde Houdini con UVs, o sin UVs usando EasyMapper (triplanar).
- Escala: UE en **cm**. Houdini en m → exportar con escala 100 o usar los ajustes de importación.
