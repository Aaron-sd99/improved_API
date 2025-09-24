from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentCreate(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    body: str
    created_at : datetime
    model_config=ConfigDict(from_attributes=True)