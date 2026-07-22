from sqlalchemy import Column, Integer, String, Boolean, Float
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="cashier")
    is_active = Column(Boolean, default=True)


class MenuItems(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    available = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    total_amount = Column(Float, default=0)
    status = Column(String, default="Pending")

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")    