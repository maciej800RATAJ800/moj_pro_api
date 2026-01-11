from schemas.user import UserCreate, UserUpdate
from repositories import user_repository

def list_users():
    return user_repository.get_all_users()


def get_user(user_id: int):
    return user_repository.get_user_by_id(user_id)


def add_user(payload: UserCreate):
    user_id = user_repository.add_user(payload.name, payload.age)
    return user_repository.get_user_by_id(user_id)


def edit_user(user_id: int, payload: UserUpdate):
    user = user_repository.get_user_by_id(user_id)
    if not user:
        return None

    name = payload.name if payload.name is not None else user["name"]
    age = payload.age if payload.age is not None else user["age"]

    user_repository.update_user(user_id, name, age)
    return user_repository.get_user_by_id(user_id)


def remove_user(user_id: int) -> bool:
    return user_repository.delete_user(user_id)
