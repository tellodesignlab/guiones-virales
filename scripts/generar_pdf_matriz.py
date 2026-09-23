#!/usr/bin/env python3
"""
Genera matriz/matriz-contenido-viral.pdf a partir de matriz/matriz-contenido-viral.md.

Uso:
    python3 scripts/generar_pdf_matriz.py

Requiere: pip install -r requirements.txt
"""
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_PATH = REPO_ROOT / "matriz" / "matriz-contenido-viral.md"
OUT_PATH = REPO_ROOT / "matriz" / "matriz-contenido-viral.pdf"

styles = getSampleStyleSheet()
cell_style = ParagraphStyle('cell', parent=styles['Normal'], fontSize=7.5, leading=9.5)
header_cell_style = ParagraphStyle('hcell', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.white, fontName='Helvetica-Bold')
h1_style = ParagraphStyle('h1', parent=styles['Title'], fontSize=18)
h2_style = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=13, spaceBefore=10, spaceAfter=6)
intro_style = ParagraphStyle('intro', parent=styles['Normal'], fontSize=9, leading=12)

# Peso relativo de cada columna. Si tu matriz tiene columnas distintas a las
# de la plantilla (PIEZA, HOOK, TIPO, TEMA, FORMATO, DURACIÓN, EMOCIÓN, CTA,
# RENDIMIENTO, PATRÓN), ajustá esta lista para que sume 1.0.
COLUMN_WEIGHTS = [0.09, 0.16, 0.09, 0.11, 0.10, 0.05, 0.07, 0.09, 0.06, 0.18]


def flush_table(story, headers, rows):
    if not headers or not rows:
        return
    header_row = [Paragraph(h, header_cell_style) for h in headers]
    data = [header_row] + [[Paragraph(c, cell_style) for c in row] for row in rows]
    page_width = landscape(A3)[0] - 20 * mm
    weights = COLUMN_WEIGHTS if len(COLUMN_WEIGHTS) == len(headers) else [1 / len(headers)] * len(headers)
    col_widths = [page_width * w for w in weights]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b2b2b')),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))


def build_story(md_text: str):
    story = [Paragraph("Matriz de Contenido Viral", h1_style), Spacer(1, 6 * mm)]
    headers, rows = None, []
    for line in md_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            flush_table(story, headers, rows)
            headers, rows = None, []
            story.append(Paragraph(stripped[3:], h2_style))
        elif stripped.startswith("# "):
            continue
        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^-+$", c.replace(":", "")) for c in cells):
                continue
            if headers is None:
                headers = cells
            else:
                rows.append(cells)
        else:
            flush_table(story, headers, rows)
            headers, rows = None, []
            if stripped:
                story.append(Paragraph(stripped, intro_style))
                story.append(Spacer(1, 2 * mm))
    flush_table(story, headers, rows)
    return story


def main():
    if not MD_PATH.exists():
        print(f"No se encontró {MD_PATH}. Corré primero el ciclo de análisis ('analiza referentes').")
        sys.exit(1)
    md_text = MD_PATH.read_text(encoding="utf-8")
    story = build_story(md_text)
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=landscape(A3),
        topMargin=12 * mm, bottomMargin=12 * mm,
        leftMargin=10 * mm, rightMargin=10 * mm,
        title="Matriz de Contenido Viral",
    )
    doc.build(story)
    print(f"PDF generado en {OUT_PATH}")


if __name__ == "__main__":
    main()
