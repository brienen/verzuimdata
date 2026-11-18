# Uitwisselspecificatie HR-gegevens Verzuimportaal

!!! warning "Concept ter bespreking"
    Dit is versie 0.1: een eerste concept om het gesprek met HR-softwareleveranciers en gemeenten te voeren. Niets op deze site is vastgesteld. Het informatiemodel volgt een wijzigingsvoorstel voor het Gemeentelijk Gegevensmodel dat nog niet is aangenomen.

VNG Risicobeheer ontwikkelt samen met gemeenten het **Verzuimportaal**: een voorziening waarmee gemeenten, en later ook provincies en waterschappen, inzicht krijgen in hun verzuim, zich met elkaar kunnen vergelijken en een realistische verzuimnorm krijgen. De gegevens die daarvoor nodig zijn, staan al in de personeels- en salarisadministratie van gemeenten. Nu worden ze jaarlijks met vragenlijsten en handmatige bewerkingen verzameld. Dat geldt ook voor de benchmark Venster voor Bedrijfsvoering en voor de Personeelsmonitor van A&O fonds Gemeenten, die grotendeels dezelfde personeelsgegevens gebruiken.

Deze site beschrijft hoe HR-softwareleveranciers die gegevens namens gemeenten geautomatiseerd kunnen aanleveren. Het doel is één specificatie die meerdere toepassingen bedient, zodat leveranciers één keer bouwen en gemeenten niet dubbel worden uitgevraagd.

## Wat staat waar

| Onderdeel | Inhoud |
| :--- | :--- |
| [JSON-schema en voorbeelden](uitwisselspecificatie.md) | De opbouw van een bericht, het JSON-schema en voorbeeldbestanden. Begin hier. |
| [Selectie en aanlevering](aanlevering.md) | Welke werknemers, contracten en verzuimgevallen in een levering horen, en de regels voor sleutels en historie. |
| [Informatiemodel](Hoofdlijnen_Model HR.md) | De betekenis van de gegevens: objecttypen, kenmerken en waardelijsten uit het Gemeentelijk Gegevensmodel. |
| [Koppelvlak API](api/index.md) | Hoe de berichten worden opgehaald en beveiligd. Dit deel is nog op hoofdlijnen. |

## Informatiemodel en uitwisselspecificatie

Een **informatiemodel** beschrijft de gegevens van een domein en hun onderlinge relaties, met eenduidige definities. Het informatiemodel van deze specificatie is het deel van Model HR van het [Gemeentelijk Gegevensmodel](https://www.gemeentelijkgegevensmodel.nl/) (GGM) dat voor het Verzuimportaal nodig is. Objecttypen en kenmerken houden de naam die zij in het GGM hebben, zodat een leverancier die het GGM ondersteunt geen tweede vertaling hoeft te maken.

Een **uitwisselspecificatie** legt vast welke gegevens uit het informatiemodel worden uitgewisseld en in welke vorm. Niet alles uit het informatiemodel wordt uitgewisseld: direct identificerende gegevens van werknemers, salarisbedragen en kosten blijven in de bron.

Beide worden uit hetzelfde model gegenereerd. Het JSON-schema en de detailspecificatie van het informatiemodel kunnen daardoor niet van elkaar afwijken.
