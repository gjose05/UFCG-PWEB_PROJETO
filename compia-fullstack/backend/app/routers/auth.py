from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.db import get_db
from app.deps import current_user
from app.models import User
from app.schemas import RegisterIn,LoginIn,TokenOut,UserOut
from app.security import hash_password,verify_password,create_token
r=APIRouter(prefix='/auth',tags=['auth'])
@r.post('/register',response_model=TokenOut)
def register(p:RegisterIn,db:Session=Depends(get_db)):
    email=str(p.email).lower()
    if db.scalar(select(User).where(func.lower(User.email)==email)): raise HTTPException(409,'E-mail já cadastrado.')
    u=User(full_name=p.full_name,email=email,password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u); return {'access_token':create_token(u.id),'user':u}
@r.post('/login',response_model=TokenOut)
def login(p:LoginIn,db:Session=Depends(get_db)):
    u=db.scalar(select(User).where(func.lower(User.email)==str(p.email).lower()))
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,'E-mail ou senha inválidos.')
    return {'access_token':create_token(u.id),'user':u}
@r.get('/me',response_model=UserOut)
def me(u=Depends(current_user)): return u
