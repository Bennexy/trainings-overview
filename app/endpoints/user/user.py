
import sys
sys.path.append(".")
from datetime import datetime
from app import mycursor, mydb
from app.endpoints.user.errors import NoArgsGivenError
from app.logger import get_logger

logger = get_logger("User-class-logger")

class User:

    def __init__(self, id=None, name=None):
        if id == None and name == None:
            raise NoArgsGivenError(message="Please specify either name or id of the User")
        self.id = id
        self.name = name
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def create(self):
        
        sql = "INSERT INTO users (name, creation_date) VALUES (%s, %s)"
        val = [(self.name, self.creation_date)]

        mycursor.executemany(sql, val)
        mydb.commit()

        mycursor.execute(f"SELECT id FROM users WHERE name = '{self.name}' AND creation_date = '{self.creation_date}' ORDER BY id DESC LIMIT 1")
        self.id = mycursor.fetchall()[0]

        logger.debug(f"User {self.id, self.name} successfully created")

    def update(self, name):
        
        self.name = name

        mycursor.execute(f"UPDATE users SET name = '{self.name}' WHERE id = {self.id}")
        mydb.commit()

        logger.debug(f"User {self.id, self.name} successfully updated")

    def delete_user(self):

        mycursor.execute(f"DELETE FROM users WHERE id = {self.id}")
        mydb.commit()

    def get_training_days(self):

        mycursor.execute(f"SELECT date FROM exercise WHERE user_id = {self.id}")
        res = mycursor.fetchall()

        if len(res) == 0:
            return {"message": "No trainings found under this user-id"}

        trainings_dates = {"dates": []}

        for date in res:
            date = date[0]
            if date not in trainings_dates["dates"]:
                print(date)
                trainings_dates["dates"].append(date)
            # if date.year not in trainings_dates["years"]:
            #     trainings_dates["years"].append({date.year: []})


        return trainings_dates

    def get_max_traings_data(self, exercise_name) -> list:

        if exercise_name != None:

            mycursor.execute(f"SELECT reps, sets, weight, date, name FROM exercise WHERE user_id = {self.id} AND name = '{exercise_name}'")

        else:
            mycursor.execute(f"SELECT reps, sets, weight, date, name FROM exercise WHERE user_id = {self.id}")

        res = mycursor.fetchall()
        max = {}
        for entry in res:
            if entry[4] not in max:
                max[str(entry[4])] = {f"name": entry[4], "weight": entry[2], "reps": entry[0], "sets": entry[1], "date": entry[3]}
            else:
                if max[str(entry[4])]["weight"] < entry[2]:
                    max[entry[4]] = {f"name": entry[4], "weight": entry[2], "reps": entry[0], "sets": entry[1], "date": entry[3]}

        return max
        
    def get_exercise_names(self):

        mycursor.execute(f"SELECT name FROM exercise WHERE user_id = {self.id}")
        res = mycursor.fetchall()
        names = []
        for name in res:
            name = name[0]
            if name not in names:
                names.append(name)

        return names

    def delete_exercise_from_db(self, exercise_data):

        # exercise_data -format = {'name': exercise_name, 'date': exercise_date, 'reps': exercise_reps, 'sets': exercise_sets, 'weight': exercise_weight}

        delete_string = f"user_id = '{self.id}' AND name = '{exercise_data['name']}' AND date = '{exercise_data['date']}'"
        if 'reps' in exercise_data:
            delete_string + f" AND reps = '{exercise_data['reps']}'"
        if 'sets' in exercise_data:
            delete_string + f" AND sets = '{exercise_data['sets']}'"
        if 'weight' in exercise_data:
            delete_string + f" AND weight = '{exercise_data['weight']}'"

        mycursor.execute(f"DELETE FROM exercise WHERE " + delete_string)
        mydb.commit()


