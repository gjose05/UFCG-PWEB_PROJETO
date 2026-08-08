from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel,EmailStr,Field
class RegisterIn(BaseModel): full_name:str=Field(min_length=3); email:EmailStr; password:str=Field(min_length=8)
class LoginIn(BaseModel): email:EmailStr; password:str
class UserOut(BaseModel):
    id:int; full_name:str; email:EmailStr; role:str; is_active:bool
    model_config={'from_attributes':True}
class TokenOut(BaseModel): access_token:str; token_type:str='bearer'; user:UserOut
class ProductBase(BaseModel):
    slug:str; title:str; author:str; category:str; product_type:str; price:Decimal=Field(gt=0); old_price:Decimal|None=None; stock:int=Field(ge=0); description:str=''; cover_color:str='book-a'; cover_image_url:str|None=None; digital_file_url:str|None=None; is_active:bool=True
class ProductOut(ProductBase):
    id:int
    model_config={'from_attributes':True}
class ProductUpdate(BaseModel):
    slug:str|None=None; title:str|None=None; author:str|None=None; category:str|None=None; product_type:str|None=None; price:Decimal|None=None; old_price:Decimal|None=None; stock:int|None=None; description:str|None=None; cover_color:str|None=None; cover_image_url:str|None=None; digital_file_url:str|None=None; is_active:bool|None=None
class CartLine(BaseModel): product_id:int; quantity:int=Field(ge=1,le=99)
class CheckoutIn(BaseModel):
    items:list[CartLine]=Field(min_length=1); payment_method:str; delivery_method:str; shipping_name:str; shipping_email:EmailStr; shipping_phone:str=''; shipping_address:str=''; shipping_city:str=''; shipping_state:str=''; shipping_zip:str=''
class OrderItemOut(BaseModel):
    id:int; product_id:int; title:str; product_type:str; quantity:int; unit_price:Decimal
    model_config={'from_attributes':True}
class OrderOut(BaseModel):
    id:int; status:str; payment_method:str; payment_status:str; delivery_method:str; subtotal:Decimal; shipping_fee:Decimal; total:Decimal; shipping_name:str; shipping_email:EmailStr; shipping_phone:str; shipping_address:str; shipping_city:str; shipping_state:str; shipping_zip:str; created_at:datetime; items:list[OrderItemOut]
    model_config={'from_attributes':True}
class CheckoutOut(BaseModel): order:OrderOut; checkout_url:str|None=None; message:str
class StatusIn(BaseModel): status:str
class StatsOut(BaseModel): products:int; users:int; orders:int; paid_orders:int; revenue:Decimal
