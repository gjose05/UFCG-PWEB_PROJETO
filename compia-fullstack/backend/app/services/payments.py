from fastapi import HTTPException
from app.config import settings
from app.services.orders import mark_paid

def prepare_payment(db,o):
    if o.payment_method=='pix': return None,'Pedido criado. PIX demonstrativo, sem integração.'
    if settings.payment_provider=='mock': mark_paid(db,o); return None,'Pagamento de desenvolvimento aprovado automaticamente.'
    if settings.payment_provider!='stripe' or not settings.stripe_secret_key: raise HTTPException(500,'Stripe não configurado.')
    import stripe
    stripe.api_key=settings.stripe_secret_key
    lines=[{'price_data':{'currency':'brl','product_data':{'name':i.title},'unit_amount':int(i.unit_price*100)},'quantity':i.quantity} for i in o.items]
    if o.shipping_fee>0: lines.append({'price_data':{'currency':'brl','product_data':{'name':'Frete'},'unit_amount':int(o.shipping_fee*100)},'quantity':1})
    s=stripe.checkout.Session.create(mode='payment',line_items=lines,customer_email=o.shipping_email,success_url=f'{settings.frontend_url}/checkout/sucesso?order={o.id}&session_id={{CHECKOUT_SESSION_ID}}',cancel_url=f'{settings.frontend_url}/checkout?cancelled=1',metadata={'order_id':str(o.id)})
    o.stripe_checkout_session_id=s.id; db.commit(); return s.url,'Redirecionando para pagamento seguro.'
