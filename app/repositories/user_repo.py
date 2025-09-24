from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.user import User
from app.core.security import hash_password

def create(db: Session, name: str, email:str, password: str) -> User:
    if db.query(User).filter(User.email ==email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado" )
    u = User(name=name, email=email, password=hash_password(password))
    db.add(u); db.commit(); db.refresh(u)
    return u

def get_by_email(db:Session, email: str) -> User | None:
    return db.query(User).filter(User.email ==email).first()
