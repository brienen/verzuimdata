# Koppelvlak API

!!! warning "Op hoofdlijnen"
    Dit deel beschrijft het koppelvlak op hoofdlijnen. De technische uitwerking, waaronder de OpenAPI-beschrijving, volgt in 2027 in afstemming met de leveranciers.

De leverancier stelt een service (API) beschikbaar waar de afnemer de gegevens ophaalt. De gegevens blijven in de bron en worden op afgesproken momenten bevraagd; er is geen centrale routeervoorziening en er worden geen bestanden verstuurd. Het antwoord op een bevraging is een bericht volgens de [uitwisselspecificatie](../uitwisselspecificatie.md).

| Onderdeel | Keuze in dit concept |
| :--- | :--- |
| Aanbieder | De HR-softwareleverancier, namens de gemeenten die daarvoor opdracht geven; een gemeente kan ook zelf aanbieden |
| Afnemer | De beheerder van het Verzuimportaal. Dezelfde service is met een eigen contract ook bruikbaar voor andere afnemers, zoals Venster voor Bedrijfsvoering of de gemeente zelf |
| Berichtvorm | JSON; één antwoordbericht kan leveringen voor meerdere gemeenten bevatten, één levering per gemeente |
| Transport | FSC volgens het Digikoppeling REST-API-profiel, met PKIoverheid-certificaten en ondertekende berichten |

## Standaarden

Het koppelvlak voldoet aan de volgende wetten, afspraken en standaarden:

- [NORA](https://www.noraonline.nl/wiki/NORA_online);
- [BIO](https://www.bio-overheid.nl/);
- [Digikoppeling, REST-API-profiel](https://logius-standaarden.github.io/Digikoppeling-Koppelvlakstandaard-REST-API/);
- [Nederlandse API-strategie](https://docs.geostandaarden.nl/api/API-Strategie/) en de [NL GOV REST API Design Rules](https://logius-standaarden.github.io/API-Design-Rules/);
- de Algemene verordening gegevensbescherming (AVG) en de Uitvoeringswet AVG;
- het [Gemeentelijk Gegevensmodel](https://www.gemeentelijkgegevensmodel.nl/) voor de inhoud van de berichten.

## Hoofdkeuzes

- De leverancier biedt een service aan die rechtstreeks door de afnemer wordt bevraagd. In het transport is geen centrale routering of opslag nodig.
- De uitwisseling volgt het Digikoppeling REST-API-profiel, met [FSC](https://fsc-standaard.nl/) (Federatieve Service Connectiviteit) voor de connectiviteit. Voor FSC is een referentie-implementatie beschikbaar (OpenFSC).
- Services worden gepubliceerd in de FSC-directory van [RINIS](https://www.rinis.nl/nl/), zodat afnemers ze kunnen vinden.
- Het transport loopt over het open internet, met tweezijdig TLS en PKIoverheid-certificaten. Aansluiting op een gesloten netwerk is niet nodig.
- Berichten worden ondertekend en niet afzonderlijk versleuteld.
- Een groot antwoord wordt over meerdere berichten verdeeld (paginering). De gegevens daarvoor horen bij de API en niet bij het uitwisselmodel.

Wie al een FSC-koppeling heeft ingericht, kan de componenten, certificaten en werkwijze hergebruiken.

## Rollen en toegang

In het berichtenverkeer zijn drie rollen te onderscheiden:

- de **aanbieder**: de HR-softwareleverancier namens de gemeente, of de gemeente zelf;
- de **afnemer**: de beheerder van het Verzuimportaal, en mogelijk andere afnemers met een eigen contract;
- de **directory** waarin de services worden gepubliceerd.

De afnemer zoekt de service op in de directory, sluit een FSC-contract met de aanbieder en haalt daarna de gegevens op. Elke gemeente geeft zelf toestemming: een afnemer ontvangt alleen de leveringen van gemeenten die voor die afnemer toestemming hebben gegeven.

## Nog uit te werken

- de OpenAPI-beschrijving (OAS3), met het vraagbericht, het antwoordbericht en de paginering;
- de wijze van ondertekenen;
- de stappen voor aansluiten en testen, en de naamgeving van de services;
- de niet-functionele eisen, zoals beschikbaarheid, de omvang van berichten en logging;
- het beveiligingsniveau, dat in de DPIA wordt vastgesteld.
