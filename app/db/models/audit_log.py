from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base 

class AuditLog(Base):
    __tablename__="audit_log"
    id = Column(Integer, primary_key=True, index=True )
    actor_id=Column(Integer, nullable=False)
    action=Column(String)
    entity=Column(String)
    entity_id= Column(Integer)
    before=Column(String, nullable=True)
    after=Column(String, nullable=True)
    at =Column(DateTime, default=datetime.utcnow)
    