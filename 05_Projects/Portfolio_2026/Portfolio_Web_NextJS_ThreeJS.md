# Portfolio web — AlvaroCaveroVFX
Tags: #portfolio #nextjs #threejs #vercel #web

## Stack técnico
- **Framework**: Next.js 14 + TypeScript
- **Estilos**: Tailwind CSS
- **Animación**: Framer Motion
- **3D/WebGL**: Three.js
- **Scroll**: Lenis (smooth scroll)
- **Deploy**: Vercel, vía GitHub (con script de deploy para push con un solo comando)

## Estructura de secciones
Full-page snap scroll con 4 secciones:
1. **Hero** — con fondo shader WebGL (efecto "FloatingPaths") y cursor personalizado dorado
2. **Showreel**
3. **Works** — grid de proyectos con `GlowCard` (efecto de spotlight azul al hacer hover)
4. **Contact** — foto de perfil circular, email, LinkedIn

## Detalles de contenido actual
- Proyectos con vídeo real embebido vía YouTube:
  - Ferrari / Ship Compo (YouTube ID: `Y6ztIPGr6_Q`)
  - Nature Takeover (YouTube ID: `ECXjw5t7fQI`)
- Contacto: `alvarocavero21@gmail.com`, LinkedIn `https://www.linkedin.com/in/alvaro-cavero/`

## Efectos de animación implementados
- Text scramble y split text animations
- Cursor custom dorado
- Shader background (FloatingPaths) en el Hero
- GlowCard con spotlight azul en tarjetas de proyecto

## Pendiente / ideas exploradas
- Concepto de logo para el nombre "Coque" (apodo personal) — explorado pero no finalizado
- Ampliar la sección Works con los nuevos shots del portfolio 2026 (dragón, bala, agua, cristal, energy FX)

## Nota para la próxima iteración (Claude Design)
Usar Claude Design para prototipar visualmente antes de tocar código: mantener la estética oscura/cinematográfica ya establecida (shader Hero, GlowCard) como punto de partida, no reinventar desde cero.
