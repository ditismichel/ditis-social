#!/bin/bash
# Maakt alle screenshots voor de Bekend Vermogen-pitch en zet ze verkleind in bekendvermogen/media.
# Aanroep: bash _bron/bekendvermogen/tools/screens.sh
D=/Users/michelgoulmy/Sites/ditis-social
R=$D/_bron/bekendvermogen/raw
M=$D/bekendvermogen/media
T=$D/_bron/bekendvermogen/tools
node $T/capture.js https://bekendvermogen.nl/ $R/mob.png mobiel
node $T/capture.js https://bekendvermogen.nl/ $R/desk.png
node $T/capture.js https://avinta.nl/ $R/ref-avinta.png
node $T/capture.js https://manders.tax/ $R/ref-manders.png
sips -s format jpeg -s formatOptions 80 -Z 844 $R/mob.png --out $M/mob.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 1200 $R/ref-avinta.png --out $M/ref-avinta.jpg >/dev/null
sips -s format jpeg -s formatOptions 80 -Z 1200 $R/ref-manders.png --out $M/ref-manders.jpg >/dev/null
i=0
for n in robin daisy tjeerd roos; do
  i=$((i+1))
  sips -s format jpeg -s formatOptions 82 -Z 360 $R/team$i.png --out $M/$n.jpg >/dev/null
done
sips -s format jpeg -s formatOptions 80 -Z 900 $R/kantoor.jpg --out $M/kantoor.jpg >/dev/null
ls -la $M
