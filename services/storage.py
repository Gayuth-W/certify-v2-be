from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from config import SUPABASE_BUCKET
from services.supabase_client import get_supabase_client


async def upload_template(file: UploadFile) -> dict:
    client = get_supabase_client()
    storage = client.storage.from_(SUPABASE_BUCKET)

    file_bytes = await file.read()
    suffix = Path(file.filename or "template").suffix
    file_path = f"{uuid4().hex}{suffix}"

    storage.upload(
        file_path,
        file_bytes,
        file_options={"content-type": file.content_type or "application/octet-stream"},
    )

    public_url = storage.get_public_url(file_path)

    return {
        "file_path": file_path,
        "public_url": public_url,
        "filename": file.filename,
    }