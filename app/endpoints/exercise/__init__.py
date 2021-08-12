import os
import sys
import datetime

from fastapi.datastructures import UploadFile
sys.path.append(".")
from fastapi import APIRouter, File
from starlette.responses import FileResponse
from app.endpoints.user.user import User
from app.endpoints.exercise.exercise import Exercise
from app.endpoints.exercise.helper.file_data_extractor import extract_data



router = APIRouter(tags=["Exercise"])

description_exercise = "Uploads data from one set of exercises to the db"
@router.post("/{user_id}", description=description_exercise)
async def exercise(user_id, name, reps, sets, weight):

    user = User(id=user_id)

    exercise = Exercise(user, reps, sets, weight, name)

    error = exercise.upload()

    if error == None:

        return {"message": "Exercise data has been uploaded to db"}
    
    else:
        return {"message": "An error has occured", "error": error}


description_file_upload = """Uploads data from a file - for format info download the demo file"""
@router.post("/file_uplaod/{user_id}", description=description_file_upload)
async def file_upload(user_id, date: str = None ,file_uplaod: UploadFile = File(...)):
    
    user = User(id=user_id)

    extract_data(user.id, file_uplaod.file)

@router.get("/demo_file_download")
async def example_file_download():
    return FileResponse(os.path.abspath("app\endpoints\exercise\helper\demo-file.txt"), media_type='application/octet-stream', filename="demo-file.txt")
              





