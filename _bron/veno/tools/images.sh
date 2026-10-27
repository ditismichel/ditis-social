#!/bin/bash
# Haalt beeld van venostal.com op voor de mockup van de nieuwe homepage.
# Aanroep: bash _bron/veno/tools/images.sh
I=/Users/michelgoulmy/Sites/ditis-social/_bron/veno/mockup/img
mkdir -p $I
U=https://www.venostal.com/wp-content/uploads
get(){ curl -sS -L --max-time 60 "$U/$1" -o "$I/$2"; echo "$2 $(wc -c < $I/$2)"; }
get 2020/03/veno-logo.png logo.png
get 2016/12/Overzicht-foto-brochure-website-1.jpg overzicht.jpg
get 2024/05/Thumbnail-voerhekken-voor-schapen-en-geiten.webp voerhekken.webp
get 2024/05/Thumbnail-schapenhekken-en-geitenhekken.webp hekken.webp
get 2024/05/Thumbnail-kraamhokken-en-toebehoren.webp kraamhokken.webp
get 2024/05/Thumbnail-voergoten-en-hooiruiven.webp voergoten.webp
get 2021/01/Behandelsystemen-Thumbnail.jpg behandel.jpg
get 2024/06/Thumbnail-Drinkbakken.webp drinkbakken.webp
get 2024/05/Thumbnail-weegbalken-en-loadcells-910x683.webp weegbalken.webp
get 2024/06/Thumbnail-Multifunctionele-Schapen-Trailer-910x683.webp trailer.webp
get 2026/04/Thumbnail-Te-Pari-910x683.webp tepari.webp
get 2026/03/Thumbnail-Universal-Feeders-910x683.webp feeders.webp
get 2024/12/Alpaca-Stalinrichting-910x683.webp alpaca.webp
# hero: grootste afbeelding uit de slider op de homepage
H=$(grep -o -E "$U/[^\"' )]+\.(jpg|jpeg|webp)" /Users/michelgoulmy/Sites/ditis-social/_bron/veno/raw/home.html | grep -i -E 'slide|banner|header|hero|schapen|sheep' | head -3)
echo "hero-kandidaten: $H"
