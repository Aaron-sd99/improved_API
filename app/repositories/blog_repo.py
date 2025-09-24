from sqlalchemy.orm import Session
from app.db.models.blog_space import BlogSpace

def create(db:Session, name: str, org_id: int) ->BlogSpace:
    b = BlogSpace(name=name, organization_id = org_id)
    db.add(b); db.commit(); db.refresh(b)
    return b

def get_in_org(db: Session, blog_id: int, org_id: int)  -> BlogSpace | None:
    return db.query(BlogSpace).filter(BlogSpace.id ==blog_id,BlogSpace.organization_id==org_id).first()

def list_in_org(db:Session, org_id: int, q:str |None = None) -> list[BlogSpace]:
    qy= db.query(BlogSpace).filter(BlogSpace.organization_id ==org_id)
    if q:qy = qy.filter(BlogSpace.name.ilike(f"%{q}%"))
    return qy.order_by(BlogSpace.id.desc()).all()


    