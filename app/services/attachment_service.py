import os
from fastapi import HTTPException
from app.core.config import settings

def validate_file(filename: str, mime:  str, size: int):
    allowed = set(settings.ALLOWED_MIME.split(","))
    if mime not in allowed:
        raise HTTPException(status_code=400, detail="MIME no permitido")
    if size > settings.MAX_ATTACHMENT_MB *1024*1024:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande")

def build_storage_path(org_id: int, blog_space_id : int, post_id :int, filename: str) -> str:
    base = os.path.join(settings.UPLOAD_DIR, str(org_id), f"blog_{blog_space_id}", f"post_{post_id}")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)
