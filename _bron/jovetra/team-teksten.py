#!/usr/bin/env python3
"""Eenmalig (28-10): Anouk als vast aanspreekpunt eruit, 'ons marketingteam', team dertien, geen beloftes over livegang. Aanroep vanuit repo-root."""
p = '_bron/jovetra/body.html'
s = open(p).read()
R = [
    ('<small>de blogs van Anouk</small>', '<small>de blogs, verder uitgebouwd</small>'),
    ('<li>De blogs van Anouk krijgen een vaste vorm:', '<li>De blogs krijgen een vaste vorm:'),
    ('<p>Anouk schrijft de blogs en kent jullie materieel en klanten. Bij ons zit zij naast de mensen die de site bouwen. Wat zij schrijft, landt dan op een site die is gemaakt om gevonden te worden.</p>',
     '<p>Ons marketingteam schrijft de blogs en kent jullie materieel en klanten. Bij ons zitten de schrijvers naast de mensen die de site bouwen. Wat zij schrijven, landt dan op een site die is gemaakt om gevonden te worden.</p>'),
    ('Anouk is jullie vaste aanspreekpunt. Achter haar staat het hele team, voor de website, Google, AI en techniek.',
     'Ons marketingteam doet LinkedIn en de blogs, en het hele team staat erachter voor de website, Google, AI en techniek.'),
    ('<div class="anouk"><img src="media/anouk.jpg" alt="Anouk, vast aanspreekpunt voor Jovetra" width="600" height="600" loading="lazy"><div><b>Anouk</b><span>Jullie vaste aanspreekpunt, voor LinkedIn, de blogs en straks de site.</span></div></div>',
     '<div class="anouk"><div><b>Ons marketingteam</b><span>Voor LinkedIn, de blogs en straks de site. Bereikbaar op <span style="white-space:nowrap">023-3020409</span> (ook WhatsApp) en <a class="ext" href="mailto:marketing@ditisabc.nl">marketing@ditisabc.nl</a>.</span></div></div>'),
    ('vanaf 1 november met veertien mensen.', 'vanaf 1 november met dertien mensen.'),
    ('<div class="feit"><b>14</b><span>mensen in ons team</span></div>', '<div class="feit"><b>13</b><span>mensen in ons team</span></div>'),
    ('We horen het meteen, en het staat dezelfde week online.', 'We horen het meteen en zetten het online.'),
    ('Elke maand een rapport in gewone taal.', 'Een vaste rapportage in gewone taal.'),
    ('dit is <i></i> waarom nu</span>', 'dit is <i></i> als jullie willen</span>'),
    ('<h2>Bouwen in de winter, gevonden in het voorjaar</h2>', '<h2>Zie het vooral als informatie</h2>'),
    ('<p>Jullie drukste periode is de zomer. Een nieuwe site die in de winter wordt gebouwd, staat in het voorjaar live en heeft dan een paar maanden om te groeien in Google en AI, vóór de drukte begint. Zullen we de vervolgstap plannen?</p>',
     '<p>Het loopt goed bij Jovetra, en de online marketing gaat gewoon door. Deze pagina laat zien wat er aan de website nog beter kan. Vinden jullie het interessant, dan kom ik graag nog een keer langs om het samen door te nemen.</p>'),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w').write(s)
print('ok')
