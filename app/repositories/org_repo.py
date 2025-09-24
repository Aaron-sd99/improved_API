from sqlalchemy.orm import Session
from app.db.models.organization import Organization
from app.db.models.user_role import UserRole, RoleEnum

def create(db: Session, name: str, billing_email: str | None, locale: str, timezone: str) -> Organization:
    org = Organization(name=name, billing_email=billing_email, locale=locale, timezone=timezone)
    db.add(org); db.commit(); db.refresh(org)
    return org


def get(db: Session, org_id: int) -> Organization | None:
    return db.query(Organization).filter(Organization.id == org_id).first()

def list_all(db:Session, q:str | None= None) -> list[Organization]:
    qy= db.query(Organization)
    if q: qy= qy.filter(Organization.name.ilike(f"%{q}%"))
    return qy.order_by(Organization.name).all()

def add_user_role(db:Session, user_id:int, org_id: int, role:RoleEnum) -> UserRole:
    r = db.query(UserRole).filter(UserRole.user_id==user_id, UserRole.organization_id==org_id).first()
    if r: r.role=role
    else:
        r = UserRole(user_id=user_id, organization_id= org_id, role=role)
        db.add(r)
    db.commit(); db.refresh(r)
    return r

def list_user_roles(db: Session, org_id: int) -> list[UserRole]:
    return db.query(UserRole).filter(UserRole.organization_id == org_id).all()
