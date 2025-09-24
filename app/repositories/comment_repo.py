from sqlalchemy.orm import Session
from app.db.models.comment import Comment

def create(db:Session, post_id: int, author_id:int, body: str) -> Comment:
    c = Comment(post_id= post_id, author_id= author_id, body=body)
    db.add(c); db.commit(); db.refresh(c)
    return c

def list_for_post(db:Session, post_id:int) -> list[Comment]:
    return db.query(Comment).filter(Comment.post_id ==post_id).order_by(Comment.id.desc()).all()

