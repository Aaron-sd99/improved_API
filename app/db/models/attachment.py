from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base

class Attachment(Base):
    __tablename__="attachments"
    id = Column(Integer, primary_key=True, index=True)
    post_id= Column(Integer, ForeignKey("posts.id"))
    filename= Column(String)
    mime = Column(String)
    size = Column(Integer)
    storage_path = Column(String)
    created_at =Column(DateTime, default=datetime.utcnow)