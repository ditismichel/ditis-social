#!/usr/bin/env python3
"""Koppelt script.json aan de woordtimings van ElevenLabs Scribe en schrijft video/timing.js.
Aanroep: python3 -I build_timing.py <words.json> <duur_audio_sec>
- window.CUE: start per scène (0,25 sec vóór het eerste gesproken woord)
- window.CAPS: ondertitels [start, eind, tekst], max ~6 woorden, breekt op leestekens
- window.DUR: laatste ondertitel + 2,6 sec
"""
import json, re, sys, pathlib

B = pathlib.Path(__file__).resolve().parent.parent
words_raw = json.load(open(sys.argv[1]))
if isinstance(words_raw, dict):
    words_raw = words_raw.get("words", words_raw.get("transcript", {}).get("words", []))
W = []
for w in words_raw:
    t = (w.get("text") or w.get("word") or "").strip()
    if not t or w.get("type") in ("spacing", "audio_event") or re.fullmatch(r"\[.*\]", t):
        continue
    W.append({"t": t, "s": float(w["start"]), "e": float(w["end"])})

def norm(x):
    return re.sub(r"[^a-z0-9éë]", "", x.lower())

script = json.load(open(B / "script.json"))
cue, pos = {}, 0
for sc in script:
    first = [norm(x) for x in re.sub(r"\[.*?\]", "", sc["spraak"]).split() if norm(x)][:2]
    for i in range(pos, len(W)):
        if norm(W[i]["t"]) == first[0] and (len(first) < 2 or i + 1 >= len(W) or norm(W[i + 1]["t"]) == first[1]):
            cue[sc["id"]] = max(0.0, round(W[i]["s"] - 0.25, 2))
            pos = i + 1
            break
    else:
        raise SystemExit(f"scène niet gevonden: {sc['id']} ({first})")

caps, cur = [], []
for i, w in enumerate(W):
    cur.append(w)
    brk = re.search(r"[.,:?!]$", w["t"]) or len(cur) >= 6
    if brk or i == len(W) - 1:
        caps.append([round(cur[0]["s"], 2), round(cur[-1]["e"] + 0.15, 2), " ".join(x["t"] for x in cur)])
        cur = []
# mailadres niet knippen: plak ondertitels samen tot het adres compleet is
i = 0
while i < len(caps) - 1:
    t = caps[i][2].lower()
    if "apenstaartje" in t and not t.rstrip().endswith("l."):
        caps[i] = [caps[i][0], caps[i + 1][1], caps[i][2] + " " + caps[i + 1][2]]
        del caps[i + 1]
        continue
    i += 1
# uitgesproken getallen in de ondertitel als cijfers tonen
REPL = [("venostal punt com", "venostal.com"), ("Zes talen", "6 talen"), ("op één", "op 1"), ("twee tot drie seconden", "2 tot 3 seconden"), ("zelfs negen", "zelfs 9"), ("vijf talen", "5 talen"), ("een derde minder", "een derde minder")]
for c in caps:
    for a, b in REPL:
        c[2] = c[2].replace(a, b)
for i in range(len(caps) - 1):  # geen overlap
    caps[i][1] = min(caps[i][1], caps[i + 1][0])
dur = round(caps[-1][1] + 2.6, 2)
out = B / "video/timing.js"
out.write_text("window.CUE=%s;\nwindow.CAPS=%s;\nwindow.DUR=%s;\n" % (json.dumps(cue), json.dumps(caps, ensure_ascii=False), dur))
print("CUE", cue)
print("ondertitels", len(caps), "DUR", dur)
