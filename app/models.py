from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
class user(Base):
    __tablename__="user"
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="cashier")
    is_active = Column(Boolean, default=True)

class menu_item(Base):
    __tablename__="menu_item"
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    catagory = Column(String, nullable=False)
    available = Column(Boolean)
   
