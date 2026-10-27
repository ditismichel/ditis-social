#!/usr/bin/env python3
"""Bouwt jovetra/index.html uit body.html + extra.css, met stijl, partnerblok en scripts van doublefonline.

Aanroep (vanuit de repo-root): python3 -I _bron/jovetra/build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(ROOT, "doublefonline/index.html")).read()
here = os.path.join(ROOT, "_bron/jovetra")
body = open(os.path.join(here, "body.html")).read()
extra = open(os.path.join(here, "extra.css")).read()

css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
head = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Een snelle site voor Jovetra | ditisABC</title>
<meta name="description" content="Wat ditisABC zag op jovetra.nl: snelheid, Google en AI, en hoe een nieuwe site eruit kan zien.">
<meta property="og:title" content="Een snelle site voor Jovetra | ditisABC">
<meta property="og:description" content="Ons antwoord op de vraag van Ruud: hoe wordt Jovetra gevonden in Google en AI?">
<meta property="og:image" content="https://www.ditis.website/jovetra/media/og.jpg">
<meta property="og:url" content="https://www.ditis.website/jovetra/">
<style>{css}{extra}</style>
</head>
"""

partners = re.search(r'(<section id="partners".*?</section>\s*<section id="nieuwsbrief".*?</section>\s*<section id="volg".*?</section>)', src, re.S).group(1)
# klanten: zakelijke klanten vooraan
kl = re.findall(r'    <a class="klant".*?</a>\n', partners, re.S)
order = ["offgridpowerstation", "culemborg", "de-centrale", "deruijtermeubel", "candyfestival", "miffytown", "glansz", "thebastard", "karinbloemenstichting"]
kl_sorted = sorted(kl, key=lambda k: next(i for i, o in enumerate(order) if o in k))
partners = partners.replace("".join(kl), "".join(kl_sorted))

gcal = re.search(r"(/\* Afspraak plannen.*?\}\)\(\);)", src, re.S).group(1)
gcal = gcal.replace("show('bel')", "show('hil')")
track = re.search(r"(<script>\n/\* Bezoekmelding.*?</script>)", src, re.S).group(1)
track = track.replace("PAGE='doublefonline'", "PAGE='jovetra'")

out = head + body.replace("@@PARTNERS@@", partners).replace("@@GCAL@@", gcal).replace("@@TRACK@@", track)
assert "@@" not in out
assert "—" not in out, "em-dash gevonden"
open(os.path.join(ROOT, "jovetra/index.html"), "w").write(out)
print("ok", len(out))
