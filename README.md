# Rechtstexte der Integra-Websites

Impressum und Datenschutzerklärung für www.2im.de, www.eproc.de und
www.suppliervision.de. Hier wird jeder Text genau einmal gepflegt. Jede
Website zeigt ihn in ihrem eigenen Design.

    impressum.html     Impressum, nur der Inhalt (ohne Kopf und Fußzeile)
    datenschutz.html   Datenschutzerklärung, gilt für alle drei Websites
    einbauen.py        setzt einen Text in eine Seite ein und prüft ihn

Das Repository ist bewusst öffentlich: Die Texte stehen ohnehin auf den
Websites, und der Deploy braucht so keinen Zugangsschlüssel. Deshalb
gehören hier **keine internen Notizen** hinein, auch nicht als
HTML-Kommentar. Interne Hintergründe stehen in den privaten
Website-Repositories.

## So kommt ein Text auf die Websites

Jede Rechtsseite enthält zwei Markierungen:

    <!-- RECHTSTEXT:datenschutz:ANFANG -->
    <!-- RECHTSTEXT:datenschutz:ENDE -->

Beim Deploy holt jede Website dieses Repository und ruft

    python3 einbauen.py <seite.html> datenschutz

auf. Alles zwischen den Markierungen wird durch den aktuellen Text
ersetzt. Schlägt die Prüfung fehl, bricht der Deploy ab und die Website
behält den bisherigen Stand.

## Einen Text ändern

1. `impressum.html` oder `datenschutz.html` ändern, das Datum unter
   „Stand“ anpassen, committen und pushen.
2. Die Deploys der drei Websites neu starten, damit der Text überall
   ankommt:

       gh workflow run deploy.yml --repo integrahh/2im-homepage
       gh workflow run deploy.yml --repo integrahh/eproc-homepage
       gh workflow run deploy.yml --repo integrahh/suppliervision-homepage

## Regeln für die Texte

- Erlaubt sind nur einfache Textelemente: `h2`, `h3`, `p`, `strong`,
  `em`, `a`, `address`, `hr`. Skripte, Frames, Formulare, `style`-Attribute
  und Event-Attribute lehnt `einbauen.py` ab.
- Abschnitte der Datenschutzerklärung sind durchnummeriert
  (`<h2>1. …</h2>`). Wer einen Abschnitt einfügt oder entfernt, muss alle
  Verweise „Abschnitt N“ anpassen. `einbauen.py` prüft, dass jeder
  Verweis auf einen vorhandenen Abschnitt zeigt.
- Die Anker `#hubspot-analyse` und `#postmailing` werden von außen
  verlinkt (unter anderem www.eproc.de/rechnung/) und bleiben erhalten.
- Was nur eine Website betrifft, wird im Text ausdrücklich so benannt,
  zum Beispiel „(nur www.eproc.de)“.
