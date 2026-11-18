"""Schrijf een JSON-bestand leesbaar weg: UTF-8-tekens voluit en twee spaties inspringing.

crunch_uml schrijft accenttekens als \\u-reeksen. Dat is geldige JSON, maar het leest slecht
in de specificatie. De inhoud van het bestand verandert niet.

Gebruik: python tools/formatteer_json.py <bestand.json> [<bestand.json> ...]
"""

import json
import sys
from pathlib import Path

for naam in sys.argv[1:]:
    pad = Path(naam)
    inhoud = json.loads(pad.read_text(encoding="utf-8"))
    pad.write_text(json.dumps(inhoud, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Leesbaar weggeschreven: {pad}")
