#!/usr/bin/env python3
"""Vervangt de voorproef-telefoon in de hero van body.html door de videospeler uit de DoubleFOnline-pitch.
Aanroep: python3 -I _bron/veno/tools/hero-video.py <duur m:ss> <seconden>"""
import pathlib, re, sys

dur, sec = sys.argv[1], int(sys.argv[2])
R = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social")
body = R / "_bron/veno/body.html"
src = (R / "doublefonline/index.html").read_text()
m = re.search(r'    <div class="phone"><div class="vwrap" id="vwrap">.*?</script>\n', src, re.S)
player = m.group(0)
player = player.replace("media/ditisabc-voor-doublefonline.mp4", "media/ditisabc-voor-veno.mp4")
player = re.sub(r"Video · \d:\d\d", "Video · " + dur, player)
player = re.sub(r"Michel legt het uit in \d:\d\d", "Michel legt het uit in " + dur, player)
player = re.sub(r'aria-label="Speel de video af, [^"]+"', f'aria-label="Speel de video af, {sec} seconden"', player)
s = body.read_text()
old = re.search(r'    <div class="phone"><div class="scr" tabindex="0" aria-label="Voorproef van de nieuwe homepage op een telefoon, scrollbaar">.*?<div class="pcap">.*?</div>\n', s, re.S)
assert old, "hero-telefoon niet gevonden"
body.write_text(s.replace(old.group(0), player))
print("hero vervangen door videospeler,", dur)
