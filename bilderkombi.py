import sys
import argparse
from collections import defaultdict
from datetime import datetime
import os

from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader

def add_border(img_path, border_color=(255, 0, 0), border_width=10):
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"Fehler: Konnte Bild nicht öffnen: {img_path} – {e}")
        return None

    new_size = (img.width + 2 * border_width, img.height + 2 * border_width)
    new_img = Image.new("RGB", new_size, border_color)
    new_img.paste(img, (border_width, border_width))
    return new_img

def read_comments(comments_file, num_images):
    comments = defaultdict(list)
    if not comments_file:
        return [""] * num_images

    if not os.path.exists(comments_file):
        print(f"Kommentar-Datei nicht gefunden: {comments_file}")
        sys.exit(1)

    with open(comments_file, encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                print(f"Zeile {line_num}: Kein Doppelpunkt – überspringe → {line}")
                continue
            try:
                idx, text = line.split(":", 1)
                idx = int(idx.strip())
                if idx < 1 or idx > num_images:
                    print(f"Zeile {line_num}: Bildindex {idx} außerhalb gültiger Bereich (1–{num_images}) – überspringe")
                    continue
                comments[idx].append(text.strip())
            except Exception as e:
                print(f"Zeile {line_num}: Fehler beim Parsen – {e}")

    final_comments = []
    for i in range(1, num_images + 1):
        joined = "\n".join(comments[i]) if i in comments else ""
        final_comments.append(joined)

    return final_comments

def create_pdf(image_paths, output_pdf, comments, title="Bilder-PDF", orientation="portrait"):
    if orientation == "landscape":
        pagesize = landscape(A4)
    else:
        pagesize = A4
    
    c = canvas.Canvas(output_pdf, pagesize=pagesize)
    width, height = pagesize

    # Titelseite mit Timestamp
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, title)
    c.setFont("Helvetica", 12)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawCentredString(width / 2, height - 130, f"Erstellt am: {timestamp}")
    c.showPage()

    for idx, (img_path, comment) in enumerate(zip(image_paths, comments), 1):
        img_with_border = add_border(img_path)
        if img_with_border is None:
            continue

        max_width = width * 0.8
        max_height = height * 0.8

        ratio = min(max_width / img_with_border.width, max_height / img_with_border.height)
        new_size = (int(img_with_border.width * ratio), int(img_with_border.height * ratio))

        resized_img = img_with_border.resize(new_size, Image.Resampling.LANCZOS)
        img_reader = ImageReader(resized_img)

        x = (width - new_size[0]) / 2
        y = (height - new_size[1]) / 2

        c.drawImage(img_reader, x, y, width=new_size[0], height=new_size[1])

        # Zahl unter dem Bild
        number_text = str(idx)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, y - 30, number_text)

        # Mehrzeiliger Kommentar
        if comment:
            c.setFont("Helvetica", 12)
            lines = comment.split("\n")
            line_height = 15
            start_y = 50

            for i, line in enumerate(lines):
                c.drawCentredString(width / 2, start_y + i * line_height, line)

        c.showPage()

    try:
        c.save()
    except Exception as e:
        print(f"Fehler beim Speichern der PDF: {e}")
        sys.exit(1)

    print(f"PDF gespeichert unter: {output_pdf}")

def generate_example_comments(num_images, output_file="comments_example.txt"):
    """Generiert eine Beispiel-Kommentardatei"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Beispiel-Kommentardatei für bilderkombi.py\n")
        f.write("# Format: <Bildnummer>: <Kommentartext>\n")
        f.write("# Mehrere Zeilen pro Bild sind möglich\n\n")
        
        for i in range(1, min(num_images + 1, 4)):  # Max 3 Beispiele
            f.write(f"{i}: Dies ist ein Beispielkommentar für Bild {i}\n")
            if i == 1:
                f.write(f"{i}: Hier ist eine zweite Zeile für Bild {i}\n")
        
        if num_images > 3:
            f.write(f"\n# Fügen Sie weitere Kommentare für Bilder 4-{num_images} hinzu...\n")
    
    print(f"Beispiel-Kommentardatei erstellt: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(
        description="Erstelle ein DIN A4 PDF mit Bildern, Rahmen, Nummern, Kommentaren und Timestamp auf der Titelseite."
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Name der Ausgabedatei, z.B. output.pdf"
    )
    parser.add_argument(
        "--input", "-i",
        nargs='+',
        required=True,
        help="Liste der Eingabebilder"
    )
    parser.add_argument(
        "--comments", "-c",
        help="Optional: Textdatei mit Kommentaren im Format '1: Kommentar'"
    )
    parser.add_argument(
        "--title", "-t",
        default="Bilder-PDF",
        help="Titel für die PDF (Standard: Bilder-PDF)"
    )
    parser.add_argument(
        "--orientation",
        choices=["portrait", "landscape"],
        default="portrait",
        help="Seitenausrichtung: portrait oder landscape (Standard: portrait)"
    )
    parser.add_argument(
        "--generate-example-comments",
        action="store_true",
        help="Generiert eine Beispiel-Kommentardatei basierend auf der Anzahl der Eingabebilder"
    )

    args = parser.parse_args()

    for img in args.input:
        if not os.path.exists(img):
            print(f"Bilddatei nicht gefunden: {img}")
            sys.exit(1)

    if args.generate_example_comments:
        example_file = generate_example_comments(len(args.input))
        if not args.comments:
            args.comments = example_file
            print(f"Verwende generierte Kommentardatei: {example_file}")

    comments = read_comments(args.comments, len(args.input))
    create_pdf(args.input, args.output, comments, args.title, args.orientation)

if __name__ == "__main__":
    main()