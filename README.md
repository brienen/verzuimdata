# Uitwisselspecificatie HR-gegevens Verzuimportaal

Uitwisselspecificatie voor HR- en verzuimgegevens van gemeenten, en later ook provincies en waterschappen, ten behoeve van het Verzuimportaal van VNG Risicobeheer. De specificatie is gebaseerd op Model HR van het Gemeentelijk Gegevensmodel (GGM).

**Status: versie 0.1, concept ter bespreking met leveranciers. Niets is vastgesteld.**

De toelichting staat op de [documentatiesite](https://brienen.github.io/verzuimdata/).

## Inhoud

| Map of bestand | Inhoud |
| :--- | :--- |
| `v0.1/` | Het JSON-schema, de voorbeeldbestanden en de wijzigingen van versie 0.1 |
| `docs/` | De documentatiesite (MkDocs) |
| `data/` | Het GGM waaruit het model wordt afgeleid |
| `tools/` | De plugins en sjablonen waarmee schema en documentatie worden gegenereerd |
| `TaskFile.yml`, `.env` | De taken en hun instellingen |

## Zelf genereren

Nodig: [Task](https://taskfile.dev) en [uv](https://docs.astral.sh/uv/) (of Python 3.13).

```bash
task              # toont een overzicht van alle taken
task alles        # installeert de tooling, genereert alles en controleert het resultaat
task build:serve  # toont de site op http://localhost:8000
```

Het JSON-schema en de detailspecificatie worden gegenereerd en staan in git. Wijzig ze niet met de hand: pas het model of de plugins in `tools/` aan en draai `task alles`.

| Wat | Waar aanpassen |
| :--- | :--- |
| Definities, kenmerken, waardelijsten | In het GGM (`data/`) |
| Welke objecttypen in het informatiemodel staan | `tools/verzuimplugin_informatiemodel.py` |
| Welke velden worden uitgewisseld, verwijzingen, de omslag van het bericht | `tools/verzuimplugin_uitwisselmodel.py` |
| De vorm van het schema en de gegenereerde pagina's | `tools/*.j2` |
| De overige pagina's | `docs/*.md` (pagina's met een versienummer: `*.md.template`) |

Publiceren naar GitHub Pages gebeurt alleen bewust, met `task publish:github`.
