import os
import sys
sys.path.append('.')
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

DB = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

with open(os.path.join("versions", "core-version.txt"), "r") as file:
    for line in file:
        VERSION = line.rstrip("\n")
        break


