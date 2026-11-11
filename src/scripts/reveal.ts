// Animaciones de entrada: los elementos con .reveal aparecen al entrar en pantalla.
// Solo se ocultan si hay JavaScript (.js), así que sin script todo se ve igual.
const root = document.documentElement;
const items = [...document.querySelectorAll<HTMLElement>('.reveal')];

const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      io.unobserve(en.target);
    });
  },
  { rootMargin: '0px 0px -8% 0px', threshold: 0.08 },
);

// Esperar a que se retire la pantalla de carga, para que la entrada de la portada se vea
const start = () => items.forEach((el) => io.observe(el));
if (root.dataset.loaded) start();
else document.addEventListener('loader:done', start, { once: true });
