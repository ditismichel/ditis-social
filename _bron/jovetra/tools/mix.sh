#!/bin/bash
# Mixt stem + muziekbed en voegt samen met de stille video.
# Aanroep: bash tools/mix.sh   (vanuit _bron/bekendvermogen)
# Stem -16 LUFS, muziek -27 LUFS met sidechain onder de stem, 3 sec uitfaden, limiter op de som.
set -e
B=/Users/michelgoulmy/Sites/ditis-social/_bron/bekendvermogen
OUT=/Users/michelgoulmy/Sites/ditis-social/bekendvermogen/media
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $B/out/video_silent.mp4)
MUZIEK=${MUZIEK:-music2.mp3}
MDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $B/audio/$MUZIEK)
# muziek korter dan video: iets vertragen (atempo, zelfde toonhoogte) zodat het slot van de muziek op het einde valt
TEMPO=$(python3 -c "print(round(max(0.8,min(1.0,$MDUR/$DUR)),4))")
FADE=$(python3 -c "print(round($DUR-3,2))")
STEM=${STEM:-take6.mp3}
MUZIEK=${MUZIEK:-music2.mp3}
ffmpeg -y -loglevel error -i $B/audio/$STEM -i $B/audio/$MUZIEK -filter_complex "\
[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur=$DUR,asplit=2[v][vsc];\
[1:a]atempo=$TEMPO,loudnorm=I=-27:TP=-2:LRA=11,aresample=48000,atrim=0:$DUR,afade=t=out:st=$FADE:d=3[m];\
[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];\
[v][md]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,atrim=0:$DUR[a]" -map "[a]" -c:a pcm_s16le $B/audio/mix.wav
ffmpeg -y -loglevel error -i $B/out/video_silent.mp4 -i $B/audio/mix.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart $OUT/ditisabc-voor-bekendvermogen.mp4
POSTER=1 node $B/tools/render.js $B/video/video.html --stills 0.7
sips -s format jpeg -s formatOptions 85 -Z 1280 $B/video/still-0.7.jpg --out $OUT/poster.jpg >/dev/null
ls -la $OUT/ditisabc-voor-bekendvermogen.mp4 $OUT/poster.jpg
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/ditisabc-voor-bekendvermogen.mp4
