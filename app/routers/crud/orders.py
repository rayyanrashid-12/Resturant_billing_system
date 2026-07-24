from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
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
