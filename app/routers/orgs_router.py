from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.auth import get_current_user, require_role, get_current_org_id
from app.db.models.user_role import RoleEnum
from app.repositories import org_repo
from app.schemas.organization import OrganizationCreate, OrganizationOut, OrgUserAssign
from app.schemas.user import UserRoleOut

router = APIRouter(prefix="/orgs", tags=["orgs"])

@router.post("", response_model=OrganizationOut)
def create_org(payload: OrganizationCreate, db:Session= Depends(get_db), user=Depends(get_current_user)):
    return org_repo.create(db, payload.name, payload.billing_email, payload.locale, payload.timezone)

@router.get("", response_model=list[OrganizationOut])
def list_orgs(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return org_repo.list_all(db)

@router.get("/{org_id}", response_model=OrganizationOut)
def get_org(org_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return org_repo.get(db, org_id)

@router.post("/{org_id}/users", response_model=UserRoleOut)
def assign_user(org_id: int, payload: OrgUserAssign, db: Session = Depends(get_db),
                user=Depends(get_current_user), x_org_id=Depends(get_current_org_id)):
    assert org_id == x_org_id, "org_id debe igualar X-Org-ID"
    return org_repo.add_user_role(db, user_id=payload.user_id, org_id=org_id, role=RoleEnum(payload.role))

@router.get("/{org_id}/users", response_model=list[UserRoleOut])
def list_org_users(org_id: int, deps=Depends(require_role(RoleEnum.admin))):
    db, user, org_id_dep, _ = deps
    return org_repo.list_user_roles(db, org_id_dep)
