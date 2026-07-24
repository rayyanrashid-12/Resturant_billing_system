from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas

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

