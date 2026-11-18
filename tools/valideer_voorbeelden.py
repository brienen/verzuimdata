"""Controleer de voorbeeldbestanden van een versie tegen het JSON-schema van die versie.

Naast het schema worden de regels gecontroleerd die een JSON-schema niet kan uitdrukken:
elke verwijzing (functie, organisatorischeEenheid, isDeelVan, formatieplaats) moet binnen
dezelfde levering bestaan, sleutels zijn binnen een levering uniek en een werknemer heeft
ten minste één aanstellingscontract.

Gebruik: python tools/valideer_voorbeelden.py <schema.json> <versiemap>
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

CONTRACTLIJSTEN = ("arbeidsovereenkomsten", "inhuurovereenkomsten", "overigeAanstellingen")


def dubbelen(waarden):
    gezien, dubbel = set(), set()
    for waarde in waarden:
        (dubbel if waarde in gezien else gezien).add(waarde)
    return sorted(dubbel)


def controleer_samenhang(bericht):
    """De regels buiten het schema; geeft een lijst met meldingen terug."""
    meldingen = []
    for levering in bericht.get("leveringen", []):
        waar = f"levering {levering.get('teller')}"
        eenheden = [e["organisatieIdentificatie"] for e in levering.get("organisatorischeEenheden", [])]
        functies = [f["code"] for f in levering.get("functies", [])]
        plaatsen = [p["formatieplaatsID"] for p in levering.get("formatieplaatsen", [])]
        werknemers = levering.get("werknemers", [])
        contracten = [c for w in werknemers for lijst in CONTRACTLIJSTEN for c in w.get(lijst, [])]

        for soort, sleutels in (
            ("organisatieIdentificatie", eenheden),
            ("functiecode", functies),
            ("formatieplaatsID", plaatsen),
            ("werknemerID", [w["werknemerID"] for w in werknemers]),
            ("aanstellingscontractID", [c["aanstellingscontractID"] for c in contracten]),
            ("verzuimID", [v["verzuimID"] for w in werknemers for v in w.get("verzuimgevallen", [])]),
        ):
            for sleutel in dubbelen(sleutels):
                meldingen.append(f"{waar}: {soort} '{sleutel}' komt meer dan één keer voor")

        def verwijzing(object_, veld, bekend, omschrijving):
            if veld in object_ and object_[veld] not in bekend:
                meldingen.append(f"{waar}: {omschrijving} verwijst met {veld} naar onbekende '{object_[veld]}'")

        for eenheid in levering.get("organisatorischeEenheden", []):
            verwijzing(eenheid, "isDeelVan", eenheden, f"eenheid {eenheid['organisatieIdentificatie']}")
        for plaats in levering.get("formatieplaatsen", []):
            verwijzing(plaats, "functie", functies, f"formatieplaats {plaats['formatieplaatsID']}")
            verwijzing(plaats, "organisatorischeEenheid", eenheden, f"formatieplaats {plaats['formatieplaatsID']}")
        for werknemer in werknemers:
            wie = f"werknemer {werknemer['werknemerID']}"
            if not any(werknemer.get(lijst) for lijst in CONTRACTLIJSTEN):
                meldingen.append(f"{waar}: {wie} heeft geen aanstellingscontract")
            for rol in werknemer.get("rollen", []):
                verwijzing(rol, "organisatorischeEenheid", eenheden, f"rol van {wie}")
            for lijst in CONTRACTLIJSTEN:
                for contract in werknemer.get(lijst, []):
                    welk = f"contract {contract['aanstellingscontractID']}"
                    verwijzing(contract, "functie", functies, welk)
                    verwijzing(contract, "organisatorischeEenheid", eenheden, welk)
                    verwijzing(contract, "formatieplaats", plaatsen, welk)
                    for inzet in contract.get("inzetten", []):
                        verwijzing(inzet, "functie", functies, f"inzet bij {welk}")
                        verwijzing(inzet, "organisatorischeEenheid", eenheden, f"inzet bij {welk}")
    return meldingen


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    schema = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    voorbeelden = sorted(Path(sys.argv[2]).glob("*Voorbeeld.json"))
    if not voorbeelden:
        sys.exit(f"Geen voorbeeldbestanden (*Voorbeeld.json) gevonden in {sys.argv[2]}")

    fouten = 0
    for voorbeeld in voorbeelden:
        bericht = json.loads(voorbeeld.read_text(encoding="utf-8"))
        meldingen = [
            f"/{'/'.join(str(deel) for deel in fout.absolute_path)}: {fout.message}"
            for fout in sorted(validator.iter_errors(bericht), key=lambda fout: list(fout.absolute_path))
        ]
        if not meldingen:
            meldingen = controleer_samenhang(bericht)
        if meldingen:
            fouten += 1
            print(f"ONGELDIG: {voorbeeld}")
            for melding in meldingen:
                print(f"  {melding}")
        else:
            print(f"Geldig: {voorbeeld}")
    sys.exit(1 if fouten else 0)


if __name__ == "__main__":
    main()
