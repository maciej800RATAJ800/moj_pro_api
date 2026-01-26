from typing import Optional
from pydantic import BaseModel, Field, validator
import re

name_regex = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż -]{2,50}$")

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Maciej")
    age: int = Field(..., ge=0, le=120, example=30)

    @validator("name")
    def name_must_be_letters(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name is required")
        if not name_regex.match(v):
            raise ValueError("Name must contain only letters, spaces or hyphens (2–50 chars)")
        return " ".join(p.capitalize() for p in v.split())

    class Config:
        schema_extra = {
            "example": {"name": "Maciej", "age": 30}
        }


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, example="Jan")
    age: Optional[int] = Field(None, ge=0, le=120, example=40)

    @validator("name")
    def name_must_be_letters_optional(cls, v):
        if v is None:
            return None
        v = v.strip()
        if not name_regex.match(v):
            raise ValueError("Name must contain only letters, spaces or hyphens (2–50 chars)")
        return " ".join(p.capitalize() for p in v.split())


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
