from app.database import Base , engine
from app.models import User,Menu
from app.models import User, MenuItems, Order, OrderItem

Base.metadata.create_all(bind=engine)
print("Database tables created succesfully")


