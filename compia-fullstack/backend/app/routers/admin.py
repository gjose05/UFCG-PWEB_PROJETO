from decimal import Decimal
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.db import get_db
from app.deps import require_roles
from app.models import Product,Order,User
from app.schemas import ProductBase,ProductUpdate,ProductOut,OrderOut,StatusIn,StatsOut,UserOut
from app.services.orders import mark_paid
r=APIRouter(prefix='/admin',tags=['admin'])
@r.get('/stats',response_model=StatsOut)
def stats(db:Session=Depends(get_db),_=Depends(require_roles('admin'))):
    return {'products':db.scalar(select(func.count(Product.id))) or 0,'users':db.scalar(select(func.count(User.id))) or 0,'orders':db.scalar(select(func.count(Order.id))) or 0,'paid_orders':db.scalar(select(func.count(Order.id)).where(Order.payment_status=='paid')) or 0,'revenue':db.scalar(select(func.coalesce(func.sum(Order.total),0)).where(Order.payment_status=='paid')) or Decimal('0')}
@r.get('/users',response_model=list[UserOut])
def users(db:Session=Depends(get_db),_=Depends(require_roles('admin'))): return db.scalars(select(User).order_by(User.created_at.desc())).all()
@r.get('/products',response_model=list[ProductOut])
def products(db:Session=Depends(get_db),_=Depends(require_roles('admin','editor'))): return db.scalars(select(Product).order_by(Product.id)).all()
@r.post('/products',response_model=ProductOut)
def create(p:ProductBase,db:Session=Depends(get_db),_=Depends(require_roles('admin','editor'))):
    if db.scalar(select(Product).where(Product.slug==p.slug)): raise HTTPException(409,'Slug já utilizado.')
    x=Product(**p.model_dump()); db.add(x); db.commit(); db.refresh(x); return x
@r.put('/products/{pid}',response_model=ProductOut)
def update(pid:int,p:ProductUpdate,db:Session=Depends(get_db),_=Depends(require_roles('admin','editor'))):
    x=db.get(Product,pid)
    if not x: raise HTTPException(404,'Produto não encontrado.')
    for k,v in p.model_dump(exclude_unset=True).items(): setattr(x,k,v)
    db.commit(); db.refresh(x); return x
@r.delete('/products/{pid}',status_code=204)
def disable(pid:int,db:Session=Depends(get_db),_=Depends(require_roles('admin','editor'))):
    x=db.get(Product,pid)
    if not x: raise HTTPException(404,'Produto não encontrado.')
    x.is_active=False; db.commit()
@r.get('/orders',response_model=list[OrderOut])
def orders(db:Session=Depends(get_db),_=Depends(require_roles('admin','seller'))): return db.scalars(select(Order).order_by(Order.created_at.desc())).unique().all()
@r.patch('/orders/{oid}/status',response_model=OrderOut)
def status(oid:int,p:StatusIn,db:Session=Depends(get_db),_=Depends(require_roles('admin','seller'))):
    if p.status not in {'pending_payment','paid','preparing','shipped','completed','cancelled'}: raise HTTPException(422,'Status inválido.')
    o=db.get(Order,oid)
    if not o: raise HTTPException(404,'Pedido não encontrado.')
    o.status=p.status; db.commit(); db.refresh(o); return o

@r.post('/orders/{oid}/confirm-payment',response_model=OrderOut)
def confirm_payment(oid:int,db:Session=Depends(get_db),_=Depends(require_roles('admin','seller'))):
    o=db.get(Order,oid)
    if not o: raise HTTPException(404,'Pedido não encontrado.')
    return mark_paid(db,o)
