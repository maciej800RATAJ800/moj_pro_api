from fastapi import APIRouter, HTTPException, Query
from src.models.user import User, UserUpdate, UserResponse
from src.models.sort_enums import SortBy, SortDir
from src.database import (
    get_all_users,
    get_user_by_id,
    add_user,
    update_user,
    delete_user,
    query_users,
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/query")
def get_filtered_users(
    page: int = Query(1),
    limit: int = Query(5),
    sort_by: SortBy = Query(SortBy.id),          # ENUM!
    sort_dir: SortDir = Query(SortDir.ASC),      # ENUM!
    min_age: int | None = Query(None),
    max_age: int | None = Query(None),
):

    offset = (page - 1) * limit

    users = query_users(
        limit,
        offset,
        sort_by.value,
        sort_dir.value,
        min_age,
        max_age
    )

    return {
        "page": page,
        "limit": limit,
        "sort_by": sort_by,
        "sort_dir": sort_dir,
        "filters": {
            "min_age": min_age,
            "max_age": max_age,
        },
        "count": (users),
        "results": users
    }



# ----------------------------------------------------------
# GET /users/list
# ----------------------------------------------------------
@router.get("/list")
def get_user_list():
    return get_all_users()

# ----------------------------------------------------------
# POST /users/add
# ----------------------------------------------------------
@router.post("/add")
def create_user(payload: User):
    new_id = add_user(payload.name, payload.age)
    return {
        "message": "User added",
        "id": new_id
    }

# ----------------------------------------------------------
# PUT /users/update/{user_id}
# ----------------------------------------------------------
@router.put("/update/{user_id}")
def update_user_data(user_id: int, payload: UserUpdate):
    user_exists = get_user_by_id(user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    name = payload.name if payload.name is not None else user_exists["name"]
    age = payload.age if payload.age is not None else user_exists["age"]

    updated = update_user(user_id, name, age)
    if not updated:
        raise HTTPException(status_code=400, detail="Update failed")

    return {
        "message": "User updated",
        "id": user_id
    }


# ----------------------------------------------------------
# DELETE /users/delete/{user_id}
# ----------------------------------------------------------
@router.delete("/delete/{user_id}")
def delete_user_record(user_id: int):
    user_exists = get_user_by_id(user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Delete failed")

    return {"message": "User deleted"}

# ----------------------------------------------------------
# GET /users/{user_id}
# ----------------------------------------------------------

@router.get("/{user_id}")
def get_single_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
