# Wijzigingen

## Versie 0.1

Versie 0.1 is het eerste concept van de uitwisselspecificatie. Er is geen eerdere gepubliceerde versie.

Ten opzichte van het concept *Specificatie koppelvlak HR-gegevens voor het Verzuimportaal* van 16 november 2026, dat het uitwisselmodel alleen op hoofdlijnen beschreef, is het volgende veranderd:

- **JSON-schema en waardelijsten.** Het schema en de waardelijsten zijn uitgewerkt en worden uit het informatiemodel gegenereerd.
- **Aanstellingscontract in plaats van Dienstverband.** Het dienstverband is vervangen door drie soorten aanstellingscontract: arbeidsovereenkomst, inhuurovereenkomst en overige aanstelling, elk met een aanstellingssoort.
- **Externe inhuur, stages en werkervaringsplaatsen** vallen binnen de specificatie. Kosten van inhuur blijven erbuiten.
- **Verzuim.** De verzuimsoort en de reden van het einde hebben een vaste waardelijst. De historie van het percentage arbeidsongeschiktheid wordt geleverd als verloop binnen het verzuimgeval.
- **Rol.** Een rol heeft een rolsoort, zodat leidinggevenden eenduidig herkenbaar zijn.
- **Functie.** Een functie heeft het kenmerk leidinggevend.

## Bestanden in deze versie

| Bestand | Inhoud |
| :--- | :--- |
| `json_schema_Uitwisselmodel.json` | Het JSON-schema van een bericht |
| `enkelvoudigVoorbeeld.json` | Voorbeeld met één levering en één werknemer |
| `meervoudigVoorbeeld.json` | Voorbeeld met twee leveringen en alle soorten aanstelling |

De voorbeeldbestanden bevatten verzonnen gegevens en zijn gecontroleerd tegen het schema van deze versie.
