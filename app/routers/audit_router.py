from fastapi import APIRouter, Depends
from app.core.auth import require_role
from app.db.models.user_role import RoleEnum
from app.repositories import audit_repo

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/posts/{post_id}")
def post_audit(post_id: int, deps=Depends(require_role(RoleEnum.author, RoleEnum.admin))):
    db, user, org_id, r = deps
    return audit_repo.list_for_entity(db, "Post", post_id)
