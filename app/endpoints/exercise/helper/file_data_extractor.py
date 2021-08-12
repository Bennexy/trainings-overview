import sys
sys.path.append('.')
from app.endpoints.exercise.errors import InvalidDateFormat, InvalidFileFormat

from datetime import datetime

def extract_data(file):

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

                    date = datetime.strptime(date, "%d.%m.%Y")
                except Exception:
                    error = InvalidDateFormat(message=f"Your date formating is faulty -> Line {line_couter}")
                    return {"message": error.message, "error": error.name}

            if '-' not in line[0] and '#' not in line[0] and line[0] != "":
                
                line[0] = line[0].split("x")

                while "" in line:
                    line.remove("")
                
                
                sets = line[0][0]
                reps = line[0][1]
                weight = line[1].replace("kg", "")
                if len(line) == 2:
                    name = name
                else:
                    name = ""
                    for i in range(2, len(line)):
                        name += line[i]
                
                print(int(sets), int(reps), int(weight), str(name))
                line_couter += 1





        return {"message": "Successfully added data to db"}

    except Exception as e:
        error = InvalidFileFormat(message=f"The syntax of your file is invalid on line nr: {line_couter}")
        return {"message": error.message, "error": error.name}




