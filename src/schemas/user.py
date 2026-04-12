from typing import Optional
from pydantic import BaseModel, Field

# 🔹 CREATE
class UserCreate(BaseModel):
    name: str
    age: int
    password: str

# LOGIN
class UserLogin(BaseModel):
    name: str
    password: str

# 🔹 UPDATE (PATCH / PUT)
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, example="Jan")
    age: Optional[int] = Field(None, ge=0, le=120, example=40)
    password: Optional[str] = Field(None, min_length=4, example="1234")


# 🔹 RESPONSE (co API zwraca)
class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        from_attributes = True  # 🔴 ważne dla SQLAlchemy