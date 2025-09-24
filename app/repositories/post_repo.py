from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.post import Post, PostStatus
from app.db.models.blog_space import BlogSpace

def create(db: Session, title: str, body: str, blog_space_id: int, author_id: int, status: PostStatus) -> Post:
    p = Post(title=title, body=body, blog_space_id=blog_space_id, author_id=author_id, status=status)
    if status == PostStatus.published:
        from datetime import datetime
        p.published_at = datetime.utcnow()
    db.add(p); db.commit(); db.refresh(p)
    return p

def list_in_org(db: Session, org_id: int, role: str, author_id: int | None,
                blog_space_id: int | None, status: PostStatus | None) -> list[Post]:
    q = (db.query(Post)
         .join(BlogSpace, BlogSpace.id == Post.blog_space_id)
         .filter(BlogSpace.organization_id == org_id))
    if role == "client":
        q = q.filter(Post.status == PostStatus.published)
    if blog_space_id:
        q = q.filter(Post.blog_space_id == blog_space_id)
    if status:
        q = q.filter(Post.status == status)
    return q.order_by(Post.id.desc()).all()



def get_in_org(db:Session, post_id: int, org_id: int) -> Post | None:
    return (db.query(Post)
            .join(BlogSpace, BlogSpace.id==Post.blog_space_id)
            .filter(Post.id==post_id, BlogSpace.organization_id ==org_id)
            .first())

def update_fields(db: Session, post: Post, data: dict) -> Post:
    for k,v in data.items():
        setattr(post, k,v)
    db.commit(); db.refresh(post)
    return post

