from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from Business import Tokenize

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data:str= Depends(oauth_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"},
                                          )
    
    
    return Tokenize.verify_token(data,credentials_exception)