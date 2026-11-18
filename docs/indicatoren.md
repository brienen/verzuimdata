# Van gegevens naar indicatoren

Deze pagina laat zien waarvoor de gegevens worden gebruikt. De indicatoren over personeel en organisatie zijn de kernindicatoren van de benchmark Venster voor Bedrijfsvoering. De verzuimindicatoren volgen de definities van de Personeelsmonitor van A&O fonds Gemeenten, die de Nationale Verzuimstatistiek volgen.

Wat als verzuim telt, wie tot de bezetting behoort en hoe uren naar fte worden omgerekend, ligt vast in gedeelde definities en niet in de software van de leverancier. De rekenregels worden centraal toegepast. De tabellen hieronder geven ze in het kort; zij zijn geen onderdeel van de uitwisselspecificatie.

## Personeel en organisatie

| Indicator | Benodigde gegevens | Rekenregel in het kort |
| :--- | :--- | :--- |
| Aantal medewerkers | Werknemer; Arbeidsovereenkomst: `datumStart`, `datumEinde` | Unieke werknemers met een arbeidsovereenkomst die op de peildatum geldt |
| Bezetting in fte | Arbeidsovereenkomst: `urenPerWeek`, `cao` | Som van de uren van geldende arbeidsovereenkomsten, gedeeld door de voltijdnorm van de cao |
| Formatie | Formatieplaats: `urenPerWeek`, `datumBegin`, `datumEinde` | Som van de uren van formatieplaatsen die op de peildatum bestaan, gedeeld door de voltijdnorm |
| Leeftijdsopbouw | Werknemer: `geboortejaar` | Leeftijd op de peildatum, ingedeeld in klassen |
| Schaalgroepen | Arbeidsovereenkomst: `schaal`, `urenPerWeek` | Fte op de peildatum per schaalgroep |
| Instroom en uitstroom | Arbeidsovereenkomst: `datumStart`, `datumEinde`, `redenEinde`, per werknemer | Werknemers die in het jaar de organisatie binnenkomen of verlaten, ook bij begin en vertrek in hetzelfde jaar; geen interne contractwissels |
| Tijdelijke dienst | Arbeidsovereenkomst: `contractsoort`, `datumStart`, `datumEinde` | Fte met contractsoort bepaalde tijd |
| Lengte dienstverband | Eerste `datumStart` van een arbeidsovereenkomst per werknemer | Diensttijd op de peildatum, ingedeeld in klassen |
| Externe inhuur en flexibele bezetting | Inhuurovereenkomst: `aanstellingssoort`, `urenPerWeek`, `datumStart`, `datumEinde` | Fte van inhuurovereenkomsten in het jaar, per soort inhuur |
| Stagiairs en werkervaringsplaatsen | OverigeAanstelling: `aanstellingssoort`, `datumStart`, `datumEinde` | Aantal in het jaar |
| Banenafspraak | Arbeidsovereenkomst: `banenafspraak`, `urenPerWeek` | Fte van overeenkomsten die voor de banenafspraak meetellen |
| Leidinggevenden en span of control | Rol: `rolsoort`, `organisatorischeEenheid`; Functie: `leidinggevend` | Aantal medewerkers per leidinggevende |
| Overhead en bedrijfsvoering | Formatieplaats; Functie: `code`; NormProfiel | Formatie per groep, via de vertaaltabel van de gemeente of het normprofiel |
| Inzet voor derden | Inzet: `bestemming`, `uren` | Fte met bestemming derden |

## Verzuim

| Indicator | Benodigde gegevens | Rekenregel in het kort |
| :--- | :--- | :--- |
| Verzuimpercentage | Verzuim: `datumtijdStart`, `datumtijdEinde`, `percentageArbeidsongeschiktheid`, `verloop`; Arbeidsovereenkomst: `urenPerWeek` | Verzuimde kalenderdagen gedeeld door beschikbare kalenderdagen, beide gewogen naar deeltijd; gedeeltelijk verzuim telt naar rato |
| Verzuim naar duur | Als verzuimpercentage | Verzuimgevallen ingedeeld naar duur in kalenderdagen: kort (tot en met 7), middellang (8 tot en met 42), lang (43 tot en met 365) en extra lang (langer dan een jaar) |
| Meldingsfrequentie | Verzuim: `datumtijdStart`; bezetting | Aantal nieuwe verzuimgevallen in het jaar, gedeeld door de gemiddelde bezetting |
| Nulverzuim | Verzuim; Werknemer; bezetting | Aandeel werknemers zonder ziekmelding in het jaar |
| Langdurig verzuim | Verzuim: `datumtijdStart`, `datumtijdEinde` | Werknemers die op 31 december langer dan een jaar ziek zijn, per 100 medewerkers |
| Herstel | Verzuim: `redenEinde` | Aandeel afgesloten verzuimgevallen dat met herstel eindigt |
| Uitsplitsingen | Werknemer: `geboortejaar`, `geslachtsaanduiding`; Arbeidsovereenkomst: `schaal`, `organisatorischeEenheid`; Functie: `werkomgeving` | De indicatoren hierboven per leeftijdsklasse, geslacht, schaalgroep, organisatieonderdeel en werkomgeving |

De uitsplitsingen zijn de reden om op registratieniveau uit te vragen: uit totalen per gemeente zijn ze niet meer te maken.

## Verlof en verzuim

Zwangerschaps- en bevallingsverlof is verlof en geen verzuim; ziekte als gevolg van zwangerschap is wel verzuim en heeft de verzuimsoort `Ziekte onder vangnet Ziektewet`. Verlof wordt geleverd om verzuim en beschikbaarheid goed te kunnen duiden, bijvoorbeeld bij langdurend zorgverlof of ouderschapsverlof.
