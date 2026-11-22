# Koparki — mapa nurkowa

Interaktywna mapa nurkowa zalanego wyrobiska Koparki w Jaworznie.

**Strona: https://jjbiernacki.github.io/koparki/**

Mapę można przesuwać i przybliżać. Na niej zaznaczono miejsca do nurkowania
(pomosty, wraki, platformy, boje), trasy między nimi z azymutami magnetycznymi
i odległościami oraz kierunki do brzegu. Do każdego miejsca jest krótki opis.
Plan można pobrać jako PDF do druku (A4 poziomo). Strona jest po polsku
i po angielsku.

*Interactive dive map of the flooded Koparki quarry in Jaworzno, Poland,
with dive sites, routes with magnetic bearings and distances, and a printable
plan. Polish and English.*

## O danych

- Podkład to ortofotomapa złożona ze zdjęć z drona, wykonanych we wrześniu 2026.
- Azymuty są magnetyczne, tak jak pokazuje kompas nurka.
- Pozycje obiektów i głębokości są przybliżone, głębokości zależą od poziomu wody.
- Mapa ma charakter informacyjny i nie zastępuje szkolenia ani zasad obowiązujących na miejscu.

## Zawartość repozytorium

| Plik | Co to |
|---|---|
| `index.html` | strona |
| `dane.json` | punkty, trasy i opisy po polsku i angielsku |
| `kafle/` | kafle mapy |
| `plan_PL.pdf`, `plan_EN.pdf` | plan do druku |
| `podglad.jpg` | obrazek podglądu linku |
| `zrodlo/` | źródło strony |

## Licencja i kontakt

- **Kod strony** (`index.html`, `zrodlo/`): licencja MIT, zobacz plik `LICENSE`.
- **Mapa, plan do druku (`plan_PL.pdf`, `plan_EN.pdf`, `koparki-mapa-nurkowa*.jpg`, `koparki-dive-map*.jpg`), kafle mapy i dane punktów (`dane.json`)**: © 2026 Jerzy Biernacki (@deeperbluediving), licencja [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.pl). Można je kopiować, drukować i przerabiać, także komercyjnie, z podaniem autora i linku do strony oraz na tej samej licencji.
- **Zdjęcia spod wody** (`zdjecia/`) nie są objęte żadną z tych licencji; prawa należą do ich autorów.

Kontakt: [@deeperbluediving](https://www.instagram.com/deeperbluediving) na Instagramie
i [facebook.com/jjbiernacki](https://www.facebook.com/jjbiernacki) na Facebooku.
