from pydantic import BaseModel



class User(BaseModel):
    name : str
    username : str
    password : str
    email : str
    line : str

class GetUser(BaseModel):
    email : str

