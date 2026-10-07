# Houdini → UE 5.8 · 00 · Setup y reglas comunes
Tags: #unreal #houdini #pipeline #setup
Volver: [[Puente_Houdini_Unreal]]

> Verificado el 2026-10-07 contra mi instalación: **Houdini 22.0.429** + **UE 5.8.2** (laptop).

## Lo que tengo instalado y lo que falta
| Pieza | Estado en mi máquina | Acción |
|---|---|---|
| Houdini 22.0.429 | ✅ | — |
| **Houdini Engine for Unreal** | ❌ no instalado | Descargar **v4.0.1** (es la versión exacta para **Houdini 22.0.429 / HAPI 9.0**, binarios para **UE 5.8** y 5.7 en Windows). La v4.0.2 pide Houdini 22.0.459 → no mezclar. El plugin también viene dentro del instalador de cada build de Houdini |
| **SideFX Labs** | ❌ no instalado (`houdini22.0/packages` vacío) | Instalar desde el Houdini Launcher / shelf "Labs" → da VAT 3.0, RBD to FBX, exportadores para juegos |
| Plugin UE **Interchange OpenVDB** | presente pero **Experimental y desactivado por defecto** | Activarlo en el proyecto para importar `.vdb` |
| Plugin UE **Alembic Importer** | activado en [[UE58_Cine_Template]] | — |
| Plugin UE **USD Importer** | activado en la plantilla | — |
| Heterogeneous Volumes (`r.HeterogeneousVolumes=1`) | activo en la plantilla | — |

Instalar Houdini Engine para UE (resumen de la doc oficial):
1. Copiar la carpeta del plugin (`HoudiniEngine`) a `UE58_Cine_Template/Plugins/` (por proyecto) o a `UE_5.8/Engine/Plugins/Runtime/` (para todos).
2. Debe coincidir con la build de Houdini instalada (22.0.429). Si actualizo Houdini → actualizar el plugin.
3. Requiere licencia de Houdini Engine (Indie/Edu incluyen Engine; la licencia Apprentice no sirve para Engine — comprobar mi licencia).

## Conversión de unidades y ejes (la fuente nº1 de errores)
| | Houdini | Unreal |
|---|---|---|
| Unidad | 1 = **1 metro** | 1 uu = **1 cm** |
| Eje arriba | **Y-up**, mano derecha | **Z-up**, mano izquierda |
| Frame rate | el de la escena (usar **24**) | Sequence a **24 fps** |

- **FBX / Alembic / USD**: el importador de UE convierte ejes; revisar escala (×100 si sale diminuto). En Alembic hay preset de conversión (Maya/Max/Custom) con `Scale` y `Rotation`.
- **VDB**: el importador de volúmenes **no** sabe de unidades → reportado en 5.4: escala ×100, rotación (90,0,0) y escala (1,-1,1) para voltear Y. *Verificar en 5.8 con un VDB de prueba y apuntar aquí el resultado.*
- Regla: hacer **siempre un test con un objeto de referencia** (cubo de 1 m en Houdini = 100 uu en UE) antes de exportar la sim gorda.

## Reglas comunes a todo lo que exporto
1. **Frame rate 24** en Houdini y en la Level Sequence. Mismo frame de inicio (yo uso 1001 en Houdini → offset en Sequencer, o empezar en 1).
2. **Limpiar atributos** que UE no usa (pesan y a veces rompen): quedarme con `P`, `N`, `uv`, `Cd`, `v` (si quiero motion vectors), `name`/`path`.
3. **Nombres** `path`/`name` limpios: UE crea una pista/componente por cada uno.
4. Cámara: si el FX se va a integrar con un plano de UE, **exportar la cámara de UE** (FBX/USD) e importarla en Houdini para simular y previsualizar con el mismo encuadre.
5. Probar primero con 10 frames y baja resolución → medir VRAM/tiempo en laptop (4090 16 GB) y desktop (5080). Apuntar en [[06_Problemas_Resueltos]] cualquier atasco >15 min.

## Fuentes
- [Houdini Engine for Unreal — Releases (GitHub SideFX)](https://github.com/sideeffects/HoudiniEngineForUnreal/releases)
- [Introduction to Houdini Engine for Unreal](https://www.sidefx.com/docs/houdini/unreal/intro.html) · [Install Houdini Engine for Unreal](https://www.sidefx.com/docs/houdini/unreal/install_houdiniengine.html)
- [Slick3D — VDB volumes and Render Layers in UE 5.4](https://slick3d.substack.com/p/volumes-and-render-layers-ue5)
