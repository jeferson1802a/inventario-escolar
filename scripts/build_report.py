"""Convierte el informe Markdown en Word; requiere python-docx.

Herramienta opcional de documentación, no necesaria para ejecutar Streamlit.
"""
from pathlib import Path
import re

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def clean(text):
    return text.replace("`", "").replace("**", "")


def main():
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21)
    sec.top_margin, sec.bottom_margin = Cm(1.7), Cm(1.7)
    sec.left_margin = sec.right_margin = Cm(2)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08
    for name, size in [("Title", 21), ("Heading 1", 12), ("Heading 2", 11)]:
        style = doc.styles[name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(9)
        style.paragraph_format.space_after = Pt(5)
    doc.core_properties.title = "Aplicación web de inventario escolar con MongoDB Atlas"
    doc.core_properties.author = ""
    doc.core_properties.subject = "Informe académico editable de diseño desarrollo y verificación"
    for line in (ROOT / "docs/INFORME.md").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        if line == "<!-- pagebreak -->":
            doc.add_page_break()
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line)
            if not match:
                raise ValueError("Referencia de imagen inválida")
            image_path = ROOT / "docs" / match[2]
            with Image.open(image_path) as screenshot:
                width_px, height_px = screenshot.size
            width_cm = min(16.7, 9.7 * width_px / height_px)
            image_paragraph = doc.add_paragraph()
            image_paragraph.alignment = 1
            picture = image_paragraph.add_run().add_picture(str(image_path), width=Cm(width_cm))
            picture._inline.docPr.set("descr", match[1])
        elif line.startswith("# "):
            doc.add_paragraph(clean(line[2:]), "Title")
        elif line.startswith("## "):
            doc.add_paragraph(clean(line[3:]), "Heading 1")
        elif line.startswith("- "):
            p = doc.add_paragraph(clean(line[2:]), "List Bullet")
            p.paragraph_format.space_after = Pt(5)
            if "https://" in line:
                for run in p.runs:
                    run.font.size = Pt(8)
        else:
            p = doc.add_paragraph(clean(line))
            if line.startswith("Figura "):
                p.paragraph_format.keep_with_next = True
                p.paragraph_format.space_before = Pt(7)
                p.paragraph_format.space_after = Pt(4)
                for run in p.runs:
                    run.font.size = Pt(9)
    footer = sec.footer.paragraphs[0]
    footer.alignment = 2
    footer.add_run("Inventario Escolar  |  ").font.size = Pt(9)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    # Algunas plantillas de Word traen una línea en el estilo Title.
    # Se elimina tanto del documento como de los estilos heredados.
    for root in (doc._element, doc.styles.element):
        for border in list(root.xpath(".//w:pBdr")):
            border.getparent().remove(border)
    output = ROOT / "docs/Informe_Inventario_Escolar.docx"
    doc.save(output)
    print(output)


if __name__ == "__main__":
    main()
