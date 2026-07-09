"""
Demo label PDF generation.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_001"
PURPOSE = "Generate a local demo label from a simulated booking"
"""

from modules.location_demo import formatiere_entfernung, formatiere_faktor
from modules.pricing_simulation import euro


def escape_pdf_text(text):
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_demo_label_pdf(booking):
    """
    Erzeugt ein einfaches Demo-PDF ohne externe Bibliotheken.
    Das ist kein echtes Versandlabel, sondern eine sichtbare Simulation des späteren API-Rücklaufs.
    """
    lines = [
        "VERSANDKOSTEN-KOMPASS · DEMO-LABEL",
        "NICHT FÜR DEN ECHTEN VERSAND VERWENDEN",
        "",
        f"Anbieter: {booking['anbieter']}",
        f"Sendungsnummer: {booking['sendungsnummer']}",
        f"Vorgang: {booking['vorgang']}",
        f"Zeit: {booking['zeit']}",
        "",
        f"Empfänger: {booking.get('empfaenger', '-')}",
        f"Versand ab: {booking.get('versandstandort', '-')}",
        f"Ziel: {booking.get('plz', '-')} {booking.get('ort', '-')} · {booking.get('land', '-')}",
        f"Demo-Entfernung: {formatiere_entfernung(booking.get('entfernung_km'))}",
        f"Demo-Distanzfaktor: {formatiere_faktor(booking.get('distanzfaktor', 1.0))}",
        "",
        f"Menge: {booking['menge']} Paket(e)",
        f"Gewicht je Paket: {booking['gewicht']:.2f} kg",
        f"Maße: {booking['masse']}",
        f"Formatklasse: {booking['formatklasse']}",
        f"Simulierter Preis: {euro(booking['preis'])}",
        "",
        "████ ███ █ ████ ██ █ ███ ████",
        "DEMO-CODE · API-ANBINDUNG NOCH NICHT AKTIV",
    ]

    content = ["BT", "/F1 17 Tf", "50 790 Td"]
    first = True
    for line in lines:
        if not first:
            content.append("0 -26 Td")
        first = False
        safe = escape_pdf_text(line)
        content.append(f"({safe}) Tj")
    content.append("ET")
    stream = "\n".join(content)

    objects = []
    objects.append("1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj")
    objects.append("2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj")
    objects.append("3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj")
    objects.append("4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj")
    stream_bytes = stream.encode("latin-1", errors="replace")
    objects.append(f"5 0 obj << /Length {len(stream_bytes)} >> stream\n{stream}\nendstream endobj")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj.encode("latin-1", errors="replace"))
        pdf.extend(b"\n")
    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode("ascii"))
    return bytes(pdf)
