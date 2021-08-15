import sys
import json
sys.path.append('.')

from datetime import datetime
from app.endpoints.exercise.errors import InvalidDateFormat


d = """{"name": "Kreuzheben ", "reps": [12, 12, 12, 6, 6, 12, 12], "sets": [1, 1, 1, 2, 2, 1, 1], "weight": [70.0, 80.0, 90.0, 95.0, 90.0, 80.0, 70.0]}"""

d = json.loads(d)

print(type(d))



