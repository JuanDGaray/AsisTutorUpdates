from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import pyqtSlot
from componentsUI import topWindow, BottomWindow, loggin
from src.dataBaseManager import db_manager
from src.selenuimManager import seleniumTakeMetricsByGroupBasic, rankData
from functools import partial
from utils import stylesheetUI
from utils.constants import data
from src.gSheetActions import  GoogleSheet, generate_uid
import datetime, json
import tempfile


imageBS64  = data["imageBS64"]
href_couse_latamByTotalName = data["href_couse_latamByTotalName"]
lesson_by_course_latam= data["lesson_by_course_latam"] 
id_couse_latamByTotalName = data["id_couse_latamByTotalName"]
textTemplate = data["textTemplate"]

import webbrowser
import base64
import os


listMetrics = []
colSpam = 0

initTW = topWindow.TopWidget()
initBW = BottomWindow.BottomWidget()
instSeleMBG= seleniumTakeMetricsByGroupBasic()
buttonContainer = {}
buttonNew= {}
language = "ENG"


def bs4Process(bs4):
    image_data = base64.b64decode(bs4.split(',')[1])
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(image_data)
    return pixmap

class Inithome(QtWidgets.QWidget):
    def __init__(self, parent, jsonG=None, name=None, user=None):
        super().__init__(parent)
        self.WindowMain = parent
        self.homeSize = "min"
        self.frameY = 0
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setGeometry(0, 30, parent.width(), parent.height() - 50)
        self.jsonG = jsonG
        status = self.WindowHome(parent, name, user)
        if not status == 'CourseNotFound':
            self.donut_thread = self.DonutThread(parent=self)
            self.donut_thread.finished.connect(self.onDonutThreadFinished)
            self.donut_thread.start()
        else:
            instSeleMBG.driverQuit()
            loggin.Loggin(self.WindowMain, error='CourseNotFound')  
             
        

    class NotificationHandler(QtCore.QObject):
        def __init__(self, vertical_layout_sidebar, labelGif, infoText, buttonCheck=None, listOrdeGroup=None, parent=None):
            super(Inithome.NotificationHandler, self).__init__(parent)
            self.verticalLayoutSidebar = vertical_layout_sidebar
            self.verticalLayoutSidebar.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            self.labelGif = labelGif
            self.infoLabelTohome = infoText
            self.buttonCheck = buttonCheck
            self.listOrdeGroup = listOrdeGroup
            
            self.iconWA = QtGui.QIcon(bs4Process(imageBS64['wa']))
        notification_signal = pyqtSignal(str, str, str, str, str, str, str, str)

        @pyqtSlot(str, str, str, str, str, str, str, str)
        def insertNotification(self, type, href_student=None, student=None, href_group=None, group=None, engagement=None,
                           balanceStudent=None, lastElementFirstLoading=None):
            QtCore.QMetaObject.invokeMethod(self, "_insertNotification",
                                 QtCore.Qt.QueuedConnection,
                                 QtCore.Qt.QueuedConnection,
                                 (type, href_student, student, href_group, group, engagement, balanceStudent, lastElementFirstLoading))

        def _insertNotification(self, type, href_student=None, student=None, href_group=None, group=None, engagement=None,
                            balanceStudent=None, lastElementFirstLoading=None):
            global buttonContainer, language, buttonNew
            contentItemsNews = QtWidgets.QWidget()
            contentItemsNews.setObjectName("contentItemsNews")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            contentItemsNews.setSizePolicy(sizePolicy)
            vertivalLayoutNewsContainer = QtWidgets.QVBoxLayout(contentItemsNews)
            

            if type == 'ActivateButton'  or lastElementFirstLoading == "yes":
                if lastElementFirstLoading == "yes":
                    self.labelGif.deleteLater()
                    self.infoLabelTohome.deleteLater()
                    self.buttonCheck.setCursor(QtCore.Qt.PointingHandCursor)
                    self.buttonCheck.setEnabled(True)
                    self.listOrdeGroup.setEnabled(True)
                    self.listOrdeGroup.setCurrentIndex(2)
                elif str(href_group) in buttonContainer:
                    for button in buttonContainer[href_group]:
                        try:                    
                            if not button.isEnabled():
                                button.setEnabled(True)
                        except Exception as e:
                            print(e)
            elif type == 'DelButton':
                try:
                    for button in buttonContainer[href_group]:
                        try:                    
                            button.setEnabled(False)
                            button.setVisible(False)
                        except Exception as e:
                            print(e)
                except Exception as e:
                            print(e)
                        
            else:
                boxToolsNotifications = QtWidgets.QComboBox()
                boxToolsNotifications.setContentsMargins(0,0,0,0)
                boxToolsNotifications.setSizePolicy(sizePolicy)
                boxToolsNotifications.setMinimumHeight(20)

                horizontalToolsLayout = QtWidgets.QHBoxLayout(boxToolsNotifications)
                horizontalToolsLayout.setContentsMargins(0,0,0,0)
                horizontalToolsLayout.addStretch(1)

                infoNews = QtWidgets.QLabel()
                if type == 'criticalGroup':
                    infoNews.setText(f"{textTemplate[language]['infoNewsCG'].replace('#href_group#', href_group).replace('#group#', group).replace('#engagement#', engagement)}")
                elif type == 'lowBalanceStudent':
                    infoNews.setText(f"{textTemplate[language]['infoNewsLB'].replace('#href_student#', href_student).replace('#student#', student).replace('#balanceStudent#', balanceStudent)}")
                    openMessageWtp = QtWidgets.QPushButton()
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                    openMessageWtp.setSizePolicy(sizePolicy)
                    openMessageWtp.setMinimumSize(18, 18) 
                    openMessageWtp.setIcon(self.iconWA)
                    openMessageWtp.setCursor(QtCore.Qt.PointingHandCursor)
                    openMessageWtp.setToolTip("Copy message to WA")
                    message = textTemplate[language]['templateWaBalanceLow'].replace('#student#', student).replace('#balance#', balanceStudent)
                    messageToWa = message.replace("\n", "%0A").replace(" ", "%20")
                    phone = href_group
                    openMessageWtp.clicked.connect(lambda: self.openLinkWaLowBalance(messageToWa, phone))
                    horizontalToolsLayout.addWidget(openMessageWtp)
                elif type ==  'NoAtt':
                    infoNews.setText(f"{textTemplate[language]['infoNewsNA'].replace('#href_group#', href_group).replace('#group#', group).replace('#engagement#', engagement)}")
                infoNews.setOpenExternalLinks(True)
                infoNews.linkActivated.connect(self.open_external_link)

                infoNews.setObjectName("infoNews")
                infoNews.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
                infoNews.setWordWrap(True)
                vertivalLayoutNewsContainer.addWidget(infoNews)

                checkNotification = QtWidgets.QPushButton()
                checkNotification.setContentsMargins(0,0,0,0)
                checkNotification.setStyleSheet("padding: 0;")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                checkNotification.setSizePolicy(sizePolicy)
                checkNotification.setMinimumSize(40, 20) 
                checkNotification.setText('Done')
                checkNotification.setCursor(QtCore.Qt.PointingHandCursor)
                checkNotification.clicked.connect(lambda: self.eliminar_widget(contentItemsNews))
                horizontalToolsLayout.addWidget(checkNotification)
                
                vertivalLayoutNewsContainer.addWidget(boxToolsNotifications)
                self.verticalLayoutSidebar.addWidget(contentItemsNews)
        def openLinkWaLowBalance(self, message, phone):
            link = "https://api.whatsapp.com/send/?phone="+phone+"&text="+message+"&type=phone_number&app_absent=0"
            webbrowser.open_new(str(link))

        def eliminar_widget(self, widget):
                widget.deleteLater()

        def open_external_link(self, url):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

        def copyMessageToWA(self, message):  
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(message)
    

    class DonutThread(QThread):
        finished = pyqtSignal()

        def run(self):
            self.parent().putMetricDonut()
            self.finished.emit()

    def onDonutThreadFinished(self):
        self.putMetricDonut()

    def retranslateUi(self, parent):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        pathuserImg = os.path.join(parent_dir,'assets/images/user (1).png')
        self._translate = QtCore.QCoreApplication.translate
        parent.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.userImg.setText(self._translate("MainWindow", f"<html><head/><body><p><img src=\"{pathuserImg}\"/></p></body></html>"))
        self.Group.setText(self._translate("MainWindow", "Groups"))

    def hideGraduatesGroup(self, state):
        if state == 2:
            for box in self.graduateBox:
                box.setVisible(True)
        else:
            for box in self.graduateBox:
                box.setVisible(False)
            
    def listOrdeGroupChange(self, text):
        if text == "ID":
            self.MakeGrid(orderBy="ID")
        elif text == "Engagement":
            self.MakeGrid(orderBy="Engagement")
        else:
            self.MakeGrid(orderBy="Nearest Class") 


    def WindowHome(self, parent, name, user):    
        self.setObjectName("centralwidgetHome)")
        
        self.homeWidget = QtWidgets.QWidget()
        self.homeWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.homeWidget.setContentsMargins(0,0,0,0)
        self.stackedWidget.addWidget(self.homeWidget)

        self.verticalLayoutMain = QtWidgets.QVBoxLayout(self)
        self.verticalLayoutMain.setContentsMargins(0, 0,0, 0)
        self.verticalLayoutMain.setSpacing(0)
        self.verticalLayoutMain.setObjectName("verticalLayout")
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(8)

       
        """SIDE BAR"""

        self.sidebar_visible = False
        

        self.sidebar = QtWidgets.QFrame(self)
        self.sidebar.setGeometry(860, 30, 230, self.WindowMain.height())
        self.sidebar.setContentsMargins(0,0,0,0)
        self.sidebar.raise_()

        self.toggle_button = QtWidgets.QPushButton(self.sidebar)
        icon = QtGui.QIcon(bs4Process(imageBS64["left"]))
        self.toggle_button.setIcon(icon)
        self.toggle_button.setGeometry(3,20, 30,30)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button.setObjectName("toggle_button")
        

        self.labeNotificationAdviser = QtWidgets.QLabel(self.toggle_button)
        self.labeNotificationAdviser.setText('!')
        self.labeNotificationAdviser.setGeometry(30,-5,10,10)


        self.animation = QtCore.QPropertyAnimation(self.sidebar, b"pos")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Linear)

       

        self.sidebarChild = QtWidgets.QFrame(self.sidebar)
        self.sidebarChild.setGeometry(24, 0, 200,  self.WindowMain.height())
        self.sidebarChild.setObjectName("sidebarChild")
        self.verticalLayoutSidebar = QtWidgets.QVBoxLayout(self.sidebarChild)
        self.verticalLayoutSidebar.setContentsMargins(14,14,14,14)
        
        self.titleSideBar = QtWidgets.QLabel()
        self.titleSideBar.setText("Notifications")
        self.titleSideBar.setFont(font)
        self.titleSideBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleSideBar.setMaximumHeight(40)

        self.scroll_areaSide = QtWidgets.QScrollArea(self.sidebarChild)
        self.scroll_areaSide.setGeometry(-2, 30, 200, self.WindowMain.height()-75)
        self.scroll_areaSide.setWidgetResizable(True)
        self.inner_widget = QtWidgets.QWidget(self.scroll_areaSide)
        self.scroll_areaSide.setWidget(self.inner_widget)
        self.inner_layout = QtWidgets.QVBoxLayout(self.inner_widget)

        self.verticalLayoutSidebar.addWidget(self.titleSideBar)
        self.verticalLayoutSidebar.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        initTW.CreateTopWidgetTitle(self.verticalLayoutMain, parent,  self.sidebarChild,self.scroll_areaSide)


        #BODY ALL
        

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.homeWidget)
        self.stackedWidget.setCurrentIndex(self.frameY)
        self.horizontalLayout.setContentsMargins(14, 14, 14, 14)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutMain.addWidget(self.stackedWidget)
        self.body = QtWidgets.QWidget(self)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy)
        self.body.setMaximumSize(QtCore.QSize(1333333, 16777215))
        self.body.setObjectName("body")


        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        #MenÃ­
        self.menu = QtWidgets.QWidget(self.body)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMinimumSize(QtCore.QSize(80, 0))
        self.menu.setMaximumSize(QtCore.QSize(70, 3001))
        self.menu.setAutoFillBackground(False)
        self.menu.setObjectName("menu")


        self.verticalLayout = QtWidgets.QVBoxLayout(self.menu)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")


        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)


        self.userImg = QtWidgets.QLabel(self.menu)
        self.userImg.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.userImg.setTextFormat(QtCore.Qt.RichText)
        self.userImg.setObjectName("userImg")


        self.verticalLayout.addWidget(self.userImg, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.tutorName = QtWidgets.QLabel(self.menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tutorName.sizePolicy().hasHeightForWidth())
        self.tutorName.setSizePolicy(sizePolicy)
        self.tutorName.setText(user)
        self.tutorName.setObjectName("tutorName")

        json_data = json.dumps(self.jsonG)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_file.write(json_data)
            temp_filename = temp_file.name
        sheet = GoogleSheet(temp_filename, 'Asistutor DB', 'INCOME PER TUTOR')
        uiid = generate_uid()
        date = datetime.date.today()
        date_str = date.strftime("%Y-%m-%d")
        value =[[date_str, user, name, uiid]]
        range = sheet.get_last_row_range()
        sheet.write_data(value, range)
        os.unlink(temp_filename)



        self.verticalLayout.addWidget(self.tutorName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        
        #BUTTON TO VIEW GROUP'
        self.Group = QtWidgets.QPushButton(self.menu)
        self.Group.animateClick(100)
        
        self.Group.setFont(font)
        self.Group.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Group.setCheckable(True)
        self.Group.setChecked(False)
        self.Group.setObjectName("Group")
        self.verticalLayout.addWidget(self.Group, 0, QtCore.Qt.AlignTop)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        #Home
        self.horizontalLayout_4.addWidget(self.menu, 0, QtCore.Qt.AlignLeft)

        

        self.homeContainer = QtWidgets.QWidget(self.body)
        self.homeContainer.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.homeContainer.setSizePolicy(sizePolicy)
        self.homeContainer.setObjectName("homeContainer")

        self.layout = QtWidgets.QVBoxLayout(self.homeContainer)


        self.headerHomeContainer  = QtWidgets.QWidget()
        self.headerHomeContainer.setObjectName("headerHomeContainer")
        self.horizaontalLayoutheaderHome = QtWidgets.QHBoxLayout(self.headerHomeContainer)
        self.buttonGridGenerator = QtWidgets.QPushButton()
        icon = QtGui.QIcon(bs4Process(imageBS64["layout"]))
        self.buttonGridGenerator.setIcon(icon)
        self.buttonGridGenerator. setVisible(False)
        self.buttonGridGeneratorOn = False  
        self.buttonTableGeneratorOn = True
        

        
        self.buttonGridGenerator.clicked.connect(lambda : self.MakeGrid())
        self.buttonGridGenerator.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonGridGenerator.setObjectName("ButtonTable")
        self.buttonTableGenerator = QtWidgets.QPushButton()
        self.buttonTableGenerator.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        ####################################################
        self.buttonTableGenerator.setVisible(False)
        ###################################################
        icon = QtGui.QIcon(bs4Process(imageBS64["more"]))
        self.buttonTableGenerator.setIcon(icon)
        self.buttonTableGenerator.clicked.connect(self.MakeTable)    
        self.buttonTableGenerator.setObjectName("ButtonGrid")
        ruta_gif = os.path.join(os.path.dirname(__file__), '..', 'rolling.gif')
        movie = QtGui.QMovie(ruta_gif)
        self.labelGif = QtWidgets.QLabel()
        self.labelGif.setMinimumSize(30,30)
        self.labelGif.setMovie(movie)
        self.labelGif.setAlignment(QtCore.Qt.AlignCenter)
        movie.start()

        self.loadingHomerTopInfo = QtWidgets.QLabel('Analyzing group commitment...')


        self.horizaontalLayoutheaderHome.addWidget(self.buttonGridGenerator)
        self.horizaontalLayoutheaderHome.addWidget(self.buttonTableGenerator)
        self.horizaontalLayoutheaderHome.addWidget(self.labelGif)
        self.horizaontalLayoutheaderHome.addWidget(self.loadingHomerTopInfo)
        self.horizaontalLayoutheaderHome.setAlignment(QtCore.Qt.AlignLeft)
        self.horizaontalLayoutheaderHome.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.headerHomeContainer)

        self.spacerHeader = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizaontalLayoutheaderHome.addSpacerItem(self.spacerHeader)

        

        self.infolistOrdeGroupContainer = QtWidgets.QHBoxLayout()

        self.labelCheckGraduate = QtWidgets.QLabel()
        self.labelCheckGraduate.setFont(font)
        self.labelCheckGraduate.setText("Graduates")
        self.inputCheckGraduate = QtWidgets.QCheckBox()
        self.inputCheckGraduate.setChecked(True)
        self.inputCheckGraduate.setEnabled(False)
        self.inputCheckGraduate.setCursor(QtCore.Qt.ForbiddenCursor)
        self.inputCheckGraduate.stateChanged.connect(self.hideGraduatesGroup)

        self.infolistOrdeGroup = QtWidgets.QLabel()
        self.infolistOrdeGroup.setText("sort by: ")
        self.infolistOrdeGroup.setObjectName("infolistOrdeGroup")
        self.listOrdeGroup = QtWidgets.QComboBox()
        self.listOrdeGroup.setObjectName("ComboBoxSortBy")
        self.listOrdeGroup.setEnabled(False)

        self.listOrdeGroup.addItem("ID")
        self.listOrdeGroup.addItem("Engagement")
        self.listOrdeGroup.addItem("Nearest Class") 
        self.listOrdeGroup.currentTextChanged.connect(self.listOrdeGroupChange)
        
        self.infolistOrdeGroupContainer.addWidget(self.labelCheckGraduate)
        self.infolistOrdeGroupContainer.addWidget(self.inputCheckGraduate)   
        self.infolistOrdeGroupContainer.addWidget(self.infolistOrdeGroup)
        self.infolistOrdeGroupContainer.addWidget(self.listOrdeGroup)

        #################################################################################
        self.horizaontalLayoutheaderHome.addLayout(self.infolistOrdeGroupContainer)
        
        ##########################################################################################

        self.scroll_area = QtWidgets.QScrollArea(self.homeContainer)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(1)
       

        self.scrollContent = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.scrollContent.setSizePolicy(sizePolicy)
        
        
        
        #Grid
        self.gridLayout = QtWidgets.QGridLayout(self.scrollContent)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)
        self.gridLayout.setRowMinimumHeight(0, 80)
        self.scroll_area.setWidget(self.scrollContent)
        self.layout.addWidget(self.scroll_area)

        self.horizontalLayout_4.addWidget(self.homeContainer, 0)
        self.horizontalLayout.addWidget(self.body)
        textReturn = self.MakeGrid()
        if textReturn == "CourseNotFound":
            return 'CourseNotFound'
        initBW.CreateBottomWidgetFooter(self.verticalLayoutMain, parent)

        parent.setCentralWidget(self)

        self.retranslateUi(parent)
        QtCore.QMetaObject.connectSlotsByName(parent)
        self.notification_handler = Inithome.NotificationHandler(self.inner_layout, self.labelGif, self.loadingHomerTopInfo, self.inputCheckGraduate, self.listOrdeGroup)
        self.notification_handler.notification_signal.connect(self.notification_handler._insertNotification)

                    
    def toggle_sidebar(self):
        print(self.sidebar.pos().x())
        if (self.sidebar.pos().x() + 40) < self.WindowMain.width():
            self.hide_sidebar()
        else:
            self.show_sidebar()


    def show_sidebar(self):
        self.animation.setStartValue(self.sidebar.pos())
        self.animation.setEndValue(self.sidebar.pos() - QtCore.QPoint(180, 0)) 
        self.animation.start()

    def hide_sidebar(self):
        self.animation.setStartValue(self.sidebar.pos())
        self.animation.setEndValue(self.sidebar.pos() + QtCore.QPoint(180, 0))
        self.animation.start()

    def apply_shadow(self, widget):
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QtGui.QColor("#555555"))
            shadow.setOffset(6, 6)
            widget.setGraphicsEffect(shadow)

    def open_external_link(self, url):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def ranking_generator_init(self, nameGroup, last_lesson=None):
            contenido = []
            point_available = rankData[nameGroup][0]
            df_sort = rankData[nameGroup][1]
            compromiso = rankData[nameGroup][2]
            color_curso = rankData[nameGroup][3]
            st_total = rankData[nameGroup][4]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            template = os.path.join(parent_dir, r"assets\template-rank-metrics", "template.html")
            with open(template, "r", encoding='utf-8') as template:
                    for linea in template:
                        columnas = linea.split(';')
                        contenido.append(';'.join(columnas)+'\n')
            ll_index = contenido.index('                    <h1 class="last_lesson"></h1>\n\n')
            Color_index = contenido.index('        --color_theme: var(--Orange)\n\n')
            pa_index = contenido.index('                    <h1 class="point_ava"></h1>\n\n')
            cc_index = contenido.index('                    <h1 class="compromiso"></h1>\n\n')
            name_course_index =contenido.index('                <h2>Python Programming Language</h2>\n\n')
            contenido[ll_index] = f'                    <h1 class="last_lesson">{last_lesson}</h1>\n\n'
            contenido[pa_index] = f'                    <h1 class="point_ava">{str(point_available)}</h1>\n\n'
            contenido[cc_index] = f'                    <h1 class="compromiso">{str(compromiso)}%</h1>\n\n'
            contenido[Color_index] = f'        --color_theme: var(--{color_curso})\n\n'
            contenido[name_course_index] = f'                <h2>{nameGroup}</h2>\n\n'

            #Modificamos el body de la plantilla
            n_index = contenido.index('        <tr class="datos_ranking">\n\n')
            principal_contend = contenido[0:n_index]
            secundary_contend = contenido[n_index+5:-1]
            middle_contend = []
            for student in range(int(st_total)):
                perfect = 'nada'
                if df_sort.iloc[student,2] >= point_available:
                    perfect = 'perfect'
                name = df_sort.iloc[student,0]
                name = name.lstrip("-")
                name = name.lstrip()
                middle_contend.append('        <tr class="datos_ranking student'+str(df_sort.iloc[student,1])+'">\n\n')
                middle_contend.append('            <td>'+str(df_sort.iloc[student,1])+'<span></span></td>\n\n')
                middle_contend.append('            <td>'+name+'</td>\n\n') 
                middle_contend.append('            <td><div class="container_puntos"><p>'+str(df_sort.iloc[student,2])+'</p></div><meter min="0" max="100" low="32" high="75" optimum="100" value="'+str((int(df_sort.iloc[student,2])/int(point_available))*100)+'"></meter><div class="contain_perfet"><div class="'+perfect+'"> </div></div> </td>\n\n')
                middle_contend.append('        </tr>\n\n')
            table_ranking = principal_contend + middle_contend + secundary_contend
            templateRanking = os.path.join(parent_dir, r"assets\template-rank-metrics", "temporal_ranking.html")
            with open(templateRanking, 'w', encoding='utf-8') as archivo:
                archivo.writelines(table_ranking)
            url = os.path.abspath(templateRanking)
            webbrowser.open(url)

    def MakeGrid(self, graduateOnOff=False, orderBy=None) :
        global buttonContainer
        self.graduateBox = []
        if self.buttonTableGeneratorOn or graduateOnOff or orderBy: 
            self.buttonGridGeneratorOn = True
            self.buttonTableGeneratorOn = False
            
            for i in reversed(range(self.gridLayout.count())):
                widget = self.gridLayout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        if self.width() >=1000:
            self.fontSize = 7
            colTarget=6
            spamDonut=5
            
        else: 
            self.fontSize = 7
            colTarget=4
            spamDonut=5

        spamStatus= 2
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(self.fontSize)
        _translate = QtCore.QCoreApplication.translate
        self.listMetrics = []

        self.n_group_list = db_manager().putGroupAtHome()
        if orderBy == "ID":
            group_list_orderById = db_manager().getNoGraduatedGroupsByID()
            self.n_group_list[:len(group_list_orderById)] = group_list_orderById
        elif orderBy == "Engagement":
            group_list_orderByEngagement = db_manager().getNoGraduatedGroupsByEngagement()
            self.n_group_list[:len(group_list_orderByEngagement)] = group_list_orderByEngagement
        elif orderBy == "Nearest Class":
            group_list_orderByNearestClass = db_manager().getNoGraduatedGroupsByNearestClass()
            self.n_group_list[:len(group_list_orderByNearestClass)] = group_list_orderByNearestClass
         
        for group in range(len(self.n_group_list)):
            div = (group)//colTarget
            rowW = 0
            colW = group
            if div >= 1:
                rowW = div
                colW = group-(div*colTarget)

            groupContainer = QtWidgets.QGroupBox()         

            groupContainer.setAutoFillBackground(False)
            groupContainer.setMinimumSize(190,170)
            groupContainer.setMaximumHeight(160)
            groupContainer.setTitle("")
            groupContainer.setFlat(False)
            groupContainer.setCheckable(False)
            groupContainer.setContentsMargins(0,0,0,0)
            groupContainer.setObjectName("groupContainer")
            


            ####
           
            
            verticalLayout = QtWidgets.QVBoxLayout(groupContainer)
            verticalLayout.setContentsMargins(0, 0, 0, 0)
            verticalLayout.setSpacing(0)
            verticalLayout.setObjectName("verticalLayout_2")


            nameGroup = QtWidgets.QLabel(groupContainer)
            nameGroup.setObjectName("nameGroup")
            nameGroup.setAlignment(QtCore.Qt.AlignTop)
            nameGroup.setMinimumHeight(30)
            nameGroup.setContentsMargins(0,0,0,0)
            
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(nameGroup.sizePolicy().hasHeightForWidth())
            nameGroup.setSizePolicy(sizePolicy)

            nameGroupContainer = QtWidgets.QHBoxLayout(nameGroup)
            nameGroupContainer.setContentsMargins(0,0,4,0)

            nameGroupText = QtWidgets.QLabel()
            nameGroupText.setObjectName("nameGroupText")
            nameGroupText.setOpenExternalLinks(True)
            nameGroupText.setText(f"<a href='https://backoffice.kodland.org/en/group_{self.n_group_list[group][0]}/'>{self.n_group_list[group][1]}</a>")
            nameGroupContainer.addWidget(nameGroupText)
            nameGroupText.linkActivated.connect(self.open_external_link)
           
            labelStatus = QtWidgets.QLabel()
            labelStatus.setFont(font)
            if  self.n_group_list[group][11] == 'NULL':
                labelStatus.setText("-")
                labelStatus.setStyleSheet("color: white")
            else:
                
                labelStatus.setText(self.n_group_list[group][11])
                if self.n_group_list[group][11] == "New":
                    labelStatus.setStyleSheet("background-color: #4287f5")  
                elif self.n_group_list[group][11] == "Graduate":
                    labelStatus.setStyleSheet("background-color: #989c99")  
                    self.graduateBox.append(groupContainer)  
                    if not self.inputCheckGraduate.isChecked():
                        groupContainer.setVisible(False)
                elif self.n_group_list[group][11] == "Perfect":
                    labelStatus.setStyleSheet("background-color:#4314a3; color: white")            
                elif self.n_group_list[group][11] == "High":
                    labelStatus.setStyleSheet("background-color:#14a33a")       
                elif self.n_group_list[group][11] == "Good":
                    labelStatus.setStyleSheet("background-color:#25d654")          
                elif self.n_group_list[group][11] == "Regular":
                    labelStatus.setStyleSheet("background-color: #ffc547")         
                elif self.n_group_list[group][11] == "Low":
                    labelStatus.setStyleSheet("background-color:#ff8901")          
                elif self.n_group_list[group][11] == "Bad":
                    labelStatus.setStyleSheet("background-color:#ff2b2a")    
                elif self.n_group_list[group][11] == "Critical":
                    labelStatus.setStyleSheet("background-color:#ff2b2a; color: white")                         
            labelStatus.setObjectName("labelStatus")
            
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            labelStatus.setSizePolicy(sizePolicy)
            labelStatus.setContentsMargins(0,0,0,0)
            labelStatus.setMinimumSize(50,15)
            labelStatus.setMaximumSize(50,15)
            labelStatus.setAlignment(QtCore.Qt.AlignCenter)
            nameGroupContainer.addWidget(labelStatus)
            
            
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(nameGroup.sizePolicy().hasHeightForWidth())
            nameGroup.setSizePolicy(sizePolicy) 
            nameGroup.setTextFormat(QtCore.Qt.RichText)
            nameGroup.setObjectName("nameGroup")
            verticalLayout.addWidget(nameGroup)


            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            metricGroup = QtWidgets.QFrame(groupContainer)
            metricGroup.setSizePolicy(sizePolicy)
            metricGroup.setContentsMargins(0,-4,0,0)
            metricGroup.setObjectName("metricGroup")
            
                
            horizontalLayout_2 = QtWidgets.QHBoxLayout(metricGroup)
            horizontalLayout_2.setObjectName("horizontalLayout_2")
            horizontalLayout_2.setContentsMargins(8,4,8,8)

            LayoutVDonutContainer = QtWidgets.QVBoxLayout()
            LayoutVDonutContainer.setContentsMargins(0,0,0,0)
            LayoutVDonutContainer.setSizeConstraint(0)
            LayoutVDonutContainer.setSpacing(2)    
            poduim = False
            if self.n_group_list[group][7] == 'undefine' or self.n_group_list[group][8] == 'undefine' : 
                self.widget = DonutChartWidget(100,0, True, False)
            else:
                poduim = True
                if self.n_group_list[group][9] == 'yes':
                    self.widget = DonutChartWidget(self.n_group_list[group][7],self.n_group_list[group][8], False, True)
                else:
                    self.widget = DonutChartWidget(self.n_group_list[group][7],self.n_group_list[group][8], False, False)
                
            self.widget.setObjectName("widget")
            self.widget.setSizePolicy(sizePolicy)
            self.widget.setStyleSheet("border-left: 3px solid red;")

            LayoutVDonutContainer.addWidget(self.widget)
    
            
            ColorPartDonut1 = QtWidgets.QLabel()
            ColorPartDonut1.setContentsMargins(0,0,0,0)
            ColorPartDonut1.setMaximumHeight(18)
            if self.n_group_list[group][7] == 'undefine' or self.n_group_list[group][8] == 'undefine' :
                ColorPartDonut1.setText('<span style="color:gray;">???/???</span>')
            elif self.n_group_list[group][9] == 'yes':
                ColorPartDonut1.setText('<span style="color:gray;">graduate</span>')
            else:
                ColorPartDonut1.setText(f'<span style="color:green;">{self.n_group_list[group][7]}/</span>{self.n_group_list[group][7] + self.n_group_list[group][8]}')

            LayoutVDonutContainer.addWidget(ColorPartDonut1)

            spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            LayoutVDonutContainer.addItem(spacerItem)

            horizontalLayout_2.addLayout(LayoutVDonutContainer)

            LayoutVMainInfoGroupContainer = QtWidgets.QVBoxLayout()
            LayoutVMainInfoGroupContainer.setContentsMargins(0,0,0,0)
            LayoutVMainInfoGroupContainer.setSizeConstraint= (0)
            LayoutVMainInfoGroupContainer.setAlignment(QtCore.Qt.AlignCenter)

            WidgetHInfoGroupContainer = QtWidgets.QWidget()
            WidgetHInfoGroupContainer.setObjectName("LayoutHInfoGroupContainer")


            LayoutHInfoGroupContainer = QtWidgets.QHBoxLayout(WidgetHInfoGroupContainer)
            LayoutHInfoGroupContainer.setContentsMargins(2,2,2,2)
            LayoutHInfoGroupContainer.setSizeConstraint= (0)
            
            
            LayoutVMainInfoGroupContainer.addWidget(WidgetHInfoGroupContainer)
            horizontalLayout_2.addLayout(LayoutVMainInfoGroupContainer)

            columnDescriptionGroupContainer = QtWidgets.QVBoxLayout()
            columnDescriptionGroupContainer.setContentsMargins(0,0,0,0)
            columnDescriptionGroupContainer.setSizeConstraint(0)


            columnArgGroupContainer = QtWidgets.QVBoxLayout()
            columnArgGroupContainer.setContentsMargins(0,0,0,0)
            columnArgGroupContainer.setSizeConstraint= (0)

            LayoutHInfoGroupContainer.addLayout(columnDescriptionGroupContainer)
            LayoutHInfoGroupContainer.addLayout(columnArgGroupContainer)

            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            LayoutVDonutContainer.addItem(spacerItem)

            labelCourseName = QtWidgets.QLabel()
            labelCourseName.setText(_translate("MainWindow","   Course:"))
            labelCourseName.setAlignment(QtCore.Qt.AlignRight)
            labelCourseName.setObjectName("LabelInforGroup")
            labelCourseName.setFont(font)
            columnDescriptionGroupContainer.addWidget(labelCourseName)

            LabelCourseNameArg = QtWidgets.QLabel()
            course = self.n_group_list[group][3]
            id_group = self.n_group_list[group][0]
            try:
                href =  href_couse_latamByTotalName[self.n_group_list[group][3]]
            except:
                href = None
            if href != None:
                LabelCourseNameArg.setText(_translate("MainWindow",f"<a href='{href}'> {self.n_group_list[group][3][0:10]}...</a>"))
                LabelCourseNameArg.linkActivated.connect(self.open_external_link)
                LabelCourseNameArg.setToolTip(_translate("MainWindow",f"{self.n_group_list[group][3][0:10]}"))
            else:
                LabelCourseNameArg.setText(_translate("MainWindow",f"{self.n_group_list[group][3][0:10]}..."))
                LabelCourseNameArg.setToolTip(_translate("MainWindow",f"{self.n_group_list[group][3][0:10]}"))
            LabelCourseNameArg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
            LabelCourseNameArg.setMinimumWidth(50)
            LabelCourseNameArg.setAlignment(QtCore.Qt.AlignLeft)
            LabelCourseNameArg.setStyleSheet("color:blue;")
            LabelCourseNameArg.setFont(font)
            columnArgGroupContainer.addWidget(LabelCourseNameArg)


            labelNextClass = QtWidgets.QLabel()
            labelNextClass.setText(_translate("MainWindow","Next Class:"))
            labelNextClass.setFont(font)
            labelNextClass.setObjectName("LabelInforGroup")
            labelNextClass.setAlignment(QtCore.Qt.AlignRight)
            columnDescriptionGroupContainer.addWidget(labelNextClass)

            labelNextClassArg = QtWidgets.QLabel()
            labelNextClassArg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
            labelNextClassArg.setMinimumWidth(50)
            labelNextClassArg.setFont(font)
            labelNextClassArg.setWordWrap(True)
            lastLesson =  self.n_group_list[group][4]
            if course in id_couse_latamByTotalName.keys():
                code = id_couse_latamByTotalName[course]
                try:
                    lessonHerfInd =  lesson_by_course_latam[code]['names'].index(lastLesson)
                    lessonHerf =  lesson_by_course_latam[code]['ref'][lessonHerfInd]
                except:
                    lessonHerfInd = ""
                    lessonHerf = ""
                labelNextClassArg.setText(_translate("MainWindow",f"<a href='{lessonHerf}'> {self.n_group_list[group][4][0:10]}</a>"))
                labelNextClassArg.setToolTip(_translate("MainWindow",f"{self.n_group_list[group][4]}"))
            elif course == None:
                code = None
                lessonHerfInd =  None
                lessonHerf =  None
                labelNextClassArg.setText(_translate("MainWindow",f"<a href='{lessonHerf}'> {self.n_group_list[group][4][0:10]}</a>"))
                labelNextClassArg.setToolTip(_translate("MainWindow",f"{self.n_group_list[group][4]}"))
            else:
                return('CourseNotFound')
            labelNextClassArg.linkActivated.connect(self.open_external_link)
            labelNextClassArg.setObjectName("LabelInforGroup")
            columnArgGroupContainer.addWidget(labelNextClassArg)

            labelStudents = QtWidgets.QLabel()
            labelStudents.setText(_translate("MainWindow","Stds:"))
            labelStudents.setFont(font)
            labelStudents.setObjectName("LabelInforGroup")
            labelStudents.setAlignment(QtCore.Qt.AlignRight)
            columnDescriptionGroupContainer.addWidget(labelStudents)

            labelStudentsArg = QtWidgets.QLabel()
            labelStudentsArg.setText(_translate("MainWindow",f"{self.n_group_list[group][2]}"))
            labelStudentsArg.setContentsMargins(0,0,0,0)
            labelStudentsArg.setFont(font)
            labelStudentsArg.setObjectName("LabelInforGroup")
            columnArgGroupContainer.addWidget(labelStudentsArg)

            NextLesson = QtWidgets.QLabel()
            NextLesson.setText(_translate("MainWindow","Next Lesson:"))
            NextLesson.setContentsMargins(0,0,0,0)
            NextLesson.setFont(font)
            NextLesson.setObjectName("LabelInforGroup")
            NextLesson.setAlignment(QtCore.Qt.AlignRight)
            columnDescriptionGroupContainer.addWidget(NextLesson)

            NextLessonArg = QtWidgets.QLabel()
            NextLessonArg.setText(_translate("MainWindow",f"{self.n_group_list[group][6]}"))
            NextLessonArg.setContentsMargins(0,0,0,0)
            NextLessonArg.setFont(font)
            NextLessonArg.setObjectName("LabelInforGroup")
            columnArgGroupContainer.addWidget(NextLessonArg)

            buttonMetricsLayout = QtWidgets.QHBoxLayout()
            buttonMetricsLayout.setSpacing(2)
            buttonMetricsLayout.setContentsMargins(0,0,0,0)
            buttonMetricsLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
            buttonMetricsLayout.setSizeConstraint(0)
            stretch = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            buttonMetricsLayout.addItem(stretch)

            if self.n_group_list[group][11] != "New":
                ButtonRecord = QtWidgets.QPushButton()
                ButtonRecord.setContentsMargins(0,0,0,0)
                ButtonRecord.setFixedSize(25,25)
                ButtonRecord.setObjectName("ButtonMetrics")
                icon = QtGui.QIcon(bs4Process(imageBS64["record"]))
                ButtonRecord.setIcon(icon)
                ButtonRecord.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                buttonMetricsLayout.addWidget(ButtonRecord)
                
                ButtonAnalytics = QtWidgets.QPushButton()
                ButtonAnalytics.setContentsMargins(0,0,0,0)
                ButtonAnalytics.setFixedSize(25,25)
                icon = QtGui.QIcon(bs4Process(imageBS64["money"]))
                ButtonAnalytics.setIcon(icon)
                ButtonAnalytics.setObjectName("ButtonMetrics")
                buttonMetricsLayout.addWidget(ButtonAnalytics)
                ButtonAnalytics.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                ButtonAnalytics.clicked.connect(partial(initBW.AddButtonFrameGroup, self.WindowMain, self.n_group_list[group][1], self.stackedWidget, self.n_group_list[group][0], self.n_group_list[group][2], self.n_group_list[group][3], self.n_group_list[group][4], self.n_group_list[group][5]))
                
                ButtonPoduin = QtWidgets.QPushButton()
                ButtonPoduin.setContentsMargins(0,0,0,0)
                ButtonPoduin.setFixedSize(25,25)
                icon = QtGui.QIcon(bs4Process(imageBS64["poduim2"]))
                ButtonPoduin.setIcon(icon)
                ButtonPoduin.setObjectName("ButtonMetrics")
                ButtonPoduin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                buttonUpdate = QtWidgets.QPushButton()
                iconUpdate = QtGui.QIcon(bs4Process(imageBS64['update']))
                buttonUpdate.setIcon(iconUpdate)
                buttonUpdate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                buttonUpdate.move(20, 130)
                buttonUpdate.setObjectName("buttonUpdate")
                buttonUpdate.setFixedSize(20,20)
                buttonUpdate.raise_()
                if (str(id_group) in buttonContainer) or poduim:
                    ButtonPoduin.setEnabled(True)
                    buttonUpdate.setEnabled(True)
                    buttonContainer[str(id_group)] = []
                    buttonContainer[str(id_group)].append(ButtonPoduin)
                    buttonContainer[str(id_group)].append(buttonUpdate)
                else:
                    ButtonPoduin.setEnabled(False)
                    buttonUpdate.setEnabled(False)
                    buttonContainer[str(id_group)] = []
                    buttonContainer[str(id_group)].append(buttonUpdate)
                    buttonContainer[str(id_group)].append(ButtonPoduin)

                if self.n_group_list[group][11] != "Graduate":
                    buttonMetricsLayout.addWidget(ButtonPoduin)
                    buttonUpdate.setParent(groupContainer)
                ButtonPoduin.clicked.connect(partial(self.ranking_generator_init, self.n_group_list[group][1], self.n_group_list[group][4]))


            spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            LayoutVMainInfoGroupContainer.addItem(spacerItem)

            LayoutVMainInfoGroupContainer.addLayout(buttonMetricsLayout)
            
            verticalLayout.addWidget(metricGroup)

            self.gridLayout.addWidget(groupContainer, rowW, colW)
            self.gridLayout.setParent(self.scrollContent)
            self.listMetrics.append([LayoutVDonutContainer, self.widget, labelStatus])

    def onDonutThreadFinished(self):
        instSeleMBG.driverQuit()

    def putMetricDonut(self):
        for n,group in enumerate(self.n_group_list): 
            listData = instSeleMBG.findPoints(group)
            listaLowBalance = listData[0]
            rows=listData[1]
            attNO = listData[2] - 1
            isGraduate = self.changeDataDonut(rows, n, group[0], attNO)
            self.putNewsSideBar(listaLowBalance, n)
            if not isGraduate:
                self.notification_handler.notification_signal.emit( 'ActivateButton',
                                                                    None,
                                                                    None,
                                                                    str(group[0]),
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    "no")
            else:
                self.notification_handler.notification_signal.emit( 'DelButton',
                                                                    None,
                                                                    None,
                                                                    str(group[0]),
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    "no")
            if n  == len(self.n_group_list) - 1:
                self.notification_handler.notification_signal.emit( None,
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    None,
                                                                    "yes")
        

    def changeDataDonut(self,rows,n, id, noAtt, last_group="no"):
            if noAtt  > 0:
                self.notification_handler.notification_signal.emit('NoAtt',
                                                                    None,
                                                                    None,
                                                                    f'https://backoffice.kodland.org/en/group_{self.n_group_list[n][0]}/',
                                                                    str(self.n_group_list[n][1]),
                                                                    str(noAtt),
                                                                    None,
                                                                    'no')
            if rows[2] == 'yes':
                self.listMetrics[n][2].setText("Graduate")
                self.listMetrics[n][2].setStyleSheet("background-color: #989c99")
                buttonContainer[self.listMetrics[n][0]] = "Graduate"
                db_manager().addEngagementStatusToDB(id,[0, 'Graduate'] )
                return True
            elif rows[2] == 'no' and self.n_group_list[n][11] == "New":
                self.listMetrics[n][2].setText("New")
                self.listMetrics[n][2].setStyleSheet("background-color:#4287f5; color: white")
                db_manager().addEngagementStatusToDB(id,[0, 'New'] )

            else:
                self.listMetrics[n][1].update_values(rows[0], rows[1], False, False)
                pointPer100 = (rows[0] / (rows[1] + rows[0])) * 100
                if pointPer100> 88:
                    self.listMetrics[n][2].setText("Perfect")
                    self.listMetrics[n][2].setStyleSheet("background-color:#4314a3; color: white")
                    db_manager().addEngagementStatusToDB(id,[7, 'Perfect'] )
                elif pointPer100> 70:
                    self.listMetrics[n][2].setText("High")
                    self.listMetrics[n][2].setStyleSheet("background-color:#14a33a")
                    db_manager().addEngagementStatusToDB(id,[6, 'High'] )
                elif pointPer100> 60:
                    self.listMetrics[n][2].setText("Good")
                    self.listMetrics[n][2].setStyleSheet("background-color:#25d654")
                    db_manager().addEngagementStatusToDB(id,[5, 'Good'] )
                elif pointPer100> 50:
                    self.listMetrics[n][2].setText("Regular")
                    self.listMetrics[n][2].setStyleSheet("background-color: #ffc547")
                    db_manager().addEngagementStatusToDB(id,[4, 'Regular'] )
                elif pointPer100> 35:
                    self.notification_handler.notification_signal.emit('criticalGroup',
                                                                    None,
                                                                    None,
                                                                    f'https://backoffice.kodland.org/en/group_{self.n_group_list[n][0]}/',
                                                                    str(self.n_group_list[n][1]),
                                                                    'low',
                                                                    None,
                                                                    'no')
                    self.listMetrics[n][2].setText("Low")
                    self.listMetrics[n][2].setStyleSheet("background-color:#ff8901")
                    db_manager().addEngagementStatusToDB(id,[3, 'Low'] )
                elif rows[0]> 25:
                    self.notification_handler.notification_signal.emit('criticalGroup',
                                                                    None,
                                                                    None,
                                                                    f'https://backoffice.kodland.org/en/group_{self.n_group_list[n][0]}/',
                                                                    str(self.n_group_list[n][1]),
                                                                    'bad',
                                                                        None,
                                                                        'no')
                    self.listMetrics[n][2].setText("Bad")
                    self.listMetrics[n][2].setStyleSheet("background-color:#ff2b2a")
                    db_manager().addEngagementStatusToDB(id,[2, 'Bad'] )
                else:
                    self.notification_handler.notification_signal.emit('criticalGroup',
                                                                    None,
                                                                    None,
                                                                    f'https://backoffice.kodland.org/en/group_{self.n_group_list[n][0]}/',
                                                                    self.n_group_list[n][1],
                                                                    'critical',
                                                                        None,
                                                                        'no')
                    self.listMetrics[n][2].setText("Critical")
                    self.listMetrics[n][2].setStyleSheet("background-color:#4a0404; color: white")
                    db_manager().addEngagementStatusToDB(id,[1, 'Critical'] )

                    

    def putNewsSideBar(self, listaLowBalance, n):
            for i,balance in enumerate(listaLowBalance):
                    name = balance[0]
                    href = balance[1]
                    phone = balance[3]
                    balance = str(balance[2])
                    self.notification_handler.notification_signal.emit('lowBalanceStudent',
                                                                href,
                                                                name,
                                                                phone,
                                                                None,
                                                                None,
                                                                balance,
                                                                'no') 
                        

    def abrir_archivo(self, enlace):
        webbrowser.open(enlace)
              

    def resizeEvent(self, event):
        if event.size().width() >=1000 and self.homeSize != "max":
            for i in reversed(range(self.gridLayout.count())):
                widget = self.gridLayout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            if self.buttonGridGeneratorOn:
                self.MakeGrid()
            else:
                self.MakeTable(resize=True)
            self.homeSize = "max" 
            self.sidebar.setGeometry(self.width()-40, 43, 230, self.height() - 43)
            self.sidebarChild.setGeometry(24, 0, 200, self.sidebar.height())
            self.sidebar_visible = False
        
        elif event.size().width() <=900 and self.homeSize != "min":
                for i in reversed(range(self.gridLayout.count())):
                    widget = self.gridLayout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

                if self.buttonGridGeneratorOn:
                    self.MakeGrid()
                else:
                    self.MakeTable(resize=True)
                self.sidebar.setGeometry(860, 43, 230, 510)
                self.sidebar_visible = False
                self.homeSize = "min"

    

        
    def MakeTable(self, resize=False):

        if self.buttonGridGeneratorOn or resize:
            self.buttonTableGeneratorOn = True
            self.buttonGridGeneratorOn = False
            for i in reversed(range(self.gridLayout.count())):
                    widget = self.gridLayout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

            labeIDHeader = QtWidgets.QLabel()        
            labeIDHeader.setText("ID")
            labeIDHeader.setObjectName("labelHeader")
            labeIDHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeNameHeader = QtWidgets.QLabel()        
            labeNameHeader.setText("Name")
            labeNameHeader.setObjectName("labelHeader")
            labeNameHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeStd = QtWidgets.QLabel()        
            labeStd.setText("Students")
            labeStd.setObjectName("labelHeader")
            labeStd.setAlignment(QtCore.Qt.AlignCenter)

            labeNameHeader = QtWidgets.QLabel()        
            labeNameHeader.setText("Name")
            labeNameHeader.setObjectName("labelHeader")
            labeNameHeader.setAlignment(QtCore.Qt.AlignCenter)
            labeNameHeader.setMinimumWidth(100)
            labeNameHeader.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)


            labeCourseHeader = QtWidgets.QLabel()        
            labeCourseHeader.setText("Course")
            labeCourseHeader.setObjectName("labelHeader")
            labeCourseHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeNextLessonHeader = QtWidgets.QLabel()        
            labeNextLessonHeader.setText("NextLesson")
            labeNextLessonHeader.setObjectName("labelHeader")
            labeNextLessonHeader.setAlignment(QtCore.Qt.AlignCenter)

            labePreviusLessonHeader = QtWidgets.QLabel()        
            labePreviusLessonHeader.setText("PreviusLesson")
            labePreviusLessonHeader.setObjectName("labelHeader")
            labePreviusLessonHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeNextClassHeader = QtWidgets.QLabel()        
            labeNextClassHeader.setText("NextClass")
            labeNextClassHeader.setObjectName("labelHeader")
            labeNextClassHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeQAHeader = QtWidgets.QLabel()        
            labeQAHeader.setText("QA")
            labeQAHeader.setObjectName("labelHeader")
            labeQAHeader.setAlignment(QtCore.Qt.AlignCenter)
            labeQAHeader.setMinimumWidth(200)
            labeQAHeader.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

            
            self.gridLayout.addWidget(labeIDHeader, 0,0)
            self.gridLayout.addWidget(labeNameHeader, 0,1)
            self.gridLayout.addWidget(labeQAHeader, 0,2)
            self.gridLayout.addWidget(labeCourseHeader, 0,3)
            self.gridLayout.addWidget(labeNextLessonHeader, 0,4)
            self.gridLayout.addWidget(labePreviusLessonHeader, 0,5)
            self.gridLayout.addWidget(labeNextClassHeader, 0,6)
            self.gridLayout.addWidget(labeStd, 0,7)
            



            for i in range(1,15):
                objeNameRow = f"LabelContend{str(i%2)}"
                labeID = QtWidgets.QLabel()        
                labeID.setText("ID")
                labeID.setObjectName(objeNameRow)
                labeID.setAlignment(QtCore.Qt.AlignCenter)

                labeName = QtWidgets.QLabel()        
                labeName.setText("<a href='http://www.ejemplo.com'>Name</a>")
                labeName.setObjectName(objeNameRow)
                labeName.setAlignment(QtCore.Qt.AlignCenter)

                labeStd = QtWidgets.QLabel()        
                labeStd.setText("1/10")
                labeStd.setObjectName(objeNameRow)
                labeStd.setAlignment(QtCore.Qt.AlignCenter)

                labeCourse = QtWidgets.QLabel()        
                labeCourse.setText("<a href='http://www.ejemplo.com'>Course</a>")
                labeCourse.setObjectName(objeNameRow)
                labeCourse.setAlignment(QtCore.Qt.AlignCenter)

                labeNextLesson = QtWidgets.QLabel()        
                labeNextLesson.setText("<a href='http://www.ejemplo.com'>NextLesson</a>")
                labeNextLesson.setObjectName(objeNameRow)
                labeNextLesson.setAlignment(QtCore.Qt.AlignCenter)

                button_style = """
                                    QPushButton {
                                        border-radius: 3px;
                                        background-color: #ede9e8;
                                        padding: 1px
                                    }

                                    QPushButton:hover {
                                        background-color: #dedcdc;
                                    }
                                    """

                labePreviusLessonWidget = QtWidgets.QWidget() 
                labePreviusLessonlayout = QtWidgets.QHBoxLayout(labePreviusLessonWidget) 
                labePreviusLesson = QtWidgets.QLabel()
                labePreviusLesson.setText("Previus\nLesson")
                labePreviusLesson.setObjectName(objeNameRow)
                labePreviusLessonWidget.setObjectName(objeNameRow)
                labePreviusLesson.setAlignment(QtCore.Qt.AlignCenter)
                ButtonRecord = QtWidgets.QPushButton()
                ButtonRecord.setContentsMargins(0,0,0,0)
                ButtonRecord.setObjectName("ButtonMetrics")
                icon = QtGui.QIcon(bs4Process(imageBS64["record"]))
                ButtonRecord.setIcon(icon)
                ButtonRecord.setStyleSheet(button_style)
                ButtonRecord.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                labePreviusLessonlayout.addWidget(labePreviusLesson)
                labePreviusLessonlayout.addWidget(ButtonRecord)


                labeNextClass = QtWidgets.QLabel()        
                labeNextClass.setText("Hoy")
                labeNextClass.setObjectName(objeNameRow)
                labeNextClass.setAlignment(QtCore.Qt.AlignCenter)

                labeQA = QtWidgets.QLabel()     
                labeQA.setObjectName(objeNameRow)
                labeQA.setAlignment(QtCore.Qt.AlignCenter)
            

                gridLabeQA = QtWidgets.QGridLayout(labeQA)
                gridLabeQA.setContentsMargins(0,3,0,3)
                gridLabeQA.setSpacing(0)
                porcentaje1 = 30
                porcentaje2 = 70

                # Barra de progreso 1
                progress_bar1 = QtWidgets.QProgressBar(self)
                progress_bar1.setValue(porcentaje1)
                progress_bar1.setObjectName("barTop")
                gridLabeQA.addWidget(progress_bar1, 0,1,1,4)

                # Etiqueta 1
                label1 = QtWidgets.QLabel(f'Attend', self)
                label1.setAlignment(QtCore.Qt.AlignRight)
                label1.setObjectName("LabelBar")
                gridLabeQA.addWidget(label1, 0,0)

                # Barra de progreso 2
                progress_bar2 = QtWidgets.QProgressBar(self)
                progress_bar2.setValue(porcentaje2)
                progress_bar2.setObjectName("barBottom")
                gridLabeQA.addWidget(progress_bar2, 1,1,1,4)

                # Etiqueta 2
                label2 = QtWidgets.QLabel(f'No Attend', self)
                label2.setAlignment(QtCore.Qt.AlignRight)
                label2.setObjectName("LabelBar")
                gridLabeQA.addWidget(label2,1,0)

                buttonMetricsWidget = QtWidgets.QWidget()
                buttonMetricsLayout = QtWidgets.QHBoxLayout(buttonMetricsWidget)
                buttonMetricsLayout.setSpacing(2)


                

                              
             
                

                buttonMetricsLayout.setContentsMargins(4,0,0,4)
                buttonMetricsLayout.setSizeConstraint(0)


                

                              
             
                

                              
                ButtonAnalytics = QtWidgets.QPushButton()
                ButtonAnalytics.setContentsMargins(0,0,0,0)
                icon = QtGui.QIcon(bs4Process(imageBS64["stats"]))
                ButtonAnalytics.setIcon(icon)
                ButtonAnalytics.setStyleSheet(button_style)
                ButtonAnalytics.setObjectName("ButtonMetrics")
                ButtonAnalytics.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                ButtonAnalytics.setMaximumSize(32,32)
                buttonMetricsLayout.addWidget(ButtonAnalytics)
                ButtonAnalytics.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                
                ButtonPoduin = QtWidgets.QPushButton()
                ButtonPoduin.setContentsMargins(0,0,0,0)
                icon = QtGui.QIcon(bs4Process(imageBS64["poduim3"]))
                ButtonPoduin.setIcon(icon)
                ButtonPoduin.setStyleSheet(button_style)
                ButtonPoduin.setMaximumSize(32,32)
                ButtonPoduin.setObjectName("ButtonMetrics")
                ButtonPoduin.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                ButtonPoduin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                buttonMetricsLayout.addWidget(ButtonPoduin)
                



                self.gridLayout.addWidget(labeID, i,0)
                self.gridLayout.addWidget(labeName, i,1)
                self.gridLayout.addWidget(labeQA, i,2)
                self.gridLayout.addWidget(labeCourse, i,3)
                self.gridLayout.addWidget(labeNextLesson, i,4)
                self.gridLayout.addWidget(labePreviusLessonWidget, i,5)
                self.gridLayout.addWidget(labeNextClass, i,6)
                self.gridLayout.addWidget(labeStd, i,7)
                self.gridLayout.addWidget(buttonMetricsWidget, i,8)

                    

class DonutChartWidget(QtWidgets.QWidget):
    def __init__(self, value1, value2,start, graduate,  *args):
        super().__init__()
        self.values = [value1, value2]
        self.start = start
        self.graduate = graduate
        self.setToolTip('Loading...')
        if self.start:
            self.values = [100, 0]
            self.negativeColor = [110, 105, 104]
            self.positiveColor = [110, 105, 104]
            if initTW.ReturnTheme() == "Dark":
                self.backgroundDonut = [39, 40, 34]
            else:
                self.backgroundDonut = [255, 255, 255]
            self.blur = QtWidgets.QGraphicsBlurEffect()
            self.blur.setBlurRadius(5)
            self.setGraphicsEffect(self.blur)
        elif initTW.ReturnTheme() == "Dark":
            self.backgroundDonut = [39, 40, 34]
            self.negativeColor = [136, 216, 41]
            self.positiveColor = [204, 86, 33]
        else:
            self.backgroundDonut = [255, 255, 255]
            self.negativeColor = [136, 216, 41]
            self.positiveColor = [204, 86, 33]


        if args:
            self.values.extend(args)


    def update_values(self, value1, value2, start, graduate, *args):
        self.values = [value1, value2]
        self.start = start
        self.graduate = graduate

        if args:
            self.values.extend(args)

        self.blur = QtWidgets.QGraphicsBlurEffect()
        self.blur.setBlurRadius(0)
        self.setGraphicsEffect(self.blur)
        self.update()  # Cambiar de repaint() a update()

    def paintEvent(self, event):
        if self.graduate:
            self.values = [100, 0]
            self.negativeColor = [110, 105, 104]
            self.positiveColor = [110, 105, 104]
            self.setToolTip(f'Graduated group')
        elif sum(self.values)>1 and not self.start:
            perAttend = int((self.values[0] / (self.values[0]  + self.values[1] ))*100)
            perNoAttend = 100 - perAttend 
            if initTW.ReturnTheme() == "Dark":
                self.backgroundDonut = [39, 40, 34]
                self.negativeColor = [136, 216, 41]
                self.positiveColor = [204, 86, 33]
            else:
                self.backgroundDonut = [255, 255, 255]
                self.negativeColor = [136, 216, 41]
                self.positiveColor = [204, 86, 33]
            self.setToolTip(f'the group has achieved a {perAttend}% of the total score.')

        total = sum(self.values)
        
        if total == 0:
            total = 100
        widget_width = self.width()
        widget_height = self.height()
        center_x = widget_width // 2
        center_y = widget_height // 2
        radius = int(min(center_x, center_y) * 0.8)
        hole_radius = int(radius * 0.5)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        start_angle = 0

        positive_brush = QtGui.QBrush(QtGui.QColor(*self.negativeColor))
        negative_brush = QtGui.QBrush(QtGui.QColor(*self.positiveColor))
        background_pen = QtGui.QPen(QtGui.QColor(*self.backgroundDonut))
        background_pen.setWidth(1)

        for i, value in enumerate(self.values):
            angle = int(value / total * 360)

            if i == 0:
                painter.setBrush(positive_brush)
            elif i == 1:
                painter.setBrush(negative_brush)

            painter.setPen(background_pen)

            painter.drawPie(center_x - radius, center_y - radius, radius * 2, radius * 2, start_angle * 16, angle * 16)
            start_angle += angle

        painter.setBrush(QtGui.QColor(*self.backgroundDonut))
        painter.drawEllipse(center_x - hole_radius, center_y - hole_radius, hole_radius * 2, hole_radius * 2)




