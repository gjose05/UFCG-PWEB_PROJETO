from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.deps import current_user
from app.models import Order
from app.schemas import CheckoutIn,CheckoutOut,OrderOut
from app.services.orders import create_order
from app.services.payments import prepare_payment
r=APIRouter(prefix='/orders',tags=['orders'])
@r.post('/checkout',response_model=CheckoutOut)
def checkout(p:CheckoutIn,db:Session=Depends(get_db),u=Depends(current_user)):
    o=create_order(db,u,p); url,msg=prepare_payment(db,o); db.refresh(o); return {'order':o,'checkout_url':url,'message':msg}
@r.get('/mine',response_model=list[OrderOut])
def mine(db:Session=Depends(get_db),u=Depends(current_user)): return db.scalars(select(Order).where(Order.user_id==u.id).order_by(Order.created_at.desc())).unique().all()
@r.get('/{oid}',response_model=OrderOut)
def get_order(oid:int,db:Session=Depends(get_db),u=Depends(current_user)):
    o=db.scalar(select(Order).where(Order.id==oid,Order.user_id==u.id))
    if not o: raise HTTPException(404,'Pedido não encontrado.')
    return o
@r.get('/{oid}/downloads')
def downloads(oid:int,db:Session=Depends(get_db),u=Depends(current_user)):
    o=db.scalar(select(Order).where(Order.id==oid,Order.user_id==u.id))
    if not o: raise HTTPException(404,'Pedido não encontrado.')
    if o.payment_status!='paid': raise HTTPException(403,'Downloads disponíveis após o pagamento.')
    return [{'title':i.title,'url':i.digital_file_url} for i in o.items if i.digital_file_url]
