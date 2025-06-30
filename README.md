# bilderkombi

Ein Python-Tool zum Erstellen von PDF-Dokumenten aus Bildern mit farbigen Rahmen und optionalen Kommentaren.

## Features

- Kombiniert mehrere Bilder zu einem PDF-Dokument
- Fügt farbige Rahmen zu Bildern hinzu (Standard: rot, 10px)
- Unterstützt mehrzeilige Kommentare für jedes Bild
- Wählbare Seitenausrichtung (Hochformat/Querformat)
- Anpassbarer PDF-Titel
- Automatischer Zeitstempel auf der Titelseite
- Generiert Beispiel-Kommentardateien

## Installation

### Mit uvx (empfohlen)

```bash
# Direkt ausführen ohne Installation
uvx --from git+https://github.com/IHR_GITHUB/bilderkombi bilderkombi -i bild1.jpg bild2.jpg -o ausgabe.pdf
```

### Manuelle Installation

```bash
# Repository klonen
git clone https://github.com/IHR_GITHUB/bilderkombi.git
cd bilderkombi

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## Verwendung

### Grundlegende Verwendung

```bash
# Einfache PDF-Erstellung
python bilderkombi.py -i bild1.jpg bild2.png bild3.jpg -o meine_bilder.pdf

# Mit Kommentaren
python bilderkombi.py -i bild1.jpg bild2.jpg -o ausgabe.pdf -c kommentare.txt

# Mit benutzerdefiniertem Titel
python bilderkombi.py -i bild1.jpg bild2.jpg -o ausgabe.pdf --title "Urlaubsfotos 2024"

# Im Querformat
python bilderkombi.py -i bild1.jpg bild2.jpg -o ausgabe.pdf --orientation landscape

# Beispiel-Kommentardatei generieren
python bilderkombi.py -i bild1.jpg bild2.jpg -o ausgabe.pdf --generate-example-comments
```

### Kommandozeilenoptionen

| Option | Kurz | Beschreibung | Erforderlich |
|--------|------|--------------|--------------|
| `--input` | `-i` | Liste der Eingabebilder | ✓ |
| `--output` | `-o` | Name der Ausgabe-PDF | ✓ |
| `--comments` | `-c` | Pfad zur Kommentardatei | ✗ |
| `--title` | `-t` | Titel für die PDF (Standard: "Bilder-PDF") | ✗ |
| `--orientation` | | Seitenausrichtung: portrait oder landscape | ✗ |
| `--generate-example-comments` | | Generiert Beispiel-Kommentardatei | ✗ |

## Kommentarformat

Erstellen Sie eine Textdatei mit folgendem Format:

```
# Kommentare beginnen mit # und werden ignoriert
1: Kommentar für das erste Bild
1: Zweite Zeile für das erste Bild
2: Kommentar für das zweite Bild
3: Dieser Kommentar gehört zum dritten Bild
```

- Format: `<Bildnummer>: <Kommentartext>`
- Bildnummern beginnen bei 1
- Mehrere Zeilen pro Bild werden zusammengefügt
- Leerzeilen und Zeilen mit # werden ignoriert

## PDF-Ausgabe

Die generierte PDF enthält:

1. **Titelseite**: Mit Titel und Erstellungszeitpunkt
2. **Bildseiten**: Ein Bild pro Seite mit:
   - Zentriertem Bild mit farbigem Rahmen
   - Bildnummer unterhalb des Bildes
   - Optionale Kommentare am Seitenende

## Beispiele

### Einfaches Fotoalbum

```bash
# Bilder sammeln
python bilderkombi.py -i foto1.jpg foto2.jpg foto3.jpg -o fotoalbum.pdf --title "Familienurlaub 2024"
```

### Dokumentation mit Beschreibungen

```bash
# Beispiel-Kommentare generieren und anpassen
python bilderkombi.py -i screenshot1.png screenshot2.png -o doku.pdf --generate-example-comments

# Kommentare bearbeiten
nano comments_example.txt

# PDF mit angepassten Kommentaren erstellen
python bilderkombi.py -i screenshot1.png screenshot2.png -o doku.pdf -c comments_example.txt
```

### Präsentation im Querformat

```bash
python bilderkombi.py -i slide1.png slide2.png slide3.png -o praesentation.pdf \
    --orientation landscape --title "Projektpräsentation"
```

## Systemanforderungen

- Python 3.6+
- Pillow (PIL) für Bildverarbeitung
- ReportLab für PDF-Generierung

## Fehlerbehandlung

Das Tool behandelt folgende Fehler:

- **Fehlende Bilddateien**: Programm bricht mit Fehlermeldung ab
- **Ungültiges Bildformat**: Bild wird übersprungen
- **Fehlende Kommentardatei**: Programm bricht ab
- **Ungültiges Kommentarformat**: Zeile wird mit Warnung übersprungen
- **Bildnummer außerhalb des Bereichs**: Kommentar wird ignoriert

## Entwicklung

### Projekt-Setup

```bash
# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# oder
.venv\Scripts\activate  # Windows

# Entwicklungsabhängigkeiten installieren
pip install -r requirements.txt
```

### Tests ausführen

```bash
# Testbilder erstellen
python -c "from PIL import Image; Image.new('RGB', (200, 300), 'blue').save('test1.jpg')"
python -c "from PIL import Image; Image.new('RGB', (300, 200), 'green').save('test2.jpg')"

# Funktionalität testen
python bilderkombi.py -i test1.jpg test2.jpg -o test.pdf
```

## Lizenz

WTFPL - Do What The F*ck You Want To Public License

## "Autor"

Jan Vanvinkenroye, jan@vanvinkenroye.de

## Beiträge

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue.
