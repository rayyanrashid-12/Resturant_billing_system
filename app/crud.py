from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

def create_user(db: Session, user:schemas.UserCreate):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already required"
        )
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=user.password,
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
