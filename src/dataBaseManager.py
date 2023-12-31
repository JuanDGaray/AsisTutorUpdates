import sqlite3 as sql
import os
from bs4 import BeautifulSoup 
import time
from datetime import datetime, timedelta

class db_manager():

    def openDB(self): 
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, 'DB', 'TutorBase1.db')
        self.bsd = sql.connect(db_path)
        self.cursor = self.bsd.cursor()

    def closeDB(self):
        self.bsd.close()

    def saveDB(self):
        return self.bsd.commit()

    def deleteTableGroups(self):
        self.cursor.execute('DELETE FROM db_groups;')

    def addValueTableGroup(self, row):
        self.cursor.executescript(f"INSERT INTO db_groups VALUES ({(row)})")

    def save_credential(self):
        self.openDB()
        self.cursor.execute(f"UPDATE Join_Data SET User = '{self.user}', Password = '{self.password}' WHERE  ID = '1'" )
        self.saveDB()
        return self.closeDB()
    
 