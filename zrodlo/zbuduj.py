"""Sklada strone z szablonu: wkleja CSS Leafleta i dane punktow (dane.json).
Wynik: index.html - pelny dokument HTML z naglowkiem (title, description, og:*), gotowy do hostowania."""
import json, os

ADRES = 'https://jjbiernacki.github.io/koparki/'   # adres publiczny strony; zmien przy wlasnej domenie
TYTUL = 'Koparki · mapa nurkowa'

Z = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(Z)
s = open(Z + '/szablon.html', encoding='utf-8').read()
s = s.replace('/*LEAFLET_CSS*/', open(Z + '/leaflet.min.css', encoding='utf-8').read())
s = s.replace('/*DANE*/', json.dumps(json.load(open(S + '/dane.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':')))

# naglowek szablonu: kolejne linie <title>/<meta>/<link> na samym poczatku
linie = s.split('\n'); i = 0
while i < len(linie) and linie[i].lstrip().startswith(('<title', '<meta', '<link')):
    i += 1
glowa = linie[:i]
tresc = '\n'.join(linie[i:])
opis = next((l.split('content="')[1].split('"')[0] for l in glowa if 'name="description"' in l), '')
meta = [
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
    *glowa,
    '<link rel="canonical" href="%s">' % ADRES,
    '<link rel="icon" href="ikona.svg" type="image/svg+xml">',   # zbiornik jako flaga nurkowa
    '<link rel="icon" href="ikona-32.png" type="image/png" sizes="32x32">',
    '<link rel="apple-touch-icon" href="ikona-180.png">',
    '<meta property="og:type" content="website">',
    '<meta property="og:url" content="%s">' % ADRES,
    '<meta property="og:title" content="%s">' % TYTUL,
    '<meta property="og:description" content="%s">' % opis,
    '<meta property="og:image" content="%spodglad.jpg">' % ADRES,
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:locale" content="pl_PL">',
    '<meta property="og:locale:alternate" content="en_GB">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="theme-color" content="#1d4f5c">',
    '<style>body{margin:0}[hidden]{display:none!important}</style>',
]
s = ('<!doctype html>\n<html lang="pl">\n<head>\n' + '\n'.join(meta) + '\n</head>\n<body>\n'
     + tresc + '\n</body>\n</html>\n')
cel = S + '/index.html'

open(cel, 'w', encoding='utf-8').write(s)
print('%s: %d znakow' % (os.path.basename(cel), len(s)))
