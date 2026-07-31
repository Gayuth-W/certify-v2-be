import io

import httpx
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas


def _to_pdf_color(value: str | None):
    if not value:
        return colors.white

    try:
        return colors.HexColor(value)
    except Exception:
        return colors.white


def generate_certificate_pdf_bytes(
    template_url: str,
    recipient_name: str,
    name_x_pos: float,
    name_y_pos: float,
    font_size: float,
    font_color: str | None,
) -> bytes:
    response = httpx.get(template_url, timeout=30)
    response.raise_for_status()

    reader = PdfReader(io.BytesIO(response.content))
    writer = PdfWriter()

    first_page = reader.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)

    packet = io.BytesIO()
    canvas_obj = canvas.Canvas(packet, pagesize=(page_width, page_height))
    canvas_obj.setFont("Helvetica", font_size)
    canvas_obj.setFillColor(_to_pdf_color(font_color))
    canvas_obj.drawCentredString(name_x_pos, name_y_pos, recipient_name)
    canvas_obj.save()
    packet.seek(0)

    overlay = PdfReader(packet)
    first_page.merge_page(overlay.pages[0])
    writer.add_page(first_page)

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
