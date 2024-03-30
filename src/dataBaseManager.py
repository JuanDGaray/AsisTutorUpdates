import sqlite3 as sql
import os
from bs4 import BeautifulSoup 
import time
from datetime import datetime, timedelta
import sqlite3

class db_manager():
    """
    A class to manage the SQLite database.

    Attributes:
        bsd: SQLite database connection.
        cursor: Cursor to execute SQL queries.
    """

    def openDB(self): 
        """
        Opens the SQLite database connection.
        """
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, 'DB', 'TutorBase1.db')
        self.bsd = sql.connect(db_path)
        self.cursor = self.bsd.cursor()

    def closeDB(self):
        """
        Closes the SQLite database connection.
        """
        self.bsd.close()

    def saveDB(self):
        """
        Saves changes to the SQLite database.
        """
        self.bsd.commit()

    def deleteTableGroups(self):
        """
        Deletes all records from the 'db_groups' table.
        """
        self.cursor.execute('DELETE FROM db_groups;')

    def addValueTableGroup(self, row):
        """
        Adds a row of values to the 'db_groups' table.

        Parameters:
            row (str): Values to be added in a SQL format.
        """
        self.cursor.executescript(f"INSERT INTO db_groups VALUES ({(row)})")

    def save_credential(self, user, password, name):
        """
        Saves user credentials to the 'Join_Data' table.

        Parameters:
            user (str): User's username.
            password (str): User's password.
        """
        nUserMemory = self.findPassAndUserCache()
        self.openDB()
        print(user, password)
        if nUserMemory != None:
            self.cursor.execute('DELETE FROM Join_Data;')
        self.cursor.execute("INSERT INTO Join_Data (ID, User, Password, name) VALUES (?, ?, ?, ?)", (1, user, password, name))
        self.saveDB()
        self.closeDB()
    
    def findPassAndUserCache(self):
        """
        Finds and retrieves cached user credentials from the database.

        Returns:
            list: List containing cached user credentials.
        """
        self.openDB()
        reviewValues = "SELECT COUNT(*) FROM Join_Data WHERE user IS NOT NULL"
        self.cursor.execute(reviewValues)
        result = self.cursor.fetchone()[0]
        if result > 0:
            resultUser = self.cursor.execute("SELECT User FROM Join_Data LIMIT 1").fetchone()
            user = resultUser[0]
            resultPass = self.cursor.execute("SELECT Password FROM Join_Data LIMIT 1").fetchone()
            passw = resultPass[0]
            name = self.cursor.execute("SELECT Name FROM Join_Data LIMIT 1").fetchone()
            self.closeDB()
            return [True, user, passw, name]
        
    def putGroupAtHome(self):
        """
        Retrieves a list of groups from the database.

        Returns:
            list: List of groups.
        """
        try:
            self.openDB()
            select_query = "SELECT * FROM db_groups ORDER BY id_group DESC"
            list_group = self.cursor.execute(select_query).fetchall()
            return list_group
        except sqlite3.Error as e:
            print("Error en la base de datos:", e)
        finally:
            self.saveDB()
            self.closeDB()


    def getNonGraduatedGroups(self):
        """
        Retrieves non-graduated groups from the database.

        Returns:
            list: List of non-graduated groups.
        """
        self.openDB()
        self.cursor.execute("SELECT * FROM db_groups WHERE isGraduate != 'yes'")
        list_non_graduated_groups = self.cursor.fetchall()
        self.closeDB()
        return list_non_graduated_groups
    
    def getNoGraduatedGroupsByID(self):
        """
        Retrieves non-graduated groups sorted by ID from the database.

        Returns:
            list: List of non-graduated groups sorted by ID.
        """
        self.openDB()
        self.cursor.execute("SELECT * FROM db_groups WHERE isGraduate != 'yes' ORDER BY id_group DESC")
        GraduatedGroupsByID = self.cursor.fetchall()
        self.closeDB()
        return GraduatedGroupsByID
    
    def getNoGraduatedGroupsByEngagement(self):
        """
        Retrieves non-graduated groups sorted by engagement from the database.

        Returns:
            list: List of non-graduated groups sorted by engagement.
        """
        self.openDB()
        self.cursor.execute("SELECT * FROM db_groups WHERE isGraduate != 'yes' ORDER BY engagmentInt DESC")
        GraduatedGroupsByengagement = self.cursor.fetchall()
        self.closeDB()
        return GraduatedGroupsByengagement
    
    def getNoGraduatedGroupsByNearestClass(self):
        """
        Retrieves non-graduated groups sorted by nearest class from the database.

        Returns:
            list: List of non-graduated groups sorted by nearest class.
        """
        self.openDB()
        self.cursor.execute("""
            SELECT * FROM db_groups
            WHERE isGraduate != 'yes'
            ORDER BY CASE
                WHEN next_class IN ('Today', 'Hoy') THEN 1
                WHEN next_class IN ('Tomorrow', 'Mañana') THEN 2
                WHEN next_class IN ('in 2 days', 'En 2 dias') THEN 3
                WHEN next_class IN ('in 3 days', 'En 3 dias') THEN 4
                WHEN next_class IN ('in 4 days', 'En 4 dias') THEN 5
                WHEN next_class IN ('in 5 days', 'En 5 dias') THEN 6
                ELSE 7
            END
        """)        
        GraduatedGroupsByNearestClass = self.cursor.fetchall()
        self.closeDB()
        return GraduatedGroupsByNearestClass
    
    def addEngagementToDb(self, id, row):
        """
        Updates engagement-related fields in the 'db_groups' table for a specific group.

        Parameters:
            id (int): ID of the group to update.
            row (tuple): Tuple containing values for 'pointsAttend', 'pointsNoAttend', and 'isGraduate'.
        """
        self.openDB()
        update_query = "UPDATE db_groups SET pointsAttend = ?, pointsNoAttend = ?, isGraduate = ? WHERE id_group = ?"
        self.cursor.execute(update_query, row + (id,))
        self.saveDB()
        self.closeDB()
    
    def addEngagementStatusToDB(self, id, row):
        """
        Updates engagement status fields in the 'db_groups' table for a specific group.

        Parameters:
            id (int): ID of the group to update.
            row (tuple): Tuple containing values for 'engagmentInt' and 'engagmentText'.
        """
        self.openDB()
        query = f"UPDATE db_groups SET engagmentInt = ?, engagmentText = ? WHERE id_group = {id}"
        self.cursor.execute(query, row)
        self.saveDB()
        self.closeDB()


    def takeEngagmenttoDb(self):
        """
        Retrieves engagement-related fields from the 'db_groups' table.

        Returns:
            list: List of tuples containing 'pointsAttend', 'pointsNoAttend', and 'isGraduate'.
        """
        self.openDB()
        self.cursor.execute("SELECT pointsAttend, pointsNoAttend, isGraduate FROM db_groups")
        rows = self.cursor.fetchall()
        self.closeDB()
        return rows
    
    def  updateScoreByGroup(self, nameGroup, pointsUpdates):
        self.openDB()
        self.cursor.execute( f"SELECT pointsAttend FROM db_groups WHERE id_group = {nameGroup}")
        valor = self.cursor.fetchone()[0]
        if valor != pointsUpdates:
            update_query = f"UPDATE db_groups SET pointsAttend = ? WHERE id_group = ?"
            self.cursor.execute(update_query, (pointsUpdates, nameGroup))
            self.saveDB()
        self.closeDB()

    

    
 