from logging import debug
import sys

sys.path.append(".")
from fastapi import FastAPI, Response

from app.app_init import db_init
from app.config import VERSION

mycursor, mydb = db_init()




app = FastAPI(title="Trainings-api-endpoints", version=VERSION, version_info="test")


from app.endpoints.user import router as router_users
from app.endpoints.exercise import router as router_exercise
from app.endpoints.evaluation import router as router_evaluation

app.include_router(router_users, prefix="/user")
app.include_router(router_exercise, prefix="/exercise")
app.include_router(router_evaluation, prefix="/evaluation")

 
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(port=8080)
