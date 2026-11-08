"""Sklada strone z szablonu: wkleja CSS Leafleta i dane punktow (dane.json z kroku 90).

Bez flag:     strona/index.html - pelny dokument HTML do hostowania (GitHub Pages).
              Naglowek z szablonu (title, description, czcionki) idzie do <head>,
              dochodza znaczniki podgladu linku (og:*) z obrazkiem podglad.jpg.
--artefakt:   strona/artefakt.html - sama tresc do publikacji jako artefakt Claude
              (bez <head>). Plik jest w .gitignore, nie trafia na GitHuba.
"""
import json, os, sys

ADRES = 'https://jjbiernacki.github.io/koparki/'   # adres publiczny strony; zmien przy wlasnej domenie
TYTUL = 'Koparki · mapa nurkowa'

Z = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(Z)
s = open(Z + '/szablon.html', encoding='utf-8').read()
s = s.replace('/*LEAFLET_CSS*/', open(Z + '/leaflet.min.css', encoding='utf-8').read())
s = s.replace('/*DANE*/', json.dumps(json.load(open(S + '/dane.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':')))

if '--artefakt' in sys.argv:
    cel = S + '/artefakt.html'
else:
    # naglowek szablonu: kolejne linie <title>/<meta>/<link> na samym poczatku
    linie = s.split('\n'); i = 0
    while i < len(linie) and linie[i].lstrip().startswith(('<title', '<meta', '<link')):
        i += 1
    glowa = [l for l in linie[:i] if 'claude:' not in l]
    tresc = '\n'.join(linie[i:])
    opis = next((l.split('content="')[1].split('"')[0] for l in glowa if 'name="description"' in l), '')
    ikona = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
             "%3Crect width='32' height='32' rx='4' fill='%23c8102e'/%3E"
             "%3Cpath d='M0 5L5 0L32 27L27 32Z' fill='%23fff'/%3E%3C/svg%3E")   # flaga nurkowa
    meta = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
        *glowa,
        '<link rel="canonical" href="%s">' % ADRES,
        '<link rel="icon" href="%s">' % ikona,
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
