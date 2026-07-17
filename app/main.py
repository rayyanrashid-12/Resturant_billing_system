from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud

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

@app.post("/user",response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session =Depends(get_db)

):
    return crud.create_user(db )

@app.get("/user", response_model=list[schemas.UserResponse])
def get_users(db: Session= Depends(get_db)):
    return crud.get_user(db)


@app.get("/user/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_user(db, user_id)
