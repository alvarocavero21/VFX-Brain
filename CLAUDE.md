# CLAUDE.md — Contexto persistente del vault VFX-Brain

## Quién soy
Álvaro (Coque), artista VFX con ~2 años de experiencia full-time en Houdini, especializado en destrucción fotorrealista, pyro/fuego, agua (FLIP) y rendering cinemático. También estudiante de primer año de Ingeniería, así que a veces trabajo en sprints cortos entre clases/exámenes — ten esto en cuenta para el ritmo y alcance de cada sesión.

## Stack técnico
- **Houdini**: SOPs, Solaris/LOPs, Karma XPU
- **Maya**: Arnold, rigging
- **Unreal Engine**
- **Nuke**
- **ComfyUI**

## Hardware
- **Laptop**: RTX 4090, i9-13980HX, 32GB RAM — trabajo diario
- **Desktop**: RTX 5080, Ryzen 9 9950X3D, 64GB RAM — simulaciones pesadas
- Houdini y ComfyUI comparten GPU en ambas máquinas.

## Regla clave: avance por fases
Cuando trabajemos en un pipeline largo (ej. un shot VFX completo), avanza **UNA FASE por sesión**, no intentes resolver el pipeline entero de golpe. Esto evita timeouts y respuestas descuidadas.

Consultar `04_Pipeline_General/Version_Reference.md` antes de proponer nodos/parámetros específicos de Houdini o Nuke.

## Documentación
- Cada shot o proyecto tiene su propio `notes.md` siguiendo la plantilla `99_Templates/Template_Shot.md`.
- Cada sesión de trabajo se registra con la plantilla `99_Templates/Template_Sesion_Produccion.md`.
- Los problemas técnicos resueltos (que costaron más de 15 min) se documentan en `06_Problemas_Resueltos/` siguiendo `99_Templates/Template_Problema_Resuelto.md`.
- Al final de cada sesión, actualiza el `notes.md` correspondiente resumiendo qué se hizo, decisiones tomadas, y siguiente paso.

## Rol de crítico técnico
Antes de pasar de fase de simulación a shading, actúa como crítico técnico: revisa si hay problemas típicos de portfolio amateur (escala incorrecta, timing plano, falta de secundarios) antes de continuar.
