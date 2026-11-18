# Detailspecificatie informatiemodel

Deze pagina beschrijft de objecttypen, kenmerken, relaties en waardelijsten van het informatiemodel. Het is het deel van Model HR van het [Gemeentelijk Gegevensmodel](https://www.gemeentelijkgegevensmodel.nl/) dat voor het Verzuimportaal nodig is. De pagina wordt uit het model gegenereerd.

Het informatiemodel beschrijft de betekenis van de gegevens. Welke gegevens daarvan worden uitgewisseld en in welke vorm, staat in de [uitwisselspecificatie](../uitwisselspecificatie.md).

## Objecttypen


### Aanstellingscontract { #Aanstellingscontract }

> Een overeenkomst op grond waarvan een werknemer werkzaamheden verricht voor de organisatie.

Abstract objecttype met de subtypen Arbeidsovereenkomst, Inhuurovereenkomst en OverigeAanstelling. Draagt de kenmerken en associaties die voor alle drie gelden. De aanstellingssoort geeft binnen elk subtype de precieze vorm. Een verlenging of een nieuwe overeenkomst is een nieuw voorkomen; de in- en uitdiensttreding van de werknemer zelf staat op Medewerker.

Subtypen: [Arbeidsovereenkomst](#Arbeidsovereenkomst), [Inhuurovereenkomst](#Inhuurovereenkomst), [OverigeAanstelling](#OverigeAanstelling).


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| aanstellingssoort | [Aanstellingssoort](#Aanstellingssoort) | 1 | De soort aanstelling. | Elke waarde hoort bij precies een subtype. Bepaalt samen met de cao of de aanstelling tot de bezetting telt, en onderscheidt de vormen van inhuur. |
| datumStart | datum | 1 | De eerste dag waarop het contract geldt. |  |
| datumEinde | datum | 0..1 | De laatste dag waarop het contract geldt. | Leeg zolang het contract loopt en geen einddatum is overeengekomen. |
| urenPerWeek | getal | 1 | Het aantal uren per week dat volgens het contract wordt gewerkt. | Grondslag voor de bezetting in fte en voor de weging van verzuim naar deeltijd. |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| heeft inzet | [Inzet](#Inzet) | 0..* | De inzet die op grond van het contract wordt verricht. |  |
| conform functie | [Functie](#Functie) | 0..1 | De functie die in het contract is overeengekomen. |  |
| onderdeel van | [OrganisatorischeEenheidHR](#OrganisatorischeEenheidHR) | 1..* | De eenheid of eenheden waartoe het contract organisatorisch behoort. |  |



### Arbeidsovereenkomst { #Arbeidsovereenkomst }

> De overeenkomst waarbij de werknemer zich verbindt om in dienst van de organisatie, tegen loon, gedurende zekere tijd arbeid te verrichten.

De definitie volgt artikel 7:610 van het Burgerlijk Wetboek. Alleen arbeidsovereenkomsten tellen voor de bezetting; welke precies, volgt uit de cao en de aanstellingssoort.

Arbeidsovereenkomst is een subtype van [Aanstellingscontract](#Aanstellingscontract) en heeft ook de kenmerken en relaties van dat objecttype.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| salaris | getal | 1 | Het bruto salaris per maand dat volgt uit schaal en periodiek, naar rato van de overeengekomen arbeidsduur. | Bestanddelen van de loonsom buiten het salaris staan in Looncomponent. |
| schaal | geheel getal | 1 | De salarisschaal waarin de werknemer is ingedeeld. | Het waardebereik volgt uit de cao; voor gemeenten 1 tot en met 20. |
| periodiek | geheel getal | 1 | Het volgnummer van de trede binnen de salarisschaal. |  |
| contractsoort | [Contractsoort](#Contractsoort) | 1 | Aanduiding of de overeenkomst voor bepaalde of voor onbepaalde tijd is aangegaan. | Grondslag voor tijdelijke dienst en voor vaste en flexibele bezetting. |
| cao | [Cao](#Cao) | 1 | De collectieve arbeidsovereenkomst die op de overeenkomst van toepassing is. |  |
| banenafspraak | ja/nee | 0..1 | Aanduiding dat de overeenkomst meetelt voor de banenafspraak voor mensen met een arbeidsbeperking. | Grondslag voor medewerkers met afstand tot de arbeidsmarkt. |
| redenEinde | [RedenEindeArbeidsovereenkomst](#RedenEindeArbeidsovereenkomst) | 0..1 | De reden waarom de overeenkomst is geëindigd. | Leeg zolang de overeenkomst loopt. Grondslag voor vrijwillige en onvrijwillige uitstroom. |





### Formatieplaats { #Formatieplaats }

> Een in het formatieplan vastgestelde arbeidsplaats bij een organisatorische eenheid.

De formatie is de toegestane omvang, niet de werkelijke bezetting. Een formatieplaats bestaat ook als zij onbezet is.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| urenPerWeek | getal | 1 | De omvang van de formatieplaats in uren per week. |  |
| datumBegin | datum | 1 | De eerste dag waarop de formatieplaats geldig is. | Grondslag voor de formatie op een peildatum. |
| datumEinde | datum | 0..1 | De laatste dag waarop de formatieplaats geldig is. | Leeg zolang de formatieplaats bestaat. |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| functie van formatieplaats | [Functie](#Functie) | 1..* | De functie waarvoor de formatieplaats is vastgesteld. |  |
| onderdeel van | [OrganisatorischeEenheidHR](#OrganisatorischeEenheidHR) | 1 | De organisatorische eenheid waartoe de formatieplaats behoort. |  |
| toegewezen aan | [Aanstellingscontract](#Aanstellingscontract) | 0..* | Het contract waarmee de formatieplaats is bezet. |  |



### Functie { #Functie }

> Het samenstel van taken en werkzaamheden dat aan een werknemer kan worden opgedragen.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| code | tekst (max. 50) | 1 | De code waarmee de functie in de organisatie wordt aangeduid. | Sleutel voor de vertaaltabel naar een landelijke indeling. |
| naam | tekst (max. 80) | 1 | De naam van de functie. |  |
| omschrijving | tekst | 0..1 | Een beschrijving van de functie. |  |
| taken | tekst | 0..1 | De taken die bij de functie horen. |  |
| schaal | geheel getal | 1 | De salarisschaal waarin de functie is gewaardeerd. |  |
| leidinggevend | ja/nee | 1 | Aanduiding dat aan de functie leidinggevende taken en personele verantwoordelijkheid zijn verbonden. | Projectleiders, meewerkend voorlieden en coördinatoren tellen niet als leidinggevend. |
| werkomgeving | [Werkomgeving](#Werkomgeving) | 0..1 | De omgeving waarin het werk van de functie zich hoofdzakelijk afspeelt. |  |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| gebaseerd op | [NormProfiel](#NormProfiel) | 0..1 | Het normprofiel waarop de functie is gebaseerd. |  |



### Functiehuis { #Functiehuis }

> Model waarin functies van een organisatie worden beschreven.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| naam | tekst (max. 80) | 1 |  |  |
| omschrijving | tekst | 1 |  |  |





### Inhuurovereenkomst { #Inhuurovereenkomst }

> Een overeenkomst op grond waarvan een externe kracht werkzaamheden verricht voor de organisatie, zonder bij haar in dienst te zijn.

Subtype van Aanstellingscontract. Omvat uitzendwerk, detachering vanuit een andere organisatie, payrolling en opdrachten aan zelfstandigen; de aanstellingssoort zegt welke vorm het is. Telt niet voor de bezetting, wel voor de externe inhuur en de flexibele bezetting.

Inhuurovereenkomst is een subtype van [Aanstellingscontract](#Aanstellingscontract) en heeft ook de kenmerken en relaties van dat objecttype.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| kosten | getal | 0..1 | De kosten van de inhuur over de looptijd van de overeenkomst, in euro's. | De financiële administratie blijft de bron; het kenmerk is bedoeld voor situaties waarin het HR-systeem de kosten kent. |





### Inzet { #Inzet }

> De inzet van een werknemer voor een functie bij een organisatorische eenheid in een bepaalde periode, op grond van een aanstellingscontract.

Een contract kan meer inzetten hebben, gelijktijdig of na elkaar. Opeenvolgende inzetten vormen de functie- en afdelingshistorie waaruit doorstroom en verblijfsduur in een functie volgen.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| datumBegin | datum | 1 | De eerste dag van de inzet. |  |
| datumEinde | datum | 0..1 | De laatste dag van de inzet. | Leeg zolang de inzet loopt. |
| uren | getal | 1 | Het aantal uren per week van de inzet. |  |
| percentage | getal | 0..1 | Het deel van de uren van de inzet dat daadwerkelijk wordt uitgevoerd, als percentage. |  |
| bestemming | [BestemmingInzet](#BestemmingInzet) | 1 | Aanduiding of de inzet voor de eigen organisatie is of voor derden. | Grondslag voor de inzet voor derden. |
| schaal | geheel getal | 0..1 | De salarisschaal waarin de werknemer voor deze inzet is ingedeeld. | Alleen gevuld als de schaal afwijkt van die van de functie, bijvoorbeeld bij een aanloopschaal. |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| inzet bij | [OrganisatorischeEenheidHR](#OrganisatorischeEenheidHR) | 1 | De organisatorische eenheid waar de inzet wordt verricht. |  |
| inzet voor functie | [Functie](#Functie) | 1 | De functie waarvoor de inzet wordt verricht. |  |



### NormProfiel { #NormProfiel }

> Een generieke functie uit een landelijk functiewaarderingssysteem, waarop functies van de organisatie zijn gebaseerd.

Voor gemeenten het systeem HR21.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| code | tekst (max. 10) | 1 | De code van het normprofiel in het functiewaarderingssysteem. |  |
| omschrijving | tekst (max. 100) | 1 | De naam of omschrijving van het normprofiel. |  |
| schaal | geheel getal | 1 | De salarisschaal die bij het normprofiel hoort. |  |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| onderdeel van | [Functiehuis](#Functiehuis) | 1 | Het functiehuis waarvan het normprofiel deel uitmaakt. |  |



### OrganisatorischeEenheidHR { #OrganisatorischeEenheidHR }

> Een organisatorische eenheid zoals vastgelegd in de personeelsadministratie.

Specialisatie van Organisatorische eenheid uit het RGBZ; de plaats in de organisatie volgt uit de associatie 'is deel van' van dat objecttype.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| organisatieIdentificatie | tekst (max. 24) | 1 | Een korte identificatie van de organisatorische eenheid. | Geërfd van OrganisatorischeEenheid |
| datumOntstaan | datum | 1 | De datum waarop de organisatorische eenheid is ontstaan. | Geërfd van OrganisatorischeEenheid |
| datumOpheffing | datum | 0..1 | De datum waarop de organisatorische eenheid is opgeheven. | Geërfd van OrganisatorischeEenheid |
| naam | tekst (max. 80) | 1 | De naam van de eenheid in de personeelsadministratie. |  |
| type | [OrganisatorischeEenheidsoort](#OrganisatorischeEenheidsoort) | 1 | Het niveau van de eenheid in de indeling van de organisatie. |  |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| Is deel van | [OrganisatorischeEenheidHR](#OrganisatorischeEenheidHR) | 0..1 |  |  |



### OverigeAanstelling { #OverigeAanstelling }

> Een aanstellingscontract dat geen arbeidsovereenkomst en geen inhuurovereenkomst is.

Subtype van Aanstellingscontract voor wie in de organisatie werkt zonder arbeidsovereenkomst en zonder te zijn ingehuurd: stagiairs, mensen op een werkervaringsplaats en overige vormen, zoals vrijwilligers. Telt niet voor de bezetting en niet voor de externe inhuur. Heeft geen eigen kenmerken; de aanstellingssoort zegt welke vorm het is.

OverigeAanstelling is een subtype van [Aanstellingscontract](#Aanstellingscontract) en heeft ook de kenmerken en relaties van dat objecttype.


OverigeAanstelling heeft geen eigen kenmerken.




### Rol { #Rol }

> Een taak of bevoegdheid die een werknemer in een bepaalde periode vervult binnen een organisatorische eenheid, naast of als onderdeel van zijn functie.

De rol legt vast wie in welke periode leiding geeft aan welke eenheid.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| datumBegin | datum | 1 | De eerste dag waarop de werknemer de rol vervult. |  |
| datumEinde | datum | 0..1 | De laatste dag waarop de werknemer de rol vervult. | Leeg zolang de rol wordt vervuld. |
| omschrijving | tekst (max. 50) | 0..1 | Een vrije omschrijving van de rol. |  |
| rolsoort | [Rolsoort](#Rolsoort) | 1 | De soort rol. | Maakt leidinggevenden eenduidig herkenbaar. |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| hoort bij | [OrganisatorischeEenheidHR](#OrganisatorischeEenheidHR) | 0..1 | De organisatorische eenheid waarbinnen de rol wordt vervuld. |  |



### Verlof { #Verlof }

> Een periode waarin een werknemer met toestemming van de werkgever, of op grond van de wet of de cao, de overeengekomen arbeid niet verricht.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| datumtijdStart | datum en tijd | 1 | Het moment waarop het verlof begint. |  |
| datumtijdEinde | datum en tijd | 1 | Het moment waarop het verlof eindigt. |  |
| datumAanvraag | datum | 0..1 | De datum waarop het verlof is aangevraagd. |  |
| datumToekenning | datum | 0..1 | De datum waarop het verlof is toegekend. |  |
| goedgekeurd | ja/nee | 1 | Aanduiding dat het verlof is goedgekeurd. |  |
| verlofsoort | [Verlofsoort](#Verlofsoort) | 1 | De soort verlof. |  |





### Verzuim { #Verzuim }

> Een aaneengesloten periode waarin een werknemer de overeengekomen arbeid geheel of gedeeltelijk niet verricht, anders dan door verlof.

Een verzuimgeval loopt van de eerste verzuimdag tot het herstel. Zwangerschaps- en bevallingsverlof is verlof en geen verzuim; ziekte als gevolg van zwangerschap is wel verzuim. De medische oorzaak wordt niet vastgelegd.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| datumtijdStart | datum en tijd | 1 | Het moment waarop het verzuim begint. |  |
| datumtijdEinde | datum en tijd | 0..1 | Het moment waarop het verzuim eindigt. | Leeg zolang het verzuim loopt. |
| percentageArbeidsongeschiktheid | getal | 1 | Het deel van de overeengekomen arbeidsduur waarvoor de werknemer verzuimt, als percentage. | 100 bij volledig verzuim. Een wijziging is historie van dit kenmerk en geen nieuw verzuimgeval. |
| verzuimsoort | [Verzuimsoort](#Verzuimsoort) | 1 | De soort verzuim. |  |
| redenEinde | [RedenEindeVerzuim](#RedenEindeVerzuim) | 0..1 | De reden waarom het verzuim is geëindigd. | Leeg zolang het verzuim loopt. Grondslag voor het aandeel hersteld. |





### Werknemer { #Werknemer }

> Een persoon die op grond van een aanstellingscontract werkzaamheden verricht voor de organisatie.

Omvat eigen personeel (arbeidsovereenkomst) en externen (inhuurovereenkomst). Specialisatie van Medewerker uit het RGBZ; de identificatie, de geslachtsaanduiding en de data van in- en uitdiensttreding worden daarvan geërfd.


| Kenmerk | Type | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| medewerkerIdentificatie | tekst (max. 24) | 1 | Een korte unieke aanduiding van de medewerker. | Geërfd van Medewerker |
| geslachtsaanduiding | tekst (max. 1) | 1 | Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht nog onbekend is. | Geërfd van Medewerker |
| naam | tekst (max. 80) | 1 | De achternaam van de werknemer. |  |
| voornaam | tekst (max. 40) | 1 | De voornaam of roepnaam van de werknemer. |  |
| geboortedatum | datum | 1 | De datum waarop de werknemer is geboren. | Grondslag voor de leeftijdsopbouw. In een uitwisseling volstaat het geboortejaar. |
| woonplaats | tekst (max. 50) | 1 | De plaats waar de werknemer woont. |  |




| Relatie | Naar | Aantal | Definitie | Toelichting |
| :--- | :--- | :--- | :--- | :--- |
| heeft verzuim | [Verzuim](#Verzuim) | 0..* | Het verzuim van de werknemer. |  |
| heeft verlof | [Verlof](#Verlof) | 0..* | Het verlof van de werknemer. |  |
| heeft | [Rol](#Rol) | 0..* | De rol die de werknemer vervult. |  |
| heeft aanstellingscontract | [Aanstellingscontract](#Aanstellingscontract) | 1..* | Het contract op grond waarvan de werknemer voor de organisatie werkt. |  |




## Waardelijsten


### Aanstellingssoort { #Aanstellingssoort }

> De soort aanstelling op grond waarvan een werknemer voor de organisatie werkt.

De eerste drie waarden horen bij Arbeidsovereenkomst, de volgende vier bij Inhuurovereenkomst en de laatste drie bij OverigeAanstelling.

| Waarde | Definitie |
| :--- | :--- |
| Reguliere arbeidsovereenkomst | Arbeidsovereenkomst met een vaste arbeidsomvang. Telt voor de bezetting. |
| Oproepovereenkomst | Arbeidsovereenkomst met een flexibel aantal uren. Telt voor de bezetting en voor de flexibele bezetting. |
| Leerarbeidsovereenkomst | Arbeidsovereenkomst met een student in de beroepsbegeleidende leerweg (bbl). Telt voor de bezetting. |
| Uitzendovereenkomst | Inhuur via een uitzendbureau. |
| Detachering | Inhuur van iemand die in dienst is bij een andere organisatie. |
| Payrollovereenkomst | Inhuur waarbij de organisatie zelf werft en het juridisch werkgeverschap bij een payrollbedrijf ligt. |
| Opdracht aan zelfstandige | Opdracht aan een zelfstandige zonder personeel (zzp). |
| Stageovereenkomst | Overeenkomst met een stagiair in het kader van een opleiding. Telt niet voor de bezetting. |
| Werkervaringsplaats | Overeenkomst voor het opdoen van werkervaring. Telt niet voor de bezetting. |
| Overig | Een andere vorm, zoals vrijwilligerswerk. |



### BestemmingInzet { #BestemmingInzet }

> De organisatie waarvoor een inzet wordt verricht.

| Waarde | Definitie |
| :--- | :--- |
| Eigen organisatie | De inzet is voor de eigen organisatie. |
| Derden | De inzet is voor een andere organisatie, bijvoorbeeld bij detachering of dienstverlening aan een andere gemeente. |



### Cao { #Cao }

> De collectieve arbeidsovereenkomst die op een arbeidsovereenkomst van toepassing is.

| Waarde | Definitie |
| :--- | :--- |
| Cao Gemeenten | De cao voor gemeenten. Telt voor de bezetting. |
| Cao SGO | De cao Samenwerkende Gemeentelijke Organisaties. Telt voor de bezetting. |
| Cao Aan de Slag | De cao voor mensen met een arbeidsbeperking in dienst van gemeenten. Telt niet voor de bezetting. |
| Cao Sociale Werkvoorziening | De cao voor de sociale werkvoorziening. Telt niet voor de bezetting. |
| Overig | Een andere cao. |



### Contractsoort { #Contractsoort }

> De duur waarvoor een arbeidsovereenkomst is aangegaan.

| Waarde | Definitie |
| :--- | :--- |
| Bepaalde tijd | De overeenkomst eindigt op een vooraf bepaald moment of bij een vooraf bepaalde gebeurtenis. |
| Onbepaalde tijd | De overeenkomst heeft geen vooraf bepaald einde. |



### OrganisatorischeEenheidsoort { #OrganisatorischeEenheidsoort }

> Het niveau van een organisatorische eenheid in de indeling van de organisatie.

| Waarde | Definitie |
| :--- | :--- |
| Concern | De organisatie als geheel. |
| Directie | Een directie of domein. |
| Afdeling | Een afdeling. |
| Team | Een team. |
| Griffie | De griffie; hoort bij de organisatie, maar staat buiten de ambtelijke lijn. |
| Overig | Een ander niveau. |



### RedenEindeArbeidsovereenkomst { #RedenEindeArbeidsovereenkomst }

> De reden waarom een arbeidsovereenkomst is geëindigd.

| Waarde | Definitie |
| :--- | :--- |
| Arbeidsongeschiktheid | Beëindiging wegens langdurige arbeidsongeschiktheid. |
| Einde tijdelijk contract | Het aflopen van een overeenkomst voor bepaalde tijd. |
| Ontslag door werkgever | Ontslag op initiatief van de werkgever, anders dan door reorganisatie. |
| Overlijden | Het overlijden van de werknemer. |
| Pensioen | Pensionering, ook bij vervroegd uittreden. |
| Reorganisatie | Boventalligheid of opheffing van de functie. |
| Vrijwillig vertrek | De werknemer heeft zelf ontslag genomen. |
| Overig | Een andere of onbekende reden. |



### RedenEindeVerzuim { #RedenEindeVerzuim }

> De reden waarom een verzuim is geëindigd.

| Waarde | Definitie |
| :--- | :--- |
| Einde aanstelling | Het contract van de werknemer is geëindigd terwijl het verzuim liep. |
| Einde wachttijd | De wettelijke periode van loondoorbetaling bij ziekte is verstreken. |
| Hersteld | De werknemer heeft het werk volledig hervat. |
| Overlijden | Het overlijden van de werknemer. |
| Overig | Een andere of onbekende reden. |



### Rolsoort { #Rolsoort }

> De soort rol die een werknemer vervult.

| Waarde | Definitie |
| :--- | :--- |
| Leidinggevende | Geeft leiding aan de eenheid en draagt personele verantwoordelijkheid. |
| Coördinerend | Stuurt werk aan zonder personele verantwoordelijkheid, zoals een coördinator, projectleider of meewerkend voorman. |
| Overig | Een andere rol. |



### Verlofsoort { #Verlofsoort }

> De soort verlof, naar de Wet arbeid en zorg en de cao.

| Waarde | Definitie |
| :--- | :--- |
| Adoptie- en pleegzorgverlof | Verlof bij adoptie of opname van een pleegkind. |
| Calamiteitenverlof | Kort verlof bij onvoorziene persoonlijke omstandigheden. |
| Geboorteverlof | Verlof voor de partner na de geboorte, ook het aanvullend geboorteverlof. |
| Kortdurend zorgverlof | Verlof voor de noodzakelijke verzorging van een naaste. |
| Langdurend zorgverlof | Verlof bij een levensbedreigende ziekte of langdurige zorgbehoefte van een naaste. |
| Onbetaald verlof | Onbetaald verlof op eigen verzoek. |
| Ouderschapsverlof betaald | Het deel van het ouderschapsverlof waarvoor een uitkering geldt. |
| Ouderschapsverlof onbetaald | Het overige ouderschapsverlof. |
| Vakantie | Vakantieverlof. |
| Zwangerschaps- en bevallingsverlof | Verlof rond zwangerschap en bevalling. Telt niet als verzuim. |
| Overig | Een andere soort verlof. |



### Verzuimsoort { #Verzuimsoort }

> De soort verzuim, voor zover een werkgever die mag vastleggen.

De waarden volgen wat een werkgever volgens de beleidsregels van de Autoriteit Persoonsgegevens over een ziekmelding mag vastleggen. Daarom is er geen waarde voor de medische oorzaak en geen onderscheid naar de afzonderlijke vangnetbepalingen. Alle waarden tellen als verzuim. Bij samenloop geldt de meest specifieke waarde.

| Waarde | Definitie |
| :--- | :--- |
| Ziekte | Verzuim door ziekte, niet vallend onder een van de andere waarden. |
| Ziekte onder vangnet Ziektewet | Verzuim waarvoor de werknemer onder een vangnetbepaling van de Ziektewet valt, zoals ziekte als gevolg van zwangerschap. Welke bepaling het is, wordt niet vastgelegd. |
| Arbeidsongeval | Verzuim dat verband houdt met een ongeval tijdens het werk. |
| Ongeval met aansprakelijke derde | Verzuim door een ongeval waarvoor een derde aansprakelijk kan zijn, bijvoorbeeld een verkeersongeval. Van belang voor het verhalen van loonkosten. |
| Overig | Een andere of onbekende soort. |



### Werkomgeving { #Werkomgeving }

> De omgeving waarin het werk van een functie zich hoofdzakelijk afspeelt.

| Waarde | Definitie |
| :--- | :--- |
| Binnendienst | Overwegend kantoor- of beeldschermwerk. |
| Buitendienst | Overwegend fysiek werk op locatie of in de buitenruimte, zoals groen, afval, reiniging, beheer en handhaving. |
| Gemengd | Een wezenlijk deel van beide. |


