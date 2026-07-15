# Aislar objetos por render layer con Holdout/Matte en Karma
Tags: #karma #render-layers #phantom #matte #holdout #compositing

## Contexto
Escena con varios assets (ej. cuerpo de un Aston Martin y un plano de suelo) que necesitaban renderizarse en capas separadas para composición en Nuke. Al usar Phantom en el objeto "que no debía verse", el objeto no aparecía, pero tampoco recortaba lo que había detrás — es decir, el suelo salía entero en vez de tener un hueco negro/transparente donde debería tapar el coche.

## Solución
Diferencia clave entre **Phantom** y **Matte/Holdout**:

- **Phantom** (Render Visibility → Invisible to primary rays): el objeto no se ve, pero tampoco recorta nada detrás — sigue afectando iluminación/reflejos si aplica, pero no dejará hueco en el alpha.
- **Matte / Holdout Mode**: el objeto no se ve, PERO recorta el alpha de todo lo que está detrás, dejando un hueco transparente/negro con su silueta exacta — esto es lo que se necesita para composición por capas.

### Setup correcto por rama de render

**Rama del suelo** (donde el coche debe recortar):
```
Render Geometry Settings
  ├── Suelo → Visible to all
  ├── Coche → Holdout Mode: Matte
  └── Resto → Invisible to primary rays (Phantom)
```

**Rama del coche** (render normal del asset):
```
Render Geometry Settings
  ├── Coche → Visible to all
  └── Resto → Invisible to primary rays (Phantom)
```

### Troubleshooting si el holdout no recorta
Si tras poner `Holdout Mode: Matte` sigue sin aparecer el hueco:
1. Comprobar que se está guardando como **EXR con alpha (RGBA)** — si se guarda como JPG/PNG sin alpha, el hueco no será visible aunque el render lo tenga.
2. Probar combinación alternativa: `Render Visibility: Visible to all` + `Holdout Mode: Matte` (en vez de Phantom + Matte) — en algunas versiones de Karma el objeto necesita ser "visible" para poder recortar correctamente aunque el resultado final no muestre su color.
3. Verificar que Phantom y Matte no están puestos en el mismo nodo/parámetro por error — deben ser dos configuraciones distintas dentro del mismo Render Geometry Settings.

## Renderizar múltiples ROPs en cola
Para lanzar varios render layers (ROPs) seguidos sin intervención manual:

- **Opción simple**: seleccionar todos los ROPs en el LOP network (Shift+clic) → clic derecho → Render. Houdini los procesa en secuencia.
- **Desde menú**: Render → Render All.
- **Con control de orden exacto** (Python Shell):
```python
rops = [
    "/stage/usdrender_rop1",
    "/stage/usdrender_rop2",
    # ...
]
for rop_path in rops:
    rop = hou.node(rop_path)
    rop.render()
    print(f"Renderizado: {rop_path}")
```
