#!/bin/bash
# Maakt de screenshots voor de ABI-pitch en zet ze verkleind in abi-5vbx32/media.
# Aanroep: bash /Users/michelgoulmy/Sites/ditis-social/_bron/abi/tools/screens.sh
D=/Users/michelgoulmy/Sites/ditis-social
SLUG=abi-5vbx32
R=$D/_bron/abi/raw
M=$D/$SLUG/media
T=$D/_bron/jovetra/tools
mkdir -p $R $M
# vaste media uit de Jovetra-pitch
for f in ditisabc-logo.svg michel.webp team.jpg anouk.jpg; do cp $D/jovetra-8hhtzv/media/$f $M/; done
cp -R $D/jovetra-8hhtzv/media/badges $D/jovetra-8hhtzv/media/klanten $M/
cp $D/michel/media/romy.jpg $M/romy.jpg
# logo ABI
curl -s -L -A "Mozilla/5.0" https://www.abi.nl/ -o $R/abi-home.html
grep -o -i -E '(src|href)="[^"]*logo[^"]*"' $R/abi-home.html | head -5
# screenshots
node $T/capture.js https://abi.foome.nl/ $R/nieuw-desk.png desktop volledig
node $T/capture.js https://abi.foome.nl/ $R/nieuw-mob.png mobiel volledig
node $T/capture.js https://www.abi.nl/ $R/oud-desk.png desktop
node $T/capture.js https://www.abi.nl/ $R/oud-mob.png mobiel
node $T/capture.js https://use-poultry-tech.com/ $R/ref-use.png
node $T/capture.js https://dutch-poultry-tech.com/ $R/ref-dpt.png
sips -s format jpeg -s formatOptions 78 -Z 6000 $R/nieuw-desk.png --out $R/nieuw-desk.jpg >/dev/null
sips -s format jpeg -s formatOptions 78 -Z 9000 $R/nieuw-mob.png --out $R/nieuw-mob.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 1200 $R/oud-desk.png --out $M/oud-desk.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 844 $R/oud-mob.png --out $M/oud-mob.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 1200 $R/ref-use.png --out $M/ref-use.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 1200 $R/ref-dpt.png --out $M/ref-dpt.jpg >/dev/null
sips -g pixelWidth -g pixelHeight $R/nieuw-desk.png $R/nieuw-mob.png
ls -la $M
