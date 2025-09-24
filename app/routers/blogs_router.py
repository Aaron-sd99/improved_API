from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import require_role
from app.db.models.user_role import RoleEnum
from app.repositories import blog_repo
from app.schemas.blog import BlogCreate, BlogOut

router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.post("", response_model=BlogOut)
def create_blog(payload: BlogCreate, deps=Depends(require_role(RoleEnum.admin))):
    db, user, org_id, _=deps
    return blog_repo.create(db, name=payload.name, org_id=org_id)


@router.get("", response_model= list[BlogOut])
def list_blogs(q:str |None = None, deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, _ = deps
    return blog_repo.list_in_org(db, org_id, q)

@router.get("/{blog_id}", response_model=BlogOut)
def get_blog(blog_id: int, deps=Depends(require_role(RoleEnum.client, RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, _ = deps
    b = blog_repo.get_in_org(db, blog_id, org_id)
    if not b:
        raise HTTPException(status_code=404, detail="Blog no encontrado")
    return b

