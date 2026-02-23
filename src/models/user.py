from typing import Optional
from pydantic import BaseModel, Field, field_validator, validator
import re


# ===== REGEX =====
name_regex = re.compile(r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż\- ]{2,50}$")


# =========================================================
# USER CREATE
# =========================================================

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Maciej")
    age: int = Field(..., ge=0, le=120, example=30)

    @field_validator("name")
    @classmethod
    def name_must_be_letters(cls, v: str):
        if not v.isalpha():
            raise ValueError("Name must contain only letters")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maciej",
                "age": 30
            }
        }

# =========================================================
# USER UPDATE (PATCH)
# =========================================================
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, example="Jan")
    age: Optional[int] = Field(None, ge=0, le=120, example=40)

    @validator("name")
    def name_must_be_letters_optional(cls, v):
        if v is None:
            return None

        v = v.strip()

        if not name_regex.match(v):
            raise ValueError(
                "Name must contain only letters, spaces or hyphens (2–50 chars)"
            )

        return " ".join(p.capitalize() for p in v.split())


# =========================================================
# USER RESPONSE
# =========================================================
class UserResponse(BaseModel):
    id: int
    name: str
    age: int


# =========================================================
# AUTH MODELS
# =========================================================
class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="1234")


class RefreshRequest(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
