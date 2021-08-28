import sys
sys.path.append('.')
import os, yaml
import regex as re
import datetime
import json

tup = ('Liegestützen', datetime.datetime(2021, 8, 27, 0, 0), '{"name": "Liegestützen", "reps": ["40"], "sets": [1], "weight": [0]}')

dic = json.loads(tup[2])
print(dic['weight'])


