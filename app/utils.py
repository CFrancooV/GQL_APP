import jwt
from datetime import datetime, timedelta,timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from app.DB.models import User
from app.DB.database import Session
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRATION_TIME_IN_MINUTES = int(os.getenv("TOKEN_EXPIRATION_TIME_IN_MINUTES"))

def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_IN_MINUTES)

    payload = {
        "sub": email,
        "exp": expiration_time
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def hash_password(pwd):
    ph =PasswordHasher() #Instanciaeted by invoking it
    return ph.hash(pwd)
    
def verify_password(pwd_hash,pwd):
    ph =PasswordHasher() #Instanciaeted by invoking it
    try:
        ph.verify(pwd_hash,pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid Password, Please try again")
    
def get_authenticated_user(context):
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')

    token = [None]
    if auth_header:
        token = auth_header.split(" ")

    if auth_header and token[0]== "Bearer" and len(token)==2:
        try:
            payload = jwt.decode(token[1],SECRET_KEY,algorithms=[ALGORITHM])
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'],tz=timezone.utc):
                raise GraphQLError("Generate another Token, expiraition time passed")
            
            session = Session()
            user = session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate User")
            return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError("Invalid authentication token")
        except Exception as e:
            raise GraphQLError("Could not authenticate user")
    else:
        raise GraphQLError("Missing Authentication token")
    
def get_auth_user(func):
    wraps(func)
    def wrapper(*args,**kuargs):
        info = args[1]
        get_authenticated_user(info.context)
        return func(*args,**kuargs)
    return wrapper
    
def auth_user_same_as(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        usrId = kwargs.get("user_id")


        if user.id != usrId:
            raise GraphQLError("Token must be generated as the same user_id you are trying to apply for")
        return func(*args,**kwargs)
    return wrapper
    
def admin_user(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)


        if user.role != "Accountadmin":
            raise GraphQLError("You must be logged as Accountadmin, or you don't have Accountadmin role")
        return func(*args,**kwargs)
    return wrapper