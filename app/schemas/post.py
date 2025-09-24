from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.common import PostStatus

class PostCreate(BaseModel):
    title: str
    body: str
    blog_space_id: int
    status: PostStatus= PostStatus.draft

class PostUpdate(BaseModel):
    title: Optional[str]=None
    body: Optional[str]=None
    status: Optional[PostStatus] = None

class PostOut(BaseModel):
    id: int
    title: str
    body: str
    status: PostStatus
    blog_space_id : int
    author_id : int
    published_at : Optional[datetime]=None
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)
    