
import sys
sys.path.append(".")
from datetime import datetime
from app import mycursor, mydb
from app.endpoints.user.errors import NoArgsGivenError
from app.logger import get_logger

logger = get_logger("User-class-logger")

class User:

    def __init__(self, id=None, name: str =None) -> None:
        if id == None and name == None:
            raise NoArgsGivenError(message="Please specify either name or id of the User")
        self.id = id
        self.name = name
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def create(self):

        
        
        sql = "INSERT INTO users (name, creation_date) VALUES (%s, %s)"
        val = [(self.name, self.creation_date)]

        mycursor.executemany(sql, val)
        mydb.commit()

        mycursor.execute(f"SELECT id FROM users WHERE name = '{self.name}' AND creation_date = '{self.creation_date}' ORDER BY id DESC LIMIT 1")
        self.id = mycursor.fetchall()[0]

        logger.debug(f"User {self.id, self.name} successfully created")

    def update(self, name):
        
        self.name = name

        mycursor.execute(f"UPDATE users SET name = '{self.name}' WHERE id = {self.id}")
        mydb.commit()

        logger.debug(f"User {self.id, self.name} successfully updated")

    def delete_user(self):

        mycursor.execute(f"DELETE FROM users WHERE id = {self.id}")
        mydb.commit()

