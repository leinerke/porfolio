"""Genera la identidad de LEINERKE en SVG, con el texto convertido a trazos.

Logotipo: "LEINERKE" en Michroma (SIL OFL 1.1, uso comercial libre),
tracking 0.2 em, con la I en verde tierra como único detalle propio.

Unidad de construcción u = altura de mayúscula.
  - Descriptor (STUDIO / RAW): alto 0.32u, justificado al ancho del logotipo,
    separado 0.6u por debajo.
  - Símbolo: la L con la I verde dentro de su esquina; cuadrado ópticamente.
  - Espacio de respeto: 1u alrededor de cualquier versión.

Uso:
  python3 -m venv .venv && .venv/bin/pip install fonttools uharfbuzz
  .venv/bin/python scripts/brand.py --fonts <carpeta con Michroma.ttf>
"""
import argparse
import os

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

PALETTE = {
    'ink': '#121417',      # Negro carbón
    'paper': '#F8F9FA',    # Papel
    'snow': '#F1F5F9',     # Blanco para fondos oscuros
    'green': '#1E523A',    # Verde tierra (racing green)
    'green_on_dark': '#3A8A62',
}
SIZE = 100
TRACK = 0.2

ap = argparse.ArgumentParser()
ap.add_argument('--fonts', required=True)
ap.add_argument('--out', default=os.path.join(os.path.dirname(__file__), '..', 'public', 'brand'))
args = ap.parse_args()
FONT = os.path.join(args.fonts, 'Michroma.ttf')

tt = TTFont(FONT)
hbf = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
UPM = tt['head'].unitsPerEm
GS, ORDER = tt.getGlyphSet(), tt.getGlyphOrder()


def shape(text, size, track, x, base):
    """Lista de (path d, caja de tinta) por letra, y el avance total."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbf, buf, {'kern': True, 'liga': False})
    s, cx, out = size / UPM, x, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        t = (s, 0, 0, -s, cx + pos.x_offset * s, base - pos.y_offset * s)
        pen, bp = SVGPathPen(GS), BoundsPen(GS)
        GS[ORDER[info.codepoint]].draw(TransformPen(pen, t))
        GS[ORDER[info.codepoint]].draw(TransformPen(bp, t))
        out.append((pen.getCommands(), bp.bounds))
        cx += pos.x_advance * s + track * size
    return out, cx - x - track * size


CAP = GS[tt.getBestCmap()[ord('L')]]
_bp = BoundsPen(GS)
CAP.draw(_bp)
U = _bp.bounds[3] / UPM * SIZE  # altura de mayúscula


def union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def wordmark(ink, accent, x=0.0, base=0.0):
    glyphs, _ = shape('LEINERKE', SIZE, TRACK, x, base)
    body = ''.join(f'<path d="{d}" fill="{accent if i == 2 else ink}"/>' for i, (d, _) in enumerate(glyphs))
    return body, union([b for _, b in glyphs])


def descriptor(text, ink, x0, x1, base):
    """Texto pequeño justificado exactamente entre x0 y x1."""
    size = 0.32 * U / (U / SIZE)
    glyphs, _ = shape(text, size, 0, 0, 0)
    natural = union([b for _, b in glyphs])
    gaps = len(text) - 1
    extra = ((x1 - x0) - (natural[2] - natural[0])) / gaps / size if gaps else 0
    glyphs, _ = shape(text, size, extra, 0, base)
    box = union([b for _, b in glyphs])
    dx = x0 - box[0]
    return f'<g transform="translate({dx:.2f} 0)">' + ''.join(f'<path d="{d}" fill="{ink}"/>' for d, _ in glyphs) + '</g>'


def svg(box, body, pad):
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    w, h = x1 - x0, y1 - y0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}">{body}</svg>\n')


def symbol(ink, accent):
    """La L de Michroma con la I verde en su esquina interior."""
    (l_path, lb), = shape('L', SIZE, 0, 0, U)[0]
    (i_path, ib), = shape('I', SIZE, 0, 0, U)[0]
    stem = ib[2] - ib[0]
    # La I se apoya sobre el pie de la L, centrada en el espacio interior
    foot = stem  # Michroma usa el mismo grosor en horizontales y verticales
    inner_x0, inner_x1 = lb[0] + stem, lb[2]
    ih = 0.62 * U
    ix = inner_x0 + (inner_x1 - inner_x0 - stem) / 2
    iy = U - foot - stem * 0.9 - ih
    i_shape = f'<rect x="{ix:.2f}" y="{iy:.2f}" width="{stem:.2f}" height="{ih:.2f}" fill="{accent}"/>'
    side = max(lb[2] - lb[0], U)
    box = [lb[0] - (side - (lb[2] - lb[0])) / 2, 0, lb[0] - (side - (lb[2] - lb[0])) / 2 + side, U]
    return f'<path d="{l_path}" fill="{ink}"/>' + i_shape, box


def write(name, content):
    open(os.path.join(args.out, name), 'w').write(content)


os.makedirs(args.out, exist_ok=True)
variants = {
    '': (PALETTE['ink'], PALETTE['green']),
    '-blanco': (PALETTE['snow'], PALETTE['green_on_dark']),
    '-negro': (PALETTE['ink'], PALETTE['ink']),          # una tinta
    '-blanco-una-tinta': ('#FFFFFF', '#FFFFFF'),
}
pad = U  # espacio de respeto incluido en el archivo
for suffix, (ink, accent) in variants.items():
    body, box = wordmark(ink, accent, 0, U)
    write(f'logo-leinerke{suffix}.svg', svg(box, body, pad))
    if suffix in ('', '-blanco'):
        # Sin espacio de respeto: para interfaces (header de la web), donde el layout ya da el aire
        write(f'logo-leinerke{suffix}-sin-margen.svg', svg(box, body, 0))
    for sub in ['STUDIO', 'RAW']:
        base = U + 0.6 * U + 0.32 * U
        d = descriptor(sub, ink if suffix else PALETTE['ink'], box[0], box[2], base)
        write(f'logo-leinerke-{sub.lower()}{suffix}.svg', svg([box[0], box[1], box[2], base], body + d, pad))
    sym, sbox = symbol(ink, accent)
    write(f'simbolo{suffix}.svg', svg(sbox, sym, pad * 0.6))

# Avatares para Instagram: .studio claro, .raw oscuro (cuadrado; IG recorta en círculo)
for name, bg, ink, accent in [('avatar-studio', PALETTE['paper'], PALETTE['ink'], PALETTE['green']),
                              ('avatar-raw', PALETTE['ink'], PALETTE['snow'], PALETTE['green_on_dark'])]:
    sym, sbox = symbol(ink, accent)
    side = (sbox[2] - sbox[0]) / 0.42
    cx, cy = (sbox[0] + sbox[2]) / 2, (sbox[1] + sbox[3]) / 2
    x0, y0 = cx - side / 2, cy - side / 2
    write(f'{name}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {side:.2f} {side:.2f}" width="1080" height="1080">'
                         f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{side:.2f}" height="{side:.2f}" fill="{bg}"/>{sym}</svg>\n')

# Favicon: símbolo sobre carbón, esquinas redondeadas
sym, sbox = symbol(PALETTE['snow'], PALETTE['green_on_dark'])
side = (sbox[2] - sbox[0]) / 0.62
cx, cy = (sbox[0] + sbox[2]) / 2, (sbox[1] + sbox[3]) / 2
x0, y0 = cx - side / 2, cy - side / 2
open(os.path.join(args.out, '..', 'favicon.svg'), 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {side:.2f} {side:.2f}">'
    f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{side:.2f}" height="{side:.2f}" rx="{side * 0.22:.2f}" fill="{PALETTE["ink"]}"/>{sym}</svg>\n')
print('Listo:', os.path.abspath(args.out))
