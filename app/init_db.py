from app.database import Base , engine
from app.models import user,menu_item
Base.metadata.create_all(bind=engine)
print("Database tables created succesfully")


