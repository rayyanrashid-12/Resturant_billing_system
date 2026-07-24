from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
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