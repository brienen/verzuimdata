# Achtergrond

## Het Verzuimportaal

VNG Risicobeheer ontwikkelt samen met gemeenten het Verzuimportaal. Het portaal geeft een gemeente inzicht in haar verzuim, maakt vergelijking met andere gemeenten mogelijk en geeft een verzuimnorm die rekening houdt met de kenmerken van de organisatie. Daarvoor zijn gegevens nodig over verzuim, maar ook over de mensen en de organisatie waarin het verzuim zich voordoet: de bezetting, de leeftijdsopbouw, de functies en de organisatieonderdelen.

## Eén uitvraag voor meer toepassingen

Dezelfde personeelsgegevens worden nu op meerdere plaatsen uitgevraagd:

- de **Personeelsmonitor** van A&O fonds Gemeenten, met de verzuimdefinities van de Nationale Verzuimstatistiek;
- de benchmark **Venster voor Bedrijfsvoering**, met kernindicatoren over personeel en organisatie;
- het **Verzuimportaal** zelf.

Deze specificatie beschrijft de gegevens op registratieniveau, in de termen van het Gemeentelijk Gegevensmodel. Uit die gegevens zijn de indicatoren van alle drie af te leiden. De voorbereiding gebeurt daarom samen met Venster voor Bedrijfsvoering en A&O fonds Gemeenten.

## Het Gemeentelijk Gegevensmodel

Het [Gemeentelijk Gegevensmodel](https://www.gemeentelijkgegevensmodel.nl/) (GGM) is een logisch gegevensmodel voor alle beleidsterreinen van gemeenten. Model HR is het deel over personeel en organisatie. Om de gegevens voor het Verzuimportaal en Venster voor Bedrijfsvoering te kunnen beschrijven, is een wijzigingsvoorstel voor Model HR opgesteld. De hoofdpunten:

- het abstracte objecttype Aanstellingscontract, met de subtypen Arbeidsovereenkomst (het vroegere Dienstverband), Inhuurovereenkomst en OverigeAanstelling;
- een verrijkte Inzet, met bestemming en geldigheid;
- het percentage arbeidsongeschiktheid, de verzuimsoort en de reden van het einde bij Verzuim;
- vaste waardelijsten in plaats van vrije tekst of losse objecttypen;
- een definitie en toelichting bij elk objecttype, kenmerk en elke relatie.

## Planning

| Periode | Stap |
| :--- | :--- |
| 2026 | Voorgesprekken met leveranciers op basis van dit concept |
| 2027 | Afstemming en vaststelling van de specificatie, DPIA, pilot met enkele gemeenten, aansluiting van de eerste leveranciers |
| Vanaf 2028 | Gebruik in het Verzuimportaal |

## Hoe deze site is gemaakt

Het informatiemodel wordt met [crunch_uml](https://github.com/brienen/crunch_uml) uit het GGM gelezen. Twee kleine plugins leiden daaruit het informatiemodel en het uitwisselmodel van deze specificatie af; het JSON-schema, de detailspecificatie en de uitleg worden uit die modellen gegenereerd. De bron staat in de [repository](https://github.com/brienen/verzuimdata).
