#!/usr/bin/env python3
"""Bouwt <SLUG>/index.html uit body.html + extra.css, met stijl, partnerblok en scripts van doublefonline.

Aanroep (vanuit de repo-root): python3 -I _bron/racesensation/build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Unieke slug: niet te raden voor andere Foome-klanten
SLUG = "racesensation-st8de2"
src = open(os.path.join(ROOT, "doublefonline/index.html")).read()
here = os.path.join(ROOT, "_bron/racesensation")
body = open(os.path.join(here, "body.html")).read()
extra = open(os.path.join(here, "extra.css")).read()

css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
head = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Race Sensation en ditisABC: zo gaan we verder | ditisABC</title>
<meta name="description" content="Wat we voor Race Sensation deden, waar de site nu staat in Google en AI, en hoe ditisABC verdergaat vanaf 1 november.">
<meta property="og:title" content="Race Sensation en ditisABC: zo gaan we verder | ditisABC">
<meta property="og:description" content="Meer racedagen via je eigen site. Wat we deden, waar je staat en wat we voorstellen.">
<meta property="og:image" content="https://ditis.marketing/{SLUG}/media/og.jpg">
<meta property="og:url" content="https://ditis.marketing/{SLUG}/">
<style>{css}{extra}</style>
</head>
"""

partners = re.search(r'(<section id="partners".*?</section>\s*<section id="nieuwsbrief".*?</section>\s*<section id="volg".*?</section>)', src, re.S).group(1)
# klanten: webshops en beleving vooraan
kl = re.findall(r'    <a class="klant".*?</a>\n', partners, re.S)
order = ["candyfestival", "miffytown", "glansz", "offgridpowerstation", "thebastard", "deruijtermeubel", "de-centrale", "karinbloemenstichting", "culemborg"]
kl_sorted = sorted(kl, key=lambda k: next(i for i, o in enumerate(order) if o in k))
partners = partners.replace("".join(kl), "".join(kl_sorted))

gcal = re.search(r"(/\* Afspraak plannen.*?\}\)\(\);)", src, re.S).group(1)
gcal = gcal.replace("show('bel')", "show('hil')")
track = re.search(r"(<script>\n/\* Bezoekmelding.*?</script>)", src, re.S).group(1)
track = track.replace("PAGE='doublefonline'", "PAGE='racesensation'")

out = head + body.replace("@@PARTNERS@@", partners).replace("@@GCAL@@", gcal).replace("@@TRACK@@", track)
assert "@@" not in out
assert "—" not in out, "em-dash gevonden"
for w in ("kosten", "eerlijk", "napersen", "korting", "promptwatch"):
    assert not re.search(r"\b" + w + r"\b", out.lower()), "verboden woord: " + w
open(os.path.join(ROOT, SLUG, "index.html"), "w").write(out)
print("ok", len(out))
