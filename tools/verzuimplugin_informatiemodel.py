"""crunch_uml-plugin: van Model HR (GGM) naar het informatiemodel van de specificatie.

Het informatiemodel is het deel van Model HR van het Gemeentelijk Gegevensmodel dat voor
het Verzuimportaal nodig is. De plugin

1. kopieert Model HR en houdt alleen de objecttypen en enumeraties uit OBJECTTYPEN en
   ENUMERATIES over;
2. neemt de kenmerken over die een objecttype van een supertype buiten Model HR erft en
   die in de specificatie nodig zijn (GEERFDE_KENMERKEN, GEERFDE_ASSOCIATIES);
3. zet 'verplicht' op basis van de kardinaliteit van een kenmerk;
4. maakt de teksten schoon (opmaak van Enterprise Architect, wijzigingsgeschiedenis in
   toelichtingen) en sorteert een aantal waardelijsten;
5. vult de definities van associaties aan uit het GGM-bestand (zie definities_van_associaties).

Objecttypen worden op naam gezocht en niet op EA-GUID, zodat de plugin leesbaar blijft
en een hernoemd of verdwenen objecttype een duidelijke foutmelding geeft.
"""

import html
import logging
import os
import re
import sqlite3

from crunch_uml.exceptions import CrunchException
from crunch_uml.transformers.plugin import Plugin

logger = logging.getLogger()

MODEL_HR_PACKAGE_ID = "EAPK_9ADEFB08_F150_4278_8D32_32465C57E8A7"

# De objecttypen van Model HR die in de specificatie zijn opgenomen.
OBJECTTYPEN = [
    "Werknemer",
    "Aanstellingscontract",
    "Arbeidsovereenkomst",
    "Inhuurovereenkomst",
    "OverigeAanstelling",
    "Inzet",
    "Rol",
    "Verzuim",
    "Verlof",
    "OrganisatorischeEenheidHR",
    "Functie",
    "NormProfiel",
    "Functiehuis",
    "Formatieplaats",
]

# De enumeraties van Model HR die in de specificatie zijn opgenomen.
ENUMERATIES = [
    "Aanstellingssoort",
    "Contractsoort",
    "Cao",
    "RedenEindeArbeidsovereenkomst",
    "BestemmingInzet",
    "Rolsoort",
    "Werkomgeving",
    "OrganisatorischeEenheidsoort",
    "Verzuimsoort",
    "RedenEindeVerzuim",
    "Verlofsoort",
]

# Kenmerken die een objecttype erft van een supertype buiten Model HR en die hier bij het
# objecttype zelf worden getoond: objecttype -> (supertype, kenmerken).
GEERFDE_KENMERKEN = {
    "Werknemer": ("Medewerker", ["medewerkerIdentificatie", "geslachtsaanduiding"]),
    "OrganisatorischeEenheidHR": (
        "OrganisatorischeEenheid",
        ["organisatieIdentificatie", "datumOntstaan", "datumOpheffing"],
    ),
}

# Associaties van een supertype buiten Model HR die tussen voorkomens van het subtype
# gelden: objecttype -> (supertype, namen van associaties naar het supertype zelf).
GEERFDE_ASSOCIATIES = {
    "OrganisatorischeEenheidHR": ("OrganisatorischeEenheid", ["Is deel van"]),
}

# Waardelijsten die alfabetisch worden gepubliceerd, met 'Overig' achteraan. De overige
# lijsten houden de volgorde van het GGM, omdat die volgorde daar betekenis heeft
# (Aanstellingssoort volgt bijvoorbeeld de drie subtypen van Aanstellingscontract).
ALFABETISCH_TE_SORTEREN = [
    "RedenEindeArbeidsovereenkomst",
    "RedenEindeVerzuim",
    "Verlofsoort",
]
ALTIJD_ACHTERAAN = ("overig", "anders", "onbekend")

# Het GGM-bestand zelf; alleen nodig voor de definities van associaties.
GGM_BESTAND = os.environ.get("GGM_BESTAND", "data/Gemeentelijk Gegevensmodel.qea")

MEMO = re.compile(r"</?memo>|#NOTES#", re.IGNORECASE)
HTML_TAG = re.compile(r"<[^>]+>")
VERWIJZING_VENSTER = re.compile(r"\s*\(W\d+\)")
ZIN = re.compile(r"(?<=[.!?])\s+")

# De toelichtingen in het GGM beschrijven ook wat er ten opzichte van de vorige versie van het
# model is veranderd. Dat is voor een leverancier geen informatie. Een zin die aan een van deze
# patronen voldoet, komt daarom niet in de specificatie.
WIJZIGINGSGESCHIEDENIS = [
    re.compile(patroon, re.IGNORECASE)
    for patroon in (
        r"^Was\b",
        r"\bVerhuisd van\b",
        r"^Optioneel gemaakt\.$",
        r"\bin plaats van (tekst|geheel getal)\b",
        r"^Vervangt de associatie\b",
        r"^De huidige definitie\b",
        r"^Het huidige objecttype\b",
        r"\bis hersteld\b",
        r"\bvervalt\.$",
        r"\bvoorgesteld wordt\b",
        r"^Omgekeerd, zodat\b",
    )
]
OPTIONEEL_GEMAAKT = re.compile(r"^(.*\b[Oo]ptioneel gemaakt): (.)(.*)$")


def schone_tekst(tekst):
    """Haal de opmaak van Enterprise Architect (memo-markering, HTML) uit een tekst."""
    if not isinstance(tekst, str) or tekst.strip().lower() in ("", "nan"):
        return None
    tekst = html.unescape(HTML_TAG.sub("", MEMO.sub("", tekst)))
    return tekst.strip() or None


def schone_toelichting(tekst):
    """Een toelichting zonder opmaak en zonder zinnen over de wijzigingsgeschiedenis."""
    tekst = schone_tekst(tekst)
    if tekst is None:
        return None
    zinnen = []
    for zin in ZIN.split(VERWIJZING_VENSTER.sub("", tekst)):
        optioneel = OPTIONEEL_GEMAAKT.match(zin)
        if optioneel:  # 'Optioneel gemaakt: leeg zolang ...' -> 'Leeg zolang ...'
            zin = optioneel.group(2).upper() + optioneel.group(3)
        if any(patroon.search(zin) for patroon in WIJZIGINGSGESCHIEDENIS):
            logger.debug(f"Zin over wijzigingsgeschiedenis weggelaten: {zin}")
            continue
        zinnen.append(zin)
    return " ".join(zinnen) or None


def definities_van_associaties(bestand):
    """De definities van associaties, rechtstreeks uit het GGM-bestand: EA-id -> definitie.

    crunch_uml (0.8.6) leest de definitie van een associatie uit de notitie van de connector,
    maar overschrijft haar daarna met de lege MIM-tag 'Definitie'. Zolang dat zo is, halen we
    de notitie hier zelf op. Is het bestand er niet, dan blijven de definities leeg.
    """
    if not os.path.isfile(bestand):
        logger.warning(f"GGM-bestand {bestand} niet gevonden; associaties blijven zonder definitie.")
        return {}
    with sqlite3.connect(f"file:{bestand}?mode=ro", uri=True) as verbinding:
        rijen = verbinding.execute(
            "SELECT ea_guid, Notes FROM t_connector WHERE Notes IS NOT NULL AND Notes <> ''"
        ).fetchall()
    return {"EAID_" + guid.strip("{}").replace("-", "_"): notitie for guid, notitie in rijen}


def sorteer_waarden(package, enum_namen):
    """Sorteer de waarden van de genoemde enumeraties alfabetisch, 'Overig' achteraan."""

    def sleutel(literal):
        naam = str(literal.name).casefold()
        return (naam in ALTIJD_ACHTERAAN, re.sub(r"^[^0-9a-z]+", "", naam), naam)

    te_sorteren = set(enum_namen)
    for enumeratie in package.enumerations:
        if enumeratie.name in te_sorteren:
            enumeratie.literals.sort(key=sleutel)
            te_sorteren.discard(enumeratie.name)
            logger.info(f"Enumeratie {enumeratie.name} alfabetisch gesorteerd.")
    if te_sorteren:
        raise CrunchException(f"Kan niet sorteren: enumeraties ontbreken in het model: {sorted(te_sorteren)}.")


class VerzuimPluginInformatiemodel(Plugin):
    def transformLogic(self, args, root_package, schema_from, schema_to):
        logger.info("Start plugin informatiemodel Verzuimportaal.")
        schema_to.clean()

        if root_package.id != MODEL_HR_PACKAGE_ID:
            raise CrunchException(
                f"{self.__class__.__name__} verwacht Model HR ({MODEL_HR_PACKAGE_ID}) als rootpackage,"
                f" niet {root_package.id}."
            )

        bron = {str(clazz.name): clazz for clazz in root_package.classes}
        ontbrekend = [naam for naam in OBJECTTYPEN if naam not in bron]
        if ontbrekend:
            raise CrunchException(f"Objecttypen ontbreken in Model HR: {ontbrekend}.")
        in_scope = {bron[naam].id for naam in OBJECTTYPEN}

        kopie = root_package.get_copy(None, materialize_generalizations=False)

        # 1. Alleen de objecttypen en enumeraties van de specificatie blijven over.
        for clazz in list(kopie.classes):
            if clazz.id not in in_scope:
                kopie.classes.remove(clazz)
                continue
            for associatie in list(clazz.uitgaande_associaties):
                if associatie.dst_class_id not in in_scope:
                    clazz.uitgaande_associaties.remove(associatie)
            for generalisatie in list(clazz.subclasses):
                if generalisatie.subclass_id not in in_scope:
                    clazz.subclasses.remove(generalisatie)

        aanwezig = {str(enum.name) for enum in kopie.enumerations}
        ontbrekend = [naam for naam in ENUMERATIES if naam not in aanwezig]
        if ontbrekend:
            raise CrunchException(f"Enumeraties ontbreken in Model HR: {ontbrekend}.")
        for enum in list(kopie.enumerations):
            if enum.name not in ENUMERATIES:
                kopie.enumerations.remove(enum)
        kopie.diagrams.clear()

        kopieen = {str(clazz.name): clazz for clazz in kopie.classes}

        # 2. Geërfde kenmerken en associaties van supertypen buiten Model HR.
        def supertype_van(naam, naam_supertype):
            for generalisatie in bron[naam].superclasses:
                if generalisatie.superclass is not None and generalisatie.superclass.name == naam_supertype:
                    return generalisatie.superclass
            raise CrunchException(f"{naam} heeft in het GGM geen supertype {naam_supertype}.")

        for naam, (naam_supertype, kenmerken) in GEERFDE_KENMERKEN.items():
            supertype = supertype_van(naam, naam_supertype)
            beschikbaar = {str(attr.name): attr for attr in supertype.attributes}
            for positie, kenmerk in enumerate(kenmerken):
                if kenmerk not in beschikbaar:
                    raise CrunchException(f"{naam_supertype} heeft geen kenmerk {kenmerk}.")
                geerfd = beschikbaar[kenmerk].get_copy(supertype)
                geerfd.id = f"{beschikbaar[kenmerk].id}_{kopieen[naam].id[-12:]}"
                geerfd.clazz_id = kopieen[naam].id
                geerfd.herkomst = f"Geërfd van {naam_supertype}"
                kopieen[naam].attributes.insert(positie, geerfd)
                logger.info(f"Kenmerk {kenmerk} van {naam_supertype} overgenomen bij {naam}.")

        for naam, (naam_supertype, associaties) in GEERFDE_ASSOCIATIES.items():
            supertype = supertype_van(naam, naam_supertype)
            for associatie in supertype.uitgaande_associaties:
                if associatie.name in associaties and associatie.dst_class_id == supertype.id:
                    geerfd = associatie.get_copy(supertype)
                    geerfd.id = f"{associatie.id}_{kopieen[naam].id[-12:]}"
                    geerfd.src_class_id = kopieen[naam].id
                    geerfd.dst_class_id = kopieen[naam].id
                    geerfd.herkomst = f"Geërfd van {naam_supertype}"
                    kopieen[naam].uitgaande_associaties.append(geerfd)
                    logger.info(f"Associatie '{associatie.name}' van {naam_supertype} overgenomen bij {naam}.")

        # 3, 4 en 5. Verplichting uit de kardinaliteit, schone teksten, definities van
        # associaties en gesorteerde waardelijsten.
        definities = definities_van_associaties(GGM_BESTAND)
        for clazz in kopie.classes:
            clazz.definitie = schone_tekst(clazz.definitie)
            clazz.toelichting = schone_toelichting(clazz.toelichting)
            for attribuut in clazz.attributes:
                attribuut.definitie = schone_tekst(attribuut.definitie)
                attribuut.toelichting = schone_toelichting(attribuut.toelichting)
                attribuut.verplicht = str(attribuut.mult_start) == "1"
            for associatie in clazz.uitgaande_associaties:
                bron_id = associatie.id[:41]  # een geërfde associatie heeft een achtervoegsel
                associatie.definitie = schone_tekst(associatie.definitie or definities.get(bron_id))
                associatie.toelichting = schone_toelichting(associatie.toelichting)
        for enum in kopie.enumerations:
            enum.definitie = schone_tekst(enum.definitie)
            enum.toelichting = schone_toelichting(enum.toelichting)
            for literal in enum.literals:
                literal.definitie = schone_tekst(literal.definitie)
        sorteer_waarden(kopie, ALFABETISCH_TE_SORTEREN)

        schema_to.add(kopie, recursive=True)
        logger.info("Plugin informatiemodel Verzuimportaal klaar.")
