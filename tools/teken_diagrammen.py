#!/usr/bin/env python3
"""Tekent de twee diagrammen van de specificatie, met vaste posities.

  docs/images/informatiemodel.png   het informatiemodel op hoofdlijnen
  docs/images/opbouw-bericht.png    de opbouw van een bericht

De afbeeldingen staan in git; dit script is alleen nodig als het model verandert. Het hoort
niet bij de gewone build en vraagt Pillow (`uv pip install pillow`) en de lettertypen van macOS.

Gebruik:  python tools/teken_diagrammen.py [uitvoermap]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 2  # schaal voor scherpte
FD = "/System/Library/Fonts/Supplemental/"


def font(naam, grootte):
    return ImageFont.truetype(FD + naam, grootte * S)


F_N = font("Arial.ttf", 12)
F_NAAM, F_ST = font("Arial Bold.ttf", 13), font("Arial Italic.ttf", 11)
F_LBL, F_CL, F_TITEL = font("Arial.ttf", 11), font("Arial Bold.ttf", 12), font("Arial Bold.ttf", 16)

KLEUR = {  # soort: (vulling, rand)
    "M": ("#FFFFFF", "#777777"),  # objecttype uit Model HR van het GGM
    "X": ("#E4ECF6", "#5F7FA3"),  # objecttype uit een ander model van het GGM
    "U": ("#D6EAD8", "#3F7F4A"),  # bestaat alleen in de uitwisseling
}
LIJN, VERVALT = "#444444", "#B5535B"
KOP, RIJ = 48, 17


class Diagram:
    def __init__(self, b, h, titel):
        self.b, self.h = b, h
        self.im = Image.new("RGB", (b * S, h * S), "white")
        self.d = ImageDraw.Draw(self.im)
        self.rect, self.boxen, self.lijnen, self.labels = {}, [], [], []
        self.d.text((24 * S, 12 * S), titel, font=F_TITEL, fill="#222222")

    # ── elementen ────────────────────────────────────────────────────────────
    def cluster(self, label, x0, y0, x1, y1):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=10 * S, fill="#F3F5F7", outline="#C9CED4", width=S)
        self.d.text(((x0 + 10) * S, (y0 + 6) * S), label, font=F_CL, fill="#5A6672")

    def box(self, sleutel, cx, top, b, status, stereo="", attrs=None, naam=None, abstract=False):
        h = KOP + (8 + RIJ * len(attrs) + 6 if attrs else 0)
        self.rect[sleutel] = (cx - b / 2, top, cx + b / 2, top + h)
        self.boxen.append((sleutel, naam or sleutel, status, stereo, attrs or [], abstract))

    def punt(self, sleutel, zijde, f=0.5):
        x0, y0, x1, y1 = self.rect[sleutel]
        return {"l": (x0, y0 + f * (y1 - y0)), "r": (x1, y0 + f * (y1 - y0)),
                "t": (x0 + f * (x1 - x0), y0), "b": (x0 + f * (x1 - x0), y1)}[zijde]

    def lijn(self, a, za, b, zb, label="", ma="", mb="", soort="assoc", fa=0.5, fb=0.5, via=None, seg=None, dx=0, dy=0):
        p1, p2 = self.punt(a, za, fa), self.punt(b, zb, fb)
        if via is None:
            via = []
            hor_a, hor_b = za in "lr", zb in "lr"
            if hor_a and hor_b and abs(p1[1] - p2[1]) > 1:
                mx = (p1[0] + p2[0]) / 2
                via = [(mx, p1[1]), (mx, p2[1])]
            elif not hor_a and not hor_b and abs(p1[0] - p2[0]) > 1:
                my = (p1[1] + p2[1]) / 2
                via = [(p1[0], my), (p2[0], my)]
            elif hor_a and not hor_b:
                via = [(p2[0], p1[1])]
            elif not hor_a and hor_b:
                via = [(p1[0], p2[1])]
        self.lijnen.append(([p1] + list(via) + [p2], soort, label, ma, mb, za, zb, seg, dx, dy))

    # ── tekenen ──────────────────────────────────────────────────────────────
    def _streep(self, p, q, kleur, gestreept):
        if not gestreept:
            self.d.line([p[0] * S, p[1] * S, q[0] * S, q[1] * S], fill=kleur, width=int(1.5 * S))
            return
        (x0, y0), (x1, y1) = p, q
        lengte = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        n = max(1, int(lengte // 9))
        for i in range(n):
            a, b = i / n, (i + 0.55) / n
            self.d.line([(x0 + (x1 - x0) * a) * S, (y0 + (y1 - y0) * a) * S, (x0 + (x1 - x0) * b) * S, (y0 + (y1 - y0) * b) * S],
                        fill=kleur, width=int(1.5 * S))

    def _tekst(self, x, y, tekst, f, kleur="#333333", achtergrond=True):
        b = self.d.textlength(tekst, font=f) / S
        if achtergrond:
            self.d.rectangle([(x - 2) * S, (y - 1) * S, (x + b + 2) * S, (y + 14) * S], fill="white")
        self.d.text((x * S, y * S), tekst, font=f, fill=kleur)

    def _mult(self, p, zijde, tekst, kleur):
        if not tekst:
            return
        b = self.d.textlength(tekst, font=F_LBL) / S
        x, y = {"r": (p[0] + 5, p[1] - 15), "l": (p[0] - 5 - b, p[1] - 15),
                "t": (p[0] + 5, p[1] - 16), "b": (p[0] + 5, p[1] + 3)}[zijde]
        self.labels.append((x, y, tekst, kleur))

    def teken(self):
        for pts, soort, label, ma, mb, za, zb, seg, dx, dy in self.lijnen:
            kleur = VERVALT if soort == "vervalt" else LIJN
            for p, q in zip(pts, pts[1:]):
                self._streep(p, q, kleur, soort == "vervalt")
            (px, py), (qx, qy) = pts[-2], pts[-1]
            lengte = max(1.0, ((qx - px) ** 2 + (qy - py) ** 2) ** 0.5)
            ux, uy = (qx - px) / lengte, (qy - py) / lengte
            if soort == "gen":  # open driehoek
                g = 13
                bx, by = qx - ux * g, qy - uy * g
                self.d.polygon([(qx * S, qy * S), ((bx - uy * 7) * S, (by + ux * 7) * S), ((bx + uy * 7) * S, (by - ux * 7) * S)],
                               fill="white", outline=kleur, width=int(1.5 * S))
            elif soort == "assoc":  # open pijlpunt
                g = 9
                bx, by = qx - ux * g, qy - uy * g
                self.d.line([(bx - uy * 4.5) * S, (by + ux * 4.5) * S, qx * S, qy * S, (bx + uy * 4.5) * S, (by - ux * 4.5) * S],
                            fill=kleur, width=int(1.5 * S))
            self._mult(pts[0], za, ma, kleur)
            self._mult(pts[-1], zb, mb, kleur)
            if label:
                segs = list(zip(pts, pts[1:]))
                i = seg if seg is not None else max(range(len(segs)), key=lambda k: abs(segs[k][0][0] - segs[k][1][0]) + abs(segs[k][0][1] - segs[k][1][1]))
                (ax, ay), (bx2, by2) = segs[i]
                tb = self.d.textlength(label, font=F_LBL) / S
                if abs(ay - by2) < 1:
                    x, y = (ax + bx2) / 2 - tb / 2, ay - 17
                else:
                    x, y = ax + 6, (ay + by2) / 2 - 7
                self.labels.append((x + dx, y + dy, label, kleur))
        for sleutel, naam, status, stereo, attrs, abstract in self.boxen:
            x0, y0, x1, y1 = self.rect[sleutel]
            vul, rand = KLEUR[status]
            self.d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=vul, outline=rand, width=int(1.5 * S))
            cx = (x0 + x1) / 2
            if stereo:
                t = f"«{stereo}»"
                self.d.text(((cx - self.d.textlength(t, font=F_ST) / S / 2) * S, (y0 + 6) * S), t, font=F_ST, fill="#555555")
            f = font("Arial Bold Italic.ttf", 13) if abstract else F_NAAM
            self.d.text(((cx - self.d.textlength(naam, font=f) / S / 2) * S, (y0 + (24 if stereo else 15)) * S), naam, font=f, fill="#111111")
            if attrs:
                self.d.line([x0 * S, (y0 + KOP) * S, x1 * S, (y0 + KOP) * S], fill=rand, width=S)
                for i, (t, f) in enumerate(attrs):
                    self.d.text(((x0 + 8) * S, (y0 + KOP + 6 + i * RIJ) * S), t, font=f, fill="#222222")
        for x, y, tekst, kleur in self.labels:
            self._tekst(x, y, tekst, F_LBL, kleur)

    def legenda(self, x, y, items):
        for i, (soort, tekst) in enumerate(items):
            vul, rand = KLEUR[soort]
            xi = x + i * 250
            self.d.rectangle([xi * S, y * S, (xi + 22) * S, (y + 14) * S], fill=vul, outline=rand, width=S)
            self.d.text(((xi + 28) * S, y * S), tekst, font=F_LBL, fill="#333333")

    def notitie(self, x, y, tekst):
        self.d.text((x * S, y * S), tekst, font=F_LBL, fill="#555555")

    def bewaar(self, pad):
        self.teken()
        self.im.save(pad)
        print(f"Getekend: {pad}")


def informatiemodel(uit):
    d = Diagram(1560, 1000, "Informatiemodel op hoofdlijnen")
    B = 180
    d.cluster("Verzuim en verlof", 25, 215, 302, 480)
    d.cluster("Aanstelling", 340, 375, 920, 685)
    d.cluster("Functie en formatie", 960, 225, 1460, 620)
    d.cluster("Organisatie", 960, 675, 1460, 920)

    d.box("Medewerker", 160, 70, B, "X", "Model Kern RGBZ")
    d.box("Werknemer", 630, 70, 190, "M")
    d.box("Rol", 1350, 70, B, "M")
    d.box("Verzuim", 110, 250, 150, "M")
    d.box("Verlof", 110, 380, 150, "M")
    d.box("Aanstellingscontract", 630, 400, 190, "M", "abstract", abstract=True)
    d.box("Arbeidsovereenkomst", 440, 620, 175, "M")
    d.box("Inhuurovereenkomst", 630, 620, 175, "M")
    d.box("OverigeAanstelling", 820, 620, 175, "M")
    d.box("Formatieplaats", 1075, 250, B, "M")
    d.box("Functie", 1075, 400, B, "M")
    d.box("Inzet", 1075, 550, B, "M")
    d.box("OEHR", 1075, 700, 210, "M", naam="OrganisatorischeEenheidHR")
    d.box("OE", 1075, 850, 210, "X", "Model Kern RGBZ", naam="OrganisatorischeEenheid")
    d.box("NormProfiel", 1350, 400, B, "M")
    d.box("Functiehuis", 1350, 550, B, "M")

    d.lijn("Werknemer", "l", "Medewerker", "r", soort="gen", fa=0.3, fb=0.3)
    d.lijn("Werknemer", "r", "Rol", "l", "heeft", "1..*", "0..*")
    d.lijn("Werknemer", "b", "Aanstellingscontract", "t", "heeft aanstellingscontract", "1", "1..*")
    d.lijn("Werknemer", "l", "Verzuim", "r", "heeft verzuim", "", "0..*", fa=0.75, via=[(318, 106), (318, 274)], seg=2)
    d.lijn("Werknemer", "l", "Verlof", "r", "heeft verlof", "", "0..*", fa=0.75, via=[(318, 106), (318, 404)], seg=2)
    for sub, x in (("Arbeidsovereenkomst", 440), ("Inhuurovereenkomst", 630), ("OverigeAanstelling", 820)):
        d.lijn(sub, "t", "Aanstellingscontract", "b", soort="gen", via=[(x, 540), (630, 540)])
    d.lijn("Aanstellingscontract", "r", "Functie", "l", "conform functie", "0..*", "0..1", fa=0.25, fb=0.25)
    d.lijn("Aanstellingscontract", "r", "Inzet", "l", "heeft inzet", "1", "0..*", fa=0.8, via=[(940, 438.4), (940, 574)], seg=1, dx=-72)
    d.lijn("Formatieplaats", "l", "Aanstellingscontract", "t", "toegewezen aan", "0..*", "0..*", fb=0.8)
    d.lijn("Formatieplaats", "b", "Functie", "t", "functie van formatieplaats")
    d.lijn("Inzet", "t", "Functie", "b", "inzet voor functie")
    d.lijn("Inzet", "b", "OEHR", "t", "inzet bij")
    d.lijn("OEHR", "b", "OE", "t", soort="gen")
    d.lijn("Functie", "r", "NormProfiel", "l", "gebaseerd op")
    d.lijn("NormProfiel", "b", "Functiehuis", "t", "onderdeel van")
    d.lijn("Rol", "r", "OEHR", "r", "hoort bij", fb=0.5, via=[(1500, 94), (1500, 724)])
    d.legenda(40, 940, [("M", "objecttype uit Model HR"), ("X", "objecttype uit een ander model van het GGM")])
    d.notitie(40, 964, "Niet getekend: een aanstellingscontract en een formatieplaats zijn onderdeel van een organisatorische eenheid, "
                       "en een organisatorische eenheid kan deel zijn van een andere eenheid.")
    d.bewaar(uit / "informatiemodel.png")


def opbouw_bericht(uit):
    d = Diagram(1330, 900, "Opbouw van een bericht")
    B, K = 226, [135, 395, 655, 915, 1175]  # breedte van een vak en het midden van de kolommen
    vakken = [  # sleutel, kolom, top, soort, rol en aantal, naam
        ("Uitwisselmodel", 0, 70, "U", "het bericht", None),
        ("Levering", 1, 70, "U", "leveringen  1..*", None),
        ("AanleverendeOrganisatie", 2, 70, "U", "aanleverendeOrganisatie  1", None),
        ("Contactpersoon", 3, 70, "U", "contactpersonen  0..*", None),
        ("OEHR", 2, 150, "M", "organisatorischeEenheden  1..*", "OrganisatorischeEenheidHR"),
        ("Functie", 2, 230, "M", "functies  0..*", None),
        ("NormProfiel", 3, 230, "M", "normProfiel  0..1", None),
        ("Functiehuis", 4, 230, "M", "functiehuis  1", None),
        ("Formatieplaats", 2, 310, "M", "formatieplaatsen  0..*", None),
        ("Werknemer", 2, 390, "M", "werknemers  0..*", None),
        ("Arbeidsovereenkomst", 3, 390, "M", "arbeidsovereenkomsten  0..*", None),
        ("Inhuurovereenkomst", 3, 470, "M", "inhuurovereenkomsten  0..*", None),
        ("OverigeAanstelling", 3, 550, "M", "overigeAanstellingen  0..*", None),
        ("Inzet", 4, 470, "M", "inzetten  0..*", None),
        ("Rol", 3, 630, "M", "rollen  0..*", None),
        ("Verzuim", 3, 710, "M", "verzuimgevallen  0..*", None),
        ("Verloop", 4, 710, "U", "verloop  0..*", "Arbeidsongeschiktheidsverloop"),
        ("Verlof", 3, 790, "M", "verlofperioden  0..*", None),
    ]
    for sleutel, kolom, top, soort, rol, naam in vakken:
        d.box(sleutel, K[kolom], top, B, soort, rol, naam=naam)
    for ouder, kinderen in (
        ("Uitwisselmodel", ["Levering"]),
        ("Levering", ["AanleverendeOrganisatie", "OEHR", "Functie", "Formatieplaats", "Werknemer"]),
        ("AanleverendeOrganisatie", ["Contactpersoon"]),
        ("Functie", ["NormProfiel"]),
        ("NormProfiel", ["Functiehuis"]),
        ("Werknemer", ["Arbeidsovereenkomst", "Inhuurovereenkomst", "OverigeAanstelling", "Rol", "Verzuim", "Verlof"]),
        ("Arbeidsovereenkomst", ["Inzet"]),
        ("Inhuurovereenkomst", ["Inzet"]),
        ("OverigeAanstelling", ["Inzet"]),
        ("Verzuim", ["Verloop"]),
    ):
        for kind in kinderen:
            d.lijn(ouder, "r", kind, "l")
    d.legenda(40, 850, [("M", "objecttype uit het informatiemodel (GGM)"), ("U", "bestaat alleen in de uitwisseling")])
    d.notitie(40, 874, "In elk vak staat boven de naam van het veld en het aantal, daaronder het objecttype. Verwijzingen naar een functie, "
                       "organisatorische eenheid of formatieplaats lopen via sleutels.")
    d.bewaar(uit / "opbouw-bericht.png")


if __name__ == "__main__":
    uitvoer = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "docs" / "images"
    uitvoer.mkdir(parents=True, exist_ok=True)
    informatiemodel(uitvoer)
    opbouw_bericht(uitvoer)
