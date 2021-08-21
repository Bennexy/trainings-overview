from app.endpoints.exercise import exercise
import os
import sys
import yaml
import regex as re
from datetime import datetime
sys.path.append('.')
from app.endpoints.exercise.errors import *
from app.endpoints.exercise.exercise import Exercise
from app.logger import get_logger


logger = get_logger("logger-exercise-file-data-extractor")

def extract_data(user, file):
    
    regex_data = get_regex()[0]

    try:
        line_couter = 0
        exercises = []
        buffer = ""
        for line in file:
                line = line.decode("utf-8").rstrip("\n") 
                line_couter += 1
                typ, groups = regex_find(regex_data, line, line_couter)

                if typ == 'date':
                    date = get_date(groups, line_couter)
                if typ == 'comment':
                    pass
                if typ == 'exercise':
                    sets = groups[0]
                    reps = groups[1]
                    weight = groups[2]
                    name = groups[3]

                    if name == None or name == buffer:
                        exercise.add_to_pyramid(reps, sets, weight)
                    else:

                        buffer = name
                        exercise = Exercise(user, reps, sets, weight, name, date)
                        exercises.append(exercise)
                    


        for exercise in exercises:
            error = exercise.upload()

    except Exception as e:
        logger.error(f"{e} has occured on line {line_couter}")
        raise InvalidFileFormat(message=f"The syntax of your file is invalid on line nr: {line_couter}", previous_error=e)
        return {"message": error.message, "error": error.name}

def get_date(date, line_num):

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
    
def get_regex(template_path=None, extraction_file=None):
    if template_path == None:
        template_path = os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates"))

    onlyfiles = [f for f in os.listdir(template_path) if os.path.isfile(os.path.join(template_path, f)) and f.endswith(".yaml") or f.endswith(".yml")]

    for file in onlyfiles:
        extract_dict = []
        if extraction_file != None:
            if file in onlyfiles:
                items = yaml.load(open(os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates", extraction_file))), Loader=yaml.FullLoader)
                extract_dict.append(items)
                
            else:
                raise ExtractionTemplateNotFound(f"error no such extraction_file '{extraction_file}' found in dir")
        else:
            for file in onlyfiles:
                items = yaml.load(open(os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates", file))), Loader=yaml.FullLoader)
                extract_dict.append(items)

    return extract_dict

def regex_find(regex_patterns, string, line_num):
    for key, pattern in regex_patterns['template']['regex'].items():
        ergeb = re.search(pattern, string)
        if ergeb != None:
            return key, ergeb.groups()
    
    return None, None



































