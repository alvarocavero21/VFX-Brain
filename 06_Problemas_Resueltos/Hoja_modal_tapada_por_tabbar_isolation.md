# Hoja inferior (sheet) tapada por la barra de pestañas: no deja hacer scroll hasta el final
Tags: #web #css #react #pwa #coquefit

## Contexto
En [[05_Projects/CoqueFit/notes|CoqueFit]] (PWA en React), las hojas modales de rachas/comodines y de "entreno a medida" no dejaban ver su parte final: la tabbar inferior tapaba el contenido aunque la hoja tuviera un `z-index` más alto.

## Solución
1. Renderizar la hoja con un **portal a `document.body`** (`createPortal(sheet, document.body)`), fuera del contenedor `.app`.
2. Añadir una prueba e2e (Playwright) que comprueba que el final de cada hoja es visible. Se verificó que la prueba falla si el fallo vuelve.

## Por qué pasaba
`pro.css` ponía `isolation: isolate` en `.app`. Eso crea un nuevo *stacking context*: el `z-index` de la hoja solo compite dentro de `.app`, nunca contra elementos de fuera como la tabbar. Con el portal, la hoja sale de ese contexto. Además, tener muchos archivos CSS que se pisaban hizo difícil verlo; después se ordenaron en `src/styles/`.
