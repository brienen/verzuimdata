# Vraag en antwoord

## Over de specificatie

**Is deze specificatie vastgesteld?**
Nee. Versie 0.1 is een concept om het gesprek met leveranciers en gemeenten te voeren. Pas na afstemming en een pilot wordt een versie vastgesteld. Daarna verandert de specificatie alleen nog via versiebeheer, omdat leveranciers erop bouwen.

**Waarom is het Gemeentelijk Gegevensmodel de basis?**
Omdat een leverancier die het GGM ondersteunt dan geen tweede vertaling hoeft te maken, en omdat dezelfde gegevens dan ook voor andere toepassingen bruikbaar zijn, zoals Venster voor Bedrijfsvoering en de Personeelsmonitor.

**Het model volgt een wijzigingsvoorstel voor het GGM. Wat als dat voorstel verandert?**
Dan verandert de specificatie mee, in een nieuwe versie. Het JSON-schema en de documentatie worden uit het model gegenereerd; een wijziging in het model komt dus op één plek binnen.

**Waarom worden gegevens op registratieniveau gevraagd en niet als totalen?**
Zo worden alle indicatoren op één plek en op dezelfde manier berekend, en zijn uitsplitsingen naar leeftijd, schaal en organisatieonderdeel mogelijk. Of levering op dit niveau doorgaat, volgt uit de gegevensbeschermingseffectbeoordeling (DPIA). Het alternatief is berekening bij de bron.

## Over de gegevens

**Waarom drie lijsten met aanstellingscontracten?**
De gegevens verschillen per soort: alleen een arbeidsovereenkomst heeft een schaal, een contractsoort en een cao. Met drie lijsten dwingt het schema af dat de juiste gegevens bij de juiste soort staan, en dat de aanstellingssoort bij de lijst past.

**Ons pakket kent geen externe inhuur. Wat nu?**
Dan blijft de lijst `inhuurovereenkomsten` weg. Wij horen graag in welk systeem de inhuur bij uw klanten wel staat.

**Mogen wij de oorzaak van het verzuim meesturen?**
Nee. De verzuimsoort kent alleen de waarden die een werkgever mag vastleggen. Een bericht met andere velden wordt afgekeurd.

**Wat is het verschil tussen het contract en de inzet?**
Het contract legt vast dat en voor hoeveel uur iemand voor de organisatie werkt. De inzet legt vast voor welke functie en bij welke eenheid die uren worden gemaakt. Werkt iemand voor twee teams, dan heeft het contract twee inzetten.

**Wat is het verschil tussen een leidinggevende functie en een leidinggevende rol?**
`leidinggevend` bij de functie zegt dat aan de functie leidinggevende taken zijn verbonden. De rol met rolsoort `Leidinggevende` zegt wie in welke periode feitelijk leiding geeft aan welke eenheid. Beide zijn nodig: de eerste voor de indeling van functies, de tweede voor de span of control.

## Openstaande keuzes

1. **Niveau van de levering.** Registratieniveau, zoals in dit concept, of berekening van indicatoren bij de bron. De keuze volgt uit de DPIA.
2. **Afnemer en rolverdeling.** Welke organisatie het Verzuimportaal beheert, wie verwerkingsverantwoordelijke is en hoe een gemeente toestemming geeft.
3. **Sleutel van de werknemer.** Hoe de sleutel wordt gemaakt, zodat hij stabiel is en niet tot een persoon te herleiden.
4. **Historie van de contractomvang.** Hoe een wijziging van de uren binnen een contract wordt geleverd.
5. **Verplichte velden.** In versie 0.1 volgt de verplichting de kardinaliteit in het informatiemodel. Wij horen graag van leveranciers welke verplichte velden niet haalbaar zijn.
6. **Afbakening van de organisatie.** Welke medewerkers en organisatieonderdelen meetellen, zoals de griffie en de sociale werkvoorziening.
7. **Frequentie en historie.** Jaarlijks of vaker, en vanaf welk jaar gegevens beschikbaar zijn.
8. **Andere overheden.** Wat nodig is om ook provincies en waterschappen aan te sluiten; een levering is nu aan een gemeentecode gebonden.
9. **Technische uitwerking van het transport.** Zie [Koppelvlak API](api/index.md#nog-uit-te-werken).
