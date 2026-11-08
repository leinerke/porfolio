// Todo el contenido de la web. Para agregar un trabajo: genera sus medios
// con `npm run media` y suma una entrada a `projects` de la submarca.

export type Mode = 'studio' | 'raw';

export const WHATSAPP = '573018830254';
export const WHATSAPP_DISPLAY = '+57 301 883 0254';
export const wa = (msg: string) => `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`;

type Photo = { kind: 'photo'; src: string; w: number; h: number };
type Reel = { kind: 'reel'; src: string; w: number; h: number };
export type Project = (Photo | Reel) & { title: string; tag: string; cats: string[]; alt: string };

const photo = (src: string, w: number, h: number) => ({ kind: 'photo' as const, src, w, h });
const reel = (src: string) => ({ kind: 'reel' as const, src, w: 720, h: 1280 });
const V = photo; // abreviaturas para que la lista se lea en una línea
const H = (src: string) => photo(src, 1600, 1280);
const P = (src: string) => photo(src, 1280, 1600);

export const brands = {
  studio: {
    name: 'leinerke.studio',
    eyebrow: 'leinerke.studio / Gastronomía · Marcas · Eventos',
    headline: 'Platos y marcas que se venden con la mirada',
    sub: 'Producción de foto y video para restaurantes, marcas y eventos, con dirección de arte incluida. Contenido listo para carta, web y redes.',
    hero: { ...P('st-carolas-bebidas'), alt: 'Jugo con borde escarchado y rodaja de limón de Carola’s Creative', meta: 'Carola’s Creative / Bebidas' },
    pickerImg: 'st-blessed',
    waMsg: 'Hola Leinerke, vi tu web y quiero cotizar un proyecto de leinerke.studio.',
    servicesTitle: 'Contenido que hace crecer tu negocio',
    ctaTitle: '¿Listo para que tu marca se vea tan bien como sabe',
    pickerText: 'Restaurantes, marcas y negocios',
    instagram: 'https://instagram.com/leinerke.studio',
    cats: ['Todo', 'Video', 'Gastronomía', 'Postres', 'Marcas'],
    services: [
      { title: 'Fotografía de menú y producto', desc: 'Fotos de carta que abren el apetito y funcionan en el menú, en apps de delivery y en redes.', items: ['Fotos de cada plato con styling', 'Formatos para delivery y redes', 'Banco de imágenes de tu marca'] },
      { title: 'Reels para restaurantes y negocios', desc: 'Videos verticales con idea, grabación y edición, listos para Instagram y TikTok.', items: ['Idea y guion del reel', 'Grabación y edición con subtítulos', 'Versiones para feed e historias'] },
      { title: 'Contenido de marca', desc: 'Retratos, procesos y espacios que muestran quién está detrás de tu negocio.', items: ['Retratos del equipo', 'Fotos del proceso y del lugar', 'Contenido para el mes'] },
      { title: 'Eventos y lanzamientos', desc: 'Cobertura de aperturas, lanzamientos y eventos de marca.', items: ['Fotos del evento editadas', 'Reel resumen del evento', 'Selección para publicar en redes'] },
    ],
    projects: [
      { ...reel('pizza-hero'), title: 'Pizzería en leña', tag: 'Reel · Hero', cats: ['Video', 'Gastronomía'], alt: 'Reel de la Pizzería en leña: preparación de la pizza' },
      { ...P('st-blessed'), title: 'Blessed Express', tag: 'Hamburguesas', cats: ['Gastronomía'], alt: 'Hamburguesa con pollo y tocineta de Blessed Express' },
      { ...P('st-carolas-carta'), title: 'Carola’s Creative', tag: 'Carta', cats: ['Gastronomía'], alt: 'Croquetas sobre salsa blanca mientras las cortan' },
      { ...reel('pan-y-fuego'), title: 'Pan y Fuego', tag: 'Reel', cats: ['Video', 'Gastronomía'], alt: 'Reel de Pan y Fuego' },
      { ...P('st-golosa-torta'), title: 'La Golosa', tag: 'Amor y amistad', cats: ['Postres'], alt: 'Torta roja decorada con corazones de La Golosa' },
      { ...reel('cocina-de-franco'), title: 'Cocina de Franco', tag: 'Reel', cats: ['Video', 'Gastronomía'], alt: 'Reel de Cocina de Franco: carnes a la parrilla' },
      { ...V('st-pizza', 1080, 1350), title: 'Pizzería en leña', tag: 'Pizza artesanal', cats: ['Gastronomía'], alt: 'Pizza artesanal sobre mesa de madera' },
      { ...P('st-golosa-productos'), title: 'La Golosa', tag: 'Productos', cats: ['Postres'], alt: 'Postres en vaso junto a empaques de La Golosa' },
      { ...P('st-ruta60-resultado'), title: 'Ruta 60 Biker Barber', tag: 'Resultado', cats: ['Marcas'], alt: 'Cliente sonriendo tras su corte en Ruta 60 Biker Barber' },
      { ...P('st-carolas-pitas'), title: 'Carola’s Creative', tag: 'Pitas', cats: ['Gastronomía'], alt: 'Pita vista desde arriba sobre plato claro' },
      { ...reel('pizza-resena'), title: 'Pizzería en leña', tag: 'Reel · Reseña', cats: ['Video', 'Gastronomía'], alt: 'Reseña en video de la Pizzería en leña' },
      { ...P('st-ruta60-proceso'), title: 'Ruta 60 Biker Barber', tag: 'Proceso', cats: ['Marcas'], alt: 'Barbero arreglando la barba de un cliente' },
    ] as Project[],
  },
  raw: {
    name: 'leinerke.raw',
    eyebrow: 'leinerke.raw / Deporte · Motor · Acción',
    headline: 'Cada segundo, en su mejor cuadro',
    sub: 'Fotografía y video para motocross, enduro y eventos de alta adrenalina. Encuentra tus fotos por número de piloto.',
    hero: { ...P('raw-828'), alt: 'Piloto #828 en pleno salto bajo un cielo de tormenta', meta: '#828 / Válida 25 oct 2026' },
    waMsg: 'Hola Leinerke, vi tu web y quiero información de leinerke.raw.',
    servicesTitle: 'Tu carrera, contada en fotos',
    ctaTitle: '¿Corriste y quieres tus fotos',
    pickerText: 'Pilotos, carreras y eventos de motor',
    pickerImg: 'raw-828',
    instagram: 'https://instagram.com/leinerke.raw',
    cats: ['Todo', 'Saltos', 'En pista'],
    services: [
      { title: 'Tus fotos de la carrera', desc: 'Encuentra tus fotos por número de piloto y quédate con las mejores de tu válida.', items: ['Fotos clasificadas por número', 'Edición de color en cada foto', 'Entrega digital en alta resolución'] },
      { title: 'Cobertura para organizadores', desc: 'Fotografía de válidas, campeonatos y eventos de motor para la organización y sus patrocinadores.', items: ['Cobertura de toda la jornada', 'Galería para pilotos y patrocinadores', 'Fotos para las redes del evento'] },
      { title: 'Sesión de piloto', desc: 'Sesión dedicada en entrenamiento para tu marca personal y tus patrocinadores.', items: ['Fotos de acción y retrato', 'Selección editada', 'Contenido para redes y patrocinadores'] },
      { title: 'Video de acción', desc: 'Clips y reels de tu carrera o tu entrenamiento.', items: ['Grabación en pista', 'Reel vertical editado', 'Clips para redes'] },
    ],
    projects: [
      { ...H('raw-35'), title: 'Piloto #35', tag: 'Válida 25 oct', cats: ['Saltos'], alt: 'Piloto #35 en el aire contra un cielo de nubes' },
      { ...P('raw-514'), title: 'Piloto #514', tag: 'Válida 25 oct', cats: ['Saltos'], alt: 'Piloto #514 saltando con montañas al fondo' },
      { ...P('raw-707'), title: 'Piloto #707', tag: 'Válida 25 oct', cats: ['Saltos'], alt: 'Piloto #707 en el aire junto a los árboles' },
      { ...P('raw-189'), title: 'Piloto #189', tag: 'Válida 25 oct', cats: ['En pista'], alt: 'Piloto #189 tomando una curva en tierra roja' },
      { ...H('raw-33'), title: 'Piloto #33', tag: 'Válida 25 oct', cats: ['Saltos'], alt: 'Piloto #33 en pleno salto frente a la montaña' },
      { ...H('raw-28'), title: 'Piloto #28', tag: 'Válida 25 oct', cats: ['En pista'], alt: 'Piloto #28 de frente en la pista' },
      { ...P('raw-1'), title: 'Piloto #1', tag: 'Válida 25 oct', cats: ['En pista'], alt: 'Piloto #1 de frente en la pista de tierra roja' },
      { ...P('raw-4'), title: 'Piloto #4', tag: 'Válida 25 oct', cats: ['En pista'], alt: 'Piloto #4 bajando por la pista entre las cintas' },
    ] as Project[],
  },
} as const;

export const capabilities = [
  { title: 'Foto y video juntos', desc: 'Una sola producción, todo el contenido que necesitas.' },
  { title: 'Reels verticales', desc: 'Editados y listos para Instagram y TikTok.' },
  { title: 'Edición y color propios', desc: 'Un look consistente en cada entrega.' },
];

// Rutas con el prefijo de publicación (p. ej. /porfolio/ en GitHub Pages)
export const asset = (path: string) => `${import.meta.env.BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;

// Rutas de medios generados por scripts/media.sh
export const img = (name: string, w: 800 | 1600 = 1600) => asset(`media/img/${name}-${w}.jpg`);
export const srcset = (name: string) => `${img(name, 800)} 800w, ${img(name, 1600)} 1600w`;
export const video = (name: string) => ({
  preview: asset(`media/video/${name}-preview.mp4`),
  full: asset(`media/video/${name}.mp4`),
  poster: asset(`media/video/${name}-poster.jpg`),
});
