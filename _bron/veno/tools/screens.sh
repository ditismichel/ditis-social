#!/bin/bash
# Screenshots van venostal.com voor de Veno-pitch, plus logo en kleuren uit de HTML.
# Aanroep: bash _bron/veno/tools/screens.sh
D=/Users/michelgoulmy/Sites/ditis-social
R=$D/_bron/veno/raw
M=$D/veno/media
C=$D/_bron/bekendvermogen/tools/capture.js
mkdir -p $R $M
node $C https://www.venostal.com/nl/ $R/desk.png desktop
node $C https://www.venostal.com/nl/ $R/desk-full.png desktop volledig
node $C https://www.venostal.com/nl/ $R/mob.png mobiel
PROD=$(curl -sS https://www.venostal.com/nl/shop/ | grep -o -E 'https://www.venostal.com/nl/product/[a-z0-9-]+/' | head -1)
echo "product: $PROD"
node $C "$PROD" $R/prod-mob.png mobiel
node $C https://www.venostal.com/nl/dealers/ $R/dealers.png desktop
sips -s format jpeg -s formatOptions 80 -Z 844 $R/mob.png --out $M/mob.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 844 $R/prod-mob.png --out $M/prod-mob.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 1440 $R/desk.png --out $M/desk.jpg >/dev/null
curl -sS https://www.venostal.com/nl/ > $R/home.html
echo "--- logo-kandidaten"
grep -o -E 'https://www.venostal.com/wp-content/uploads/[^"'"'"' ]*(logo|Logo|LOGO)[^"'"'"' ]*' $R/home.html | sort -u | head
echo "--- kleuren (top)"
grep -o -E '#[0-9a-fA-F]{6}\b' $R/home.html | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -12
echo "--- fonts"
grep -o -E 'font-family:[^;"]{3,60}' $R/home.html | sort | uniq -c | sort -rn | head -6
echo "--- og:image"
grep -o -E 'og:image" content="[^"]+' $R/home.html | head -2
