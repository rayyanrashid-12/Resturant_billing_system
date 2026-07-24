from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
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
