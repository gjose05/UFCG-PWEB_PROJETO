from fastapi import APIRouter,Depends,Request,HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.config import settings
from app.models import Order
from app.services.orders import mark_paid
r=APIRouter(prefix='/payments',tags=['payments'])
@r.post('/stripe/webhook',include_in_schema=False)
async def webhook(req:Request,db:Session=Depends(get_db)):
    if not settings.stripe_webhook_secret: raise HTTPException(503,'Webhook Stripe não configurado.')
    import stripe
    try: event=stripe.Webhook.construct_event(await req.body(),req.headers.get('stripe-signature',''),settings.stripe_webhook_secret)
    except Exception: raise HTTPException(400,'Webhook inválido.')
    if event['type']=='checkout.session.completed':
        oid=int(event['data']['object'].get('metadata',{}).get('order_id',0) or 0); o=db.get(Order,oid) if oid else None
        if o: mark_paid(db,o)
    return {'received':True}
