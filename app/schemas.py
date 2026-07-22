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

class UserLogin(BaseModel):
    email: str
    password: str 

class Token(BaseModel):
    access_token: str
    token_type: str

class MenuItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    category: str
    available: bool

    class Config:
        from_attributes = True


class MenuItemUpdate(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str
    available: bool

class OrderCreate(BaseModel):
    customer_name: str


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    status: str

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True    
