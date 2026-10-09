#!/usr/bin/env python3
"""Rechtstexte in eine Seite einsetzen.

Aufruf:
    python3 einbauen.py <seite.html> <impressum|datenschutz>

Ersetzt in <seite.html> alles zwischen

    <!-- RECHTSTEXT:datenschutz:ANFANG -->
    <!-- RECHTSTEXT:datenschutz:ENDE -->

durch den Inhalt von datenschutz.html aus diesem Ordner. Kopf, Fusszeile
und Gestaltung bleiben Sache der jeweiligen Website.

Bricht mit Fehler ab (und damit den Deploy), wenn
- die Markierungen fehlen oder doppelt vorkommen,
- der Text Skripte, Frames, Formulare, Inline-Styles oder
  Event-Attribute enthaelt (das Repository ist oeffentlich lesbar,
  in die Seiten soll trotzdem nur reiner Text gelangen),
- ein Verweis "Abschnitt N" auf eine Nummer zeigt, die es nicht gibt.
"""

import re
import sys
from pathlib import Path

ORDNER = Path(__file__).resolve().parent
TEXTE = ("impressum", "datenschutz")

VERBOTEN = [
    (r"<\s*(script|iframe|object|embed|form|input|style|link|meta|base)\b", "verbotenes Element"),
    (r"\son[a-z]+\s*=", "Event-Attribut"),
    (r"\sstyle\s*=", "Inline-Style"),
    (r"javascript:", "javascript:-Link"),
]


def fehler(meldung):
    print(f"FEHLER: {meldung}", file=sys.stderr)
    sys.exit(1)


def pruefen(name, text):
    if "<h2" not in text:
        fehler(f"{name}.html enthaelt keine Ueberschrift, Datei leer oder kaputt?")
    for muster, was in VERBOTEN:
        treffer = re.search(muster, text, re.IGNORECASE)
        if treffer:
            fehler(f"{name}.html enthaelt {was}: {treffer.group(0).strip()}")
    if name == "datenschutz":
        nummern = {int(n) for n in re.findall(r"<h2[^>]*>\s*(\d+)\.", text)}
        if not nummern:
            fehler("datenschutz.html: keine nummerierten Abschnitte gefunden")
        if sorted(nummern) != list(range(1, max(nummern) + 1)):
            fehler(f"datenschutz.html: Abschnittsnummern luecken- oder fehlerhaft: {sorted(nummern)}")
        for gruppe in re.findall(r"Abschnitte?\s+(\d+(?:\s*(?:,|und)\s*\d+)*)", text):
            for n in re.findall(r"\d+", gruppe):
                if int(n) not in nummern:
                    fehler(f"datenschutz.html verweist auf Abschnitt {n}, den es nicht gibt")


def einsetzen(seite, name):
    if name not in TEXTE:
        fehler(f"unbekannter Text '{name}', erlaubt: {', '.join(TEXTE)}")
    text = (ORDNER / f"{name}.html").read_text(encoding="utf-8").strip()
    pruefen(name, text)

    pfad = Path(seite)
    html = pfad.read_text(encoding="utf-8")
    anfang = f"<!-- RECHTSTEXT:{name}:ANFANG -->"
    ende = f"<!-- RECHTSTEXT:{name}:ENDE -->"
    if html.count(anfang) != 1 or html.count(ende) != 1:
        fehler(f"{seite}: Markierungen fuer '{name}' fehlen oder kommen mehrfach vor")
    vorher, rest = html.split(anfang)
    _, nachher = rest.split(ende)

    # Einrueckung der Anfangsmarkierung uebernehmen, damit der Quelltext
    # der Seite lesbar bleibt.
    zeile = vorher.rsplit("\n", 1)[-1]
    einzug = zeile if zeile.strip() == "" else ""
    eingerueckt = "\n".join((einzug + z) if z else z for z in text.split("\n"))

    neu = f"{vorher}{anfang}\n{eingerueckt}\n{einzug}{ende}{nachher}"
    if neu != html:
        pfad.write_text(neu, encoding="utf-8")
        print(f"{seite}: {name} aktualisiert")
    else:
        print(f"{seite}: {name} unveraendert")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        fehler("Aufruf: python3 einbauen.py <seite.html> <impressum|datenschutz>")
    einsetzen(sys.argv[1], sys.argv[2])
