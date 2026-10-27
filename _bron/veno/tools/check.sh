#!/bin/bash
# Rendert de lokale Veno-pitch volledig (desktop en mobiel) en knipt hem in stukken om te bekijken.
# Aanroep: bash _bron/veno/tools/check.sh   (preview-server op poort 4321 moet draaien)
R=/Users/michelgoulmy/Sites/ditis-social/_bron/veno/raw/check
C=/Users/michelgoulmy/Sites/ditis-social/_bron/bekendvermogen/tools/capture.js
mkdir -p $R
rm -f $R/*.jpg
node $C "http://localhost:4321/veno/?ik=1" $R/desk.png desktop volledig
node $C "http://localhost:4321/veno/?ik=1" $R/mob.png mobiel volledig
H=$(sips -g pixelHeight $R/desk.png | awk '/pixelHeight/{print $2}')
echo "desktop hoogte $H"
i=0; y=0
while [ $y -lt $H ]; do
  ffmpeg -loglevel error -y -i $R/desk.png -vf "crop=1440:min(1800\,ih-$y):0:$y,scale=900:-1" -q:v 5 $R/d$i.jpg
  y=$((y+1800)); i=$((i+1))
done
HM=$(sips -g pixelHeight $R/mob.png | awk '/pixelHeight/{print $2}')
echo "mobiel hoogte $HM"
i=0; y=0
while [ $y -lt $HM ]; do
  ffmpeg -loglevel error -y -i $R/mob.png -vf "crop=780:min(3200\,ih-$y):0:$y,scale=390:-1" -q:v 5 $R/m$i.jpg
  y=$((y+3200)); i=$((i+1))
done
ls $R
