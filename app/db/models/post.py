from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime
from app.db.base import Base

class PostStatus(str, PyEnum):
    draft = "draft"
    published="published"
    archived="archived"

class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body=Column(String)
    status = Column(Enum(PostStatus), default=PostStatus.draft)
    blog_space_id=  Column(Integer, ForeignKey("blog_spaces.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    blog_space= relationship("BlogSpace")


