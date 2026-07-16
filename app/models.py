from sqlalchemy import Column, Integer, String, Boolean, Float
from app.database import Base
class User(Base):
    __tablename__="user"
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="cashier")
    is_active = Column(Boolean, default=True)

class MenuItems(Base):
    __tablename__="menu_items"
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    category = Column(String, nullable=False)
    available = Column(Boolean, default=True)
   
