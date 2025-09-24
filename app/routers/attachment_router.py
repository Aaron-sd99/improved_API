import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from app.core.auth import require_role
from app.db.models.user_role import RoleEnum
from app.repositories import post_repo, attachment_repo
from app.services.attachment_service import validate_file, build_storage_path

router = APIRouter(prefix="/posts/{post_id}/attachments", tags=["attachments"])

@router.post("")
async def upload_attachment(post_id: int, file: UploadFile = File(...),
                            deps=Depends(require_role(RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    content = await file.read()
    validate_file(file.filename, file.content_type, len(content))
    path = build_storage_path(org_id, p.blog_space_id, post_id, file.filename)
    with open(path, "wb") as f:
        f.write(content)
    meta = attachment_repo.create_meta(db, post_id=post_id, filename=file.filename,
                                       mime=file.content_type, size=len(content), storage_path=path)
    return {"id": meta.id, "filename": meta.filename, "size": meta.size, "mime": meta.mime}

@router.get("")
def list_attachments(post_id: int, deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return attachment_repo.list_for_post(db, post_id)

@router.get("/download/{attachment_id}")
def download_attachment(post_id: int, attachment_id: int,
                        deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p: raise HTTPException(status_code=404, detail="Post no encontrado")
    att = attachment_repo.get_by_id_for_posts(db, attachment_id, [p.id])
    if not att: raise HTTPException(status_code=404, detail="Adjunto no encontrado")
    if not os.path.exists(att.storage_path):
        raise HTTPException(status_code=410, detail="Archivo no disponible")
    return FileResponse(att.storage_path, media_type=att.mime, filename=att.filename)
