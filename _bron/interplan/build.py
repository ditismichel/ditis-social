#!/usr/bin/env python3
"""Bouwt <SLUG>/index.html uit body.html + extra.css, met stijl, partnerblok en scripts van doublefonline.

Aanroep (vanuit de repo-root): python3 -I _bron/interplan/build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Unieke slug: niet te raden voor andere Foome-klanten
SLUG = "interplan-488we5"
src = open(os.path.join(ROOT, "doublefonline/index.html")).read()
here = os.path.join(ROOT, "_bron/interplan")
body = open(os.path.join(here, "body.html")).read()
extra = open(os.path.join(here, "extra.css")).read()

css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
head = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Interplan en ditisABC: zo gaan we verder | ditisABC</title>
<meta name="description" content="Wat er loopt op LinkedIn voor Interplan Bouwsupport en Interplan Projecten, en hoe ditisABC verdergaat vanaf 1 november.">
<meta property="og:title" content="Interplan en ditisABC: zo gaan we verder | ditisABC">
<meta property="og:description" content="Jullie mensen zijn jullie beste posts. Wat er loopt, wat werkt en wat we voorstellen.">
<meta property="og:image" content="https://www.ditis.social/{SLUG}/media/og.jpg">
<meta property="og:url" content="https://www.ditis.social/{SLUG}/">
<style>{css}{extra}</style>
</head>
"""

partners = re.search(r'(<section id="partners".*?</section>\s*<section id="nieuwsbrief".*?</section>\s*<section id="volg".*?</section>)', src, re.S).group(1)
# klanten: zakelijke klanten vooraan
kl = re.findall(r'    <a class="klant".*?</a>\n', partners, re.S)
order = ["culemborg", "offgridpowerstation", "de-centrale", "deruijtermeubel", "karinbloemenstichting", "candyfestival", "miffytown", "glansz", "thebastard"]
kl_sorted = sorted(kl, key=lambda k: next(i for i, o in enumerate(order) if o in k))
partners = partners.replace("".join(kl), "".join(kl_sorted))

gcal = re.search(r"(/\* Afspraak plannen.*?\}\)\(\);)", src, re.S).group(1)
gcal = gcal.replace("show('bel')", "show('hil')")
track = re.search(r"(<script>\n/\* Bezoekmelding.*?</script>)", src, re.S).group(1)
track = track.replace("PAGE='doublefonline'", "PAGE='interplan'")

out = head + body.replace("@@PARTNERS@@", partners).replace("@@GCAL@@", gcal).replace("@@TRACK@@", track)
assert "@@" not in out
assert "—" not in out, "em-dash gevonden"
# los woord; "bouwkostenadviseur" is de vakterm van de klant en mag
for w in ("kosten", "eerlijk", "napersen", "korting"):
    assert not re.search(r"\b" + w + r"\b", out.lower()), "verboden woord: " + w
open(os.path.join(ROOT, SLUG, "index.html"), "w").write(out)
print("ok", len(out))
