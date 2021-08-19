import os
import sys
import yaml
from datetime import datetime
sys.path.append('.')
from app.endpoints.exercise.errors import InvalidDateFormat, InvalidFileFormat
from app.endpoints.exercise.exercise import Exercise
from app.logger import get_logger

logger = get_logger("logger-exercise-file-data-extractor")

def extract_data(user, file):

    exercises = []
    try:
        line_couter = 1
        for line in file:
            line = line.decode("utf-8").rstrip("\n") 
            
            line = line.split(" ")

            if '-' in line[0]:
                try:

                    if '-' == line[0]:
                        date = line[1]
                    elif '-' in line[0]:
                        date = line[0].replace('-', "")
                    else:
                        raise InvalidDateFormat(message=f"Your date formating is faulty -> Line {line_couter}")
                    date = get_date(date, line_couter)
                except Exception as e:
                    logger.error(e)
                    error = InvalidDateFormat(message=f"Your date formating is faulty -> Line {line_couter}")
                    return {"message": error.message, "error": error.name}

            if '-' not in line[0] and '#' not in line[0] and line[0] != "":
                
                line[0] = line[0].split("x")

                while "" in line:
                    line.remove("")
                
                
                sets = int(line[0][0])
                reps = int(line[0][1])
                weight = float(line[1].replace("kg", "").replace(",", "."))
                if len(line) == 2:
                    exercise.add_to_pyramid(reps, sets, weight)
                
                else:
                    name = ""
                    for i in range(2, len(line)):
                        name += line[i] + " "

                    exercise = Exercise(user, reps, sets, weight, name, date)
                    exercises.append(exercise)

            
            line_couter += 1



        for exercise in exercises:
            error = exercise.upload()

            if error != None:
                return error

        return None

    except Exception as e:
        logger.error(f"{e} has occured on line {line_couter}")
        raise InvalidFileFormat(message=f"The syntax of your file is invalid on line nr: {line_couter}", previous_error=e)
        return {"message": error.message, "error": error.name}


def get_date(date_in, line):

    date = date_in.split(".")
    dt = datetime.today()

    if len(date) == 1:

        date = datetime.strptime(f"{date[0]}.{dt.month}.{dt.year}", "%d.%m.%Y")
        return date

    elif len(date) == 2:

        date = datetime.strptime(f"{date[0]}.{date[1]}.{dt.year}", "%d.%m.%Y")
        return date
    
    elif len(date) == 3:
        if len(date[2]) == 2:
            date[2] = "20" + date[2]

        date = datetime.strptime(f"{date[0]}.{date[1]}.{date[2]}", "%d.%m.%Y")
        return date
    
    #else:
    #    raise InvalidDateFormat(f"Your date formating is invalid -> line {line}. Date given -> {date} must have this format: dd or dd.mm or dd.mm.yy")


def get_regex(template_path=None):
    if template_path == None:
        template_path = os.path.abspath(os.path.join("app", "endpoints", "exercise","templates"))
        dict = yaml.load(template_path)



































