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

## Marca
- Logos en `public/brand/` (logotipo, submarcas .studio/.raw, símbolo, una tinta, avatares). Se regeneran con `scripts/brand.py` (necesita Michroma.ttf; ver instrucciones en el archivo).
- Fuentes: Michroma (marca y titulares cortos), Manrope (web y subtítulos de video, ExtraBold), JetBrains Mono (metadatos). Todas SIL OFL, uso comercial libre.
- Colores: verde tierra #1E523A, verde luz #3A8A62, carbón #121417, grafito #2A2F36, plata #C9CDD2, papel #F8F9FA, dorado #B89A5E (solo especiales).
