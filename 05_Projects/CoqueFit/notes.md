# Proyecto: CoqueFit (app de entreno personal)
## Estado: Fases 0–4c publicadas y en producción. Personaje ilustrado retirado; quedan estadísticas por zona. Pendiente: revisión completa en el iPhone real.
## Última sesión: 2026-10-09

### Descripción
PWA de entrenamiento personal para iPhone 13 Pro (sin Mac, sin App Store). Proyecto aparte del vault.
- Código: `C:\Users\alvar\Documents\entreno-app`
- Repo: `github.com/alvarocavero21/coquefit`
- Producción: https://coquefit.vercel.app (cada push a `main` despliega solo)
- Stack: Vite + React 19 + TypeScript, Dexie (IndexedDB), vite-plugin-pwa, funciones Node en `/api` de Vercel, Upstash Redis, `web-push` (VAPID). Tests con vitest + fake-indexeddb y Playwright (e2e y visual).
- Todo el texto de la app en español. Offline-first.

Sesiones: [[Sesion_2026-10-08_CoqueFit]] · [[Sesion_2026-10-09_CoqueFit]]

### Fases
| Fase | Qué incluye | Commit |
|---|---|---|
| 0 | Base PWA, copia de seguridad JSON (exportar/importar) | 46aff63 |
| 1 | Configuración inicial, generador de plan con progresión, pantalla Hoy, temporizador de descanso, XP, historial | 987a88c |
| 2 | Motivación: racha con comodines, logros, celebraciones, colección de criaturas | 9346e97 → 433d431 |
| 2b | Pestaña Progreso: calendario, gráficas de peso/medidas/volumen, aviso de medidas en Hoy | 0aaf20e |
| 3 | Recordatorios push diarios | b78496f → a62efde |
| 4a–4c | Familias: colección compartida, pantalla Familia, administración | 283f7d9, 406a4db, a66b3d9 |
| Extras 09-oct | Entrenos a medida, maniquí de fatiga, look pro, esfuerzo por serie, e2e, CSS ordenado | 37137ad → 40b48d3 |

### Decisiones tomadas
- **Privacidad ante todo.** Entrenos, peso, medidas, sexo y configuración se quedan en el dispositivo. El servidor nunca recibe datos personales (hay tests que lo garantizan).
  - Push: Upstash solo guarda suscripción + hora + zona horaria (+ lastSent). El texto del aviso lo escribe el service worker con datos locales.
  - Familia: el servidor solo guarda nombre, avatar, criaturas, criatura actual + etapa, racha y última actividad. Sin cuentas: clave por dispositivo y el servidor solo guarda su hash. El secreto de familia no entra en las copias de seguridad.
- **Racha**: los días de descanso cuentan; 1 comodín cada 7 días (máx. 3).
- **Colección**: 36 criaturas de Tuxemon (CC BY-SA 4.0, créditos obligatorios en Ajustes → Créditos). Evoluciona cada 2 sesiones; en la etapa máxima se guarda (marco dorado + MÁX) y llega la siguiente línea. Cada persona empieza con una criatura distinta. Se llaman "criaturas", no Pokémon (se rechazó integrar arte oficial de Pokémon).
- **Recordatorios**: 24 crons diarios (uno por hora) por el límite del plan Hobby de Vercel (cada cron solo 1 vez/día, ±59 min). Diagnóstico en `/api/push/status`, protegido con `CRON_SECRET`.
- **Sexo en el perfil** (solo local): Mujer = descansos −15 % y patrón de glúteo en el plan. Hombre / "prefiero no decirlo" = plan estándar.
- **Medidas**: peso semanal; la cintura se retiró (`RETIRED_MEASURES`).
- **Reinicio de temporada** único (marca `seasonReset1`, copia en `meta.preResetBackup`). No volver a reiniciar sin pedirlo; otra temporada necesitaría `seasonReset2`.
- **Personaje ilustrado: retirado (09-oct).** Se probaron varias versiones (cartoon, maniquí line-art, poses de confianza → superhéroe) y al final se quitó. Solo quedan las estadísticas Brazos / Torso / Abdomen / Piernas. Código recuperable en git (último commit con él: `2adf2fa`).
- **Esfuerzo por serie** (Fácil / Justo / Al límite, opcional): todo fácil → sube peso antes; máximo alcanzado pero ≥ mitad al límite → mantiene; no llega al mínimo yendo al límite → baja ~5 %.
- **Tema claro colorido por defecto**; oscuro en Ajustes → Aspecto. Nivel de animaciones ajustable, y se calman durante la sesión de entreno.

### Problemas resueltos
- **El push a GitHub no llegaba** (repo vacío): comprobar con `git remote -v`, `git status` y `git log origin/main --oneline`; resuelto con `git push -u origin main`.
- **Variables de Redis**: Vercel/Upstash crea `KV_REST_API_URL` y `KV_REST_API_TOKEN`; el código tiene que usar exactamente esos nombres.
- **Hojas tapadas por la barra de pestañas**: ver [[Hoja_modal_tapada_por_tabbar_isolation]].
- **Bajada de peso redondeaba de más** (60 → 55 kg): detectado por tests antes de publicar; ahora 60 → 57,5 kg.

### Comandos útiles
- `npm run test:e2e`: recorrido completo en Chrome a tamaño iPhone 13.
- `VISUAL=1 npx playwright test visual`: comparación visual de 12 pantallas (claro/oscuro). Tras un cambio de diseño intencionado, añadir `--update-snapshots`.
- `npm run css:limpiar`: elimina CSS muerto. Los estilos viven en `src/styles/` con un único punto de entrada.
- `npm run siluetas`: regenera las siluetas de las criaturas.

### Ideas pendientes (propuestas, sin hacer)
- [ ] Récords y fuerza por ejercicio (gráfica, 1RM estimado, mejores marcas)
- [ ] Cronómetro en ejercicios por tiempo (plancha)
- [ ] Series de calentamiento automáticas (50 % y 75 %)
- [ ] Calculadora de discos
- [ ] Resumen semanal el domingo por notificación
- [ ] Retos semanales en familia y reacciones 👏🔥
- [ ] Fotos de progreso (solo en el iPhone) y exportar a CSV
- [ ] Revisar el contraste del tema claro
- Apple Salud: no es posible desde una PWA.

### Siguiente paso
Hacer una pasada por todas las pantallas en el iPhone real (tema claro y oscuro), apuntando lo que vaya lento o se vea mal. Probar también los recordatorios push y el esfuerzo por serie en el próximo entreno. Después, elegir la siguiente mejora (recomendadas: récords por ejercicio y cronómetro).
