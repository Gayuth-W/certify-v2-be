from fastapi import APIRouter, HTTPException, Response

from services.certificate_pdf import generate_certificate_pdf_bytes
from services.database import get_certificate_by_certificate_id, get_template_by_id

router = APIRouter(
    prefix="/certificate",
    tags=["certificate"],
)


@router.get(
    "/{certificate_id}/preview",
    responses={400: {"description": "Certificate preview generation failed"}},
)
def preview_certificate(certificate_id: str):
    try:
        certificate = get_certificate_by_certificate_id(certificate_id)
        template = get_template_by_id(certificate["template_id"])

        if not template.get("url"):
            raise ValueError("Template URL is missing")

        pdf_bytes = generate_certificate_pdf_bytes(
            template_url=template["url"],
            recipient_name=certificate["recipient_name"],
            name_x_pos=float(template.get("name_x_pos") or 720),
            name_y_pos=float(template.get("name_y_pos") or 360),
            font_size=float(template.get("font_size") or 55),
            font_color=template.get("font_color"),
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="certificate-{certificate_id}.pdf"'
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
