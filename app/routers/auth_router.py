from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from app.core.security import verify_password, create_access_token
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    user =db.query(User).filter(User.email==form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token= create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token= token)

