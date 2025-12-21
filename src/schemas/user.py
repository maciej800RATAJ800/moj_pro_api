from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=120)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

