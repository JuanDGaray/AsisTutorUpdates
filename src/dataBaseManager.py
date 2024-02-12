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
        self.bsd.commit()

    def deleteTableGroups(self):
        self.cursor.execute('DELETE FROM db_groups;')

    def addValueTableGroup(self, row):
        self.cursor.executescript(f"INSERT INTO db_groups VALUES ({(row)})")

    def save_credential(self, user, password):
        nUserMemory = self.findPassAndUserCache()
        self.openDB()
        print(user, password)
        if nUserMemory != None:
            self.cursor.execute('DELETE FROM Join_Data;')
        self.cursor.execute("INSERT INTO Join_Data (ID, User, Password) VALUES (?, ?, ?)", (1, user, password))
        self.saveDB()
        print("lo guardé")
        self.closeDB()
    
    def findPassAndUserCache(self):
        self.openDB()
        reviewValues = "SELECT COUNT(*) FROM Join_Data WHERE user IS NOT NULL"
        self.cursor.execute(reviewValues)
        result = self.cursor.fetchone()[0]
        if result > 0:
            resultUser = self.cursor.execute("SELECT User FROM Join_Data LIMIT 1").fetchone()
            user = resultUser[0]
            resultPass = self.cursor.execute("SELECT Password FROM Join_Data LIMIT 1").fetchone()
            passw = resultPass[0]
            self.closeDB()
            return [True, user, passw]
        
    def putGroupAtHome(self):
        self.openDB()
        self.cursor.execute("SELECT * FROM db_groups")
        list_group = self.cursor.fetchall()
        self.closeDB
        return list_group
    
    def addEngagementToDb(self, id, row):
        self.openDB()
        query = f"UPDATE db_groups SET pointsAttend =  ?, pointsNoAttend = ?, isGraduate = ? WHERE id_group = {id}"
        self.cursor.execute(query, row)
        self.saveDB()
        self.closeDB()
    
    def addEngagementStatusToDB(self, id, row):
        self.openDB()
        query = f"UPDATE db_groups SET engagmentInt = ?, engagmentText = ? WHERE id_group = {id}"
        self.cursor.execute(query, row)
        self.saveDB()
        self.closeDB()


    def takeEngagmenttoDb(self):
        self.openDB()
        self.cursor.execute("SELECT pointsAttend, pointsNoAttend, isGraduate FROM db_groups")
        rows = self.cursor.fetchall()
        self.closeDB()
        return rows

    

    
 