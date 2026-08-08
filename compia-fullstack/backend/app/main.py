from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth,products,orders,admin,payments
app=FastAPI(title='COMPIA API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
for x in (auth.r,products.r,orders.r,admin.r,payments.r): app.include_router(x,prefix='/api/v1')
@app.get('/health')
def health(): return {'status':'ok'}
