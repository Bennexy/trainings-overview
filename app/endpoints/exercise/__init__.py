import os
import sys
import datetime

from fastapi.datastructures import UploadFile
sys.path.append(".")
from fastapi import APIRouter, File
from starlette.responses import FileResponse

from app.endpoints.exercise.exercise import Exercise
from app.endpoints.exercise.helper.file_data_extractor import Extractor
from app.endpoints.user.user import User
from app.logger import get_logger

logger = get_logger("exercise-endpoints")


router = APIRouter(tags=["Exercise"])

description_exercise = "Uploads data from one set of exercises to the db"
@router.post("/{user_id}", description=description_exercise)
async def exercise(user_id : int, name: str, reps: int, weight: float, sets: int = None):
    
    try:
        user = User(id=user_id)

        exercise = Exercise(user, reps, sets, weight, name.lower())

        exercise.upload()

        return {"message": "Exercise data has been uploaded to db"}
    
    except Exception as e:
        return e

description_file_upload = """Uploads data from a file - for format info download the demo file"""
@router.post("/file_uplaod/{user_id}", description=description_file_upload)
async def file_upload(user_id : int, date: str = None , file_uplaod: UploadFile = File(...)):
    
    try:
        user = User(id=user_id)

        extractor = Extractor(user=user)

        extractor.template_load()

        extractor.extract_data(file_uplaod.file)

        return {"message": "Exercise data has been uploaded to db"}
    except Exception as e:
        print(e)
        return e


@router.get("/demo_file_download")
async def example_file_download():
    return FileResponse(os.path.abspath("app\endpoints\exercise\helper\demo-file.txt"), media_type='application/octet-stream', filename="demo-file.txt")


@router.put("/update_exercise_name/{user_id}")              
async def update_exercise_name(user_id : int, exercise_name_old: str, exercise_name_new: str):

    try:
        user = User(id=user_id)

        exercise = Exercise(user, name=exercise_name_old.lower())

        res = exercise.rename(exercise_name_new.lower())

        return res
    
    except Exception as e:
        logger.error(f"{e} has occured while trying to execute 'update_exercise_name'")
        return e

@router.delete("/delete_exercise/{user_id}", description="Needs exercise data in form of a dict")
async def delete_exercise(user_id : int, exercise_data: dict):

    exercise = Exercise(User(user_id))

    exercise.delete_exercise_from_db(exercise_data)

    return {"message": "Data has been deleted from db"}

@router.get("/regex")
async def get_regex():
    return get_regex()


