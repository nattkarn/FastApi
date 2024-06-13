from typing import Optional
from SecurityConfig import JWTConfig
from jose import jwt,JWTError
import pytz
import datetime
from ModelReq import TokenModel
from SecurityConfig import JWTConfig




def create_access_token(data:dict):
    data_encode = data.copy()
    expire = expiration_time()
    data_encode.update({"exp":expire})
    return  jwt.encode(data_encode,JWTConfig.SECRET_KEY,algorithm=JWTConfig.ALGORITHM)
    

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,JWTConfig.SECRET_KEY,access_token=JWTConfig.ALGORITHM)
        email:str = payload.get('sub')
        
        if email is None:
            raise credentials_exception
        token_data = TokenModel.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    return token_data
    



def expiration_time():
    bangkok_timezone = pytz.timezone('Asia/Bangkok')
    current_time_bangkok = datetime.datetime.now(bangkok_timezone)

    
    expiration_time = current_time_bangkok + datetime.timedelta(minutes=int(JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES))
    return expiration_time
