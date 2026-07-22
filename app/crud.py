from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from app.security import hash_password, verify_password
from app.auth import create_access_token

def create_user(db: Session, user:schemas.UserCreate):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password = hash_password(user.password),
        role=user.role,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = user_update.name
    user.email = user_update.email
    user.role = user_update.role

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

def login_user(db: Session, login: schemas.UserLogin):
    user = db.query(models.User).filter(
        models.User.email == login.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="email and password are invalid"
        )

    if not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
    )
    token = create_access_token(user.id)

    return {
    "access_token": token,
    "token_type": "bearer"
}


# ---------------- MENU CRUD ----------------

def create_menu_item(db: Session, menu_item: schemas.MenuItemCreate):
    db_item = models.MenuItems(
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        category=menu_item.category
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_menu_items(db: Session):
    return db.query(models.MenuItems).all()


def get_menu_item(db: Session, item_id: int):
    item = db.query(models.MenuItems).filter(
        models.MenuItems.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return item


def update_menu_item(
    db: Session,
    item_id: int,
    menu_item: schemas.MenuItemUpdate
):
    item = db.query(models.MenuItems).filter(
        models.MenuItems.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    item.name = menu_item.name
    item.description = menu_item.description
    item.price = menu_item.price
    item.category = menu_item.category
    item.available = menu_item.available

    db.commit()
    db.refresh(item)

    return item


def delete_menu_item(db: Session, item_id: int):
    item = db.query(models.MenuItems).filter(
        models.MenuItems.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    db.delete(item)
    db.commit()

    return {"message": "Menu item deleted successfully"}


# ---------------- ORDER CRUD ----------------

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        customer_name=order.customer_name,
        total_amount=0,
        status="Pending"
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


def add_item_to_order(
    db: Session,
    order_id: int,
    item: schemas.OrderItemCreate
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    menu_item = db.query(models.MenuItems).filter(
        models.MenuItems.id == item.menu_item_id
    ).first()

    if menu_item is None:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    order_item = models.OrderItem(
        order_id=order.id,
        menu_item_id=menu_item.id,
        quantity=item.quantity,
        price=menu_item.price
    )

    db.add(order_item)

    # Update total automatically
    order.total_amount += menu_item.price * item.quantity

    db.commit()
    db.refresh(order)

    return order

# ---------------- BILLING ----------------

def generate_bill(db: Session, order_id: int):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    tax = order.total_amount * 0.10
    grand_total = order.total_amount + tax

    return {
        "order_id": order.id,
        "customer_name": order.customer_name,
        "subtotal": order.total_amount,
        "tax": tax,
        "grand_total": grand_total,
        "status": order.status
    }

# ---------------- REPORTS ----------------

from sqlalchemy import func

def sales_report(db: Session):
    total_orders = db.query(models.Order).count()

    total_sales = db.query(
        func.sum(models.Order.total_amount)
    ).scalar()

    if total_sales is None:
        total_sales = 0

    return {
        "total_orders": total_orders,
        "total_sales": total_sales
    }