from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Product,Order,OrderItem

def create_order(db:Session,user,p):
    if p.payment_method not in ('card','pix'): raise HTTPException(422,'Forma de pagamento inválida.')
    ids=[x.product_id for x in p.items]; products=db.scalars(select(Product).where(Product.id.in_(ids),Product.is_active.is_(True))).all(); by={x.id:x for x in products}
    if len(by)!=len(set(ids)): raise HTTPException(404,'Um ou mais produtos não estão disponíveis.')
    subtotal=Decimal('0'); only_digital=True; items=[]
    for line in p.items:
        prod=by[line.product_id]; only_digital &= prod.product_type=='digital'
        if prod.product_type!='digital' and prod.stock<line.quantity: raise HTTPException(409,f'Estoque insuficiente para {prod.title}.')
        subtotal += prod.price*line.quantity
        items.append(OrderItem(product_id=prod.id,title=prod.title,product_type=prod.product_type,quantity=line.quantity,unit_price=prod.price,digital_file_url=prod.digital_file_url))
    delivery='digital' if only_digital else p.delivery_method
    if not only_digital and delivery not in ('shipping','pickup'): raise HTTPException(422,'Forma de entrega inválida.')
    if delivery=='shipping' and not all([p.shipping_address.strip(),p.shipping_city.strip(),p.shipping_state.strip(),p.shipping_zip.strip()]): raise HTTPException(422,'Endereço completo é obrigatório para entrega.')
    fee=Decimal(str(settings.shipping_flat_rate)) if delivery=='shipping' else Decimal('0')
    o=Order(user_id=user.id,payment_method=p.payment_method,delivery_method=delivery,subtotal=subtotal,shipping_fee=fee,total=subtotal+fee,shipping_name=p.shipping_name,shipping_email=str(p.shipping_email),shipping_phone=p.shipping_phone,shipping_address=p.shipping_address,shipping_city=p.shipping_city,shipping_state=p.shipping_state,shipping_zip=p.shipping_zip,items=items)
    db.add(o); db.commit(); db.refresh(o); return o

def mark_paid(db:Session,o:Order):
    if o.payment_status=='paid': return o
    ids=[i.product_id for i in o.items]; products=db.scalars(select(Product).where(Product.id.in_(ids)).with_for_update()).all(); by={p.id:p for p in products}
    for i in o.items:
        p=by.get(i.product_id)
        if p and p.product_type!='digital':
            if p.stock<i.quantity: raise HTTPException(409,f'Estoque insuficiente para {p.title}.')
            p.stock-=i.quantity
    o.payment_status='paid'; o.status='paid'; db.commit(); db.refresh(o); return o
