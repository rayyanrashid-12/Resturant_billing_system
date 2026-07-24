from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, models
from app.routers.crud import users
from app.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Restaurant Billing System API"}


@app.get("/health")
def health():
    return {"STATUS": "RUNNING"}

@app.post("/user", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return users.create_user(db, user)

@app.get("/user", response_model=list[schemas.UserResponse])
def get_users(db: Session= Depends(get_db)):
    return users.get_users(db)


@app.get("/user/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return users.get_user(db, user_id)

@app.put("/user/{user_id}",response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session= Depends(get_db)

):
    return users.update_user(db, user_id, user_update)

@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    login_data = schemas.UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return users.login_user(db, login_data)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ---------------- MENU ----------------

@app.post("/menu", response_model=schemas.MenuItemResponse)
def create_menu(
    menu_item: schemas.MenuItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_menu_item(db, menu_item)


@app.get("/menu", response_model=list[schemas.MenuItemResponse])
def get_menu(
    db: Session = Depends(get_db)
):
    return crud.get_menu_items(db)


@app.get("/menu/{item_id}", response_model=schemas.MenuItemResponse)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_menu_item(db, item_id)


@app.put("/menu/{item_id}", response_model=schemas.MenuItemResponse)
def update_menu(
    item_id: int,
    menu_item: schemas.MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.update_menu_item(db, item_id, menu_item)


@app.delete("/menu/{item_id}")
def delete_menu(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.delete_menu_item(db, item_id)


# ---------------- ORDER ----------------

@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_order(db, order)


@app.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_orders(db)


@app.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_order(db, order_id)


@app.post("/orders/{order_id}/items", response_model=schemas.OrderResponse)
def add_item(
    order_id: int,
    item: schemas.OrderItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.add_item_to_order(db, order_id, item)


@app.get("/bill/{order_id}")
def bill(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.generate_bill(db, order_id)

@app.get("/reports")
def reports(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.sales_report(db)
