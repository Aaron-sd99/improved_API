from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.auth import require_role
from app.db.models.user_role import RoleEnum
from app.db.models.post import PostStatus
from app.repositories import post_repo, blog_repo
from app.schemas.post import PostCreate, PostUpdate, PostOut
from app.utils.csv_export import to_csv_response

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostOut)
def create_post(payload: PostCreate, deps=Depends(require_role(RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, role = deps
    blog = blog_repo.get_in_org(db, payload.blog_space_id, org_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog no pertenece a tu organización")
    p = post_repo.create(db, title=payload.title, body=payload.body,
                         blog_space_id=payload.blog_space_id, author_id=user.id, status=payload.status)
    return p

@router.get("", response_model=list[PostOut])
def list_posts(
    blog_space_id: int | None = None,
    status: PostStatus | None = None,
    deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))
):
    db, user, org_id, r = deps
    return post_repo.list_in_org(db, org_id, r.role.value, author_id=user.id,
                                 blog_space_id=blog_space_id, status=status)

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    # client ve sólo published
    if r.role.value == "client" and p.status != PostStatus.published:
        raise HTTPException(status_code=403, detail="No autorizado")
    return p

@router.patch("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate, deps=Depends(require_role(RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    p = post_repo.get_in_org(db, post_id, org_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    from app.services.post_service import apply_patch
    return apply_patch(db, p, payload.model_dump(exclude_none=True), actor_id=user.id)

@router.get("/export.csv")
def export_posts(
    blog_space_id: int | None = None,
    status: PostStatus | None = None,
    deps=Depends(require_role(RoleEnum.author, RoleEnum.admin))
):
    db, user, org_id, r = deps
    items = post_repo.list_in_org(db, org_id, r.role.value, author_id=user.id,
                                  blog_space_id=blog_space_id, status=status)
    rows = [{
        "id": i.id, "title": i.title, "status": i.status.value if hasattr(i.status, "value") else str(i.status),
        "blog_space_id": i.blog_space_id, "author_id": i.author_id, "published_at": (i.published_at or ""),
        "created_at": i.created_at
    } for i in items]
    return to_csv_response(rows, filename="posts.csv")
