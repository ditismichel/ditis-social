#!/usr/bin/env python3
"""Bouwt <SLUG>/index.html uit body.html + extra.css, met stijl, partnerblok en scripts van doublefonline.

Aanroep (vanuit de repo-root): python3 -I _bron/abi/build.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Unieke slug: niet te raden voor andere Foome-klanten
SLUG = "abi-5vbx32"
src = open(os.path.join(ROOT, "doublefonline/index.html")).read()
here = os.path.join(ROOT, "_bron/abi")
body = open(os.path.join(here, "body.html")).read()
extra = open(os.path.join(here, "extra.css")).read()

css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
head = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Wat we doen voor ABI | ditisABC</title>
<meta name="description" content="Wat Foome en ditisABC voor ABI deden en waar we nu aan werken.">
<meta property="og:title" content="Wat we doen voor ABI | ditisABC">
<meta property="og:description" content="Socials, beeld, drukwerk, de nieuwe website en Direct Drive: wat er gedaan is en wat er nu loopt.">
<meta property="og:image" content="https://www.ditis.website/{SLUG}/media/og.jpg">
<meta property="og:url" content="https://www.ditis.website/{SLUG}/">
<style>{css}{extra}</style>
</head>
"""

partners = re.search(r'(<section id="partners".*?</section>\s*<section id="nieuwsbrief".*?</section>\s*<section id="volg".*?</section>)', src, re.S).group(1)
# klanten: zakelijke klanten vooraan
kl = re.findall(r'    <a class="klant".*?</a>\n', partners, re.S)
order = ["offgridpowerstation", "culemborg", "de-centrale", "deruijtermeubel", "candyfestival", "miffytown", "glansz", "thebastard", "karinbloemenstichting"]
kl_sorted = sorted(kl, key=lambda k: next(i for i, o in enumerate(order) if o in k))
partners = partners.replace("".join(kl), "".join(kl_sorted))
# partner voor ABI: Bakker Studios (video en fotografie)
bakker = """    <div class="badge bakker">
      <img src="media/badges/bakker-studios.svg" alt="Bakker Studios" width="659" height="182" loading="lazy">
      <small>Video en fotografie</small>
    </div>
"""
wp = re.search(r'<b>WordPress</b>.*?</small>\n    </div>\n', partners, re.S)
partners = partners[:wp.end()] + bakker + partners[wp.end():]
assert "bakker-studios.svg" in partners

gcal = re.search(r"(/\* Afspraak plannen.*?\}\)\(\);)", src, re.S).group(1)
gcal = gcal.replace("show('bel')", "show('hil')")
track = re.search(r"(<script>\n/\* Bezoekmelding.*?</script>)", src, re.S).group(1)
track = track.replace("PAGE='doublefonline'", "PAGE='abi'")

out = head + body.replace("@@PARTNERS@@", partners).replace("@@GCAL@@", gcal).replace("@@TRACK@@", track)
assert "@@" not in out
assert "—" not in out, "em-dash gevonden"
open(os.path.join(ROOT, SLUG, "index.html"), "w").write(out)
print("ok", len(out))
