#!/bin/bash
# Zet fonts, vaste beelden en mockup-renders klaar in veno/.
# Aanroep: bash _bron/veno/tools/media.sh
D=/Users/michelgoulmy/Sites/ditis-social
S=$D/doublefonline
V=$D/veno
R=$D/_bron/veno/raw
mkdir -p $V/fonts $V/media
cp $S/fonts/* $V/fonts/
cp -R $S/media/badges $S/media/klanten $V/media/
cp $S/media/team.jpg $S/media/michel.webp $S/media/ditisabc-logo.svg $V/media/
cp $D/_bron/veno/mockup/img/logo.png $V/media/veno-logo.png
sips -s format jpeg -s formatOptions 78 --resampleWidth 1200 $R/mock-desk.png --out $V/media/mock-desk.jpg >/dev/null
sips -s format jpeg -s formatOptions 78 --resampleWidth 390 $R/mock-mob.png --out $V/media/mock-mob.jpg >/dev/null
ffmpeg -loglevel error -y -i $R/mock-desk.png -vf "crop=1440:720:0:0,scale=1200:600" -q:v 4 $V/media/og.jpg
ls -la $V/media | head -30
