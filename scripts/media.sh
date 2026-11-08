#!/bin/zsh
# Genera las versiones web de fotos y reels a partir de los originales.
# Uso: zsh scripts/media.sh   (los originales no se modifican)
set -e
P="$HOME/Sites/claude/instagram-automatizacion/posts"
C="$P/2026-10-25-carrera"
V="$HOME/Movies/dist"
OUT="${0:A:h}/../public/media"
mkdir -p "$OUT/img" "$OUT/video"

photo() { # origen, nombre
  for w in 800 1600; do
    [[ -f "$OUT/img/$2-$w.jpg" ]] || magick "$1" -resize "${w}x${w}>" -strip -quality 80 -interlace Plane "$OUT/img/$2-$w.jpg"
  done
}
reel() { # origen, nombre, segundo de inicio del preview
  [[ -f "$OUT/video/$2-preview.mp4" ]] || ffmpeg -v error -y -ss $3 -t 8 -i "$1" -an -vf "scale=540:-2,fps=30" -c:v libx264 -pix_fmt yuv420p -crf 28 -preset slow -movflags +faststart "$OUT/video/$2-preview.mp4"
  [[ -f "$OUT/video/$2.mp4" ]] || ffmpeg -v error -y -i "$1" -vf "scale=720:-2" -c:v libx264 -pix_fmt yuv420p -crf 26 -preset slow -c:a aac -b:a 128k -movflags +faststart "$OUT/video/$2.mp4"
  [[ -f "$OUT/video/$2-poster.jpg" ]] || ffmpeg -v error -y -ss $(($3+1)) -i "$1" -frames:v 1 -vf "scale=720:-2" -q:v 4 "$OUT/video/$2-poster.jpg"
}

# .raw — válida del 25 de octubre (números según seleccion.md)
photo "$C/serie-1/DSC00642.jpg" raw-828
photo "$C/serie-4/DSC09636.jpg" raw-35
photo "$C/serie-1/DSC08844.jpg" raw-514
photo "$C/serie-1/DSC07739.jpg" raw-707
photo "$C/serie-1/DSC00541.jpg" raw-189
photo "$C/serie-4/DSC08690.jpg" raw-33
photo "$C/serie-4/DSC09031.jpg" raw-28
photo "$C/serie-1/DSC00173.jpg" raw-1
photo "$C/serie-1/DSC08792.jpg" raw-4

# .studio — portadas de la grilla
photo "$P/Blessed Express (@blessedexpress_)/DSC08765.jpg" st-blessed
photo "$P/Carola’s Creative (@carolas.creative)/DSC08245.jpg" st-carolas-bebidas
photo "$P/Carola’s Creative (@carolas.creative)/DSC08422.jpg" st-carolas-carta
photo "$P/Carola’s Creative (@carolas.creative)/DSC08396.jpg" st-carolas-pitas
photo "$P/La golosa postres (@lagolosa.postres)/DSC08141.jpg" st-golosa-torta
photo "$P/La golosa postres (@lagolosa.postres)/DSC08184.jpg" st-golosa-productos
photo "$P/Pizzería Artesanal en leña (@pizza.en.lena)/DSC07050.jpg" st-pizza
photo "$P/Ruta 60 Biker Barber (@ruta60bikerbarber)/DSC07541.jpg" st-ruta60-resultado
photo "$P/Ruta 60 Biker Barber (@ruta60bikerbarber)/DSC07332.jpg" st-ruta60-proceso

# Retrato para "Sobre mí"
photo "$HOME/.claude/uploads/20de673c-b8ae-46a6-9368-8fc10bea4210/f3b200fd-image.jpg" retrato

# Reels
reel "$V/pizza en lena/00-demostracion/Hero 1.mov" pizza-hero 2
reel "$V/pan y fuego/demostracion.mov" pan-y-fuego 20
reel "$V/Cocina de Franco.mov" cocina-de-franco 12
reel "$V/pizza en lena/00-demostracion/review.mov" pizza-resena 4
echo "Listo: $OUT"
