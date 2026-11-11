"""Genera los logos de leinerke en SVG con el texto convertido a trazos.

Reglas de construcción (unidad u = altura de la "l" de leinerke):
  - Horizontal (balance): símbolo de 2u de alto, centrado sobre la banda
    de texto (sobresale 0.5u arriba y abajo); separación símbolo-texto 0.5u.
  - Vertical (regla de 3): símbolo de 3u de alto; separación 1u;
    símbolo centrado sobre el ancho del texto.

Uso:
  python3 -m venv .venv && .venv/bin/pip install fonttools uharfbuzz
  .venv/bin/python scripts/brand.py --fonts <carpeta> [--guides <carpeta>]
La carpeta de fuentes debe tener CocoGothic-Bold_trial.ttf (o la versión
con licencia, renombrada igual) y Questrial.ttf.
"""
import argparse
import os

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

INK, SNOW, GREEN, GREEN_ON_DARK = '#121417', '#F1F5F9', '#1E523A', '#3A8A62'
SIZE = 100           # tamaño de fuente de referencia
PAD = 4              # margen del lienzo SVG
TRACK_MAIN = -0.01   # tracking de "leinerke" (em)
EXT_SCALE = 0.92     # tamaño de la extensión respecto a "leinerke"

ap = argparse.ArgumentParser()
ap.add_argument('--fonts', required=True)
ap.add_argument('--out', default=os.path.join(os.path.dirname(__file__), '..', 'public', 'brand'))
ap.add_argument('--guides', help='carpeta donde guardar las láminas con guías de construcción')
args = ap.parse_args()
MAIN = os.path.join(args.fonts, 'CocoGothic-Bold_trial.ttf')
EXT = os.path.join(args.fonts, 'Questrial.ttf')

_fonts = {}


def font(path):
    if path not in _fonts:
        _fonts[path] = (TTFont(path), hb.Font(hb.Face(hb.Blob.from_file_path(path))))
    return _fonts[path]


def run(path, text, size, track, x, base):
    """Texto a trazos. Devuelve (d, avance, caja de tinta [x0, y0, x1, y1])."""
    tt, hbf = font(path)
    upm = tt['head'].unitsPerEm
    gs, order = tt.getGlyphSet(), tt.getGlyphOrder()
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbf, buf, {'kern': True, 'liga': False})
    s, cx, d = size / upm, x, []
    bp = BoundsPen(gs)
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        t = (s, 0, 0, -s, cx + pos.x_offset * s, base - pos.y_offset * s)
        pen = SVGPathPen(gs)
        gs[order[info.codepoint]].draw(TransformPen(pen, t))
        gs[order[info.codepoint]].draw(TransformPen(bp, t))
        d.append(pen.getCommands())
        cx += pos.x_advance * s + track * size
    return ' '.join(d), cx - x - track * size, list(bp.bounds)


def glyph_box(path, ch):
    tt, _ = font(path)
    gs = tt.getGlyphSet()
    bp = BoundsPen(gs)
    gs[tt.getBestCmap()[ord(ch)]].draw(bp)
    return [v / tt['head'].unitsPerEm for v in bp.bounds]


lbox = glyph_box(MAIN, 'l')
STEM = lbox[2] - lbox[0]
U = lbox[3] * SIZE  # altura de la "l": la unidad de todas las proporciones


def wordmark(ext, ink, g, x=0.0, base=0.0):
    """leinerke + punto verde + extensión. Devuelve (svg, caja de tinta)."""
    d1, w1, b1 = run(MAIN, 'leinerke', SIZE, TRACK_MAIN, x, base)
    r = STEM * SIZE * 0.62
    gap = SIZE * 0.035
    cx = x + w1 + gap + r
    parts = [f'<path d="{d1}" fill="{ink}"/>', f'<circle cx="{cx:.2f}" cy="{base - r:.2f}" r="{r:.2f}" fill="{g}"/>']
    box = [b1[0], b1[1], cx + r, b1[3]]
    if ext:
        d2, _, b2 = run(EXT, ext, SIZE * EXT_SCALE, 0, cx + r + gap, base)
        parts.append(f'<path d="{d2}" fill="{ink}"/>')
        box = [min(box[0], b2[0]), min(box[1], b2[1]), max(box[2], b2[2]), max(box[3], b2[3])]
    # BoundsPen trabaja con y hacia arriba; tras la transformación ya es y hacia abajo
    return ''.join(parts), box


# Símbolo "l.": la caja visible mide 49.5 x 80 en su cuadro de 100
SYM_W, SYM_H = 49.5, 80


def symbol(ink, g, x, y, h):
    """Símbolo con su caja visible en (x, y) y alto visible h."""
    k = h / SYM_H
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{19 * k:.2f}" height="{80 * k:.2f}" rx="{9.5 * k:.2f}" fill="{ink}"/>'
            f'<circle cx="{x + 38 * k:.2f}" cy="{y + 68.5 * k:.2f}" r="{11.5 * k:.2f}" fill="{g}"/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}">{body}</svg>\n')


def horizontal(ext, ink, g):
    sh = 2 * U
    gap = 0.5 * U
    base = PAD + 1.5 * U            # el símbolo empieza en PAD y sobresale 0.5u sobre la "l"
    sx = PAD
    body, box = wordmark(ext, ink, g, 0, base)
    shift = sx + sh * SYM_W / SYM_H + gap - box[0]
    body, box = wordmark(ext, ink, g, shift, base)
    w = box[2] + PAD
    h = PAD + sh + PAD
    return svg(w, h, symbol(ink, g, sx, PAD, sh) + body), dict(base=base, sym=(sx, PAD, sh), box=box, w=w, h=h, gap=gap)


def vertical(ext, ink, g):
    sh = 3 * U
    gap = U
    base = PAD + sh + gap + U
    body, box = wordmark(ext, ink, g, 0, base)
    body, box = wordmark(ext, ink, g, PAD - box[0], base)
    text_w = box[2] - box[0]
    sw = sh * SYM_W / SYM_H
    sx = box[0] + (text_w - sw) / 2
    w = box[2] + PAD
    h = max(box[3], base) + PAD
    return svg(w, h, symbol(ink, g, sx, PAD, sh) + body), dict(base=base, sym=(sx, PAD, sh), box=box, w=w, h=h, gap=gap)


def guide_sheet(kind, geo, art):
    """Lámina con las líneas de construcción, al estilo de las referencias."""
    m = 60
    W, H = geo['w'] + 2 * m, geo['h'] + 2 * m
    red = '#E5484D'
    base, (sx, sy, sh), box = geo['base'] + m, geo['sym'], geo['box']
    sx, sy = sx + m, sy + m
    lines = []
    hline = lambda y, lab='': lines.append(
        f'<line x1="0" x2="{W}" y1="{y:.2f}" y2="{y:.2f}" stroke="{red}" stroke-width="1.4"/>'
        + (f'<text x="6" y="{y - 4:.2f}" font-family="monospace" font-size="13" fill="{red}">{lab}</text>' if lab else ''))
    vline = lambda x: lines.append(f'<line y1="0" y2="{H}" x1="{x:.2f}" x2="{x:.2f}" stroke="{red}" stroke-width="1.4"/>')
    if kind == 'horizontal':
        for i, y in enumerate([sy, base - U, base, sy + sh]):
            hline(y, ['símbolo', 'altura de la l', 'línea base', 'símbolo'][i])
        sym_r = sx + sh * SYM_W / SYM_H
        vline(sym_r)
        vline(sym_r + geo['gap'])
    else:
        for k in range(4):
            hline(sy + k * U, f'{k}u' if k else '')
        hline(base - U, 'altura de la l')
        hline(base, 'línea base')
        vline(box[0] + m)
        vline(box[2] + m)
        vline(sx + sh * SYM_W / SYM_H / 2)
    inner = art.split('>', 1)[1].rsplit('</svg>', 1)[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W * 2:.0f}" height="{H * 2:.0f}">'
            f'<rect width="100%" height="100%" fill="#F8F9FA"/><g transform="translate({m},{m})">{inner}</g>{"".join(lines)}</svg>\n')


os.makedirs(args.out, exist_ok=True)
for tone, ink, g in [('', INK, GREEN), ('-blanco', SNOW, GREEN_ON_DARK)]:
    open(os.path.join(args.out, f'simbolo{tone}.svg'), 'w').write(
        svg(100, 100, symbol(ink, g, (100 - SYM_W) / 2, 10, 80)))
    for ext in ['', 'studio', 'raw']:
        name = 'leinerke' + (f'.{ext}' if ext else '')
        body, box = wordmark(ext, ink, g, 0, PAD + U)
        body, box = wordmark(ext, ink, g, PAD - box[0], PAD + U)
        open(os.path.join(args.out, f'wordmark-{name}{tone}.svg'), 'w').write(svg(box[2] + PAD, box[3] + PAD, body))
        for kind, fn in [('horizontal', horizontal), ('vertical', vertical)]:
            art, geo = fn(ext, ink, g)
            open(os.path.join(args.out, f'logo-{kind}-{name}{tone}.svg'), 'w').write(art)
            if args.guides and tone == '' and ext == 'studio':
                os.makedirs(args.guides, exist_ok=True)
                open(os.path.join(args.guides, f'guia-{kind}.svg'), 'w').write(guide_sheet(kind, geo, art))
print('Listo:', os.path.abspath(args.out))
