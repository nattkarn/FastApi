from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    accessToken:str
    tokenType:str

class TokenData(BaseModel):
    email:Optional[str] = None