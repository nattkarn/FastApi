from fastapi import APIRouter,Depends,HTTPException,status
from ModelReq import UserModels,UserEdit,UserLoginModel
from Entity import UserEntity
from database import get_db
from sqlalchemy.orm import Session
from repositories import UserRepositories
from SecurityConfig import oauth2
from fastapi.security import OAuth2PasswordBearer
oauth_schema = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"message": "Not found"}}
)

#path parameter
# @app.get('/user/register/{id}')
# def register(id:int):
#     return {"register" : id}



@router.post('/test',tags=["Test"], include_in_schema=False)
def test():
    pass

#request parameter
@router.post('/register')
def register(request: UserModels.User, db: Session = Depends(get_db),status_code = status.HTTP_201_CREATED):
    return UserRepositories.UserCreate(request,db)
    


@router.post('/login')
def login(request: UserLoginModel.Login, db: Session = Depends(get_db)):
    return UserRepositories.UserLogin(request,db)

    
        


@router.post('/getall')
def getAll(db:Session = Depends(get_db),currant_user:UserModels.User = Depends(oauth2.get_current_user)):
    allUser = db.query(UserEntity.User).all()
    return allUser




@router.post('/getuser')
def getUserProfile(request:UserModels.GetUser ,db:Session = Depends(get_db),getCurrentUser:UserModels.User = Depends(oauth2.get_current_user)):
    print(f"==>> getCurrentUser: {getCurrentUser}")
    email = request.email
    print(f"==>> email: {email}")
    user = db.query(UserEntity.User).filter(UserEntity.User.email == email).first()

    # If user is not found, return an HTTP 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user



@router.patch('/edituser')
def editUser(request:UserEdit.EditUser,db:Session = Depends(get_db)):
    getid = request.id
    getname = request.name
    editUser = db.query(UserEntity.User).filter(UserEntity.User.id == getid).first()
    editUser.name = getname
    db.commit()
    db.refresh(editUser)
    context = {
        
    }
    return editUser


# @router.delete('/delleteuser')
# def editUser(request:UserEdit.EditUser,db:Session = Depends(get_db)):
#     getid = request.id
#     getname = request.name
#     editUser = db.query(UserEntity.User).filter(UserEntity.User.id == getid).first()
#     db.delete()
#     db.commit()
#     db.refresh(editUser)
#     return editUser