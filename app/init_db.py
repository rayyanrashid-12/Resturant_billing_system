from app.database import Base , engine
from app.models import User,MenuItems
Base.metadata.create_all(bind=engine)
print("Database tables created succesfully")


