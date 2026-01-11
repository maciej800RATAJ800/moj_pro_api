from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserUpdate, UserRead
from services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserRead])
def list_users():
    return user_service.list_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate):
    return user_service.add_user(payload)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate):
    user = user_service.edit_user(user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    deleted = user_service.remove_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
