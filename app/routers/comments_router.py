from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_role
from app.db.models.user_role import RoleEnum
from app.repositories import post_repo, comment_repo
from app.schemas.comment import CommentCreate, CommentOut
from app.db.models.post import PostStatus

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@router.post("", response_model=CommentOut)
def add_comment(post_id: int, payload: CommentCreate,
                deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    # clients sólo comentan en publicados (regla simple para MVP)
    if r.role.value == "client" and p.status != PostStatus.published:
        raise HTTPException(status_code=403, detail="No autorizado")
    return comment_repo.create(db, post_id=post_id, author_id=user.id, body=payload.body)

@router.get("", response_model=list[CommentOut])
def list_comments(post_id: int, deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if r.role.value == "client" and p.status != PostStatus.published:
        raise HTTPException(status_code=403, detail="No autorizado")
    return comment_repo.list_for_post(db, post_id)
