from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Organization(Base):
    __tablename__="organizations"
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, unique=True, index=True)
    billing_email= Column(String, nullable=True)
    locale =Column(String, default="es")
    timezone = Column(String, default="UTC")

    