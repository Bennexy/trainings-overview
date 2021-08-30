import sys
import json
sys.path.append(".")
from app.endpoints.user.user import User
from datetime import datetime
from app.config import DB_NAME
from app import mydb

class Evaluation:

    def __init__(self, user: User) -> None:
        self.user = user
        self.mycursor = mydb.cursor()
        self.mycursor.execute("USE " + str(DB_NAME))
    
    def get_training_days(self):

        self.mycursor.execute(f"SELECT date FROM exercise WHERE user_id = {self.user.id}")
        res = self.mycursor.fetchall()

        if len(res) == 0:
            return {"message": "No trainings found under this user-id"}

        trainings_dates = {"dates": [], "years": []}

        for date in res:
            date = date[0]
            if date not in trainings_dates["dates"]:
                print(date)
                trainings_dates["dates"].append(date)
            if date.year not in trainings_dates["years"]:
                trainings_dates["years"].append(date.year)


        return trainings_dates

    def get_max_traings_data(self, exercise_name) -> dict:

        if exercise_name != None:

            self.mycursor.execute(f"SELECT name, date, pyramid FROM exercise WHERE user_id = {self.user.id} AND name = '{exercise_name}'")

        else:
            self.mycursor.execute(f"SELECT name, date, pyramid FROM exercise WHERE user_id = {self.user.id}")

        res = self.mycursor.fetchall()
        max = {}
        for entry in res:
            pyramid = json.loads(entry[2])
            max_weight = 0.0
            counter_max_weight = None
            for counter in range(0, len(pyramid['weight'])):

                if float(pyramid['weight'][counter]) >= max_weight:
                    counter_max_weight = counter
                    max_weight = float(pyramid['weight'][counter])

            if str(entry[0]) not in max:
                max[str(entry[0])] = {f"name": entry[0], "weight": float(pyramid['weight'][counter_max_weight]), "reps": int(pyramid['reps'][counter_max_weight]), "sets": int(pyramid['sets'][counter_max_weight]), "date": entry[1]}
            else:
                if max[str(entry[0])]["weight"] < float(pyramid['weight'][counter_max_weight]):
                    max[str(entry[0])] = {f"name": entry[0], "weight": float(pyramid['weight'][counter_max_weight]), "reps": int(pyramid['reps'][counter_max_weight]), "sets": int(pyramid['sets'][counter_max_weight]), "date": entry[1]}

        return max
        
    def get_exercise_names(self) -> list:

        self.mycursor.execute(f"SELECT name FROM exercise WHERE user_id = {self.user.id}")
        res = self.mycursor.fetchall()
        names = []
        for name in res:
            name = name[0]
            if name not in names:
                names.append(name)

        return names

    def get_exercise_history(self, exercise_name) -> dict:

        if exercise_name != None:
            self.mycursor.execute(f"SELECT date, pyramid FROM exercise WHERE user_id = '{self.user.id}' AND name = '{exercise_name}'")
        else:
            self.mycursor.execute(f"SELECT date, pyramid FROM exercise WHERE user_id = '{self.user.id}'")

        res = self.mycursor.fetchall()

        data = {}
        for entry in res:
            print
            pyramid_data = json.loads(str(entry[1]))
            if pyramid_data["name"].lower() not in data:
                data[pyramid_data['name'].lower()] = []
            
            for i in range(0, len(pyramid_data['reps'])):
                data[pyramid_data['name'].lower()].append({'date': entry[0], 'name': pyramid_data['name'], 'reps': pyramid_data['reps'][i], 'sets': pyramid_data['sets'][i], 'weight': pyramid_data['weight'][i]})


        return data

    def get_max_weight_per_day(self, exercise_name) -> dict:

        results = {}

        if exercise_name != None:
            self.mycursor.execute(f"SELECT name, date, pyramid FROM exercise WHERE user_id = {self.user.id} AND name = '{exercise_name}'")
        else:
            self.mycursor.execute(f"SELECT name, date, pyramid FROM exercise WHERE user_id = {self.user.id}")

        res = self.mycursor.fetchall()

        for entry in res:
            pyramid = json.loads(entry[2])
            max_weight = 0.0
            counter_max_weight = None
            for counter in range(0, len(pyramid['weight'])):

                if float(pyramid['weight'][counter]) >= max_weight:
                    counter_max_weight = counter
                    max_weight = float(pyramid['weight'][counter])
            
            if str(entry[1]) not in results:
                results[str(entry[1])] = []

            results[str(entry[1])].append({f"name": entry[0], "weight": float(pyramid['weight'][counter_max_weight]), "reps": int(pyramid['reps'][counter_max_weight]), "sets": int(pyramid['sets'][counter_max_weight]), "date": entry[1]})

        return results

