"""Sklada strone z szablonu: wkleja CSS Leafleta i dane punktow (dane.json).
Wynik: index.html - pelny dokument HTML z naglowkiem (title, description, og:*, dane strukturalne),
gotowy do hostowania, oraz sitemap.xml (strona, zdjecia, obraz planu, PDF-y planu).

Lista atrakcji jest od razu wpisana w HTML (po polsku), zeby wyszukiwarki widzialy tresc bez
uruchamiania skryptow; skrypt strony zastepuje ja ta sama lista po zaladowaniu.
Obraz planu (koparki-mapa-nurkowa*.jpg) musi pochodzic z aktualnych PDF-ow - sprawdzane
po sha256 z plan_obraz.json; inaczej budowanie jest przerywane."""
import json, os, re, hashlib, datetime
from html import escape as _esc

ADRES = 'https://jjbiernacki.github.io/koparki/'   # adres publiczny strony; zmien przy wlasnej domenie
TYTUL = 'Mapa nurkowa Koparki (Jaworzno) – atrakcje, trasy, plan PDF'
OPIS = ('Interaktywna mapa nurkowa zbiornika Koparki w Jaworznie: wrak Wilhelm, Ford Fairlane, '
        'koparki i inne atrakcje z głębokościami, trasy z azymutami, plan do druku.')

Z = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(Z)
esc = lambda x: _esc(str(x), quote=True)

# --- obraz planu musi byc zrobiony z aktualnych PDF-ow ---------------------------------
PO = json.load(open(S + '/plan_obraz.json', encoding='utf-8'))
for jez, o in PO.items():
    h = hashlib.sha256(open(S + '/' + o['pdf'], 'rb').read()).hexdigest()
    if h != o['sha256']:
        raise SystemExit('BLAD: %s zmienil sie po zrobieniu obrazu %s - najpierw wygeneruj obraz planu '
                         'z aktualnych PDF-ow (plan_obraz.json).' % (o['pdf'], o['obraz']))

D = json.load(open(S + '/dane.json', encoding='utf-8'))
F = S + '/zdjecia/zdjecia.json'
FOTO = json.load(open(F, encoding='utf-8')) if os.path.exists(F) else {}

s = open(Z + '/szablon.html', encoding='utf-8').read()
s = s.replace('/*LEAFLET_CSS*/', open(Z + '/leaflet.min.css', encoding='utf-8').read())
s = s.replace('/*DANE*/', json.dumps(D, ensure_ascii=False, separators=(',', ':')))
s = s.replace('/*ZDJECIA*/', json.dumps(FOTO, separators=(',', ':')))   # galeria w widoku punktu
s = s.replace('/*PLAN_OBRAZ*/', json.dumps(PO, separators=(',', ':')))

# --- lista atrakcji wprost w HTML (ta sama co rysuje skrypt w widoku listy, po polsku) ------
DEP = re.compile(r'^\s*((?:ok\.\s*|approx\.\s*)?\d+(?:[.,]\d+)?\s*m\*?)(?!\w)\s*(?:·\s*)?')
def ico(p, n):
    if not p.get('ikona'): return ''
    i = esc(p['ikona'])
    return ('<span class="ico"><img class="ico-l" src="%s" alt="" width="%d" height="%d">'
            '<img class="ico-d" src="%s" alt="" width="%d" height="%d"></span>'
            % (i, n, n, i.replace('.png', '_c.png'), n, n))
pozycje = []
for p in sorted(D['punkty'], key=lambda p: (int(re.match(r'\d+', p['nr']).group()), p['nr'])):
    opis = p.get('opis_pl') or ''
    m = DEP.match(opis); gl = m.group(1) if m else ''; reszta = DEP.sub('', opis)
    sub = p['nr'] == '7b'
    pozycje.append('<li class="%s"><button data-id="%s"><span class="badge%s">%s</span>%s<span><span class="t">%s%s</span>%s</span></button></li>'
                   % ('sub' if sub else '', esc(p['id']), ' small' if sub or p.get('maly') else '', esc(p['nr']), ico(p, 32),
                      esc(p['pl']), '<span class="dep">%s</span>' % esc(gl) if gl else '',
                      '<span class="s">%s</span>' % esc(reszta) if reszta else ''))
cap = re.search(r"listCap: '([^']*)'", s).group(1)
pl = PO['PL']
plan_fig = ('<figure class="plan-fig"><a href="%s"><img src="%s" alt="Mapa nurkowa zbiornika Koparki – plan z atrakcjami, głębokościami, trasami i azymutami" width="%d" height="%d" loading="lazy"></a>'
            '<figcaption>Mapa nurkowa zbiornika Koparki: <a href="%s">obraz JPG</a> · <a href="%s">PDF A4</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pl" target="_blank" rel="noopener license">CC BY-SA 4.0</a></figcaption></figure>'
            % (pl['obraz'], pl['podglad'], pl['w_podglad'], pl['h_podglad'], pl['obraz'], pl['pdf']))
lista = '<div class="view"><p class="list-cap">%s</p><ul class="list">%s</ul>%s</div>' % (cap, ''.join(pozycje), plan_fig)
assert s.count('<div class="body" id="body"></div>') == 1
s = s.replace('<div class="body" id="body"></div>', '<div class="body" id="body">%s</div>' % lista)

# --- dane strukturalne (schema.org) ---------------------------------------------------------
zdj = [ADRES + z['plik'] for v in FOTO.values() for z in v]
ld = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'WebSite', '@id': ADRES + '#strona', 'url': ADRES, 'name': TYTUL, 'inLanguage': ['pl', 'en']},
    {'@type': 'TouristAttraction', '@id': ADRES + '#koparki', 'name': 'Koparki',
     'alternateName': ['Zbiornik Koparki', 'Koparki Jaworzno'], 'url': ADRES, 'description': OPIS,
     'touristType': 'Nurkowie',
     'address': {'@type': 'PostalAddress', 'addressLocality': 'Jaworzno', 'addressCountry': 'PL'},
     'geo': {'@type': 'GeoCoordinates', 'latitude': 50.2288, 'longitude': 19.3108},
     'hasMap': ADRES + PO['PL']['obraz'],
     'image': [ADRES + PO['PL']['obraz']] + zdj[:12]},
    {'@type': 'ImageObject', '@id': ADRES + '#mapa', 'contentUrl': ADRES + PO['PL']['obraz'],
     'thumbnailUrl': ADRES + PO['PL']['podglad'], 'name': 'Mapa nurkowa Koparki',
     'caption': 'Mapa nurkowa zbiornika Koparki w Jaworznie z atrakcjami, głębokościami, trasami i azymutami',
     'width': PO['PL']['w'], 'height': PO['PL']['h'], 'license': 'https://creativecommons.org/licenses/by-sa/4.0/', 'acquireLicensePage': ADRES, 'creator': {'@type': 'Person', 'name': 'Jerzy Biernacki', 'url': 'https://www.instagram.com/deeperbluediving'}, 'copyrightNotice': '© 2026 Jerzy Biernacki (@deeperbluediving), CC BY-SA 4.0', 'creditText': '@deeperbluediving', 'inLanguage': 'pl'},
    {'@type': 'ImageObject', 'contentUrl': ADRES + PO['EN']['obraz'], 'name': 'Koparki dive map',
     'caption': 'Dive map of the Koparki flooded quarry in Jaworzno, Poland: dive sites, depths, routes and bearings',
     'width': PO['EN']['w'], 'height': PO['EN']['h'], 'license': 'https://creativecommons.org/licenses/by-sa/4.0/', 'acquireLicensePage': ADRES, 'creator': {'@type': 'Person', 'name': 'Jerzy Biernacki', 'url': 'https://www.instagram.com/deeperbluediving'}, 'copyrightNotice': '© 2026 Jerzy Biernacki (@deeperbluediving), CC BY-SA 4.0', 'creditText': '@deeperbluediving', 'inLanguage': 'en'},
]}

# --- naglowek: kolejne linie <title>/<meta>/<link> na poczatku szablonu ----------------------
linie = s.split('\n'); i = 0
while i < len(linie) and linie[i].lstrip().startswith(('<title', '<meta', '<link')):
    i += 1
glowa = [l for l in linie[:i] if not l.lstrip().startswith(('<title', '<meta name="description"'))]
tresc = '\n'.join(linie[i:])
meta = [
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
    '<title>%s</title>' % esc(TYTUL),
    '<meta name="description" content="%s">' % esc(OPIS),
    *glowa,
    '<link rel="canonical" href="%s">' % ADRES,
    '<link rel="sitemap" type="application/xml" href="sitemap.xml">',
    '<link rel="icon" href="ikona.svg" type="image/svg+xml">',   # zbiornik jako flaga nurkowa
    '<link rel="icon" href="ikona-32.png" type="image/png" sizes="32x32">',
    '<link rel="apple-touch-icon" href="ikona-180.png">',
    '<meta property="og:type" content="website">',
    '<meta property="og:url" content="%s">' % ADRES,
    '<meta property="og:title" content="%s">' % esc(TYTUL),
    '<meta property="og:description" content="%s">' % esc(OPIS),
    '<meta property="og:image" content="%spodglad.jpg">' % ADRES,
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:locale" content="pl_PL">',
    '<meta property="og:locale:alternate" content="en_GB">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="theme-color" content="#1d4f5c">',
    '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False, separators=(',', ':')),
    '<style>body{margin:0}[hidden]{display:none!important}</style>',
]
s = ('<!doctype html>\n<html lang="pl">\n<head>\n' + '\n'.join(meta) + '\n</head>\n<body>\n'
     + tresc + '\n</body>\n</html>\n')
open(S + '/index.html', 'w', encoding='utf-8').write(s)
print('index.html: %d znakow, %d atrakcji w HTML' % (len(s), len(pozycje)))

# --- sitemap.xml: strona z obrazami (plan PL/EN, zdjecia), PDF-y planu ----------------------
dzis = datetime.date.today().isoformat()
obrazy = [PO['PL']['obraz'], PO['EN']['obraz']] + [z['plik'] for v in FOTO.values() for z in v]
obrazy = list(dict.fromkeys(obrazy))                 # bez powtorzen (te same zdjecia przy dwoch punktach)
x = ['<?xml version="1.0" encoding="UTF-8"?>',
     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
     '<url><loc>%s</loc><lastmod>%s</lastmod>' % (ADRES, dzis)]
x += ['<image:image><image:loc>%s%s</image:loc></image:image>' % (ADRES, esc(o)) for o in obrazy]
x += ['</url>']
x += ['<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (ADRES, PO[j]['pdf'], dzis) for j in ('PL', 'EN')]
x += ['</urlset>', '']
open(S + '/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(x))
print('sitemap.xml: 3 adresy, %d obrazow' % len(obrazy))
