from datetime import datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from app.config import settings
ph=PasswordHasher()
def hash_password(p): return ph.hash(p)
def verify_password(p,h):
    try: return ph.verify(h,p)
    except (VerifyMismatchError,InvalidHashError): return False
def create_token(uid): return jwt.encode({'sub':str(uid),'exp':datetime.now(timezone.utc)+timedelta(days=1)},settings.secret_key,algorithm='HS256')
def decode_token(t):
    try: return jwt.decode(t,settings.secret_key,algorithms=['HS256']).get('sub')
    except jwt.PyJWTError: return None
