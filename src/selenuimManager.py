from selenium import webdriver
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading as th
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta
import time
from componentsUI import loading, home, loggin
from src import dataBaseManager
from utils import constants


driver = None
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
InstaciaADB = dataBaseManager.db_manager()

class SelenuimThreadLoggin(QThread):
    update_text_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.UserName = None
        self.UserPass = None
        self.NewLogin = None
        

    def set_credentials(self, UserName, UserPass, NewLogin):
        self.UserName = UserName
        self.UserPass = UserPass
        self.NewLogin = NewLogin 
        


    def run(self):
        global driver
        """ try:"""
        self.update_text_signal.emit("Open page Kodland...")
        driver = webdriver.Chrome(options=options)
        self.update_text_signal.emit("Comprobando credenciales...")
        self.login_scrapping1(self.UserName,self.UserPass,self.NewLogin)
        """except Exception as e:
                self.finished_signal.emit(True, f"Error: {e}")
                driver.quit()"""

    def login_scrapping1(self, UserName,UserPass,NewLogin): 
            userPortable = UserName
            passwordPortable = UserPass
               
            driver.get("https://backoffice.kodland.org/en/groups/")
            mBox = driver.find_element(by=By.CSS_SELECTOR,value='#id_username')
            mBox.send_keys(UserName)
            mBox = driver.find_element(by=By.XPATH, value='//*[@id="id_password"]')
            mBox.send_keys(UserPass)
            button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/form/button')
            button.click()  
            url_join = driver.current_url
            if url_join == 'https://backoffice.kodland.org/en/groups/':
                self.update_text_signal.emit("Extracting groups...")
                self.take_groups()
                self.update_text_signal.emit("Open groups...")
                self.finished_signal.emit(False, None)
            else:
                self.finished_signal.emit(True, None)
                driver.quit()

    def take_groups(self):
            global drive
            curso = {'802':'¡La magia del código con Scratch!', '714': 'Python', '663': 'Scratch'}
            soup = BeautifulSoup(driver.page_source, "html.parser")
            n_tablegroup = len(soup.find_all('a', class_="endless_page_link"))
            if n_tablegroup == 0:
                n_tablegroup = 1
            count=0
            InstaciaADB.openDB()
            InstaciaADB.deleteTableGroups()
            for table in range(1,n_tablegroup+1):
                n_group = int(len(soup.find_all('a', class_="table-link"))/2)
                for group in range(n_group):
                    id = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[1]').text
                    namegroup = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[2]').text
                    self.update_text_signal.emit(f"Extracting groups ({namegroup})")
                    sa = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[6]').text
                    c = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[4]').text
                    try :
                        c = curso[c[1:4]]
                    except:
                        c = 'undefine'
                    ls = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[7]').text
                    start = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[5]').text
                    start= start[:-6]
                    ahora = datetime.now()
                    try:
                        last_class = datetime.strptime(start, "%d.%m.%Y")
                        y_t = int(abs(((last_class+timedelta((int(((ahora - last_class)//7).total_seconds())//86400)*7))-ahora).total_seconds()//86400)) 
                        if y_t == 7:
                            y_t = "Mañana"
                        elif (8-y_t) == 7:
                            y_t = "Hoy"
                        else:
                            y_t = f"En {str(8-y_t)} dias"
                        s_t = str(last_class+timedelta((int(((ahora - last_class)//7).total_seconds())//86400)*7))
                        s_t= s_t[:-9]
                    except:
                        s_t = None
                        y_t = None
                    
                    row = f"{id},'{namegroup}','{sa}','{c}','{ls}','{s_t}','{y_t}'"
                    InstaciaADB.addValueTableGroup(row)
                if table < n_tablegroup:
                    if table == 1:
                        link = 2
                    else:
                        link = table+2
                    driver.find_element(by=By.CSS_SELECTOR, value=f'#table_to_change >ul>li:nth-child({link}) > a').click()
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source)
            InstaciaADB.saveDB()
            return InstaciaADB.closeDB()

class seleniumTakeMetricsByGroupBasic():

    def findPoints(self, id, totalStudents):
        if totalStudents > 0:
            driver.get(f"https://backoffice.kodland.org/en/group_{id}/")
            time.sleep(2)
            ranks = driver.find_elements(By.CLASS_NAME, "table_student-rank")
            n_class= self.waitElement(driver, constants.textXPathgroup['Lessons completed']).text.split('/')
            n_class = int(n_class[0])
            id_course= self.waitElement(driver, constants.textXPathgroup['Course']).text.split(' ')
            if id_course[0] == '[802]¡La':
                id_course = ['[802]']
            total_Points_By_Actual_Lesson = sum(constants.points_total_course_latam[id_course[0]][0:n_class])
            totalPoints = total_Points_By_Actual_Lesson * totalStudents
            totalPointsByStudents = 0
            
            for element in ranks:
                point = element.text.split('/')
                point = int(point[-1])
                totalPointsByStudents += point
            print(f'ID {id}: {totalPointsByStudents}/{totalPoints}')
            if totalPoints == 0 or totalPointsByStudents == 0:
                return[0,0]
            totalPointsByStudentsPercent = (totalPointsByStudents/totalPoints)*100
            totalPointsNoAttendPercent = 100 - totalPointsByStudentsPercent
            print(f'ID {id}: {totalPointsByStudentsPercent}/{totalPointsNoAttendPercent}, numero de clase: {n_class}, numero de estudiantes {totalStudents}')
            return [totalPointsNoAttendPercent, totalPointsByStudentsPercent]
        else:
            return[0,0]

    def waitElement(self, driver, XPATH):
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPATH))
        )