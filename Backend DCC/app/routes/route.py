# from fastapi import APIRouter
# from models.todos import Todo
# from config.database import collection_name
# from schema.schemas import individual_serial, list_serial
# from bson import ObjectId #lo que usa mongo para identificar los objetos que el mismo crea


# router = APIRouter()

# #GET
# @router.get("/")
# async def get_todos():
#     todos = list_serial(collection_name.find())
#     return todos


# #POST
# @router.post("/")
# async def post_todo(todo: Todo):
#     collection_name.insert_one(dict(todo))

# #PUT
# @router.put("/{id}")
# async def put_todo(id: str, todo:Todo):
#     collection_name.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})

# #DELETE
# @router.delete("/{id}")
# async def delete_todo(id: str):
#     collection_name.find_one_and_delete({"_id": ObjectId(id)})

from fastapi import APIRouter
from ..schemas.user_schema import UserCreateSchema, UserResponseSchema
from ..services.user_service import create_user, get_users
from typing import List

router = APIRouter()

@router.post("/users/", response_model=UserResponseSchema)
async def register_user(user: UserCreateSchema):
    user_id = await create_user(user)
    return {"id": user_id, "name": user.name, "email": user.email}

@router.get("/users/", response_model=List[UserResponseSchema])
async def list_users():
    return await get_users()
