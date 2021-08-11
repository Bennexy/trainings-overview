import sys
sys.path.append('.')
from app.config import DB, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
import mysql.connector



def db_init():
    mydb = mysql.connector.connect(host=DB, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
    mycursor = mydb.cursor()
    mycursor.execute("USE " + str(DB_NAME))
    return mycursor, mydb