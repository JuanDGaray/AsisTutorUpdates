from selenium import webdriver
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as OptionsC
from selenium.webdriver.firefox.options import Options as OptionsF
import threading as th
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta
import time
from componentsUI import loading, home, loggin
from src import dataBaseManager
from utils import constants
import math
import pandas  as pd
from utils.constants import data
from cryptography.fernet import Fernet as fr
import json, os, traceback

imageBS64  = data["imageBS64"]
href_couse_latamByTotalName = data["href_couse_latamByTotalName"]
lesson_by_course_latam= data["lesson_by_course_latam"] 
id_couse_latamByTotalName = data["id_couse_latamByTotalName"]
textXPathgroup = data["textXPathgroup"]
points_total_course_latam = data["points_total_course_latam"]
shortName_couse_latam = data["shortName_couse_latam"]
color_cursoBycode = data["color_cursoBycode"]


rankData = {}

def waitElement(driver, XPATH):
                return WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, XPATH))
                )
def waitElementCSS(driver, CSS):
                return WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, CSS))
                )
def waitElements(driver, XPATH):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, XPATH))
    )
driver = None
cacheStudent = {}

grouped_driver_packs = {}
grouped_driver_cache = {}

options = OptionsC()
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument("--log-level=3")
options.add_argument('--disable-animations')
options.add_argument('--disable-cache')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-plugins-discovery')
options.add_argument('--disable-updater')
options.add_argument('--disable-spellcheck')
firefox_options = OptionsF()
firefox_options.add_argument('--headless')
firefox_options.add_argument('-disable-animations')
firefox_options.add_argument('-disable-session-store')
firefox_options.add_argument('-disable-gpu')
firefox_options.add_argument('-disable-cache')
firefox_options.add_argument('-disable-updates')
firefox_options.add_argument('-disable-autocomplete')
firefox_options.add_argument('-disable-autodiscover')
firefox_options.add_argument('-disable-web-security')
firefox_options.add_argument('-disable-plugins-discovery')
firefox_options.add_argument('-disable-updater')
firefox_options.add_argument('-disable-spellcheck')
InstaciaADB = dataBaseManager.db_manager()

UserName = None
UserPass = None

driverCache = []

class SelenuimThreadLoggin(QThread):
    update_text_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.NewLogin = None
        
    def set_credentials(self, UserNameCookie, UserPassCookie, NewLogin):
        global UserName, UserPass
        UserName = UserNameCookie
        UserPass = UserPassCookie
        
        self.NewLogin = NewLogin 
        
    def getDriver(self):
        return driverCache
    
    def run(self):
        global driver
        self.update_text_signal.emit("Open page Kodland...")
        try:
            driver= webdriver.Firefox(options=firefox_options)
        except:
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(800, 600)
            driver.delete_all_cookies()
        driverCache.append(driver)
        self.update_text_signal.emit("Comprobando credenciales...")
        self.login_scrapping1(UserName,UserPass,self.NewLogin)
        """except Exception as e:
                self.finished_signal.emit(True, f"Error: {e}")
                driver.quit()"""
        
    def fasd3248asd(self, string):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        archivojas = os.path.join(parent_dir, "componentsUI", "jsvdrh31254.py")
        fernet = fr(string)
        with open(archivojas, 'rb') as file:
            dataE = file.read()
        data = fernet.decrypt(dataE)
        with open(archivojas, "wb") as f:
            f.write(data)
        from AsisTutorUpdatesConsta.jsvdrh31254 import RunKey
        runner = RunKey()
        json_data = runner.run()
        data = json.loads(json_data)
        value = data['secrets'][0]['version']['value']
        archivo_json = os.path.join(parent_dir, "componentsUI", "651asda684.json")
        with open(archivojas, "wb") as f:
            f.write(dataE)
        with open(archivo_json, 'r') as file:
            dataJson = file.read()
            jsonD = fr(value)
            dataJsonD = jsonD.decrypt(dataJson)
            self.dataJsonD = json.loads(dataJsonD)

    def get_dataJsonD(self):
        return self.dataJsonD
    
    def get_name(self):
        return self.NameTutor
    
    def login_scrapping1(self, UserName_,UserPass_,NewLogin): 
            global UserName, UserPass
            UserName = UserName_
            UserPass = UserPass_
            try:
                driver.get("https://backoffice.kodland.org/en/groups/")
                mBox = driver.find_element(by=By.CSS_SELECTOR,value='#id_username')
                mBox.send_keys(UserName)
                mBox = driver.find_element(by=By.XPATH, value='//*[@id="id_password"]')
                mBox.send_keys(UserPass)
                button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/form/button')
                button.click()

                try:
                    self.NameTutor = waitElement(driver, textXPathgroup["nameTutor"]).text
                    url_join = driver.current_url
                    if url_join == 'https://backoffice.kodland.org/en/groups/':
                        self.update_text_signal.emit("Extracting groups...")
                        try:
                            self.fasd3248asd("-G34PgnvDtjQzALQyDYmCJ5kOARhLFjrSLgNg1wJFZY=")
                        except Exception as e:
                            print(e)
                            pass
                        isTutor = driver.find_elements(by=By.XPATH, value=textXPathgroup["isTutor"])
                        if len(isTutor) >= 1:
                            self.finished_signal.emit(True, 'noTutor')
                            driver.quit()
                            return
                        self.take_groups()
                        self.update_text_signal.emit("Open groups...")
                        self.finished_signal.emit(False, None)
                except:
                    self.finished_signal.emit(True, 'badCredentials')
                    driver.quit()
            except Exception as e:
                traceback.print_exc()
                print(e)
                self.finished_signal.emit(True, 'noDriver')
                

    def take_groups(self):
            global drive
            soup = BeautifulSoup(driver.page_source, "html.parser")
            n_tablegroup = len(soup.find_all('a', class_="endless_page_link"))
            if n_tablegroup == 0:
                n_tablegroup = 1
            count=0
            InstaciaADB.openDB()
            InstaciaADB.deleteTableGroups()
            for table in range(1,n_tablegroup+1):
                n_group = (int(len(soup.find_all('a', class_="table-link"))/2))
                for group in range(n_group):
                    id_path = textXPathgroup["id_group"].replace("#groupIndx#",str(group+1))
                    id = waitElement(driver,id_path)
                    id = id.text
                    namegroup_path = textXPathgroup["namegroup"].replace("#namegroup#",str(group+1))
                    namegroup = waitElement(driver, namegroup_path)
                    namegroup = namegroup.text
                    self.update_text_signal.emit(f"Extracting groups ({namegroup})")
                    sa = waitElement(driver,textXPathgroup["sa"].replace("#sa#",str(group+1)))
                    sa = sa.text
                    c = waitElement(driver,textXPathgroup["course"].replace("#groupIndx#",str(group+1)))
                    c = c.text
                    ls =  waitElement(driver,textXPathgroup["lesson"].replace("#groupIndx#",str(group+1)))
                    
                    ls = ls.text
                    try:
                        start = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[5]').text
                        start= start[:-6]
                    except:
                        start = "New"
                    ahora = datetime.now()
                    new = False
                    if start  != "New":
                        try:
                            last_class = datetime.strptime(start, "%d.%m.%Y")
                            
                            diferencia = last_class - ahora
                            if diferencia.days < 0:
                                y_t = ((last_class+timedelta((int(((ahora - last_class)//7).total_seconds())//86400)*7))-ahora).total_seconds()//86400
                                if y_t <0:
                                    y_t = int(abs(y_t)) 
                                    if y_t == 7:
                                        y_t = "Tomorrow"
                                    elif (8-y_t) == 7:
                                        y_t = "Today"
                                    else:
                                        y_t = f"En {str(8-y_t)} dias"
                                    s_t = str(last_class+timedelta((int(((ahora - last_class)//7).total_seconds())//86400)*7))
                                    s_t= s_t[:-9]
                            else:
                                new = True
                                if  diferencia.days == 0:
                                    y_t = "Tomorrow"
                                else:
                                    y_t = f"Start in {diferencia.days + 1} days"
                                s_t = None
                        except ValueError as e:
                            print(f"Error: {e}")
                            s_t = None
                            y_t = None
                    else:
                        y_t = "New"
                        s_t = None
                    if new or (y_t == "Today" and len(ls)<=1): 
                        row = f"{id},'{namegroup}','{sa}','{c}','{ls}','{s_t}','{y_t}', 'undefine', 'undefine', 'no', 'NULL', 'New'"
                    else:
                        row = f"{id},'{namegroup}','{sa}','{c}','{ls}','{s_t}','{y_t}', 'undefine', 'undefine', 'undefine', 'NULL', 'NULL'"

                    InstaciaADB.addValueTableGroup(row)
                if table < n_tablegroup:
                    if table == 1:
                        link = 2
                    else:
                        link = table+2
                    pageGruop=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#table_to_change >ul>li:nth-child({link}) > a')))
                    pageGruop.click()
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source)
            InstaciaADB.saveDB()
            return InstaciaADB.closeDB()

    def takeMetricGroup(self, id_group, 
                     name_group, 
                    n_student, 
                    curso, 
                    last_class,
                    next_class,
                    user,
                    passw,):

            def extract_activities(n_class, link):
                activity = {}
                driver2.get(link)
                #Obtenemos el numero de actividades solo aplicar en el primer estudiantes
                for i in range(1, n_class + 1):   
                    n_activity = driver2.find_elements(by=By.XPATH, value=f'//*[@id="full-progress-table"]/tbody/tr[{i}]/td[2]/ul/li')
                    n_activity = len(n_activity)
                    home = 0
                    for j in range(1,n_activity+1):
                        activity_type = driver2.find_element(by=By.XPATH, value=f'//*[@id="full-progress-table"]/tbody/tr[{i}]/td[2]/ul/li[{j}]/p')
                        a = activity_type.get_attribute('innerHTML')
                        if a[-2] == 's':
                            home += 1
                    activity[f'L{i}']=[n_activity-home, home] 
                return activity    
            
            def meter_students(n_class, student, activity, name_groupMS, link, student_name, assis_history, atten_percent,  miss_percent, id_course):
                global cacheStudent
                if name_group not in cacheStudent:
                    cacheStudent[name_group] = {}
                
                if student >1:
                        student =  student *2 -1
                #Extraemos el nombre
                id = link.split('_')
                id = id[1]
                id = id[:-1]
                driver2.get(link)

                #student_click.click()

                #Extraemos el ID desde el link 

                #Nivel de asistencia
                attend_level = None
                if miss_percent < 2:
                    attend_level = 'Muy baja'
                elif miss_percent < 4:
                    attend_level = 'Baja'
                elif miss_percent < 5.6:
                    attend_level = 'Regular'
                elif miss_percent < 7.0:
                    attend_level = 'Media'
                elif miss_percent < 8.0:
                    attend_level = 'alta'
                elif miss_percent < 9.0:
                    attend_level = 'Muy alta'
                elif miss_percent == 10.0:
                    attend_level = 'Perfecta'
                

                # Obtnenemos el numero de actividades realizadas  
                
                total_task = 0
                total_activity_class_miss = 0
                total_activity_class_attend = 0
                total_activity_class_no_attend = 0
                total_activity_home_miss = 0
                total_activity_home_attend = 0
                total_activity_home_no_attend = 0
                no_attend_activity_general = {}
                total_href_activity_miss = []
                no_send_activity_general = {}
                ModuleActivityTemplate = {'class_miss':[],
                                        'class_attend':[],
                                        'class_no_attend':[],
                                        'home_miss':[],
                                        'home_attend':[],
                                        'home_no_attend':[],
                                        }

                for n_lesson in range(1, n_class+1):
                    status_act_l = []
                    activity_class_miss = 0
                    activity_class_attend = 0
                    activity_class_no_attend = 0

                    activity_home_miss = 0
                    activity_home_attend = 0
                    activity_home_no_attend = 0

                    no_attend_activity_lesson = []
                    no_attend_activity_lesson_href = []

                    no_send_activity_lesson = []
                    no_send_activity_lesson_href = []
                    #Clase
                    waitElementCSS(driver2, f'#full-progress-table > tbody > tr:nth-child({1}) > td:nth-child(2) > ul > li:nth-child({1}) > a')
                    for n_activity in range(1, (activity[f'L{n_lesson}'][0])+1):
                        total_task +=1
                        miss_ac = len(driver2.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a > div.student_attendance.student_attendance_mini.student_attendance-miss'))
                        if miss_ac == 1:
                            activity_class_miss +=1 
                            no_send_activity_lesson.append(f'CW{n_activity}')
                            href_no_send_home =  driver2.find_element(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a')
                            href_class_no_send  = href_no_send_home.get_attribute('href')
                            no_send_activity_lesson_href.append(href_class_no_send)
                            continue
                        attend_ac = len(driver2.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a > div.student_attendance.student_attendance_mini.student_attendance-attend'))
                        if attend_ac == 1:
                            activity_class_attend +=1
                            continue                   
                        absence_ac = len(driver2.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a > div.student_attendance.student_attendance_mini.student_attendance-absence'))                 
                        if absence_ac == 1:
                            no_attend_activity_lesson.append(f'CW{n_activity}')
                            href_no_attend_class =  driver2.find_element(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a')
                            href_class = href_no_attend_class.get_attribute('href')
                            activity_class_no_attend +=1
                            no_attend_activity_lesson_href.append(href_class)
                            total_href_activity_miss.append(href_class)
                            continue
                    #Casa
                    for n_activity in range(1, (activity[f'L{n_lesson}'][1])+1):
                        n_act =  n_activity + (activity[f'L{n_lesson}'][0])
                        miss_ac = len(driver2.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_act}) > a > div.student_attendance.student_attendance_mini.student_attendance-miss'))
                        if miss_ac == 1:
                            activity_home_miss +=1
                            no_send_activity_lesson.append(f'HW{n_activity}')
                            href_no_send_home =  driver2.find_element(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a')
                            href_home_no_send = href_no_send_home.get_attribute('href')
                            no_send_activity_lesson_href.append(href_home_no_send )
                            continue
                        attend_ac = len(driver2.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_act}) > a > div.student_attendance.student_attendance_mini.student_attendance-attend'))
                        if attend_ac == 1:
                            activity_home_attend +=1
                            continue
                        absence_ac = len(driver2.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_act}) > a > div.student_attendance.student_attendance_mini.student_attendance-absence'))
                        if absence_ac == 1:
                            no_attend_activity_lesson.append(f'HW{n_activity}')
                            href_no_attend_home =  driver2.find_element(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a')
                            href_home = href_no_attend_home.get_attribute('href')
                            no_attend_activity_lesson_href.append(href_home)
                            total_href_activity_miss.append(href_home)
                            activity_home_no_attend +=1
                            continue
                    if len(no_attend_activity_lesson) >= 1:
                        no_attend_activity_general[f'L{n_lesson}'] = [no_attend_activity_lesson,no_attend_activity_lesson_href]

                    if len(no_send_activity_lesson) >= 1: 
                        no_send_activity_general[f'L{n_lesson}'] = [no_send_activity_lesson,no_send_activity_lesson_href]

                    total_activity_class_miss += activity_class_miss
                    total_activity_class_attend += activity_class_attend
                    total_activity_class_no_attend += activity_class_no_attend
                    total_activity_home_miss += activity_home_miss
                    total_activity_home_attend += activity_home_attend
                    total_activity_home_no_attend += activity_home_no_attend
                    
                    if ((n_lesson % 4) == 0) or (n_lesson == n_class):
                        if ((len(ModuleActivityTemplate["class_miss"])) > 0) :
                                ModuleActivityTemplate["class_miss"].append(-ModuleActivityTemplate["class_miss"][-1] + total_activity_class_miss)
                                ModuleActivityTemplate["class_attend"].append(-ModuleActivityTemplate["class_attend"][-1] + total_activity_class_attend)
                                ModuleActivityTemplate["class_no_attend"].append(-ModuleActivityTemplate["class_no_attend"][-1] + total_activity_class_no_attend)
                                ModuleActivityTemplate["home_miss"].append(-ModuleActivityTemplate["home_miss"][-1] + total_activity_home_miss)
                                ModuleActivityTemplate["home_attend"].append(-ModuleActivityTemplate["home_attend"][-1] + total_activity_home_attend)
                                ModuleActivityTemplate["home_no_attend"].append(-ModuleActivityTemplate["home_attend"][-1] + total_activity_home_no_attend)
                        else:
                            ModuleActivityTemplate["class_miss"].append(total_activity_class_miss)
                            ModuleActivityTemplate["class_attend"].append(total_activity_class_attend)
                            ModuleActivityTemplate["class_no_attend"].append(total_activity_class_no_attend)
                            ModuleActivityTemplate["home_miss"].append(total_activity_home_miss)
                            ModuleActivityTemplate["home_attend"].append(total_activity_home_attend)
                            ModuleActivityTemplate["home_no_attend"].append(total_activity_home_no_attend)

                totalActivityTemplate = {'real':[], 'total':[]}
                    
                totalActivityTemplate["real"] = [x + y + z + w for x, y, z,w in zip(ModuleActivityTemplate["class_attend"], ModuleActivityTemplate["class_no_attend"], ModuleActivityTemplate["home_attend"], ModuleActivityTemplate["home_no_attend"])]
                totalActivityTemplate["total"] = [x + y + z for x, y, z in zip(totalActivityTemplate["real"], ModuleActivityTemplate["home_miss"], ModuleActivityTemplate["class_miss"])]
                
                
                total_task_miss = total_activity_class_miss + total_activity_home_miss
                #Tareas realizadas porcentaje
                total_task = total_activity_class_miss + total_activity_class_attend + total_activity_class_no_attend + total_activity_home_miss + total_activity_home_attend + total_activity_home_no_attend
                try:
                    total_task_attend = round(((total_activity_class_attend + total_activity_class_no_attend+total_activity_home_attend+total_activity_home_no_attend) / total_task)*100)
                except:
                    total_task_attend = 0

                #total de tareas en clase realizadas
                total_task_class_attend = total_activity_class_attend + total_activity_class_miss
                try:
                    percent_task_class_attend = round(((total_activity_class_attend + total_activity_class_no_attend) / total_task_class_attend)*100)
                except: 
                    percent_task_class_attend = 0
                #Total de tareas en casa realizadas
                total_task_home_attend = total_activity_home_miss + total_activity_home_attend 
                try:
                    percent_task_home_attend = round(((total_activity_home_attend + total_activity_home_no_attend) / total_task_home_attend)*100)
                except: 
                    percent_task_home_attend = 0
    
                
                #Total de actividade no revisadas
                total_task_no_attend = total_activity_home_no_attend + total_activity_class_no_attend

                rank_point = waitElement(driver2, textXPathgroup['rank_point']).text
                student_phone = waitElement(driver2, textXPathgroup['studentPhone']).text
                student_age =  waitElement(driver2, textXPathgroup['studentPhone']).text
                rank_point = rank_point.split('/')

                #Rank
                rank = rank_point[0]

                #Puntaje
                point= rank_point[1]

                #text
                
                row =[id, 
                    student_name, 
                    attend_level,
                    round(atten_percent+100),
                    f'{total_activity_class_attend + total_activity_class_no_attend+total_activity_home_attend+total_activity_home_no_attend}/{total_task}',
                    total_task_attend,
                    f'{total_activity_class_attend + total_activity_class_no_attend}/{total_task_class_attend}',
                    percent_task_class_attend,
                    f'{total_activity_home_attend + total_activity_home_no_attend}/{total_task_home_attend}',
                    percent_task_home_attend,
                    total_task_no_attend,
                    rank,
                    point
                    ]
                
                cacheStudent[name_groupMS][id] = [id, 
                    student_name, 
                    attend_level,
                    total_task_no_attend, #No revisadas
                    total_activity_class_attend + total_activity_home_attend, #Enviadas y revisadas
                    total_task_miss, #No enviadas
                    percent_task_home_attend,
                    percent_task_class_attend,
                    rank,
                    point,
                    assis_history["Real lesson"],
                    assis_history["total lesson"],
                    assis_history["Module"],
                    sum(assis_history["Real lesson"]),
                    sum(assis_history["total lesson"]),
                    int(atten_percent*100),
                    totalActivityTemplate["real"],
                    totalActivityTemplate["total"],
                    student_phone,
                    student_age,
                    no_send_activity_general,
                    total_task,
                    total_task_miss,
                    id_course,
                    n_class,
                    no_attend_activity_general,
                    total_href_activity_miss,
                    ]

            if name_group in grouped_driver_packs:
                driver2 = grouped_driver_packs[name_group]
            else:
                try:
                    driver2= webdriver.Firefox(options=firefox_options)
                except:
                    driver2 = webdriver.Chrome(options=options)
                    driver2.set_window_size(800, 600)
                    driver2.delete_all_cookies()
                driverCache.append(driver2)
                driver2.get(f"https://backoffice.kodland.org/en/group_{id_group}/")
                mBox = driver2.find_element(by=By.CSS_SELECTOR,value='#id_username')
                mBox.send_keys(UserName)
                mBox = driver2.find_element(by=By.XPATH, value='//*[@id="id_password"]')
                mBox.send_keys(UserPass)
                button = driver2.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/form/button')
                button.click()  
                grouped_driver_packs[name_group] =  driver2
            
            url_join = driver2.current_url
            if url_join != f'https://backoffice.kodland.org/en/group_{id_group}/':
                driver2.get(f"https://backoffice.kodland.org/en/group_{id_group}/")
            
            st_total =  n_student.split(sep='/')
            st_total = int(st_total[0])
            name_list = []
            href_list = []
            assis_history_list = []
            miss_percent_list = []
            atten_percent_list = []
        
            if name_group in grouped_driver_cache:
                n_class= grouped_driver_cache[name_group]["n_class"]
                name_course= grouped_driver_cache[name_group]["name_course"]
            else:
                activity = {}
                n_class= waitElement(driver2,textXPathgroup["Lessons completed"]).text.split('/')
                n_class = int(n_class[0])
                name_course= waitElement(driver2, textXPathgroup["Course"]).text
                grouped_driver_cache[name_group] = {}
                grouped_driver_cache[name_group]["n_class"] = n_class
                grouped_driver_cache[name_group]["name_course"] = name_course


            for i in range(1,st_total+1):
                student = i
                if student >1:
                    student =  student *2 -1
                assis_history = {'Module':[], 'Real lesson':[], 'total lesson':[]}
                total_miss = 0  
                total_attend = 0
                modules = math.ceil(n_class/4)
                for mod in range(1, modules+1):
                
                    if mod>4:
                        ul = 2
                        clas = mod - 4
                    else:
                        ul = 1
                        clas = mod
                    xpath =         f'//*[@id="test1"]/table/tbody/tr[{student}]/td[2]/ul[{ul}]/div[{clas}]/div[2]'
                    td_element =    driver2.find_element(By.XPATH, xpath)
                    miss_class =    len(td_element.find_elements(By.CLASS_NAME, value="student_attendance-miss"))
                    attend_class =  len(td_element.find_elements(By.CLASS_NAME, value="student_attendance-attend"))
                    absence_class = len(td_element.find_elements(By.CLASS_NAME, value="student_attendance-absence"))
                    error_class =   len(td_element.find_elements(By.CLASS_NAME, value="student_attendance-no-att"))
                    total_miss =    total_miss + miss_class + absence_class
                    total_attend =  total_attend + attend_class + error_class
                    assis_history["Module"].append(f'Mod {mod}')
                    assis_history["Real lesson"].append(attend_class + error_class)
                    assis_history["total lesson"].append(attend_class + error_class + absence_class + miss_class)
                try:
                    miss_percent_list.append((total_miss / n_class)*100)
                    atten_percent_list.append((total_attend / n_class))
                except:
                    miss_percent_list.append(0)
                    atten_percent_list.append(0)
                assis_history_list.append(assis_history)
                if  "name_list" not in grouped_driver_cache[name_group]:
                    student_click = waitElement(driver2, f'//*[@id="test1"]/table/tbody/tr[{student}]/td[1]/div/div[1]/a')
                    student_name = student_click.text.encode('utf-8').decode('utf-8')
                    link = student_click.get_attribute('href')
                    href_list.append(link)
                    name_list.append(student_name)
                    

            if  "name_list" in grouped_driver_cache[name_group]:
                href_list= grouped_driver_cache[name_group]["href_list"]
                name_list= grouped_driver_cache[name_group]["name_list"]
            else:
                grouped_driver_cache[name_group]["href_list"] = href_list
                grouped_driver_cache[name_group]["name_list"] = name_list
                
            if "activity" in grouped_driver_cache[name_group]:
                activity = grouped_driver_cache[name_group]["activity"]
            else:
                activity = extract_activities(n_class, href_list[0])
                grouped_driver_cache[name_group]["activity"] = activity

            for student in range (1, st_total+1):   
                meter_students(n_class, student, activity, name_group,
                                href_list[student-1], name_list[student-1], 
                                assis_history_list[student-1], atten_percent_list[student-1],
                                miss_percent_list[student-1], name_course
                                )
            return cacheStudent

    def quitDriver(self, name):
        try:
            driverGroup = grouped_driver_packs[name]
            driverGroup.quit()
            del grouped_driver_packs[name]
        except:
            print(f'{name} is already closed!')
    
       
class seleniumTakeMetricsByGroupBasic():
    global rankData
    listRows = []
    listIdsGroup = []
    def findPoints(self, group):
            listStLowBalance= []
            n_std = group[2].split('/')
            n_std = int(n_std[0])
            id_course = id_couse_latamByTotalName[group[3]]
            print(lesson_by_course_latam[id_course])
            try:
                if n_std > 0 and (lesson_by_course_latam[id_course]['names'].index(group[4]) < 31):
                    print("contando")
                    driver.get(f"https://backoffice.kodland.org/en/group_{group[0]}/")
                    grupo_name = group[1]
                    curso_name = group[3]
                    point_available = points_total_course_latam[id_course][n_std-1]
                    color_curso = color_cursoBycode[id_course] 
                    df = pd.DataFrame(columns=['Nombre', 'Puesto', 'Puntaje', 'Estado', 'Balance'])
                    st_total_range = n_std * 2
                    for student in range(1, st_total_range, 2):
                        table = waitElement(driver,f'{textXPathgroup["Row Student"]}[{str(student)}]').text
                        table_balance =  waitElement(driver,f'{textXPathgroup["Row Student"]}[{str(student+1)}]').text
                        balance = table_balance.split(sep=':')
                        balance[1] = balance[1].split()
                        balance = (balance[1])
                        vp = table.split(sep='\n')
                        extra = [vp[0],vp[-1]]
                        two = extra[1].split()
                        one= two[0].split(sep='/')
                        two.pop(0)
                        extra.pop(1)
                        extra = extra + [int(one[0])] + [int(one[1])] + two + balance
                        extra[2] = int(extra[2])
                        df.loc[len(df)] = extra
                    df_sort = df.sort_values('Puesto') 
                    df_sort.reset_index(inplace=True, drop=True)
                    compromiso = round((df_sort['Puntaje'].sum()/(point_available*n_std))*100)
                    empty_attendances = len(driver.find_elements(By.CLASS_NAME, "student_attendance-no-att"))
                    n_class= waitElement(driver, textXPathgroup['Lessons completed']).text.split('/')
                    n_class = int(n_class[0])
                    total_Points_By_Actual_Lesson = sum(points_total_course_latam[id_course][:n_class])
                    listIdStd = driver.find_elements(By.CLASS_NAME, "balance__text")
                    while listIdStd[-1].text == 'Calculating...':
                        time.sleep(0.5)
                        listIdStd = driver.find_elements(By.CLASS_NAME, "balance__text")
                    for i, element in enumerate(listIdStd):
                        intBalance = int(element.text)
                        if intBalance < 3: 
                            if i == 0:
                                ind = 1
                            else:
                                ind = (i+1)+((((i+1)*2)/2)-1)
                            nameSele = waitElement(driver, textXPathgroup["Name Student"].replace("#n_std#", str(int(ind))))
                            name_std = nameSele.text
                            href_std = nameSele.get_attribute("href")
                            driver.execute_script(f"window.open('{href_std}', 'new_window')")
                            driver.switch_to.window(driver.window_handles[1])
                            phone = waitElement(driver, '/html/body/div[3]/div[2]/div/div[2]/div[2]/table/tbody/tr[3]/td/a').text
                            listStLowBalance.append([name_std, href_std,intBalance, phone])
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                    totalPoints = total_Points_By_Actual_Lesson * n_std
                    totalPointsByStudents = int(df_sort["Puntaje"].sum())
                    InstaciaADB.addEngagementToDb(group[0], (totalPointsByStudents, totalPoints-totalPointsByStudents, 'no'))
                    rankData[grupo_name] = [total_Points_By_Actual_Lesson, df_sort, int((totalPointsByStudents/totalPoints)*100), color_curso, n_std]
                    return [listStLowBalance, [totalPointsByStudents, totalPoints-totalPointsByStudents, 'no'], empty_attendances]
                else:
                    print("No contando")
                    InstaciaADB.addEngagementToDb(group[0], (0,0,'yes'))
                    return [listStLowBalance, [0,0,'yes'], 0]
            except Exception as e:
                print(e)
                traceback.print_exc()
                if group[11] == "New":
                    InstaciaADB.addEngagementToDb(group[0], (0,0,'no'))
                    return [listStLowBalance, [0,0,'no'], 0]
                else:
                    InstaciaADB.addEngagementToDb(group[0], (0,0,'yes'))
                    return [listStLowBalance, [0,0,'yes'], 0]
            
    def driverQuit(self):
        driver.quit()


def waitElementCSS(driver, XPATH):
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, XPATH))
    )

