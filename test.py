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


date = "24.07.2021"
date = date.split(".")

print(date)

dt = datetime.today()

if len(date) == 1:

    date = datetime.strptime(f"{date[0]}.{dt.month}.{dt.year}", "%d.%m.%Y")
    print(date)

elif len(date) == 2:

    date = datetime.strptime(f"{date[0]}.{date[1]}.{dt.year}", "%d.%m.%Y")
    print(date)

elif len(date) == 3:

    date = datetime.strptime(f"{date[0]}.{date[1]}.{date[2]}", "%d.%m.%Y")
    print(date)










