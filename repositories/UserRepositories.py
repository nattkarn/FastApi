from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ModelReq import UserModels,UserModesResponse,UserEdit,UserLoginModel
from Entity import UserEntity
import bcrypt
from Business import Tokenize
from SecurityConfig import JWTConfig


def UserCreate(request:UserModels.User,db:Session):
        
    if not all([request.name, request.email, request.password, request.username]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
    

    user_record = db.query(UserEntity.User).filter(UserEntity.User.username == request.username).first()
    if user_record:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="User doest exited.")
    

    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')  # Store this in the database
    

    try:
        newUser = UserEntity.User(name=request.name, email=request.email, password=hashed_password_str, username=request.username)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        

        #add another table with relation 
        newProfile = UserEntity.Profile(line = request.line,owner = newUser)
        db.add(newProfile)
        db.commit()
        db.refresh(newProfile)

        context = {
            "name" : newUser.name,
            "username" : newUser.username,
            "email" : newUser.email,
            "isActive" : newUser.is_active,
            "pass" : newUser.password
        }
        return context
    
    except Exception as e:
        print("Error:", e)  # Log the error
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Create Failed")
    


def UserLoginOauth(request:OAuth2PasswordRequestForm,db:Session):
    user = db.query(UserEntity.User).filter(UserEntity.User.username == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"This Email {request.username} is not register")
    
    if not JWTConfig.Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
    
    access_token = Tokenize.create_access_token(data={"sub":user.email})
    
    return {"access_token":access_token,"type":"bearer"}



def UserLogin(request: UserLoginModel.Login,db: Session):
    if not all([request.password, request.username]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    user_record = db.query(UserEntity.User).filter(UserEntity.User.username == request.username).first()
    if not user_record:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="User not found.")
    
    stored_hash = user_record.password.encode('utf-8')
    strUser = str(request.username)
    # Verify the input password against the stored hash
    if bcrypt.checkpw(request.password.encode('utf-8'), stored_hash):
        #TODO : return token key
        token = Tokenize.create_access_token(data={"sub":user_record.email})
        # print(f"==>> token: {token}")

        return {"TOKEN" : token}
    else:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Incorrect username or password.")
 