import sys
sys.path.append(".")
from app.endpoints.user.user import User
from datetime import datetime
from app import mycursor, mydb



class Evaluation:

    def __init__(self, user: User) -> None:
        self.user = user
    
    def get_training_days(self):

        mycursor.execute(f"SELECT date FROM exercise WHERE user_id = {self.user.id}")
        res = mycursor.fetchall()

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

            mycursor.execute(f"SELECT reps, sets, weight, date, name FROM exercise WHERE user_id = {self.user.id} AND name = '{exercise_name}'")

        else:
            mycursor.execute(f"SELECT reps, sets, weight, date, name FROM exercise WHERE user_id = {self.user.id}")

        res = mycursor.fetchall()
        max = {}
        for entry in res:
            if entry[4] not in max:
                max[str(entry[4])] = {f"name": entry[4], "weight": entry[2], "reps": entry[0], "sets": entry[1], "date": entry[3]}
            else:
                if max[str(entry[4])]["weight"] < entry[2]:
                    max[entry[4]] = {f"name": entry[4], "weight": entry[2], "reps": entry[0], "sets": entry[1], "date": entry[3]}

        return max
        
    def get_exercise_names(self) -> list:

        mycursor.execute(f"SELECT name FROM exercise WHERE user_id = {self.user.id}")
        res = mycursor.fetchall()
        names = []
        for name in res:
            name = name[0]
            if name not in names:
                names.append(name)

        return names

    def get_exercise_history(self, exercise_name) -> dict:

        if exercise_name != None:
            mycursor.execute(f"SELECT date, name, reps, sets, weight FROM exercise WHERE user_id = '{self.user.id}' AND name = '{exercise_name}'")
        else:
            mycursor.execute(f"SELECT date, name, reps, sets, weight FROM exercise WHERE user_id = '{self.user.id}'")


        res = mycursor.fetchall()
        data = {}
        for entry in res:
            if entry[1] not in data:
                data[entry[1]] = [{'date': entry[0], 'name': entry[1], 'reps': entry[2], 'sets': entry[3], 'weight': entry[4]}]
            else:
                data[entry[1]].append({'date': entry[0], 'name': entry[1], 'reps': entry[2], 'sets': entry[3], 'weight': entry[4]})

        return data

