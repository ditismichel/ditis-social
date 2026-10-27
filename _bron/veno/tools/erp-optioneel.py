#!/usr/bin/env python3
"""ERP-koppeling in de Veno-pitch optioneel maken en als vraag aan Bob stellen (Michel 27-10-2026).
Aanroep: python3 -I _bron/veno/tools/erp-optioneel.py"""
import pathlib

B = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social/_bron/veno")
body = B / "body.html"
s = body.read_text()
rep = {
    "Eigen prijzen in eigen valuta, nabestellen uit de orderhistorie, gekoppeld aan jullie nieuwe ERP.":
        "Eigen prijzen in eigen valuta en nabestellen uit de orderhistorie. Als jullie dat willen, gekoppeld aan het nieuwe ERP.",
    " Het nieuwe ERP nemen we vanaf de eerste dag mee.":
        " Een koppeling met jullie nieuwe ERP kan, maar hoeft niet: dat bepalen jullie.",
    "Eerst een verkenning: ERP-koppeling, dealerprijzen per valuta, nabestellen, en jullie vakjargon per taal.":
        "Eerst een verkenning: dealerprijzen per valuta, nabestellen, jullie vakjargon per taal, en of de webshop aan het nieuwe ERP gekoppeld wordt.",
    "Een dealeromgeving waarin dealers zelf bestellen, gekoppeld aan het nieuwe ERP.":
        "Een dealeromgeving waarin dealers zelf bestellen, desgewenst gekoppeld aan het nieuwe ERP.",
    "Een nieuwe webshop met ERP-koppeling in zes talen vraagt een paar maanden.":
        "Een nieuwe webshop in zes talen vraagt een paar maanden, met een ERP-koppeling iets langer.",
    "Elke order die een dealer zelf plaatst, scheelt jullie team handwerk.</p>":
        "Elke order die een dealer zelf plaatst, scheelt jullie team handwerk.</p>\n      <p><b>En:</b> willen jullie de nieuwe webshop direct aan het nieuwe ERP koppelen? Dat kan, maar hoeft niet. Technisch is het goed mogelijk en we koppelen webshops vaker aan een ERP. Welk systeem het wordt, bepaalt hoe. Welk ERP kiezen jullie?</p>",
}
for a, b in rep.items():
    assert a in s, a[:60]
    s = s.replace(a, b)
body.write_text(s)

m = B / "mockup/home.html"
t = m.read_text()
a = "Log in en zie je eigen prijzen in je eigen valuta, gekoppeld aan ons ERP."
assert a in t
m.write_text(t.replace(a, "Log in en zie je eigen prijzen in je eigen valuta, en bestel na uit je orderhistorie."))
print("ERP optioneel gemaakt in body en mockup")
