"""crunch_uml-plugin: van het informatiemodel naar het uitwisselmodel.

Het uitwisselmodel is de boom die als JSON wordt uitgewisseld. De plugin leidt het af van
het informatiemodel (Model HR van het GGM) en doet daarvoor het volgende:

1. De kenmerken van het abstracte Aanstellingscontract worden overgenomen in de drie
   subtypen; het supertype zelf verdwijnt. Een werknemer krijgt drie lijsten:
   arbeidsovereenkomsten, inhuurovereenkomsten en overigeAanstellingen.
2. De waardelijst Aanstellingssoort wordt per subtype gesplitst, zodat het JSON-schema
   afdwingt dat de aanstellingssoort bij het subtype past.
3. Werknemer wordt ontdaan van direct identificerende gegevens: er blijft een sleutel,
   het geboortejaar en de geslachtsaanduiding over.
4. Per objecttype staat in KENMERKEN welke kenmerken worden uitgewisseld, in welke
   volgorde. Wat daar niet staat, wordt niet uitgewisseld.
5. Associaties worden óf genest (NESTEN: het doel staat als object of lijst binnen de
   bron) óf vervangen door een verwijzing met de sleutel van het doel (VERWIJZINGEN).
6. De objecttypen van de uitwisseling zelf worden toegevoegd: Uitwisselmodel, Levering,
   AanleverendeOrganisatie, Contactpersoon en Arbeidsongeschiktheidsverloop.
7. Datatypen worden omgezet naar de eenvoudige typen van het JSON-schema.

Objecttypen worden op naam gezocht. Nieuwe elementen krijgen een id dat van hun naam is
afgeleid, zodat een nieuwe run exact hetzelfde model oplevert.
"""

import logging
import uuid

from crunch_uml.db import Association, Attribute, Class, Enumeratie, EnumerationLiteral
from crunch_uml.exceptions import CrunchException
from crunch_uml.transformers.plugin import Plugin

logger = logging.getLogger()

MODEL_HR_PACKAGE_ID = "EAPK_9ADEFB08_F150_4278_8D32_32465C57E8A7"
UITWISSELMODEL_ID = "EAID_UITWISSELMODEL_VERZUIMPORTAAL"  # ook in .env: ROOT_CLASS_UM
NAAMRUIMTE = uuid.UUID("5f0c2f3e-7b0a-4a51-9d0e-6f1f1c5a2b10")

SUPERTYPE = "Aanstellingscontract"
SUBTYPEN = {
    # subtype: (rolnaam bij Werknemer, naam van de eigen waardelijst, toegestane aanstellingssoorten)
    "Arbeidsovereenkomst": (
        "arbeidsovereenkomsten",
        "AanstellingssoortArbeidsovereenkomst",
        ["Reguliere arbeidsovereenkomst", "Oproepovereenkomst", "Leerarbeidsovereenkomst"],
    ),
    "Inhuurovereenkomst": (
        "inhuurovereenkomsten",
        "AanstellingssoortInhuurovereenkomst",
        ["Uitzendovereenkomst", "Detachering", "Payrollovereenkomst", "Opdracht aan zelfstandige"],
    ),
    "OverigeAanstelling": (
        "overigeAanstellingen",
        "AanstellingssoortOverigeAanstelling",
        ["Stageovereenkomst", "Werkervaringsplaats", "Overig"],
    ),
}

# Welke kenmerken per objecttype worden uitgewisseld, in deze volgorde. Kenmerken die het
# informatiemodel niet kent (sleutels, verwijzingen) staan in NIEUWE_KENMERKEN.
CONTRACT = ["aanstellingscontractID", "aanstellingssoort", "datumStart", "datumEinde", "urenPerWeek"]
PLAATS = ["functie", "organisatorischeEenheid", "formatieplaats"]
KENMERKEN = {
    "OrganisatorischeEenheidHR": [
        "organisatieIdentificatie", "naam", "type", "isDeelVan", "datumOntstaan", "datumOpheffing",
    ],
    "Functie": ["code", "naam", "schaal", "leidinggevend", "werkomgeving"],
    "NormProfiel": ["code", "omschrijving", "schaal"],
    "Functiehuis": ["naam"],
    "Formatieplaats": [
        "formatieplaatsID", "urenPerWeek", "datumBegin", "datumEinde", "functie", "organisatorischeEenheid",
    ],
    "Werknemer": ["werknemerID", "geboortejaar", "geslachtsaanduiding"],
    "Arbeidsovereenkomst": CONTRACT + ["schaal", "contractsoort", "cao", "banenafspraak", "redenEinde"] + PLAATS,
    "Inhuurovereenkomst": CONTRACT + PLAATS,
    "OverigeAanstelling": CONTRACT + PLAATS,
    "Inzet": [
        "datumBegin", "datumEinde", "uren", "percentage", "bestemming", "schaal", "functie",
        "organisatorischeEenheid",
    ],
    "Rol": ["rolsoort", "omschrijving", "datumBegin", "datumEinde", "organisatorischeEenheid"],
    "Verzuim": [
        "verzuimID", "datumtijdStart", "datumtijdEinde", "percentageArbeidsongeschiktheid", "verzuimsoort",
        "redenEinde",
    ],
    "Verlof": ["datumtijdStart", "datumtijdEinde", "verlofsoort"],
}

NAAR_FUNCTIE = "Verwijst met de code naar een functie in dezelfde levering."
NAAR_EENHEID = "Verwijst met de organisatieIdentificatie naar een organisatorische eenheid in dezelfde levering."
NAAR_FORMATIEPLAATS = "Verwijst met het formatieplaatsID naar een formatieplaats in dezelfde levering."

# Kenmerken die alleen in de uitwisseling bestaan: (objecttype, naam) -> eigenschappen.
# 'vervangt' noemt het kenmerk of de associatie uit het informatiemodel die erdoor wordt vervangen.
NIEUWE_KENMERKEN = {
    ("Werknemer", "werknemerID"): dict(
        primitive="AN64", verplicht=True, vervangt="medewerkerIdentificatie",
        definitie="Een sleutel zonder betekenis die de werknemer binnen de gemeente aanduidt.",
        toelichting=(
            "De sleutel is in elke levering dezelfde, zodat gegevens over meerdere perioden bij elkaar"
            " horen. Het personeelsnummer, het burgerservicenummer of een deel van de naam mogen er niet"
            " in voorkomen of uit af te leiden zijn."
        ),
    ),
    ("Werknemer", "geboortejaar"): dict(
        primitive="int", verplicht=True, vervangt="geboortedatum", minimum="1900", maximum="2100",
        definitie="Het jaar waarin de werknemer is geboren.",
        toelichting="Het geboortejaar vervangt de geboortedatum; het is genoeg voor de leeftijdsopbouw.",
    ),
    ("Werknemer", "geslachtsaanduiding"): dict(
        enumeratie="Geslachtsaanduiding", verplicht=True, vervangt="geslachtsaanduiding",
        definitie="Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht onbekend is.",
    ),
    ("OrganisatorischeEenheidHR", "isDeelVan"): dict(
        primitive="AN24", verplicht=False, vervangt="Is deel van",
        definitie="De organisatorische eenheid waarvan deze eenheid deel uitmaakt.",
        toelichting=NAAR_EENHEID + " Leeg bij de hoogste eenheid, de organisatie als geheel.",
    ),
    ("Formatieplaats", "formatieplaatsID"): dict(
        primitive="AN64", verplicht=True,
        definitie="Een sleutel die de formatieplaats binnen de levering aanduidt.",
    ),
    ("Formatieplaats", "functie"): dict(
        primitive="AN50", verplicht=True, vervangt="functie van formatieplaats",
        definitie="De functie waarvoor de formatieplaats is bestemd.", toelichting=NAAR_FUNCTIE,
    ),
    ("Formatieplaats", "organisatorischeEenheid"): dict(
        primitive="AN24", verplicht=True, vervangt="onderdeel van",
        definitie="De organisatorische eenheid waartoe de formatieplaats behoort.", toelichting=NAAR_EENHEID,
    ),
    (SUPERTYPE, "aanstellingscontractID"): dict(
        primitive="AN64", verplicht=True,
        definitie="Een sleutel die het aanstellingscontract binnen de levering aanduidt.",
        toelichting="De sleutel is in elke levering dezelfde.",
    ),
    (SUPERTYPE, "functie"): dict(
        primitive="AN50", verplicht=False, vervangt="conform functie",
        definitie="De functie die in het contract is overeengekomen.", toelichting=NAAR_FUNCTIE,
    ),
    (SUPERTYPE, "organisatorischeEenheid"): dict(
        primitive="AN24", verplicht=True, vervangt="onderdeel van",
        definitie="De organisatorische eenheid waarbij de werknemer op grond van het contract is geplaatst.",
        toelichting=NAAR_EENHEID + " Werkt iemand voor meer eenheden, dan volgt de verdeling uit de inzet.",
    ),
    (SUPERTYPE, "formatieplaats"): dict(
        primitive="AN64", verplicht=False,
        definitie="De formatieplaats waaraan het contract is toegewezen.", toelichting=NAAR_FORMATIEPLAATS,
    ),
    ("Inzet", "functie"): dict(
        primitive="AN50", verplicht=True, vervangt="inzet voor functie",
        definitie="De functie waarvoor de werknemer wordt ingezet.", toelichting=NAAR_FUNCTIE,
    ),
    ("Inzet", "organisatorischeEenheid"): dict(
        primitive="AN24", verplicht=True, vervangt="inzet bij",
        definitie="De organisatorische eenheid waarbij de werknemer wordt ingezet.", toelichting=NAAR_EENHEID,
    ),
    ("Rol", "organisatorischeEenheid"): dict(
        primitive="AN24", verplicht=False, vervangt="hoort bij",
        definitie="De organisatorische eenheid waarbinnen de werknemer de rol vervult.", toelichting=NAAR_EENHEID,
    ),
    ("Verzuim", "verzuimID"): dict(
        primitive="AN64", verplicht=True,
        definitie="Een sleutel die het verzuimgeval binnen de levering aanduidt.",
        toelichting="De sleutel is in elke levering dezelfde, zodat lopend verzuim over perioden heen te volgen is.",
    ),
}

# Associaties uit het informatiemodel die genest worden: (bron, naam, doel) -> (rolnaam, volgorde).
NESTEN = {
    ("Werknemer", "heeft", "Rol"): ("rollen", 4),
    ("Werknemer", "heeft verzuim", "Verzuim"): ("verzuimgevallen", 5),
    ("Werknemer", "heeft verlof", "Verlof"): ("verlofperioden", 6),
    ("Functie", "gebaseerd op", "NormProfiel"): ("normProfiel", 1),
    ("NormProfiel", "onderdeel van", "Functiehuis"): ("functiehuis", 1),
}
# Associaties die vervallen omdat een verwijzing (NIEUWE_KENMERKEN) of een nieuwe nesting ze vervangt.
VERVALLEN = [
    ("Werknemer", "heeft aanstellingscontract", SUPERTYPE),
    (SUPERTYPE, "heeft inzet", "Inzet"),
    (SUPERTYPE, "conform functie", "Functie"),
    (SUPERTYPE, "onderdeel van", "OrganisatorischeEenheidHR"),
    ("Formatieplaats", "functie van formatieplaats", "Functie"),
    ("Formatieplaats", "onderdeel van", "OrganisatorischeEenheidHR"),
    ("Formatieplaats", "toegewezen aan", SUPERTYPE),
    ("Inzet", "inzet bij", "OrganisatorischeEenheidHR"),
    ("Inzet", "inzet voor functie", "Functie"),
    ("Rol", "hoort bij", "OrganisatorischeEenheidHR"),
    ("OrganisatorischeEenheidHR", "Is deel van", "OrganisatorischeEenheidHR"),
]

# In de uitwisseling wijkt de verplichting van een paar kenmerken af van het GGM.
VERPLICHT_ANDERS = {
    ("OrganisatorischeEenheidHR", "datumOntstaan"): False,  # vaak niet geregistreerd in het HR-pakket
}
# Grenzen van getallen: (objecttype of '*', kenmerk) -> (minimum, maximum).
GRENZEN = {
    ("*", "urenPerWeek"): ("0", "168"),
    ("*", "uren"): ("0", "168"),
    ("*", "percentage"): ("0", "100"),
    ("*", "percentageArbeidsongeschiktheid"): ("0", "100"),
    ("*", "schaal"): ("1", None),
}
# Toelichtingen die in de uitwisseling anders luiden dan in het informatiemodel, omdat zij daar
# naar kenmerken of relaties verwijzen die in een bericht niet of anders voorkomen.
TOELICHTING_ANDERS = {
    "Werknemer": (
        "Omvat eigen personeel, ingehuurde krachten, stagiairs en mensen op een werkervaringsplaats. Een werknemer"
        " wordt aangeduid met een sleutel zonder betekenis; naam, burgerservicenummer, geboortedatum en adres worden"
        " niet uitgewisseld."
    ),
    "OrganisatorischeEenheidHR": "De plaats in de organisatie volgt uit het veld isDeelVan.",
    "Arbeidsovereenkomst": (
        "Voor eigen personeel. Alleen arbeidsovereenkomsten tellen voor de bezetting; welke precies, volgt uit de cao"
        " en de aanstellingssoort. Een verlenging of een nieuwe overeenkomst is een nieuw voorkomen."
    ),
    "Inhuurovereenkomst": (
        "Voor externe krachten: uitzendwerk, detachering vanuit een andere organisatie, payrolling en opdrachten aan"
        " zelfstandigen; de aanstellingssoort zegt welke vorm het is. Telt niet voor de bezetting, wel voor de externe"
        " inhuur en de flexibele bezetting."
    ),
    "OverigeAanstelling": (
        "Voor wie in de organisatie werkt zonder arbeidsovereenkomst en zonder te zijn ingehuurd: stagiairs, mensen op"
        " een werkervaringsplaats en overige vormen, zoals vrijwilligers. Telt niet voor de bezetting en niet voor de"
        " externe inhuur."
    ),
}
# Definities die in het GGM nog ontbreken en voor de uitwisseling zijn aangevuld.
AANGEVULDE_DEFINITIES = {
    ("Functiehuis", None): "Een samenhangend stelsel van normprofielen waarmee functies worden beschreven en gewaardeerd.",
    ("Functiehuis", "naam"): "De naam van het functiehuis, bijvoorbeeld HR21.",
}
PATRONEN = {"gemeentecode": "^[0-9]{4}$", "kvkNummer": "^[0-9]{8}$"}

DATATYPEN = {"date": "Datum", "datetime": "datumtijd", "integer": "int", "boolean": "boolean", "decimal": "Getal"}


def nieuw_id(*delen):
    """Een vast id voor een element dat de plugin toevoegt."""
    return "EAID_" + str(uuid.uuid5(NAAMRUIMTE, "/".join(delen))).replace("-", "_")


class VerzuimPluginUitwisselmodel(Plugin):
    def transformLogic(self, args, root_package, schema_from, schema_to):
        logger.info("Start plugin uitwisselmodel Verzuimportaal.")
        schema_to.clean()
        if root_package.id != MODEL_HR_PACKAGE_ID:
            raise CrunchException(
                f"{self.__class__.__name__} verwacht Model HR ({MODEL_HR_PACKAGE_ID}) als rootpackage,"
                f" niet {root_package.id}."
            )
        self.schema_id = schema_to.schema_id
        namen_bron = {clazz.id: str(clazz.name) for clazz in root_package.classes}

        kopie = root_package.get_copy(None, materialize_generalizations=True)
        kopie.name = "Uitwisselmodel"
        self.kopie = kopie
        self.klassen = {str(clazz.name): clazz for clazz in kopie.classes}
        self.enums = {str(enum.name): enum for enum in kopie.enumerations}

        self.splits_aanstellingssoort()
        self.voeg_geslachtsaanduiding_toe()
        self.verwerk_associaties(namen_bron)
        self.zet_kenmerken()
        self.zet_datatypen()
        self.voeg_verloop_toe()
        self.voeg_levering_toe()
        self.controleer_definities()

        # Het abstracte supertype is nu overbodig: de subtypen dragen zijn kenmerken.
        kopie.classes.remove(self.klassen.pop(SUPERTYPE))

        schema_to.add(kopie, recursive=True)
        logger.info("Plugin uitwisselmodel Verzuimportaal klaar.")

    # ------------------------------------------------------------------ bouwstenen
    def klasse(self, naam, definitie, toelichting=None, vast_id=None):
        clazz = Class(
            id=vast_id or nieuw_id("klasse", naam), name=naam, schema_id=self.schema_id, package=self.kopie,
            definitie=definitie, toelichting=toelichting,
        )
        self.klassen[naam] = clazz
        return clazz

    def kenmerk(self, clazz, naam, *, primitive=None, enumeratie=None, verplicht=False, definitie=None,
                toelichting=None, lengte=None, minimum=None, maximum=None, **_):
        attribuut = Attribute(
            id=nieuw_id("kenmerk", str(clazz.name), naam), name=naam, schema_id=self.schema_id,
            primitive=primitive, verplicht=verplicht, definitie=definitie, toelichting=toelichting, lengte=lengte,
            minimumwaarde_inclusief=minimum, maximumwaarde_inclusief=maximum, formeel_patroon=PATRONEN.get(naam),
        )
        if enumeratie:
            attribuut.enumeration_id = self.enums[enumeratie].id
            attribuut.primitive = None
        if primitive and primitive.startswith("AN") and primitive[2:].isdigit():
            attribuut.lengte = primitive[2:]
        clazz.attributes.append(attribuut)
        return attribuut

    def nest(self, bron, doel, rolnaam, minimaal, meervoudig, volgorde, definitie):
        associatie = Association(
            id=nieuw_id("nesting", str(bron.name), rolnaam), name=rolnaam, schema_id=self.schema_id,
            src_class_id=bron.id, dst_class_id=doel.id, src_role=rolnaam, definitie=definitie, order=volgorde,
            dst_mult_start=str(minimaal), dst_mult_end="*" if meervoudig else "1",
        )
        bron.uitgaande_associaties.append(associatie)
        return associatie

    # ------------------------------------------------------------------ stappen
    def splits_aanstellingssoort(self):
        """Eén waardelijst per subtype, met alleen de aanstellingssoorten van dat subtype."""
        bron = self.enums["Aanstellingssoort"]
        waarden = {str(literal.name): literal for literal in bron.literals}
        verdeeld = [waarde for _, _, lijst in SUBTYPEN.values() for waarde in lijst]
        if sorted(verdeeld) != sorted(waarden):
            raise CrunchException(
                "De waarden van Aanstellingssoort in het GGM komen niet overeen met de verdeling over de"
                f" subtypen in SUBTYPEN: {sorted(set(verdeeld) ^ set(waarden))}."
            )
        for subtype, (_, enum_naam, lijst) in SUBTYPEN.items():
            enum = Enumeratie(
                id=nieuw_id("enumeratie", enum_naam), name=enum_naam, schema_id=self.schema_id, package=self.kopie,
                definitie=f"{bron.definitie} Deze lijst bevat de soorten die bij {subtype} horen.",
            )
            for waarde in lijst:
                enum.literals.append(
                    EnumerationLiteral(
                        id=nieuw_id("waarde", enum_naam, waarde), name=waarde, schema_id=self.schema_id,
                        definitie=waarden[waarde].definitie,
                    )
                )
            self.enums[enum_naam] = enum
        self.kopie.enumerations.remove(bron)
        del self.enums["Aanstellingssoort"]

    def voeg_geslachtsaanduiding_toe(self):
        enum = Enumeratie(
            id=nieuw_id("enumeratie", "Geslachtsaanduiding"), name="Geslachtsaanduiding", schema_id=self.schema_id,
            package=self.kopie,
            definitie="Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht onbekend is.",
            toelichting="De waarden volgen de geslachtsaanduiding van Medewerker in het GGM.",
        )
        for waarde, definitie in (
            ("Vrouw", "De persoon is een vrouw."),
            ("Man", "De persoon is een man."),
            ("Onbekend", "Het geslacht is niet bekend of niet als man of vrouw geregistreerd."),
        ):
            enum.literals.append(
                EnumerationLiteral(
                    id=nieuw_id("waarde", "Geslachtsaanduiding", waarde), name=waarde, schema_id=self.schema_id,
                    definitie=definitie,
                )
            )
        self.enums["Geslachtsaanduiding"] = enum

    def verwerk_associaties(self, namen_bron):
        """Nest de associaties uit NESTEN en verwijder die uit VERVALLEN; iets anders is een fout."""
        gezien = set()
        for naam, clazz in self.klassen.items():
            for associatie in list(clazz.uitgaande_associaties):
                sleutel = (naam, str(associatie.name), namen_bron.get(associatie.dst_class_id))
                gezien.add(sleutel)
                if sleutel in NESTEN:
                    associatie.src_role, associatie.order = NESTEN[sleutel]
                elif sleutel in VERVALLEN:
                    clazz.uitgaande_associaties.remove(associatie)
                else:
                    raise CrunchException(
                        f"Associatie {sleutel} staat niet in NESTEN of VERVALLEN: leg vast hoe zij wordt uitgewisseld."
                    )
        ontbrekend = (set(NESTEN) | set(VERVALLEN)) - gezien
        if ontbrekend:
            raise CrunchException(f"Associaties uit NESTEN of VERVALLEN ontbreken in het informatiemodel: {ontbrekend}.")

        werknemer, inzet = self.klassen["Werknemer"], self.klassen["Inzet"]
        for volgorde, (subtype, (rolnaam, _, _)) in enumerate(SUBTYPEN.items(), start=1):
            self.nest(
                werknemer, self.klassen[subtype], rolnaam, 0, True, volgorde,
                f"De aanstellingscontracten van de werknemer van het subtype {subtype}.",
            )
            self.nest(
                self.klassen[subtype], inzet, "inzetten", 0, True, 1,
                "De inzet die op grond van het contract wordt verricht.",
            )

    def zet_kenmerken(self):
        """Breng elk objecttype terug tot de kenmerken uit KENMERKEN, in die volgorde."""
        for naam, gewenst in KENMERKEN.items():
            clazz = self.klassen[naam]
            aanwezig = {str(attr.name): attr for attr in clazz.attributes}
            for attribuut in list(clazz.attributes):
                clazz.attributes.remove(attribuut)
                attribuut.clazz_id = None
            for kenmerk in gewenst:
                nieuw = NIEUWE_KENMERKEN.get((naam, kenmerk)) or (
                    NIEUWE_KENMERKEN.get((SUPERTYPE, kenmerk)) if naam in SUBTYPEN else None
                )
                if nieuw:
                    attribuut = self.kenmerk(clazz, kenmerk, **nieuw)
                elif kenmerk in aanwezig:
                    attribuut = aanwezig[kenmerk]
                    attribuut.clazz_id = clazz.id
                    clazz.attributes.append(attribuut)
                else:
                    raise CrunchException(f"{naam} heeft in het informatiemodel geen kenmerk {kenmerk}.")
                if kenmerk == "aanstellingssoort":
                    attribuut.id = nieuw_id("kenmerk", naam, kenmerk)
                    attribuut.enumeration_id = self.enums[SUBTYPEN[naam][1]].id
                if (naam, kenmerk) in VERPLICHT_ANDERS:
                    attribuut.verplicht = VERPLICHT_ANDERS[(naam, kenmerk)]
                grenzen = GRENZEN.get((naam, kenmerk)) or GRENZEN.get(("*", kenmerk))
                if grenzen and not nieuw:
                    attribuut.minimumwaarde_inclusief, attribuut.maximumwaarde_inclusief = grenzen
        niet_genoemd = set(self.klassen) - set(KENMERKEN) - {SUPERTYPE}
        if niet_genoemd:
            raise CrunchException(f"Objecttypen zonder regel in KENMERKEN: {sorted(niet_genoemd)}.")

    def zet_datatypen(self):
        """Vertaal de datatypen van het GGM naar de eenvoudige typen van het JSON-schema."""
        for clazz in self.klassen.values():
            for attribuut in clazz.attributes:
                attribuut.type_class_id = None
                if attribuut.enumeration_id:
                    attribuut.primitive = None
                    continue
                type_ggm = str(attribuut.primitive or "").lower()
                if type_ggm in DATATYPEN:
                    attribuut.primitive = DATATYPEN[type_ggm]
                    attribuut.lengte = None
                elif type_ggm == "characterstring":
                    lengte = str(attribuut.lengte or "")
                    attribuut.primitive = f"AN{lengte}" if lengte.isdigit() else "AN"
                    attribuut.lengte = lengte if lengte.isdigit() else None

    def controleer_definities(self):
        """Vul de definities aan die het GGM nog mist; wat dan nog ontbreekt, is een fout."""
        zonder = []
        for naam, clazz in self.klassen.items():
            if naam == SUPERTYPE:
                continue
            clazz.definitie = clazz.definitie or AANGEVULDE_DEFINITIES.get((naam, None))
            clazz.toelichting = TOELICHTING_ANDERS.get(naam, clazz.toelichting)
            if not clazz.definitie:
                zonder.append(naam)
            for attribuut in clazz.attributes:
                attribuut.definitie = attribuut.definitie or AANGEVULDE_DEFINITIES.get((naam, str(attribuut.name)))
                if not attribuut.definitie:
                    zonder.append(f"{naam}.{attribuut.name}")
        if zonder:
            raise CrunchException(f"Zonder definitie in het uitwisselmodel: {zonder}. Vul AANGEVULDE_DEFINITIES aan.")

    def voeg_verloop_toe(self):
        verloop = self.klasse(
            "Arbeidsongeschiktheidsverloop",
            "Een periode binnen een verzuimgeval waarin het percentage arbeidsongeschiktheid gelijk blijft.",
            "Bestaat alleen in de uitwisseling. In het GGM is het percentage een kenmerk van Verzuim met historie;"
            " dit objecttype levert die historie. Een periode loopt tot de begindatum van de volgende periode, of"
            " tot het einde van het verzuim.",
        )
        self.kenmerk(
            verloop, "datumBegin", primitive="Datum", verplicht=True,
            definitie="De eerste dag waarop het percentage geldt.",
        )
        self.kenmerk(
            verloop, "percentageArbeidsongeschiktheid", primitive="Getal", verplicht=True, minimum="0", maximum="100",
            definitie="Het deel van de overeengekomen arbeidsduur waarvoor de werknemer in deze periode verzuimt, als percentage.",
        )
        self.nest(
            self.klassen["Verzuim"], verloop, "verloop", 0, True, 1,
            "Het verloop van het percentage arbeidsongeschiktheid binnen het verzuimgeval. Alleen nodig als het"
            " percentage tijdens het verzuim is gewijzigd.",
        )

    def voeg_levering_toe(self):
        uitwisselmodel = self.klasse(
            "Uitwisselmodel",
            "Eén bericht met HR-gegevens van één of meer gemeenten over één verslagperiode.",
            vast_id=UITWISSELMODEL_ID,
        )
        self.kenmerk(
            uitwisselmodel, "codeGegevensleverancier", primitive="AN200", verplicht=True,
            definitie="De naam van de gegevensleverancier (softwareleverancier of hostingpartij) en de versie van het pakket.",
        )
        self.kenmerk(
            uitwisselmodel, "versieSpecificatie", primitive="AN20", verplicht=True,
            definitie="De versie van de uitwisselspecificatie waaraan het bericht voldoet, bijvoorbeeld v0.1.",
        )
        self.kenmerk(
            uitwisselmodel, "startdatumLevering", primitive="Datum", verplicht=True,
            definitie="De eerste dag van de verslagperiode.",
        )
        self.kenmerk(
            uitwisselmodel, "einddatumLevering", primitive="Datum", verplicht=True,
            definitie="De laatste dag van de verslagperiode.",
        )
        self.kenmerk(
            uitwisselmodel, "aanleverdatumEnTijd", primitive="datumtijd", verplicht=True,
            definitie="Het moment waarop het bericht is samengesteld.",
        )

        levering = self.klasse(
            "Levering", "De HR-gegevens van precies één gemeente over de verslagperiode.",
            "Een leverancier die voor meerdere gemeenten levert, neemt per gemeente één levering op.",
        )
        self.kenmerk(
            levering, "teller", primitive="int", verplicht=True, minimum="1",
            definitie="Het volgnummer van de levering binnen het bericht, te beginnen bij 1.",
        )
        self.kenmerk(
            levering, "gemeentecode", primitive="AN4", verplicht=True,
            definitie="De CBS-gemeentecode van de gemeente waarover de gegevens gaan, vier cijfers met voorloopnullen.",
        )

        organisatie = self.klasse(
            "AanleverendeOrganisatie", "De organisatie die de gegevens van de levering aanlevert.",
            "Levert de gemeente zelf, dan is dit de gemeente; anders de leverancier die namens de gemeente levert.",
        )
        self.kenmerk(
            organisatie, "naam", primitive="AN200", verplicht=True,
            definitie="De naam van de aanleverende organisatie.",
        )
        self.kenmerk(
            organisatie, "kvkNummer", primitive="AN8", verplicht=False,
            definitie="Het KvK-nummer van de aanleverende organisatie, acht cijfers.",
            toelichting="Verplicht als een andere organisatie dan de gemeente aanlevert.",
        )

        contactpersoon = self.klasse(
            "Contactpersoon", "Een persoon bij de aanleverende organisatie die vragen over de levering kan beantwoorden.",
        )
        self.kenmerk(contactpersoon, "naam", primitive="AN200", verplicht=True, definitie="De naam van de contactpersoon.")
        self.kenmerk(contactpersoon, "functietitel", primitive="AN100", definitie="De functie van de contactpersoon.")
        self.kenmerk(contactpersoon, "email", primitive="email", definitie="Het e-mailadres van de contactpersoon.")
        self.kenmerk(contactpersoon, "telefoonnummer", primitive="AN20", definitie="Het telefoonnummer van de contactpersoon.")

        k = self.klassen
        self.nest(uitwisselmodel, levering, "leveringen", 1, True, 1, "De leveringen in het bericht: één per gemeente.")
        self.nest(levering, organisatie, "aanleverendeOrganisatie", 1, False, 1, "De organisatie die de levering aanlevert.")
        self.nest(organisatie, contactpersoon, "contactpersonen", 0, True, 1, "De contactpersonen voor de levering.")
        self.nest(
            levering, k["OrganisatorischeEenheidHR"], "organisatorischeEenheden", 1, True, 2,
            "De organisatorische eenheden van de gemeente die in de verslagperiode bestaan.",
        )
        self.nest(levering, k["Functie"], "functies", 0, True, 3, "De functies waarnaar in de levering wordt verwezen.")
        self.nest(
            levering, k["Formatieplaats"], "formatieplaatsen", 0, True, 4,
            "De formatieplaatsen die in de verslagperiode bestaan, ook de onbezette.",
        )
        self.nest(
            levering, k["Werknemer"], "werknemers", 0, True, 5,
            "De werknemers met ten minste één aanstellingscontract dat de verslagperiode raakt.",
        )
