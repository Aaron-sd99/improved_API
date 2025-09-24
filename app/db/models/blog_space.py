from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class BlogSpace(Base):
    __tablename__ ="blog_spaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    organization_id =Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization")

