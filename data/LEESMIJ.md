# Het model

`Gemeentelijk Gegevensmodel.qea` is het Gemeentelijk Gegevensmodel (GGM) als Enterprise Architect-bestand. Uit Model HR in dit bestand worden het informatiemodel en het uitwisselmodel van de specificatie afgeleid (`task import:model`).

Het bestand is een kopie van `v3.0.0/Gemeentelijk Gegevensmodel.qea` uit de werkversie van het GGM (branch `Voorbereidingen-Release-v3.0.0`), met daarin het wijzigingsvoorstel *Uitbreiding HR-domein: aanstelling, inzet en verzuim* (versie 0.5) doorgevoerd. Stand: 18 november 2026.

Een `.qea`-bestand is een SQLite-database. De kopie is gemaakt met `VACUUM INTO`, zodat zij geen lege ruimte bevat:

```bash
sqlite3 "<ggm-repo>/v3.0.0/Gemeentelijk Gegevensmodel.qea" "VACUUM INTO 'data/Gemeentelijk Gegevensmodel.qea'"
```

Het pad naar het bestand staat in `.env` (`GGM_BESTAND`). Wie het GGM lokaal heeft staan, kan daar ook rechtstreeks naar verwijzen.
