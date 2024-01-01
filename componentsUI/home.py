from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from componentsUI import topWindow
from src.dataBaseManager import db_manager
from src.selenuimManager import seleniumTakeMetricsByGroupBasic
from utils import stylesheetUI
import webbrowser

listMetrics = []
colSpam = 0

initTW = topWindow.TopWidget()



class Inithome(QtWidgets.QWidget):

    class DonutThread(QThread):
        finished = pyqtSignal()

        def run(self):
            print("DonutThread is running...")
            self.parent().putMetricDonut()
            print("DonutThread is finished.")
            self.finished.emit()

    def __init__(self, parent):
        super().__init__(parent)
        self.WindowHome(parent)
        self.homeSize = "Min"
        self.WindowMain = parent
        self.donut_thread = self.DonutThread(parent=self)
        self.donut_thread.finished.connect(self.onDonutThreadFinished)
        self.donut_thread.start()

        
        
    def onDonutThreadFinished(self):
        self.putMetricDonut()

    def retranslateUi(self, parent):
        self._translate = QtCore.QCoreApplication.translate
        parent.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.userImg.setText(self._translate("MainWindow", "<html><head/><body><p><img src=\"assets/images/user (1).png\"/></p></body></html>"))
        self.tutorName.setText(self._translate("MainWindow", "$TutorName"))
        self.Group.setText(self._translate("MainWindow", "Groups"))

    def WindowHome(self, parent):    
        self.setObjectName("centralwidgetHome")

        self.verticalLayoutMain = QtWidgets.QVBoxLayout(self)
        self.verticalLayoutMain.setContentsMargins(0, 0,0, 0)
        self.verticalLayoutMain.setSpacing(0)
        self.verticalLayoutMain.setObjectName("verticalLayout")

        initTW.CreateTopWidgetTitle(self.verticalLayoutMain, parent)

        #BODY ALL
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(14, 14, 14, 14)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutMain.addLayout(self.horizontalLayout)
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

        #Mení
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
        self.tutorName.setObjectName("tutorName")


        self.verticalLayout.addWidget(self.tutorName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        
        #BUTTON TO VIEW GROUP
        self.Group = QtWidgets.QPushButton(self.menu)
        self.Group.animateClick(100)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(8)
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
        icon = QtGui.QIcon("assets/images/layout.png")
        self.buttonGridGenerator.setIcon(icon)
        self.buttonGridGeneratorOn = False  
        self.buttonTableGeneratorOn = True

        
        self.buttonGridGenerator.clicked.connect(lambda : self.MakeGrid())
        self.buttonGridGenerator.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonGridGenerator.setObjectName("ButtonTable")
        self.buttonTableGenerator = QtWidgets.QPushButton()
        self.buttonTableGenerator.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon("assets/images/more.png")
        self.buttonTableGenerator.setIcon(icon)
        self.buttonTableGenerator.clicked.connect(self.MakeTable)    
        self.buttonTableGenerator.setObjectName("ButtonGrid")

        self.horizaontalLayoutheaderHome.addWidget(self.buttonGridGenerator)
        self.horizaontalLayoutheaderHome.addWidget(self.buttonTableGenerator)
        self.horizaontalLayoutheaderHome.setAlignment(QtCore.Qt.AlignLeft)
        self.horizaontalLayoutheaderHome.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.headerHomeContainer)

        self.spacerHeader = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizaontalLayoutheaderHome.addSpacerItem(self.spacerHeader)

        

        self.infolistOrdeGroupContainer = QtWidgets.QHBoxLayout()

        self.infolistOrdeGroup = QtWidgets.QLabel()
        self.infolistOrdeGroup.setText("sort by: ")
        self.infolistOrdeGroup.setObjectName("infolistOrdeGroup")
        self.listOrdeGroup = QtWidgets.QComboBox()
        self.listOrdeGroup.setObjectName("ComboBoxSortBy")

        # Agregar opciones al QComboBox
        self.listOrdeGroup .addItem("ID")
        self.listOrdeGroup .addItem("Engagement")
        self.listOrdeGroup .addItem("Nearest Class") 

        self.infolistOrdeGroupContainer.addWidget(self.infolistOrdeGroup)
        self.infolistOrdeGroupContainer.addWidget(self.listOrdeGroup)


        self.horizaontalLayoutheaderHome.addLayout(self.infolistOrdeGroupContainer)


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
        self.gridLayout.setVerticalSpacing(0)
        self.scroll_area.setWidget(self.scrollContent)
        self.layout.addWidget(self.scroll_area)

        self.horizontalLayout_4.addWidget(self.homeContainer, 0)
        self.horizontalLayout.addWidget(self.body)

        self.MakeGrid()

        parent.setCentralWidget(self)

        """SIDE BAR"""

        self.sidebar_visible = False
        

        self.sidebar = QtWidgets.QFrame(self)
        self.sidebar.setGeometry(860, 43, 230, 510)
        self.sidebar.setContentsMargins(0,0,0,0)
        self.sidebar.raise_()

        self.toggle_button = QtWidgets.QPushButton(self.sidebar)
        icon = QtGui.QIcon("assets/images/left-chevron.png")
        self.toggle_button.setIcon(icon)
        self.toggle_button.setGeometry(3,20, 30,30)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button.setObjectName("toggle_button")

        self.animation = QtCore.QPropertyAnimation(self.sidebar, b"pos")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Linear)

       

        self.sidebarChild = QtWidgets.QFrame(self.sidebar)
        sidebar_geometry = self.sidebar.geometry()  # Obtiene la geometría del sidebar
        self.sidebarChild.setGeometry(24, 0, 200, sidebar_geometry.height())
        self.sidebarChild.setObjectName("sidebarChild")
        self.verticalLayoutSidebar = QtWidgets.QVBoxLayout(self.sidebarChild)
        self.verticalLayoutSidebar.setContentsMargins(14,14,14,14)
        
        self.titleSideBar = QtWidgets.QLabel()
        self.titleSideBar.setText("Notifications")
        self.titleSideBar.setFont(font)
        self.titleSideBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleSideBar.setMaximumHeight(40)

        self.verticalLayoutSidebar.addWidget(self.titleSideBar)
        self.verticalLayoutSidebar.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)

        for i in range(3):
            contentItemsNews = QtWidgets.QWidget()
            contentItemsNews.setObjectName("contentItemsNews")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            contentItemsNews.setSizePolicy(sizePolicy)
            contentItemsNews.setMinimumSize(40,60)

            vertivalLayoutNewsContainer = QtWidgets.QVBoxLayout(contentItemsNews)

            infoNews = QtWidgets.QLabel()
            infoNews.setText("Texto normal y <a href='http://www.ejemplo.com'>enlace</a> en color azul.")
            infoNews.setObjectName("infoNews")
            infoNews.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
            infoNews.setWordWrap(True)
            vertivalLayoutNewsContainer.addWidget(infoNews)

            self.verticalLayoutSidebar.addWidget(contentItemsNews)


    
        self.retranslateUi(parent)
        QtCore.QMetaObject.connectSlotsByName(parent)
        



    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.hide_sidebar()
        else:
            self.show_sidebar()
        self.sidebar_visible = not self.sidebar_visible

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
    def MakeGrid(self):
        if self.buttonTableGeneratorOn :
            self.buttonGridGeneratorOn = True
            self.buttonTableGeneratorOn = False
            
            for i in reversed(range(self.gridLayout.count())):
                widget = self.gridLayout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        if self.width() >=1000:
            self.fontSize = 10
            colTarget=5
            spamDonut=4
            
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
            groupContainer.setTitle("")
            groupContainer.setFlat(False)
            groupContainer.setCheckable(False)
            groupContainer.setContentsMargins(0,0,0,0)
            groupContainer.setObjectName("groupContainer")
            
            verticalLayout = QtWidgets.QVBoxLayout(groupContainer)
            verticalLayout.setContentsMargins(0, 0, 0, 0)
            verticalLayout.setSpacing(0)
            verticalLayout.setObjectName("verticalLayout_2")


            nameGroup = QtWidgets.QLabel(groupContainer)
            nameGroup.setObjectName("nameGroup")
            nameGroup.setAlignment(QtCore.Qt.AlignTop)
            nameGroup.setMinimumHeight(30)
            nameGroup.setContentsMargins(0,0,0,0)
            
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(nameGroup.sizePolicy().hasHeightForWidth())
            nameGroup.setSizePolicy(sizePolicy)

            nameGroupContainer = QtWidgets.QHBoxLayout(nameGroup)
            nameGroupContainer.setContentsMargins(0,0,4,0)

            nameGroupText = ClickableLabel()
            nameGroupText.setObjectName("nameGroupText")
            nameGroupText.setOpenExternalLinks(True)
            nameGroupText.setText(f"<a href='https://backoffice.kodland.org/en/group_{self.n_group_list[group][0]}/'>{self.n_group_list[group][1]}</a>")
            nameGroupContainer.addWidget(nameGroupText)
            nameGroupText.link_clicked.connect(self.abrir_archivo)


            labelStatus = QtWidgets.QLabel()
            labelStatus.setFont(font)
            labelStatus.setText("-")
            labelStatus.setObjectName("labelStatus")
            labelStatus.setStyleSheet("color: black")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            labelStatus.setSizePolicy(sizePolicy)
            labelStatus.setContentsMargins(0,0,0,0)
            labelStatus.setMinimumSize(30,15)
            labelStatus.setMaximumSize(40,15)
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

            widget = DonutChartWidget(40,50)
            widget.setObjectName("widget")
            widget.setSizePolicy(sizePolicy)
            widget.setStyleSheet("border-left: 3px solid red;")
            LayoutVDonutContainer.addWidget(widget)
    
            
            ColorPartDonut1 = DonutChartWidget(40,60)
            ColorPartDonut1.setObjectName("BoxColorDonut1")
            ColorPartDonut1.setContentsMargins(0,0,0,0)
            ColorPartDonut1.setMaximumHeight(7)
            InfoPartDonut1 = QtWidgets.QLabel()
            InfoPartDonut1.setText(_translate("MainWindow","attend"))
            InfoPartDonut1.setObjectName("Text")
            InfoPartDonut1.setContentsMargins(0,0,0,0)
            InfoPartDonut1.setMaximumHeight(7)
            InfoPartDonut1.setFont(font)

            LayoutVDonutContainer.addWidget(ColorPartDonut1)
            LayoutVDonutContainer.addWidget(InfoPartDonut1)


            ColorPartDonut2 = QtWidgets.QLabel()
            ColorPartDonut2.setContentsMargins(0,0,0,0)
            ColorPartDonut2.setObjectName("BoxColorDonut2")
            ColorPartDonut2.setMaximumHeight(7)
            InfoPartDonut2 = QtWidgets.QLabel()
            InfoPartDonut2.setText(_translate("MainWindow","No attend"))
            InfoPartDonut2.setContentsMargins(0,0,0,0)
            InfoPartDonut2.setMaximumHeight(7)
            InfoPartDonut2.setObjectName("Text")
            InfoPartDonut2.setFont(font)

            LayoutVDonutContainer.addWidget(ColorPartDonut2)
            LayoutVDonutContainer.addWidget(InfoPartDonut2)

            spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
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
            columnDescriptionGroupContainer.setSizeConstraint= (0)


            columnArgGroupContainer = QtWidgets.QVBoxLayout()
            columnArgGroupContainer.setContentsMargins(0,0,0,0)
            columnArgGroupContainer.setSizeConstraint= (0)

            LayoutHInfoGroupContainer.addLayout(columnDescriptionGroupContainer)
            LayoutHInfoGroupContainer.addLayout(columnArgGroupContainer)

            labelCourseName = QtWidgets.QLabel()
            labelCourseName.setText(_translate("MainWindow","   Course:"))
            labelCourseName.setAlignment(QtCore.Qt.AlignRight)
            labelCourseName.setObjectName("LabelInforGroup")
            labelCourseName.setFont(font)
            columnDescriptionGroupContainer.addWidget(labelCourseName)

            LabelCourseNameArg = QtWidgets.QLabel()
            LabelCourseNameArg.setText(_translate("MainWindow",f"<a href='http://www.google.com'> {self.n_group_list[group][3]} </a>"))
            LabelCourseNameArg.linkActivated.connect(self.abrir_archivo)
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
            labelNextClassArg.setText(_translate("MainWindow",f"<a href='http://www.google.com'> {self.n_group_list[group][4]} </a>"))
            labelNextClassArg.setFont(font)
            labelNextClassArg.linkActivated.connect(self.abrir_archivo)
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
            buttonMetricsLayout.setSizeConstraint(0)

            ButtonRecord = QtWidgets.QPushButton()
            ButtonRecord.setContentsMargins(0,0,0,0)
            ButtonRecord.setObjectName("ButtonMetrics")
            icon = QtGui.QIcon("assets/images/video-camera.png")
            ButtonRecord.setIcon(icon)
            ButtonRecord.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            buttonMetricsLayout.addWidget(ButtonRecord)
            
            ButtonAnalytics = QtWidgets.QPushButton()
            ButtonAnalytics.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon("assets/images/money-graph-with-up-arrow.png")
            ButtonAnalytics.setIcon(icon)
            ButtonAnalytics.setObjectName("ButtonMetrics")
            buttonMetricsLayout.addWidget(ButtonAnalytics)
            ButtonAnalytics.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
            ButtonPoduin = QtWidgets.QPushButton()
            ButtonPoduin.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon("assets/images/podium (2).png")
            ButtonPoduin.setIcon(icon)
            ButtonPoduin.setObjectName("ButtonMetrics")
            ButtonPoduin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            buttonMetricsLayout.addWidget(ButtonPoduin)

            spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            LayoutVMainInfoGroupContainer.addItem(spacerItem)

            LayoutVMainInfoGroupContainer.addLayout(buttonMetricsLayout)
            
            verticalLayout.addWidget(metricGroup)

            self.gridLayout.addWidget(groupContainer, rowW, colW)
            self.gridLayout.setParent(self.scrollContent)
            self.listMetrics.append([LayoutVDonutContainer, widget, labelStatus])

    def onDonutThreadFinished(self):
        print("Donut Thread Finished")

    def load_gif(self, path):
        movie = QtGui.QMovie(path)
        self.gif.setMovie(movie)
        movie.start()



    def putMetricDonut(self):
        for i in range(len(self.listMetrics)):           
            n_std = self.n_group_list[i][2].split('/')
            n_std = int(n_std[0])
            argList = seleniumTakeMetricsByGroupBasic().findPoints(self.n_group_list[i][0], n_std)
            self.listMetrics[i][1].update_values(*argList)
            if argList[1]> 88:
                self.listMetrics[i][2].setText("Perfect")
                self.listMetrics[i][2].setStyleSheet("color:blue")
            elif argList[1]> 70:
                self.listMetrics[i][2].setText("High")
                self.listMetrics[i][2].setStyleSheet("color:cyan")
            elif argList[1]> 60:
                self.listMetrics[i][2].setText("Good")
                self.listMetrics[i][2].setStyleSheet("color:green")
            elif argList[1]> 50:
                self.listMetrics[i][2].setText("Regular")
                self.listMetrics[i][2].setStyleSheet("color:yellow")
            elif argList[1]> 35:
                self.listMetrics[i][2].setText("Low")
                self.listMetrics[i][2].setStyleSheet("color:orange")
            elif argList[1]> 25:
                self.listMetrics[i][2].setText("Bad")
                self.listMetrics[i][2].setStyleSheet("color:red")
            else:
                self.listMetrics[i][2].setText("Critical")
                self.listMetrics[i][2].setStyleSheet("color:brown")

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
                icon = QtGui.QIcon("assets/images/video-camera.png")
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
                icon = QtGui.QIcon("assets/images/stats.png")
                ButtonAnalytics.setIcon(icon)
                ButtonAnalytics.setStyleSheet(button_style)
                ButtonAnalytics.setObjectName("ButtonMetrics")
                ButtonAnalytics.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                ButtonAnalytics.setMaximumSize(32,32)
                buttonMetricsLayout.addWidget(ButtonAnalytics)
                ButtonAnalytics.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                
                ButtonPoduin = QtWidgets.QPushButton()
                ButtonPoduin.setContentsMargins(0,0,0,0)
                icon = QtGui.QIcon("assets/images/podium.png")
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
    def __init__(self, value1, value2, *args):
        super().__init__()
        self.values = [value1, value2]
        if initTW.ReturnTheme() == "Dark":
            self.backgroundDonut =  [39, 40, 34]
            self.negativeColor =    [136, 216, 41]
            self.positiveColor =    [204, 86, 33]
        else :
            self.backgroundDonut =  [255, 255, 255]
            self.negativeColor =    [136, 216, 41]
            self.positiveColor =    [204, 86, 33]

        if args:
            self.values.extend(args)

    def update_values(self, value1, value2, *args):
        self.values = [value1, value2]
        if sum(self.values) <1:
            self.values = [100,0]
            self.negativeColor = [110, 105, 104]
            self.positiveColor = [110, 105, 104]
        if args:
            self.values.extend(args)
        self.repaint()


    def paintEvent(self, event):
        total = sum(self.values)
        widget_width = self.width()
        widget_height = self.height()
        center_x = widget_width // 2
        center_y = widget_height // 2
        radius = int(min(center_x, center_y) * 0.8)
        hole_radius = int(radius * 0.5)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        start_angle = 0

        positive_brush = QtGui.QBrush(QtGui.QColor(*self.positiveColor))
        negative_brush = QtGui.QBrush(QtGui.QColor(*self.negativeColor))
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

        painter.end()

class ClickableLabel(QtWidgets.QLabel):
    link_clicked = QtCore.pyqtSignal(QtCore.QUrl)

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        self.setStyleSheet("color: blue; text-decoration: underline;")

    def mousePressEvent(self, event):
        anchor = self.anchorAt(event.pos())
        if anchor:
            url = QtCore.QUrl(anchor)
            self.link_clicked.emit(url)
        super(ClickableLabel, self).mousePressEvent(event)