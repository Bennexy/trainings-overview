from logging import debug
import sys
sys.path.append(".")
from fastapi import FastAPI

from app.app_init import db_init

mycursor, mydb = db_init()




app = FastAPI(title="Trainings-api-endpoints")


from app.endpoints.user import router as router_users
from app.endpoints.exercise import router as router_exercise

app.include_router(router_users, prefix="/user")
app.include_router(router_exercise, prefix="/exercise")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, debug=True)


