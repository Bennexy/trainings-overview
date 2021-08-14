import sys
sys.path.append(".")

from datetime import datetime
from app import mycursor, mydb
from mysql.connector.errors import IntegrityError
from mysql.connector.errors import DataError
from app.endpoints.user.errors import UserIdNotValidError
from app.endpoints.exercise.errors import ExerciseNameToLongError

from app.logger import get_logger


logger = get_logger("logger-exercise")

class Exercise:

    def __init__(self, user, reps: int = None, sets: int = None, weight: int = None, name: str = None, date: datetime.date = None) -> None:
        self.user = user
        self.name = name
        self.reps = reps
        self.sets = sets
        self.weight = weight
        self.date = date
        if date == None:
            self.date = datetime.now().strftime("%Y-%m-%d")

    def upload(self) -> None:
        try:
            sql = "INSERT INTO exercise (user_id, name, reps, sets, weight, date) VALUES (%s, %s, %s, %s, %s, %s)"
            val = [(self.user.id, self.name, self.reps, self.sets, self.weight, self.date)]

            mycursor.executemany(sql, val)
            mydb.commit()
        
        except DataError as e:
            logger.error(f"{e} occured while trying to upload data to db len of str {len(self.name)}")
            raise ExerciseNameToLongError(message="the given user id is not valid")

        except IntegrityError as e:
            raise UserIdNotValidError(message="the given user id is not valid")

    def rename(self, new_name):

        mycursor.execute(f"UPDATE exercise SET name = '{new_name}' WHERE user_id = '{self.user.id}' AND name = '{self.name}'")
        mydb.commit()

        return {'message': f'{mycursor.rowcount} entries renamed'}
