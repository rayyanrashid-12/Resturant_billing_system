from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = int(payload["sub"])

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None