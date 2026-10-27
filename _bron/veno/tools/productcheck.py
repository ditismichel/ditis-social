#!/usr/bin/env python3
"""Telt op venostal.com: producten met prijs 0,00 en zonder productfoto (steekproef via de sitemap).
Aanroep: python3 -I _bron/veno/tools/productcheck.py [aantal]"""
import re, sys, urllib.request, random

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) Chrome/128"}

def get(u):
    import subprocess
    return subprocess.run(["curl", "-sS", "-L", "--max-time", "40", u], capture_output=True, text=True, errors="ignore").stdout

print("robots.txt sitemap-regels:", re.findall(r"(?im)^sitemap:.*$", get("https://www.venostal.com/robots.txt")))
urls = set()
for pg in range(1, 9):
    h = get(f"https://www.venostal.com/nl/shop/page/{pg}/" if pg > 1 else "https://www.venostal.com/nl/shop/")
    found = set(re.findall(r'https://www\.venostal\.com/nl/product/[a-z0-9-]+/', h))
    if not found:
        break
    urls |= found
nl = sorted(urls)
print("producten via shoppagina's:", len(nl))
dup = [u for u in nl if re.search(r"-\d/$", u)]
print("URL's met volgnummer (mogelijk dubbel):", len(dup), dup[:3])
random.seed(7)
sample = random.sample(nl, min(N, len(nl)))
zero = noimg = 0
ex_zero, ex_img = [], []
for u in sample:
    h = get(u)
    prices = re.findall(r'woocommerce-Price-amount amount"><bdi>(?:<span[^>]*>[^<]*</span>)?(?:&nbsp;|\s)*([0-9.,]+)', h)
    p = "0,00" if not [x for x in prices if x not in ("0,00", "0.00")] else "ok"
    has_img = bool(re.search(r'wp-content/uploads/\d{4}/\d{2}/[^"\' ]+-910x\d+\.(?:jpg|png|webp)', h))
    if p in ("0,00", "0.00"):
        zero += 1; ex_zero.append(u)
    if not has_img:
        noimg += 1; ex_img.append(u)
print(f"steekproef {len(sample)}: prijs 0,00 = {zero}, zonder productfoto = {noimg}")
print("voorbeelden 0,00:", ex_zero[:4])
print("voorbeelden zonder foto:", ex_img[:4])
