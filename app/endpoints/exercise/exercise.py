import sys
import json
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

    def __init__(self, user, reps: int = None, sets: int = None, weight: int = None, name: str = None, date: datetime.date = None, pyramid: dict = None) -> None:
        self.user = user
        self.name = name
        self.reps = reps
        self.sets = sets
        self.weight = weight
        self.date = date
        self.pyramid = pyramid
        if date == None:
            self.date = datetime.now().strftime("%Y-%m-%d")
        if self.weight == None:
            self.weight = 0
        if pyramid == None:
            self.pyramid = {
                'name': self.name, 
                'reps': [self.reps], 
                'sets': [self.sets],
                'weight': [self.weight]
                }
            

    def upload(self) -> None:
        try:
            sql = "INSERT INTO exercise (user_id, name, date, pyramid) VALUES (%s, %s, %s, %s)"
            val = [(self.user.id, self.name, self.date, json.dumps(self.pyramid))]

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

    # still needs fixing
    def delete_exercise_from_db(self, exercise_data):

        # exercise_data -format = {'name': exercise_name, 'date': exercise_date, 'reps': exercise_reps, 'sets': exercise_sets, 'weight': exercise_weight}

        delete_string = f"user_id = '{self.user.id}' AND name = '{exercise_data['name']}' AND date = '{exercise_data['date']}'"
        if 'reps' in exercise_data:
            delete_string + f" AND reps = '{exercise_data['reps']}'"
        if 'sets' in exercise_data:
            delete_string + f" AND sets = '{exercise_data['sets']}'"
        if 'weight' in exercise_data:
            delete_string + f" AND weight = '{exercise_data['weight']}'"

        mycursor.execute(f"DELETE FROM exercise WHERE " + delete_string)
        mydb.commit()

    def add_to_pyramid(self, reps: int, sets: int, weight: int):
        if weight == None:
            weight = 0
        self.pyramid["reps"].append(reps)
        self.pyramid["sets"].append(sets)
        self.pyramid["weight"].append(weight)


