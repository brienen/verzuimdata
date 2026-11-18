# Uitwisselspecificatie uitgelegd

Deze pagina beschrijft in gewone taal welke gegevens een bericht bevat. De technische vastlegging staat in het JSON-schema op de pagina [Uitwisselspecificatie](uitwisselspecificatie.md); bij een verschil geldt het schema. De tabellen op deze pagina worden uit hetzelfde model gegenereerd als het schema.

## Opbouw van een bericht

Een bericht is als volgt opgebouwd:

1. **Het bericht** zelf noemt de gegevensleverancier, de verslagperiode en het moment van aanleveren.
2. Een bericht bevat één of meer **leveringen**. Een levering bevat de gegevens van precies één gemeente.
3. Een levering begint met de organisatie: de **organisatorische eenheden**, de **functies** en de **formatieplaatsen**.
4. Daarna volgen de **werknemers**. Bij elke werknemer staan de aanstellingscontracten (arbeidsovereenkomsten, inhuurovereenkomsten en overige aanstellingen) met de bijbehorende inzet, en verder de rollen, het verzuim en het verlof.

Een werknemer, contract of formatieplaats verwijst naar een functie of organisatorische eenheid met de sleutel van dat object: de `code` van de functie, de `organisatieIdentificatie` van de eenheid of het `formatieplaatsID`. Het object waarnaar wordt verwezen, staat in dezelfde levering.

!!! note "Geen direct identificerende gegevens"
    Een bericht bevat geen naam, burgerservicenummer, geboortedatum, adres of contactgegevens van werknemers. Een werknemer wordt aangeduid met een sleutel zonder betekenis, en in plaats van de geboortedatum wordt het geboortejaar geleverd. De oorzaak of diagnose van verzuim maakt geen deel uit van de uitwisseling.

## Onderdelen van het bericht


### Het bericht { #Uitwisselmodel }

Eén bericht met HR-gegevens van één of meer gemeenten over één verslagperiode.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `codeGegevensleverancier` | tekst (max. 200) | ja | De naam van de gegevensleverancier (softwareleverancier of hostingpartij) en de versie van het pakket. |
| `versieSpecificatie` | tekst (max. 20) | ja | De versie van de uitwisselspecificatie waaraan het bericht voldoet, bijvoorbeeld v0.1. |
| `startdatumLevering` | datum | ja | De eerste dag van de verslagperiode. |
| `einddatumLevering` | datum | ja | De laatste dag van de verslagperiode. |
| `aanleverdatumEnTijd` | datum en tijd | ja | Het moment waarop het bericht is samengesteld. |
| `leveringen` | lijst van [Levering](#Levering) | ja | De leveringen in het bericht: één per gemeente. |


### Levering { #Levering }

De HR-gegevens van precies één gemeente over de verslagperiode. Een leverancier die voor meerdere gemeenten levert, neemt per gemeente één levering op.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `teller` | geheel getal, vanaf 1 | ja | Het volgnummer van de levering binnen het bericht, te beginnen bij 1. |
| `gemeentecode` | tekst (max. 4) | ja | De CBS-gemeentecode van de gemeente waarover de gegevens gaan, vier cijfers met voorloopnullen. |
| `aanleverendeOrganisatie` | één [Aanleverende organisatie](#AanleverendeOrganisatie) | ja | De organisatie die de levering aanlevert. |
| `organisatorischeEenheden` | lijst van [Organisatorische eenheid](#OrganisatorischeEenheidHR) | ja | De organisatorische eenheden van de gemeente die in de verslagperiode bestaan. |
| `functies` | lijst van [Functie](#Functie) | nee | De functies waarnaar in de levering wordt verwezen. |
| `formatieplaatsen` | lijst van [Formatieplaats](#Formatieplaats) | nee | De formatieplaatsen die in de verslagperiode bestaan, ook de onbezette. |
| `werknemers` | lijst van [Werknemer](#Werknemer) | nee | De werknemers met ten minste één aanstellingscontract dat de verslagperiode raakt. |


### Aanleverende organisatie { #AanleverendeOrganisatie }

De organisatie die de gegevens van de levering aanlevert. Levert de gemeente zelf, dan is dit de gemeente; anders de leverancier die namens de gemeente levert.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `naam` | tekst (max. 200) | ja | De naam van de aanleverende organisatie. |
| `kvkNummer` | tekst (max. 8) | nee | Het KvK-nummer van de aanleverende organisatie, acht cijfers. Verplicht als een andere organisatie dan de gemeente aanlevert. |
| `contactpersonen` | lijst van [Contactpersoon](#Contactpersoon) | nee | De contactpersonen voor de levering. |


### Contactpersoon { #Contactpersoon }

Een persoon bij de aanleverende organisatie die vragen over de levering kan beantwoorden.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `naam` | tekst (max. 200) | ja | De naam van de contactpersoon. |
| `functietitel` | tekst (max. 100) | nee | De functie van de contactpersoon. |
| `email` | e-mailadres | nee | Het e-mailadres van de contactpersoon. |
| `telefoonnummer` | tekst (max. 20) | nee | Het telefoonnummer van de contactpersoon. |


### Organisatorische eenheid { #OrganisatorischeEenheidHR }

Een organisatorische eenheid zoals vastgelegd in de personeelsadministratie. De plaats in de organisatie volgt uit het veld isDeelVan.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `organisatieIdentificatie` | tekst (max. 24) | ja | Een korte identificatie van de organisatorische eenheid. |
| `naam` | tekst (max. 80) | ja | De naam van de eenheid in de personeelsadministratie. |
| `type` | waarde uit [OrganisatorischeEenheidsoort](#OrganisatorischeEenheidsoort) | ja | Het niveau van de eenheid in de indeling van de organisatie. |
| `isDeelVan` | tekst (max. 24) | nee | De organisatorische eenheid waarvan deze eenheid deel uitmaakt. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. Leeg bij de hoogste eenheid, de organisatie als geheel. |
| `datumOntstaan` | datum | nee | De datum waarop de organisatorische eenheid is ontstaan. |
| `datumOpheffing` | datum | nee | De datum waarop de organisatorische eenheid is opgeheven. |


### Functie { #Functie }

Het samenstel van taken en werkzaamheden dat aan een werknemer kan worden opgedragen.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `code` | tekst (max. 50) | ja | De code waarmee de functie in de organisatie wordt aangeduid. Sleutel voor de vertaaltabel naar een landelijke indeling. |
| `naam` | tekst (max. 80) | ja | De naam van de functie. |
| `schaal` | geheel getal, vanaf 1 | ja | De salarisschaal waarin de functie is gewaardeerd. |
| `leidinggevend` | ja/nee (`true` of `false`) | ja | Aanduiding dat aan de functie leidinggevende taken en personele verantwoordelijkheid zijn verbonden. Projectleiders, meewerkend voorlieden en coördinatoren tellen niet als leidinggevend. |
| `werkomgeving` | waarde uit [Werkomgeving](#Werkomgeving) | nee | De omgeving waarin het werk van de functie zich hoofdzakelijk afspeelt. |
| `normProfiel` | één [Normprofiel](#NormProfiel) | nee | Het normprofiel waarop de functie is gebaseerd. |


### Normprofiel { #NormProfiel }

Een generieke functie uit een landelijk functiewaarderingssysteem, waarop functies van de organisatie zijn gebaseerd. Voor gemeenten het systeem HR21.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `code` | tekst (max. 10) | ja | De code van het normprofiel in het functiewaarderingssysteem. |
| `omschrijving` | tekst (max. 100) | ja | De naam of omschrijving van het normprofiel. |
| `schaal` | geheel getal, vanaf 1 | ja | De salarisschaal die bij het normprofiel hoort. |
| `functiehuis` | één [Functiehuis](#Functiehuis) | ja | Het functiehuis waarvan het normprofiel deel uitmaakt. |


### Functiehuis { #Functiehuis }

Model waarin functies van een organisatie worden beschreven.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `naam` | tekst (max. 80) | ja | De naam van het functiehuis, bijvoorbeeld HR21. |


### Formatieplaats { #Formatieplaats }

Een in het formatieplan vastgestelde arbeidsplaats bij een organisatorische eenheid. De formatie is de toegestane omvang, niet de werkelijke bezetting. Een formatieplaats bestaat ook als zij onbezet is.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `formatieplaatsID` | tekst (max. 64) | ja | Een sleutel die de formatieplaats binnen de levering aanduidt. |
| `urenPerWeek` | getal, 0 tot en met 168 | ja | De omvang van de formatieplaats in uren per week. |
| `datumBegin` | datum | ja | De eerste dag waarop de formatieplaats geldig is. Grondslag voor de formatie op een peildatum. |
| `datumEinde` | datum | nee | De laatste dag waarop de formatieplaats geldig is. Leeg zolang de formatieplaats bestaat. |
| `functie` | tekst (max. 50) | ja | De functie waarvoor de formatieplaats is bestemd. Verwijst met de code naar een functie in dezelfde levering. |
| `organisatorischeEenheid` | tekst (max. 24) | ja | De organisatorische eenheid waartoe de formatieplaats behoort. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. |


### Werknemer { #Werknemer }

Een persoon die op grond van een aanstellingscontract werkzaamheden verricht voor de organisatie. Omvat eigen personeel, ingehuurde krachten, stagiairs en mensen op een werkervaringsplaats. Een werknemer wordt aangeduid met een sleutel zonder betekenis; naam, burgerservicenummer, geboortedatum en adres worden niet uitgewisseld.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `werknemerID` | tekst (max. 64) | ja | Een sleutel zonder betekenis die de werknemer binnen de gemeente aanduidt. De sleutel is in elke levering dezelfde, zodat gegevens over meerdere perioden bij elkaar horen. Het personeelsnummer, het burgerservicenummer of een deel van de naam mogen er niet in voorkomen of uit af te leiden zijn. |
| `geboortejaar` | geheel getal, 1900 tot en met 2100 | ja | Het jaar waarin de werknemer is geboren. Het geboortejaar vervangt de geboortedatum; het is genoeg voor de leeftijdsopbouw. |
| `geslachtsaanduiding` | waarde uit [Geslachtsaanduiding](#Geslachtsaanduiding) | ja | Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht onbekend is. |
| `arbeidsovereenkomsten` | lijst van [Arbeidsovereenkomst](#Arbeidsovereenkomst) | nee | De aanstellingscontracten van de werknemer van het subtype Arbeidsovereenkomst. |
| `inhuurovereenkomsten` | lijst van [Inhuurovereenkomst](#Inhuurovereenkomst) | nee | De aanstellingscontracten van de werknemer van het subtype Inhuurovereenkomst. |
| `overigeAanstellingen` | lijst van [Overige aanstelling](#OverigeAanstelling) | nee | De aanstellingscontracten van de werknemer van het subtype OverigeAanstelling. |
| `rollen` | lijst van [Rol](#Rol) | nee | De rol die de werknemer vervult. |
| `verzuimgevallen` | lijst van [Verzuim](#Verzuim) | nee | Het verzuim van de werknemer. |
| `verlofperioden` | lijst van [Verlof](#Verlof) | nee | Het verlof van de werknemer. |


### Arbeidsovereenkomst { #Arbeidsovereenkomst }

De overeenkomst waarbij de werknemer zich verbindt om in dienst van de organisatie, tegen loon, gedurende zekere tijd arbeid te verrichten. Voor eigen personeel. Alleen arbeidsovereenkomsten tellen voor de bezetting; welke precies, volgt uit de cao en de aanstellingssoort. Een verlenging of een nieuwe overeenkomst is een nieuw voorkomen.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `aanstellingscontractID` | tekst (max. 64) | ja | Een sleutel die het aanstellingscontract binnen de levering aanduidt. De sleutel is in elke levering dezelfde. |
| `aanstellingssoort` | waarde uit [AanstellingssoortArbeidsovereenkomst](#AanstellingssoortArbeidsovereenkomst) | ja | De soort aanstelling. Elke waarde hoort bij precies een subtype. Bepaalt samen met de cao of de aanstelling tot de bezetting telt, en onderscheidt de vormen van inhuur. |
| `datumStart` | datum | ja | De eerste dag waarop het contract geldt. |
| `datumEinde` | datum | nee | De laatste dag waarop het contract geldt. Leeg zolang het contract loopt en geen einddatum is overeengekomen. |
| `urenPerWeek` | getal, 0 tot en met 168 | ja | Het aantal uren per week dat volgens het contract wordt gewerkt. Grondslag voor de bezetting in fte en voor de weging van verzuim naar deeltijd. |
| `schaal` | geheel getal, vanaf 1 | ja | De salarisschaal waarin de werknemer is ingedeeld. Het waardebereik volgt uit de cao; voor gemeenten 1 tot en met 20. |
| `contractsoort` | waarde uit [Contractsoort](#Contractsoort) | ja | Aanduiding of de overeenkomst voor bepaalde of voor onbepaalde tijd is aangegaan. Grondslag voor tijdelijke dienst en voor vaste en flexibele bezetting. |
| `cao` | waarde uit [Cao](#Cao) | ja | De collectieve arbeidsovereenkomst die op de overeenkomst van toepassing is. |
| `banenafspraak` | ja/nee (`true` of `false`) | nee | Aanduiding dat de overeenkomst meetelt voor de banenafspraak voor mensen met een arbeidsbeperking. Grondslag voor medewerkers met afstand tot de arbeidsmarkt. |
| `redenEinde` | waarde uit [RedenEindeArbeidsovereenkomst](#RedenEindeArbeidsovereenkomst) | nee | De reden waarom de overeenkomst is geëindigd. Leeg zolang de overeenkomst loopt. Grondslag voor vrijwillige en onvrijwillige uitstroom. |
| `functie` | tekst (max. 50) | nee | De functie die in het contract is overeengekomen. Verwijst met de code naar een functie in dezelfde levering. |
| `organisatorischeEenheid` | tekst (max. 24) | ja | De organisatorische eenheid waarbij de werknemer op grond van het contract is geplaatst. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. Werkt iemand voor meer eenheden, dan volgt de verdeling uit de inzet. |
| `formatieplaats` | tekst (max. 64) | nee | De formatieplaats waaraan het contract is toegewezen. Verwijst met het formatieplaatsID naar een formatieplaats in dezelfde levering. |
| `inzetten` | lijst van [Inzet](#Inzet) | nee | De inzet die op grond van het contract wordt verricht. |


### Inhuurovereenkomst { #Inhuurovereenkomst }

Een overeenkomst op grond waarvan een externe kracht werkzaamheden verricht voor de organisatie, zonder bij haar in dienst te zijn. Voor externe krachten: uitzendwerk, detachering vanuit een andere organisatie, payrolling en opdrachten aan zelfstandigen; de aanstellingssoort zegt welke vorm het is. Telt niet voor de bezetting, wel voor de externe inhuur en de flexibele bezetting.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `aanstellingscontractID` | tekst (max. 64) | ja | Een sleutel die het aanstellingscontract binnen de levering aanduidt. De sleutel is in elke levering dezelfde. |
| `aanstellingssoort` | waarde uit [AanstellingssoortInhuurovereenkomst](#AanstellingssoortInhuurovereenkomst) | ja | De soort aanstelling. Elke waarde hoort bij precies een subtype. Bepaalt samen met de cao of de aanstelling tot de bezetting telt, en onderscheidt de vormen van inhuur. |
| `datumStart` | datum | ja | De eerste dag waarop het contract geldt. |
| `datumEinde` | datum | nee | De laatste dag waarop het contract geldt. Leeg zolang het contract loopt en geen einddatum is overeengekomen. |
| `urenPerWeek` | getal, 0 tot en met 168 | ja | Het aantal uren per week dat volgens het contract wordt gewerkt. Grondslag voor de bezetting in fte en voor de weging van verzuim naar deeltijd. |
| `functie` | tekst (max. 50) | nee | De functie die in het contract is overeengekomen. Verwijst met de code naar een functie in dezelfde levering. |
| `organisatorischeEenheid` | tekst (max. 24) | ja | De organisatorische eenheid waarbij de werknemer op grond van het contract is geplaatst. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. Werkt iemand voor meer eenheden, dan volgt de verdeling uit de inzet. |
| `formatieplaats` | tekst (max. 64) | nee | De formatieplaats waaraan het contract is toegewezen. Verwijst met het formatieplaatsID naar een formatieplaats in dezelfde levering. |
| `inzetten` | lijst van [Inzet](#Inzet) | nee | De inzet die op grond van het contract wordt verricht. |


### Overige aanstelling { #OverigeAanstelling }

Een aanstellingscontract dat geen arbeidsovereenkomst en geen inhuurovereenkomst is. Voor wie in de organisatie werkt zonder arbeidsovereenkomst en zonder te zijn ingehuurd: stagiairs, mensen op een werkervaringsplaats en overige vormen, zoals vrijwilligers. Telt niet voor de bezetting en niet voor de externe inhuur.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `aanstellingscontractID` | tekst (max. 64) | ja | Een sleutel die het aanstellingscontract binnen de levering aanduidt. De sleutel is in elke levering dezelfde. |
| `aanstellingssoort` | waarde uit [AanstellingssoortOverigeAanstelling](#AanstellingssoortOverigeAanstelling) | ja | De soort aanstelling. Elke waarde hoort bij precies een subtype. Bepaalt samen met de cao of de aanstelling tot de bezetting telt, en onderscheidt de vormen van inhuur. |
| `datumStart` | datum | ja | De eerste dag waarop het contract geldt. |
| `datumEinde` | datum | nee | De laatste dag waarop het contract geldt. Leeg zolang het contract loopt en geen einddatum is overeengekomen. |
| `urenPerWeek` | getal, 0 tot en met 168 | ja | Het aantal uren per week dat volgens het contract wordt gewerkt. Grondslag voor de bezetting in fte en voor de weging van verzuim naar deeltijd. |
| `functie` | tekst (max. 50) | nee | De functie die in het contract is overeengekomen. Verwijst met de code naar een functie in dezelfde levering. |
| `organisatorischeEenheid` | tekst (max. 24) | ja | De organisatorische eenheid waarbij de werknemer op grond van het contract is geplaatst. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. Werkt iemand voor meer eenheden, dan volgt de verdeling uit de inzet. |
| `formatieplaats` | tekst (max. 64) | nee | De formatieplaats waaraan het contract is toegewezen. Verwijst met het formatieplaatsID naar een formatieplaats in dezelfde levering. |
| `inzetten` | lijst van [Inzet](#Inzet) | nee | De inzet die op grond van het contract wordt verricht. |


### Inzet { #Inzet }

De inzet van een werknemer voor een functie bij een organisatorische eenheid in een bepaalde periode, op grond van een aanstellingscontract. Een contract kan meer inzetten hebben, gelijktijdig of na elkaar. Opeenvolgende inzetten vormen de functie- en afdelingshistorie waaruit doorstroom en verblijfsduur in een functie volgen.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `datumBegin` | datum | ja | De eerste dag van de inzet. |
| `datumEinde` | datum | nee | De laatste dag van de inzet. Leeg zolang de inzet loopt. |
| `uren` | getal, 0 tot en met 168 | ja | Het aantal uren per week van de inzet. |
| `percentage` | getal, 0 tot en met 100 | nee | Het deel van de uren van de inzet dat daadwerkelijk wordt uitgevoerd, als percentage. |
| `bestemming` | waarde uit [BestemmingInzet](#BestemmingInzet) | ja | Aanduiding of de inzet voor de eigen organisatie is of voor derden. Grondslag voor de inzet voor derden. |
| `schaal` | geheel getal, vanaf 1 | nee | De salarisschaal waarin de werknemer voor deze inzet is ingedeeld. Alleen gevuld als de schaal afwijkt van die van de functie, bijvoorbeeld bij een aanloopschaal. |
| `functie` | tekst (max. 50) | ja | De functie waarvoor de werknemer wordt ingezet. Verwijst met de code naar een functie in dezelfde levering. |
| `organisatorischeEenheid` | tekst (max. 24) | ja | De organisatorische eenheid waarbij de werknemer wordt ingezet. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. |


### Rol { #Rol }

Een taak of bevoegdheid die een werknemer in een bepaalde periode vervult binnen een organisatorische eenheid, naast of als onderdeel van zijn functie. De rol legt vast wie in welke periode leiding geeft aan welke eenheid.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `rolsoort` | waarde uit [Rolsoort](#Rolsoort) | ja | De soort rol. Maakt leidinggevenden eenduidig herkenbaar. |
| `omschrijving` | tekst (max. 50) | nee | Een vrije omschrijving van de rol. |
| `datumBegin` | datum | ja | De eerste dag waarop de werknemer de rol vervult. |
| `datumEinde` | datum | nee | De laatste dag waarop de werknemer de rol vervult. Leeg zolang de rol wordt vervuld. |
| `organisatorischeEenheid` | tekst (max. 24) | nee | De organisatorische eenheid waarbinnen de werknemer de rol vervult. Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering. |


### Verzuim { #Verzuim }

Een aaneengesloten periode waarin een werknemer de overeengekomen arbeid geheel of gedeeltelijk niet verricht, anders dan door verlof. Een verzuimgeval loopt van de eerste verzuimdag tot het herstel. Zwangerschaps- en bevallingsverlof is verlof en geen verzuim; ziekte als gevolg van zwangerschap is wel verzuim. De medische oorzaak wordt niet vastgelegd.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `verzuimID` | tekst (max. 64) | ja | Een sleutel die het verzuimgeval binnen de levering aanduidt. De sleutel is in elke levering dezelfde, zodat lopend verzuim over perioden heen te volgen is. |
| `datumtijdStart` | datum en tijd | ja | Het moment waarop het verzuim begint. |
| `datumtijdEinde` | datum en tijd | nee | Het moment waarop het verzuim eindigt. Leeg zolang het verzuim loopt. |
| `percentageArbeidsongeschiktheid` | getal, 0 tot en met 100 | ja | Het deel van de overeengekomen arbeidsduur waarvoor de werknemer verzuimt, als percentage. 100 bij volledig verzuim. Een wijziging is historie van dit kenmerk en geen nieuw verzuimgeval. |
| `verzuimsoort` | waarde uit [Verzuimsoort](#Verzuimsoort) | ja | De soort verzuim. |
| `redenEinde` | waarde uit [RedenEindeVerzuim](#RedenEindeVerzuim) | nee | De reden waarom het verzuim is geëindigd. Leeg zolang het verzuim loopt. Grondslag voor het aandeel hersteld. |
| `verloop` | lijst van [Verloop van de arbeidsongeschiktheid](#Arbeidsongeschiktheidsverloop) | nee | Het verloop van het percentage arbeidsongeschiktheid binnen het verzuimgeval. Alleen nodig als het percentage tijdens het verzuim is gewijzigd. |


### Verloop van de arbeidsongeschiktheid { #Arbeidsongeschiktheidsverloop }

Een periode binnen een verzuimgeval waarin het percentage arbeidsongeschiktheid gelijk blijft. Bestaat alleen in de uitwisseling. In het GGM is het percentage een kenmerk van Verzuim met historie; dit objecttype levert die historie. Een periode loopt tot de begindatum van de volgende periode, of tot het einde van het verzuim.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `datumBegin` | datum | ja | De eerste dag waarop het percentage geldt. |
| `percentageArbeidsongeschiktheid` | getal, 0 tot en met 100 | ja | Het deel van de overeengekomen arbeidsduur waarvoor de werknemer in deze periode verzuimt, als percentage. |


### Verlof { #Verlof }

Een periode waarin een werknemer met toestemming van de werkgever, of op grond van de wet of de cao, de overeengekomen arbeid niet verricht.

| Veld | Type | Verplicht | Betekenis |
| :--- | :--- | :--- | :--- |
| `datumtijdStart` | datum en tijd | ja | Het moment waarop het verlof begint. |
| `datumtijdEinde` | datum en tijd | ja | Het moment waarop het verlof eindigt. |
| `verlofsoort` | waarde uit [Verlofsoort](#Verlofsoort) | ja | De soort verlof. |



## Waardelijsten

Bij een veld met een waardelijst is alleen een waarde uit die lijst toegestaan, precies zoals zij hier is geschreven.


### AanstellingssoortArbeidsovereenkomst { #AanstellingssoortArbeidsovereenkomst }

De soort aanstelling op grond waarvan een werknemer voor de organisatie werkt. Deze lijst bevat de soorten die bij Arbeidsovereenkomst horen.

| Waarde | Betekenis |
| :--- | :--- |
| `Reguliere arbeidsovereenkomst` | Arbeidsovereenkomst met een vaste arbeidsomvang. Telt voor de bezetting. |
| `Oproepovereenkomst` | Arbeidsovereenkomst met een flexibel aantal uren. Telt voor de bezetting en voor de flexibele bezetting. |
| `Leerarbeidsovereenkomst` | Arbeidsovereenkomst met een student in de beroepsbegeleidende leerweg (bbl). Telt voor de bezetting. |



### AanstellingssoortInhuurovereenkomst { #AanstellingssoortInhuurovereenkomst }

De soort aanstelling op grond waarvan een werknemer voor de organisatie werkt. Deze lijst bevat de soorten die bij Inhuurovereenkomst horen.

| Waarde | Betekenis |
| :--- | :--- |
| `Uitzendovereenkomst` | Inhuur via een uitzendbureau. |
| `Detachering` | Inhuur van iemand die in dienst is bij een andere organisatie. |
| `Payrollovereenkomst` | Inhuur waarbij de organisatie zelf werft en het juridisch werkgeverschap bij een payrollbedrijf ligt. |
| `Opdracht aan zelfstandige` | Opdracht aan een zelfstandige zonder personeel (zzp). |



### AanstellingssoortOverigeAanstelling { #AanstellingssoortOverigeAanstelling }

De soort aanstelling op grond waarvan een werknemer voor de organisatie werkt. Deze lijst bevat de soorten die bij OverigeAanstelling horen.

| Waarde | Betekenis |
| :--- | :--- |
| `Stageovereenkomst` | Overeenkomst met een stagiair in het kader van een opleiding. Telt niet voor de bezetting. |
| `Werkervaringsplaats` | Overeenkomst voor het opdoen van werkervaring. Telt niet voor de bezetting. |
| `Overig` | Een andere vorm, zoals vrijwilligerswerk. |



### BestemmingInzet { #BestemmingInzet }

De organisatie waarvoor een inzet wordt verricht.

| Waarde | Betekenis |
| :--- | :--- |
| `Eigen organisatie` | De inzet is voor de eigen organisatie. |
| `Derden` | De inzet is voor een andere organisatie, bijvoorbeeld bij detachering of dienstverlening aan een andere gemeente. |



### Cao { #Cao }

De collectieve arbeidsovereenkomst die op een arbeidsovereenkomst van toepassing is.

| Waarde | Betekenis |
| :--- | :--- |
| `Cao Gemeenten` | De cao voor gemeenten. Telt voor de bezetting. |
| `Cao SGO` | De cao Samenwerkende Gemeentelijke Organisaties. Telt voor de bezetting. |
| `Cao Aan de Slag` | De cao voor mensen met een arbeidsbeperking in dienst van gemeenten. Telt niet voor de bezetting. |
| `Cao Sociale Werkvoorziening` | De cao voor de sociale werkvoorziening. Telt niet voor de bezetting. |
| `Overig` | Een andere cao. |



### Contractsoort { #Contractsoort }

De duur waarvoor een arbeidsovereenkomst is aangegaan.

| Waarde | Betekenis |
| :--- | :--- |
| `Bepaalde tijd` | De overeenkomst eindigt op een vooraf bepaald moment of bij een vooraf bepaalde gebeurtenis. |
| `Onbepaalde tijd` | De overeenkomst heeft geen vooraf bepaald einde. |



### Geslachtsaanduiding { #Geslachtsaanduiding }

Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht onbekend is. De waarden volgen de geslachtsaanduiding van Medewerker in het GGM.

| Waarde | Betekenis |
| :--- | :--- |
| `Vrouw` | De persoon is een vrouw. |
| `Man` | De persoon is een man. |
| `Onbekend` | Het geslacht is niet bekend of niet als man of vrouw geregistreerd. |



### OrganisatorischeEenheidsoort { #OrganisatorischeEenheidsoort }

Het niveau van een organisatorische eenheid in de indeling van de organisatie.

| Waarde | Betekenis |
| :--- | :--- |
| `Concern` | De organisatie als geheel. |
| `Directie` | Een directie of domein. |
| `Afdeling` | Een afdeling. |
| `Team` | Een team. |
| `Griffie` | De griffie; hoort bij de organisatie, maar staat buiten de ambtelijke lijn. |
| `Overig` | Een ander niveau. |



### RedenEindeArbeidsovereenkomst { #RedenEindeArbeidsovereenkomst }

De reden waarom een arbeidsovereenkomst is geëindigd.

| Waarde | Betekenis |
| :--- | :--- |
| `Arbeidsongeschiktheid` | Beëindiging wegens langdurige arbeidsongeschiktheid. |
| `Einde tijdelijk contract` | Het aflopen van een overeenkomst voor bepaalde tijd. |
| `Ontslag door werkgever` | Ontslag op initiatief van de werkgever, anders dan door reorganisatie. |
| `Overlijden` | Het overlijden van de werknemer. |
| `Pensioen` | Pensionering, ook bij vervroegd uittreden. |
| `Reorganisatie` | Boventalligheid of opheffing van de functie. |
| `Vrijwillig vertrek` | De werknemer heeft zelf ontslag genomen. |
| `Overig` | Een andere of onbekende reden. |



### RedenEindeVerzuim { #RedenEindeVerzuim }

De reden waarom een verzuim is geëindigd.

| Waarde | Betekenis |
| :--- | :--- |
| `Einde aanstelling` | Het contract van de werknemer is geëindigd terwijl het verzuim liep. |
| `Einde wachttijd` | De wettelijke periode van loondoorbetaling bij ziekte is verstreken. |
| `Hersteld` | De werknemer heeft het werk volledig hervat. |
| `Overlijden` | Het overlijden van de werknemer. |
| `Overig` | Een andere of onbekende reden. |



### Rolsoort { #Rolsoort }

De soort rol die een werknemer vervult.

| Waarde | Betekenis |
| :--- | :--- |
| `Leidinggevende` | Geeft leiding aan de eenheid en draagt personele verantwoordelijkheid. |
| `Coördinerend` | Stuurt werk aan zonder personele verantwoordelijkheid, zoals een coördinator, projectleider of meewerkend voorman. |
| `Overig` | Een andere rol. |



### Verlofsoort { #Verlofsoort }

De soort verlof, naar de Wet arbeid en zorg en de cao.

| Waarde | Betekenis |
| :--- | :--- |
| `Adoptie- en pleegzorgverlof` | Verlof bij adoptie of opname van een pleegkind. |
| `Calamiteitenverlof` | Kort verlof bij onvoorziene persoonlijke omstandigheden. |
| `Geboorteverlof` | Verlof voor de partner na de geboorte, ook het aanvullend geboorteverlof. |
| `Kortdurend zorgverlof` | Verlof voor de noodzakelijke verzorging van een naaste. |
| `Langdurend zorgverlof` | Verlof bij een levensbedreigende ziekte of langdurige zorgbehoefte van een naaste. |
| `Onbetaald verlof` | Onbetaald verlof op eigen verzoek. |
| `Ouderschapsverlof betaald` | Het deel van het ouderschapsverlof waarvoor een uitkering geldt. |
| `Ouderschapsverlof onbetaald` | Het overige ouderschapsverlof. |
| `Vakantie` | Vakantieverlof. |
| `Zwangerschaps- en bevallingsverlof` | Verlof rond zwangerschap en bevalling. Telt niet als verzuim. |
| `Overig` | Een andere soort verlof. |



### Verzuimsoort { #Verzuimsoort }

De soort verzuim, voor zover een werkgever die mag vastleggen. De waarden volgen wat een werkgever volgens de beleidsregels van de Autoriteit Persoonsgegevens over een ziekmelding mag vastleggen. Daarom is er geen waarde voor de medische oorzaak en geen onderscheid naar de afzonderlijke vangnetbepalingen. Alle waarden tellen als verzuim. Bij samenloop geldt de meest specifieke waarde.

| Waarde | Betekenis |
| :--- | :--- |
| `Ziekte` | Verzuim door ziekte, niet vallend onder een van de andere waarden. |
| `Ziekte onder vangnet Ziektewet` | Verzuim waarvoor de werknemer onder een vangnetbepaling van de Ziektewet valt, zoals ziekte als gevolg van zwangerschap. Welke bepaling het is, wordt niet vastgelegd. |
| `Arbeidsongeval` | Verzuim dat verband houdt met een ongeval tijdens het werk. |
| `Ongeval met aansprakelijke derde` | Verzuim door een ongeval waarvoor een derde aansprakelijk kan zijn, bijvoorbeeld een verkeersongeval. Van belang voor het verhalen van loonkosten. |
| `Overig` | Een andere of onbekende soort. |



### Werkomgeving { #Werkomgeving }

De omgeving waarin het werk van een functie zich hoofdzakelijk afspeelt.

| Waarde | Betekenis |
| :--- | :--- |
| `Binnendienst` | Overwegend kantoor- of beeldschermwerk. |
| `Buitendienst` | Overwegend fysiek werk op locatie of in de buitenruimte, zoals groen, afval, reiniging, beheer en handhaving. |
| `Gemengd` | Een wezenlijk deel van beide. |


