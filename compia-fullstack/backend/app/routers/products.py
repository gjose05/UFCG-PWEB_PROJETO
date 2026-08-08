from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,func,or_
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Product
from app.schemas import ProductOut
r=APIRouter(prefix='/products',tags=['products'])
@r.get('',response_model=list[ProductOut])
def list_products(search:str|None=None,category:str|None=None,order:str|None=None,featured:bool=False,db:Session=Depends(get_db)):
    q=select(Product).where(Product.is_active.is_(True))
    if search:
        n=f'%{search.lower()}%'; q=q.where(or_(func.lower(Product.title).like(n),func.lower(Product.author).like(n),func.lower(Product.category).like(n)))
    if category: q=q.where(Product.category==category)
    q=q.order_by(Product.price.desc() if order=='price-desc' else Product.price.asc() if order=='price-asc' else Product.title.asc())
    if featured: q=q.limit(3)
    return db.scalars(q).all()
@r.get('/{pid}',response_model=ProductOut)
def get_product(pid:int,db:Session=Depends(get_db)):
    p=db.scalar(select(Product).where(Product.id==pid,Product.is_active.is_(True)))
    if not p: raise HTTPException(404,'Produto não encontrado.')
    return p
