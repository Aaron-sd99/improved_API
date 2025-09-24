from sqlalchemy.orm import Session
from app.db.models.attachment import Attachment

def create_meta(db: Session, post_id: int, filename: str, mime: str, size:int, storage_path:str ) -> Attachment:
    a = Attachment(post_id=post_id, filename=filename, mime=mime, size=size, storage_path=storage_path)
    db.add(a); db.commit(); db.refresh(a)
    return a

def list_for_post(db:Session, post_id: int) -> list[Attachment]:
    return db.query(Attachment).filter(Attachment.post_id==post_id).order_by(Attachment.id.desc()).all()

def get_by_id_for_posts(db: Session, attachment_id: int, allowed_post_ids: list[int]) -> Attachment | None:
    a = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not a or a.post_id not in allowed_post_ids:
        return None
    return a
