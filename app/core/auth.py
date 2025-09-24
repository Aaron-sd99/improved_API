from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.user import User
from app.db.models.user_role import UserRole, RoleEnum
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Could not validate credentials",
                             headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise cred_exc
    except Exception:
        raise cred_exc
    user = db.query(User).filter(User.id == int(sub)).first()
    if not user:
        raise cred_exc
    return user

def get_current_org_id(x_org_id: int | None = Header(default=None)) -> int:
    if not x_org_id:
        raise HTTPException(status_code=400, detail="X-Org-ID requerido")
    return x_org_id

def require_role(*roles: RoleEnum):
    def _dep(db: Session = Depends(get_db),
             user: User = Depends(get_current_user),
             org_id: int = Depends(get_current_org_id)):
        r = db.query(UserRole).filter(UserRole.user_id == user.id, UserRole.organization_id == org_id).first()
        if not r or (roles and r.role not in roles):
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return (db, user, org_id, r)
    return _dep
