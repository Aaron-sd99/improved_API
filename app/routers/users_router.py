from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.auth import get_current_user
from app.repositories import user_repo
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db:Session= Depends(get_db)):
    return user_repo.create(db, name=payload.name, email=payload.email, password=payload.password)

@router.get("/me", response_model=UserOut)
def me(user= Depends(get_current_user)):
    return user