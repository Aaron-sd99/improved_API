from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.db.base import Base

class RoleEnum(str, PyEnum):
    admin="admin"
    author="author"
    client="client"

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    role = Column(Enum(RoleEnum), nullable=False)

    user = relationship("User")
    organization = relationship("Organization")

    