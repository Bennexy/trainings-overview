from regex.regex import template
from app.endpoints.exercise import exercise
import os
import sys
import yaml
import regex as re
from datetime import datetime
sys.path.append('.')
from app.endpoints.exercise.errors import *
from app.endpoints.exercise.exercise import Exercise
from app.endpoints.user.user import User
from app.logger import get_logger
from tempfile import SpooledTemporaryFile


logger = get_logger("logger-exercise-file-data-extractor")

class Extractor:

    def __init__(self, user: User, template_folder: str = "default") -> None:

        self.user = user

        self.template_folder = template_folder
        self.templates_raw = []

        # chosen template data
        self.name = None
        self.documentation = None
        self.date_regex = None
        self.exercise_regex = None


        if template_folder == "default":
            self.template_folder = os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates"))
    
    def template_load(self, template_name: str = "default"):

        files = [f for f in os.listdir(self.template_folder) if os.path.isfile(os.path.join(self.template_folder, f)) and f.endswith(".yaml") or f.endswith(".yml")]

        for file in files:
            items = yaml.load(open(os.path.join(self.template_folder, file)), Loader=yaml.FullLoader)
            self.templates_raw.append(items)

        for temp in self.templates_raw:
            if temp['name'] == template_name:
                reg = temp['template']['regex']
                self.name = temp['name']
                self.documentation = temp['template']['format']
                self.date_regex = reg['date']
                self.exercise_regex = reg['exercise']

        # print(self.name)
        # print(self.documentation)
        # print(self.date_regex)
        # print(self.exercise_regex)

    def extract_data(self, file: SpooledTemporaryFile):
        
        line_num = 0
        exercises = []

        for line in file:
            line = line.decode("utf-8").rstrip("\n") 
            line_num += 1

            res = self.find_regex_matches(self.date_regex, line)

            if len(res) != 0:
                res = res[0]
                date = self.get_date_obj(res, line_num)
                res = []
            else:
                res = self.find_regex_matches(self.exercise_regex, line)
                
            
            if len(res) != 0:
                res = res[0]


                sets = res[0]
                if sets == None:
                    sets = 1

                reps = int(res[1])

                weight = res[2]
                if weight != None:
                    weight = float(str(weight).replace("kg", "").replace(",", "."))
                else:
                    weight = 0

                name = res[3]
                if name.rstrip(" ") == "":
                    name = None

                if name == None:
                    exercise.add_to_pyramid(int(reps), int(sets), float(weight))
                else:
                    exercise = Exercise(self.user, int(reps), int(sets), float(weight), name.lower(), date)
                    exercises.append(exercise)
        
        for exercise in exercises:
            exercise.upload()
        



    @staticmethod
    def find_regex_matches(regex, line):
        ergeb = []
        
        if type(regex) == list:
            for pattern in regex:
                res = re.search(pattern, line)
                if res != None:
                    ergeb.append(res.groups())
        
        else:
            res = re.search(regex, line)
            if res != None:
                ergeb.append(res.groups())
        
        return ergeb

    @staticmethod
    def get_date_obj(date, line_num):
        dt = datetime.today()

        if date[0] == None:
            raise InvalidDateFormat(f"The date on line {line_num} has an invalid format. The day must be defined")

        elif date[1] == None:

            date = datetime.strptime(f"{date[0]}.{dt.month}.{dt.year}")

        elif date[2] == None:
            date = datetime.strptime(f"{date[0]}.{date[1]}.{dt.year}", "%d.%m.%Y")
        
        else:
            if len(date[2]) == 2:
                year = "20" + date[2]
            else: 
                year = date[2]
            date = datetime.strptime(f"{date[0]}.{date[1]}.{year}", "%d.%m.%Y")
        
        return date
























