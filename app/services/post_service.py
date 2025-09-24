import json
from datetime import datetime
from app.db.models.post import Post, PostStatus
from app.repositories import audit_repo

def apply_patch(db, post: Post, payload:dict, actor_id: int):
    before = json.dumps({
        "title":post.title,
        "body": post.body,
        "status": post.status.value if hasattr(post.status, "value") else str(post.status)
    })

    status_changed_to_publsihed =("status" in payload and payload["status"] == PostStatus.published)
    for k,v in payload.items():
        setattr(post, k,v)
    if status_changed_to_publsihed and not post.published_at:
        post.published_at = datetime.utcnow()
    
    db.commit(); db.refresh(post)
    after = json.dumps({
        "title": post.title,
        "body": post.body,
        "status": post.status.value if hasattr(post.status, "value") else str(post.status)

    })

    audit_repo.append(db, actor_id=actor_id, action="post.update", entity="Post",
                      entity_id=post.id, before=before, after=after)
    return post