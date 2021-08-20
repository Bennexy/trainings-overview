import os
import sys
import yaml
import regex as re
from datetime import datetime
sys.path.append('.')
from app.endpoints.exercise.errors import InvalidDateFormat, InvalidFileFormat, ExtractionTemplateNotFound
from app.endpoints.exercise.exercise import Exercise
from app.logger import get_logger


logger = get_logger("logger-exercise-file-data-extractor")

def extract_data(user, file):

    regex_data = get_regex()

    try:
        with open(file, "r") as file:
            for line in file:
                regex_find(line, regex_data)

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

def get_regex(template_path=None, extraction_file=None):

    if template_path == None:
        template_path = os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates"))

    onlyfiles = [f for f in os.listdir(template_path) if os.path.isfile(os.path.join(template_path, f)) and f.endswith(".yaml") or f.endswith(".yml")]

    for file in onlyfiles:
        extract_dict = []
        if extraction_file != None:
            if file in onlyfiles:
                items = yaml.load(open(os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates", extraction_file))), Loader=yaml.FullLoader)                
            else:
                raise ExtractionTemplateNotFound(f"error no such extraction_file '{extraction_file}' found in dir")
        else:
            for file in onlyfiles:
                items = yaml.load(open(os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates", "main.yaml"))), Loader=yaml.FullLoader)

    return items

def regex_find(string, regex_data):
    for key, pattern in regex_data['template']['regex'].items():
        if key.lower() != 'comment':
            re.search(regex_data, pattern)

































