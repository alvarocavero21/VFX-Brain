# Sesión: 2026-10-08
## Proyecto/Shot: CoqueFit ([[05_Projects/CoqueFit/notes|notes]])

### Qué se hizo hoy
- Limpieza previa: se borró el proyecto del canal de YouTube (`canal-youtube`, `05_Projects/Canal_YouTube` y su carpeta de proyecto de Claude Code), creado el 07-oct junto con un acceso directo "Claude - Canal YouTube".
- Repo `coquefit` en GitHub, primer push y despliegue en Vercel. Probado en el iPhone: instalación, offline y copia exportar/importar OK.
- **Fase 1**: configuración inicial, plan con progresión, pantalla Hoy, temporizador, XP e historial.
- **Fase 2**: racha con comodines, logros y celebraciones. El personaje pasó de llama → Nurbs → colección de criaturas, y al final se usaron las 36 de Tuxemon (zip `coquefit-tuxemon` de Descargas).
- **Fase 2b**: pestaña Progreso (calendario, gráficas, aviso de medidas).
- Lavado de cara visual (fondo vivo, profundidad) y varias tandas de "más animaciones" por pantalla.
- **Fase 3**: recordatorios push. Upstash conectado, 9 variables en Vercel, botón "Enviar notificación de prueba" en Ajustes.
- **Fases 4a–4c**: familias (cada uno en su móvil, sin cuentas), pantalla Familia, administración (expulsar, regenerar código, códigos de recuperación 24 h, código de admin). El perfil pide el sexo y adapta el plan.
- Criatura inicial distinta por persona, cronómetro de entreno (inicio/fin), tema claro colorido, reinicio de temporada único y nombre en el perfil.

### Decisiones tomadas
- El servidor no guarda nunca entrenos ni datos personales (ver [[05_Projects/CoqueFit/notes|notes]]).
- 24 crons diarios para los recordatorios por el límite del plan Hobby.
- `/api/push/status` protegido con `CRON_SECRET` y sin mostrar valores de claves.

### Problemas encontrados
- El primer push no llegó a GitHub; se resolvió con `git push -u origin main`.
- Nombres de variables de Redis: hay que usar `KV_REST_API_URL` / `KV_REST_API_TOKEN`.

### Siguiente paso
Probar en el iPhone el tema claro, las familias y las notificaciones.
