from pydantic import BaseModel



class EditUser(BaseModel):
    id : int
    name : str


