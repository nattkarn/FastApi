from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from repositories import UserRepositories
from database import get_db

router = APIRouter()
#### for Oauth2

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UserRepositories.UserLoginOauth(request,db)