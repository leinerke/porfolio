# leinerke — web

Portafolio de **leinerke.studio** (gastronomía, marcas, eventos) y **leinerke.raw** (motor y deporte). Astro, sin frameworks extra.

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # genera dist/ para publicar
```

## Agregar un trabajo
1. Agrega la foto o el reel en `scripts/media.sh` (función `photo` o `reel`) y ejecuta `npm run media`. Los originales no se tocan; las versiones web quedan en `public/media/`.
2. Suma una entrada a `projects` de la submarca en `src/data/content.ts`, con su ancho y alto reales. Las fotos nunca se recortan.

## Enlaces útiles
- `?modo=raw` o `?modo=studio` abre la web directo en esa submarca, sin la ventana de bienvenida (sirve para la bio de cada Instagram).
- WhatsApp y textos de cada botón: `src/data/content.ts`.
