from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.security import decode_token
bearer=HTTPBearer(auto_error=False)
def current_user(c:HTTPAuthorizationCredentials|None=Depends(bearer),db:Session=Depends(get_db)):
    if not c: raise HTTPException(401,'Autenticação necessária.')
    uid=decode_token(c.credentials)
    if not uid: raise HTTPException(401,'Token inválido ou expirado.')
    u=db.scalar(select(User).where(User.id==int(uid),User.is_active.is_(True)))
    if not u: raise HTTPException(401,'Usuário não encontrado.')
    return u
def require_roles(*roles):
    def dep(u:User=Depends(current_user)):
        if u.role not in roles: raise HTTPException(403,'Acesso não autorizado.')
        return u
    return dep
