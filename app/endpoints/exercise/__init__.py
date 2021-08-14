import os
import sys
import datetime

from fastapi.datastructures import UploadFile
sys.path.append(".")
from fastapi import APIRouter, File
from starlette.responses import FileResponse

from app.endpoints.exercise.exercise import Exercise
from app.endpoints.exercise.helper.file_data_extractor import extract_data
from app.endpoints.user.user import User
from app.logger import get_logger

logger = get_logger("exercise-endpoints")


router = APIRouter(tags=["Exercise"])

description_exercise = "Uploads data from one set of exercises to the db"
@router.post("/{user_id}", description=description_exercise)
async def exercise(user_id : int,name, reps, sets, weight):
    
    try:
        user = User(id=user_id)

        exercise = Exercise(user, reps, sets, weight, name)

        exercise.upload()

        return {"message": "Exercise data has been uploaded to db"}
    
    except Exception as e:
        return e

description_file_upload = """Uploads data from a file - for format info download the demo file"""
@router.post("/file_uplaod/{user_id}", description=description_file_upload)
async def file_upload(user_id : int,date: str = None ,file_uplaod: UploadFile = File(...)):
    
    user = User(id=user_id)

    error = extract_data(user, file_uplaod.file)

    if error == None:

        return {"message": "Exercise data has been uploaded to db"}
    
    else:
        return {"message": "An error has occured", "error": error}

@router.get("/demo_file_download")
async def example_file_download():
    return FileResponse(os.path.abspath("app\endpoints\exercise\helper\demo-file.txt"), media_type='application/octet-stream', filename="demo-file.txt")

@router.put("/update_exercise_name/{user_id}")              
async def update_exercise_name(user_id : int, exercise_name_old: str, exercise_name_new: str):

    try:
        user = User(id=user_id)

        exercise = Exercise(user, name=exercise_name_old)

        res = exercise.rename(exercise_name_new)

        return res
    
    except Exception as e:
        logger.error(f"{e} has occured while trying to execute 'update_exercise_name'")
        return e






