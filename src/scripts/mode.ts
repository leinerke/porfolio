// Cambia toda la web entre .studio (claro) y .raw (oscuro).
// Cualquier elemento con data-set-mode="studio|raw" actúa como selector.
import type { Mode } from '../data/content';

const THEME_COLOR: Record<Mode, string> = { studio: '#F8F9FA', raw: '#121417' };

export function currentMode(): Mode {
  return document.documentElement.dataset.mode === 'raw' ? 'raw' : 'studio';
}

export function setMode(mode: Mode) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const doc = document as Document & { startViewTransition?: (cb: () => void) => unknown };
  if (doc.startViewTransition && !reduce && currentMode() !== mode) {
    doc.startViewTransition(() => applyMode(mode));
  } else applyMode(mode);
}

function applyMode(mode: Mode) {
  const root = document.documentElement;
  root.dataset.mode = mode;
  delete root.dataset.firstVisit;
  try {
    localStorage.setItem('leinerke-mode', mode);
  } catch {
    // modo privado: la elección dura solo esta visita
  }
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', THEME_COLOR[mode]);
  syncButtons();
  document.dispatchEvent(new CustomEvent<Mode>('modechange', { detail: mode }));
}

function syncButtons() {
  const mode = currentMode();
  document.querySelectorAll<HTMLElement>('[data-set-mode][aria-pressed]').forEach((el) => {
    el.setAttribute('aria-pressed', String(el.dataset.setMode === mode));
  });
}

document.addEventListener('click', (e) => {
  const el = (e.target as HTMLElement).closest<HTMLElement>('[data-set-mode]');
  if (el) setMode(el.dataset.setMode === 'raw' ? 'raw' : 'studio');
});

syncButtons();
document.querySelector('meta[name="theme-color"]')?.setAttribute('content', THEME_COLOR[currentMode()]);
