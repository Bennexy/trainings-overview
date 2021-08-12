import sys
sys.path.append('.')

from datetime import datetime
from app.endpoints.exercise.errors import InvalidDateFormat

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

date_ = "80.09.2021"

# print(datetime.strptime(date_, "%dd.%mm.%YYYY"))


lines = [['-', '08.09.2021', 'Brust'], ['-08.09.2021', 'Brust']]



for line in lines:
    if '-' == line[0]:
        date = line[1]
    elif '-' in line[0]:
        date =  line[0].replace('-', "")
    else: 
        raise InvalidDateFormat
    
    # date.split('.')
    # print(date)
    date = datetime.strptime(date, "%d.%m.%Y")

    print(date)














