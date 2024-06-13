from pydantic import BaseModel

# Pydantic model for user read operations
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
