# Koparki — mapa nurkowa

Interaktywna mapa nurkowa zalanego wyrobiska Koparki (okolice Trzebini i Jaworzna):
atrakcje pod wodą, trasy z azymutami magnetycznymi i odległościami, kursy do brzegu,
plan do druku w PDF. Strona po polsku i angielsku.

**Strona:** https://jjbiernacki.github.io/koparki/

*Interactive dive map of the flooded Koparki quarry near Trzebinia, Poland.
Polish and English.*

## Skąd dane

Podkład to ortofotomapa złożona ze zdjęć z drona z 13.09.2026 (3,92 cm/px).
Pozycje punktów liczone z dwóch nalotów (13.09 i 20.09.2026). Azymuty są
magnetyczne, tak jak pokazuje kompas nurka (deklinacja +6,3°E).
Głębokości pochodzą ze starego planu bazy i zależą od poziomu wody.

## Co jest w repozytorium

| Plik | Co to |
|---|---|
| `index.html` | strona (zbudowana, nie edytować ręcznie) |
| `dane.json` | punkty, połączenia z azymutami, obrys wraku Wilhelm |
| `kafle/{z}/{x}_{y}.jpg` | kafle mapy 512 px, poziomy 0–5, poziom 5 = 3,92 cm/px |
| `plan_PL.pdf`, `plan_EN.pdf` | plan do druku, A4 poziomo |
| `podglad.jpg` | obrazek podglądu linku (1200 × 630) |
| `zrodlo/` | źródło strony: `szablon.html`, `zbuduj.py`, CSS Leafleta |

## Jak zaktualizować

1. Po zmianie planu w projekcie Koparki: `python3 skrypty/90_strona_dane.py`
   (nadpisuje `dane.json`, `kafle/` i PDF-y).
2. Po zmianie wyglądu albo tekstów: edycja `zrodlo/szablon.html`.
3. `python3 zrodlo/zbuduj.py` składa `index.html`.
4. Commit i push na gałąź `main`. GitHub Pages publikuje w ciągu 1–2 minut.

`python3 zrodlo/zbuduj.py --artefakt` robi wersję do publikacji jako artefakt
Claude (`artefakt.html`, poza repozytorium).

Kontakt: [@deeperbluediving](https://www.instagram.com/deeperbluediving)
