
from app.endpoints.evaluation.evaluation import Evaluation
import sys
sys.path.append(".")
from fastapi import APIRouter
from app.endpoints.user import User
from app.logger import get_logger

logger = get_logger("evalation-endpoints")

router = APIRouter(tags=["Evaluation"])


@router.get("/get_traning_days({user_id}")
async def get_training_days(user_id : int):

        evaluation = Evaluation(user=User(id=user_id))

        return evaluation.get_training_days()
    
@router.get("/get_max_weight/{user_id}/")
async def get_max_weight(user_id : int, exercise: str = None):

    evaluation = Evaluation(user=User(id=user_id))

    max = evaluation.get_max_traings_data(exercise.lower())

    return max

@router.get("/get_exercise_names/{user_id}")
async def get_exercise_names(user_id : int):

    evaluation = Evaluation(user=User(id=user_id))

    return evaluation.get_exercise_names()

@router.get("/get_exercise_history/{user_id}")
async def get_exercise_history(user_id: int, exercise_name: str = None):

    try:
        evaluation = Evaluation(user=User(id=user_id))

        return evaluation.get_exercise_history(exercise_name)
    except Exception as e:
        logger.error(e)
        return {"error": e}











