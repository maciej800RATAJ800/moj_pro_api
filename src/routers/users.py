from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import UserModel 
from src.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from src.schemas.token import Token
from src.services.auth_service import (hash_password, verify_password, create_access_token, create_refresh_token)

router = APIRouter(prefix="/users", tags=["Users"])

# 🔹 GET ALL
@router.get("/",
response_model=list[UserResponse])
def get_users(
    skip: int = 0, limit: int = 10, sort_by: str = Query("id"), order: str = Query("asc"), db: Session = Depends(get_db)
    ):
    query = db.query(UserModel)

# Sorting Logic

    if sort_by in ["id", "name", "age"]:
        column = getattr(UserModel, sort_by)
        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

# PAGINATION LOGIC            
            query = query.offset(skip).limit(limit)

    return query.all()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # hash password and create user
    hashed_password = hash_password(user.password)
    
    # Create user instance
    new_user = UserModel(name=user.name, age=user.age, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# 🔹 GET BY ID
@router.get("/{user_id}", 
            response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 UPDATE
@router.put("/{user_id}", 
response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
     raise HTTPException(status_code=404, detail="User not found")

    if user.name is not None: 
        db_user.name = user.name
    if user.age is not None:
        db_user.age = user.age
    if user.password is not None:
        db_user.password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)

    return db_user


# 🔹 DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}

#   Login
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.name == user.name).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }