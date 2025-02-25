from ..models.user_model import UserModel
from ..database import database
from bson import ObjectId

users_collection = database["users"]

async def create_user(user_data: UserModel):
    user_dict = user_data.dict()
    new_user = await users_collection.insert_one(user_dict)
    return str(new_user.inserted_id)

async def get_users():
    users_cursor = users_collection.find({})
    users = await users_cursor.to_list(length=100)
    return [{**user, "id": str(user["_id"])} for user in users]
