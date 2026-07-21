from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "cashier"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
    

class UserUpdate(BaseModel):
    name: str
    email :str
    role: str
    
    class Config:
        from_attributes= True
        