# Selectie en aanlevering

Deze pagina beschrijft welke gegevens in een levering horen en welke regels gelden naast het JSON-schema.

## Uitwisselvarianten

Het begrip levering maakt het mogelijk om in één bericht voor één of voor meerdere gemeenten te leveren.

| Variant | Aantal leveringen | Aanleverende organisatie |
| :--- | :--- | :--- |
| De gemeente levert zelf | Eén | Naam van de gemeente; geen KvK-nummer |
| Een derde levert voor één gemeente | Eén | Naam en KvK-nummer van de leverancier |
| Een leverancier levert voor meerdere gemeenten | Eén per gemeente, genummerd met de teller | Naam en KvK-nummer van de leverancier, in elke levering herhaald |

In alle varianten bevat elke levering de gemeentecode van de gemeente waarover de gegevens gaan. Een leverancier levert uitsluitend voor gemeenten die daarvoor opdracht hebben gegeven.

## Verslagperiode

Een levering gaat over een verslagperiode: `startdatumLevering` tot en met `einddatumLevering`. In eerste instantie is dat een kalenderjaar, met 31 december als peildatum. Levering per kwartaal is een mogelijke vervolgstap.

## Selectieregels

- **Werknemers.** Alle werknemers met ten minste één aanstellingscontract dat de verslagperiode raakt. Een werknemer die binnen de periode begint en weer vertrekt, hoort er dus bij.
- **Aanstellingscontracten.** Alle contracten van die werknemers die de periode raken: arbeidsovereenkomsten, inhuurovereenkomsten en overige aanstellingen. Een verlenging of een nieuwe overeenkomst is een nieuw contract.
- **Inzet.** Alle inzet op die contracten die de periode raakt. Opeenvolgende inzetten laten zien wanneer iemand van functie of organisatieonderdeel is gewisseld.
- **Verzuim.** Alle verzuim dat de periode raakt, met de werkelijke begindatum, ook als die vóór de periode ligt. Dat is nodig om de verzuimduur te bepalen. Lopend verzuim heeft geen einddatum.
- **Verlof.** Toegekend verlof dat de periode raakt. Vakantieverlof hoeft niet te worden geleverd.
- **Rollen.** Alle rollen die in de periode gelden. De rol met rolsoort `Leidinggevende` bepaalt wie aan welke eenheid leiding geeft.
- **Formatieplaatsen, functies en organisatorische eenheden.** Alle voorkomens die in de periode bestaan, ook onbezette formatieplaatsen. Elk object waarnaar een contract, inzet, rol of formatieplaats verwijst, staat in de levering.

## Drie soorten aanstelling

Wie voor de gemeente werkt, doet dat op grond van een aanstellingscontract. De specificatie kent drie soorten, elk met een eigen lijst bij de werknemer en een eigen waardelijst voor de aanstellingssoort.

| Lijst | Voor wie | Aanstellingssoorten | Telt voor de bezetting |
| :--- | :--- | :--- | :--- |
| `arbeidsovereenkomsten` | Eigen personeel | Reguliere arbeidsovereenkomst, Oproepovereenkomst, Leerarbeidsovereenkomst | Ja; welke precies volgt uit de cao en de aanstellingssoort |
| `inhuurovereenkomsten` | Externe krachten | Uitzendovereenkomst, Detachering, Payrollovereenkomst, Opdracht aan zelfstandige | Nee; wel voor externe inhuur en flexibele bezetting |
| `overigeAanstellingen` | Stagiairs, werkervaringsplaatsen en overige vormen | Stageovereenkomst, Werkervaringsplaats, Overig | Nee |

De schaal, de contractsoort, de cao en de reden van het einde bestaan alleen bij een arbeidsovereenkomst. Wie eerst is ingehuurd en daarna in dienst komt, houdt hetzelfde `werknemerID` en krijgt een arbeidsovereenkomst naast de afgesloten inhuurovereenkomst.

## Sleutels

- Het **`werknemerID`** is een sleutel zonder betekenis. Het personeelsnummer, het burgerservicenummer of een deel van de naam mogen er niet in voorkomen en mogen er niet uit af te leiden zijn. De leverancier gebruikt in elke levering voor dezelfde werknemer bij dezelfde gemeente dezelfde sleutel, zodat gegevens over meerdere perioden bij elkaar horen.
- Het **`aanstellingscontractID`**, het **`verzuimID`** en het **`formatieplaatsID`** zijn binnen een levering uniek en in elke levering dezelfde voor hetzelfde object.
- De **`code`** van een functie en de **`organisatieIdentificatie`** van een organisatorische eenheid zijn de sleutels die de gemeente zelf gebruikt.

Hoe de sleutel van een werknemer precies wordt gemaakt, ligt nog niet vast.

## Historie

- **Contractomvang.** Het veld `urenPerWeek` bevat de omvang aan het einde van de verslagperiode, of aan het einde van het contract als dat eerder ligt. Hoe een wijziging van de contracturen binnen een contract wordt geleverd, ligt nog niet vast.
- **Percentage arbeidsongeschiktheid.** Het veld `percentageArbeidsongeschiktheid` van een verzuimgeval bevat het laatst geldende percentage. Is het percentage tijdens het verzuim gewijzigd, bijvoorbeeld bij gedeeltelijk herstel, dan staat de historie in `verloop`: één regel per periode, met de begindatum en het percentage. Een wijziging van het percentage is geen nieuw verzuimgeval.
- **Formatie.** Een wijziging van de omvang van een formatieplaats wordt geleverd als een nieuwe formatieplaats met een eigen begindatum; de oude krijgt een einddatum.

## Regels buiten het schema

Een JSON-schema kan niet alles afdwingen. Voor een geldig bericht gelden ook deze regels:

1. Elke verwijzing bestaat in dezelfde levering: `functie` verwijst naar de `code` van een functie, `organisatorischeEenheid` en `isDeelVan` naar de `organisatieIdentificatie` van een eenheid, en `formatieplaats` naar een `formatieplaatsID`.
2. Sleutels zijn binnen een levering uniek.
3. Een werknemer heeft ten minste één aanstellingscontract, in een van de drie lijsten.
4. Precies één organisatorische eenheid heeft geen `isDeelVan`: de organisatie als geheel.
5. Een einddatum ligt niet vóór de bijbehorende begindatum.
6. Het `kvkNummer` van de aanleverende organisatie is gevuld als een andere organisatie dan de gemeente aanlevert.

De eerste drie regels worden bij de voorbeeldbestanden van deze specificatie automatisch gecontroleerd.

## Wat niet wordt uitgewisseld

- **Direct identificerende gegevens van werknemers**: naam, burgerservicenummer, geboortedatum, adres en contactgegevens.
- **De oorzaak of diagnose van verzuim.** Medische gegevens liggen bij bedrijfsarts en arbodienst; een werkgever mag ze niet vastleggen.
- **Salarisbedragen, loonsom, inhuurkosten en opleidingskosten.** Deze gegevens komen uit de salaris-, inkoop- en financiële administratie. Zij zijn kandidaat voor een latere versie.
- **Financiën, ICT en huisvesting.** Dit zijn geen HR-gegevens.

!!! note "Verzuim per werknemer blijft een gezondheidsgegeven"
    Ook zonder naam is verzuim per werknemer een gezondheidsgegeven. Levering op dit niveau kan daarom pas na een gegevensbeschermingseffectbeoordeling (DPIA), verwerkersafspraken en toestemming van de gemeente. Het alternatief is dat de indicatoren bij de bron worden berekend en alleen totalen worden geleverd. De gegevens en definities in deze specificatie zijn in beide gevallen dezelfde.
