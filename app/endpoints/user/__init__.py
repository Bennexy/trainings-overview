import sys
sys.path.append(".")
from fastapi import APIRouter
from app.endpoints.user.user import User


router = APIRouter(tags=["User-Actions"])



@router.post("/new_user/{user_name}")
async def create_user(user_name):

    user = User(name = user_name)

    error = user.create()

    if error == None:

        return {"message": "New user created", "user_name": user.name, "creation_date": user.creation_date, "user_id": user.id}
    
    return {"message": "An error has occured", "error": error}



@router.put("/update_user/{user_id}")
async def upadate_user(user_id : int, user_name: str = None):

    if user_name == None:
        return {"message": "no values transferd"}
    
    user = User(id=user_id)

    error = user.update(name = user_name)

    if error == None:
        return {"message": "User has been successfully updated", "user_id": user.id}
    
    return {"message": "An error has occured", "error": error}



@router.delete("/delete_user/{user_id}")
async def delete_user(user_id : int):

    user = User(id=user_id)

    error = user.delete_user()

    if error == None:
        return {"message": "user has been deleted"}

    else:
        return {"message": "An error has occured", "error": error}







