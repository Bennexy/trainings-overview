import sys

from fastapi.datastructures import UploadFile
sys.path.append(".")
from fastapi import APIRouter, File
from app.endpoints.user.user import User
from app.endpoints.exercise.exercise import Exercise


router = APIRouter()

@router.post("/{user_id}")
async def exercise(user_id, name, reps, sets, weight):

    user = User(id=user_id)

    exercise = Exercise(user, reps, sets, weight, name)

    error = exercise.upload()

    if error == None:

        return {"message": "Exercise data has been uploaded to db"}
    
    else:
        return {"message": "An error has occured", "error": error}



@router.post("/file_uplaod/{user_id}")
async def file_upload(user_id, file_uplaod: UploadFile = File(...)):
    
    user = User(id=user_id)

    extract_data(file_uplaod.file)



def extract_data(file):

    for line in file:
        line = line.decode("utf-8").rstrip("\n") 
        
        line = line.split(" ")

        if '-' not in line[0] and line[0] != "":
            
            line[0] = line[0].split("x")

            while "" in line:
                line.remove("")
            
            
            sets = line[0][0]
            reps = line[0][1]
            weight = line[1].replace("kg", "")
            if len(line) == 2:
                name = name
            else:
                name = ""
                for i in range(2, len(line)):
                    name += line[i]
            
            print(sets, reps, weight, name)

                





