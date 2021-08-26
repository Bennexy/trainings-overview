import os
import sys
sys.path.append(".")

from dotenv import find_dotenv, load_dotenv

import mysql.connector

load_dotenv(find_dotenv())

DB = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

mydb = mysql.connector.connect(host=DB, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
mycursor = mydb.cursor()
mycursor.execute("USE " + str(DB_NAME))


def trunicate_exercise():
    mycursor.execute("TRUNCATE exercise")
    mydb.commit()

trunicate_exercise()

