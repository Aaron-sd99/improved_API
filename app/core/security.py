from datetime import datetime, timedelta, timezone
from jose import jwt 
from passlib.context import CryptContext
from app.core.config import settings

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated ="auto")

def hash_password(p:str) -> str:
    return pwd_cxt.hash(p)

def verify_password(plain: str, hashed: str)-> bool:
    return pwd_cxt.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int | None=None ) -> str:
    to_encode= data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.JWT_EXPIRES_MIN) 
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict: 
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])

