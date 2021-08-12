import sys
sys.path.append(".")

from datetime import datetime
from app import mycursor, mydb
from mysql.connector.errors import IntegrityError
from app.endpoints.user.errors import UserIdNotValidError


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

    def upload(self):
        try:
            sql = "INSERT INTO exercise (user_id, name, reps, sets, weight, date) VALUES (%s, %s, %s, %s, %s, %s)"
            val = [(self.user.id, self.name, self.reps, self.sets, self.weight, self.date)]

            mycursor.executemany(sql, val)
            mydb.commit()

            return None

        except IntegrityError as e:
            raise UserIdNotValidError(message="This user_id is not valid")

        except Exception as e:
            return e