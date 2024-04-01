"""
Python module for managing a graphical user interface (GUI) application using PyQt5.

Classes:
- SpiderChartWidget: Widget for displaying a spider chart.
- BottomWidget: Widget for managing the bottom section of the GUI.
- PopupWindow: Popup window for displaying messages.

Functions:
- bs4Process: Process image data using BeautifulSoup.
- textStatusStudent: Determine the status of a student based on their task engagement percentage.
"""
from PyQt5 import QtWidgets, QtCore, QtGui
import threading as th
from functools import partial
from src.selenuimManager import SelenuimThreadLoggin, UserName, UserPass
from src.dataBaseManager import db_manager
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import webbrowser, time
from utils.constants import data
imageBS64  = data["imageBS64"]
href_couse_latamByTotalName = data["href_couse_latamByTotalName"]
lesson_by_course_latam= data["lesson_by_course_latam"] 
id_couse_latamByTotalName = data["id_couse_latamByTotalName"]
points_total_course_latam = data["points_total_course_latam"]
textTemplate = data["textTemplate"]
from utils import constants
import base64, traceback

Theme = "Light"
frameDelete = 0

instSele= SelenuimThreadLoggin()
intDB = db_manager()

def bs4Process(bs4):
    """
    Process image data using BeautifulSoup.

    Args:
    - bs4 (str): Base64-encoded image data.

    Returns:
    - QtGui.QPixmap: Processed image data.
    """
    image_data = base64.b64decode(bs4.split(',')[1])
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(image_data)

    return pixmap

class SpiderChartWidget(QtWidgets.QWidget):
    """
    Widget for displaying a spider chart.

    Attributes:
    - categories (list): List of categories for the chart.
    - data (list): List of data points for the chart.
    """
    def __init__(self, data, categories):
        """
        Initialize SpiderChartWidget.

        Args:
        - data (list): List of data points for the chart.
        - categories (list): List of categories for the chart.
        """
        super().__init__()
        self.categories = categories
        self.data = data
        self.initUI()
        

    def initUI(self):
        """
        Initialize the user interface for the spider chart.
        """
        self.setContentsMargins(0,0,0,0)
        self.setObjectName("SpiderChart")
        angles = np.linspace(0, 2 * np.pi, len(self.categories), endpoint=False).tolist()
        values = self.data + [self.data[0]]
        angles += angles[:1]

        fig, ax = plt.subplots(subplot_kw=dict(polar=True), figsize=(1.5, 1.5))
        fig.subplots_adjust(left=-0.1, right=0.9, top=0.9, bottom=0.1)
        ax.fill(angles, values, color='teal', alpha=0.25)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.patch.set_alpha(0)
        ax.set_xticklabels(self.categories, fontsize=8, ha='center', rotation=45)
        ax.set_ylim(0, max(self.data) + 2)
        fig.patch.set_alpha(0) 
        canvas = FigureCanvas(fig)
        canvas.setFixedHeight(180)
        canvas.setFixedWidth(220) 
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(canvas)
        self.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        plt.close(fig)

class BottomWidget():
    """
    Widget for managing the bottom section of the GUI.
    """

    class BottomWidgetSignals(QtCore.QObject):
        """
        Signals for BottomWidget class.
        """
        updateGridLayoutSignal = QtCore.pyqtSignal(list, list, list, QtWidgets.QLayout, QtWidgets.QWidget, QtWidgets.QWidget, QtWidgets.QLabel, int, QtWidgets.QHBoxLayout, str, str, QtWidgets.QStackedWidget, QtWidgets.QWidget)

    def __init__(self):
        """
        Initialize BottomWidget.
        """
        self.frame = 0
        self.screenID = {}
        self.ScreensGroup = []
        self.signals = self.BottomWidgetSignals()
        self.signals.updateGridLayoutSignal.connect(self.updateGridLayout)

    def OpenTemplateMetric(self, jsonList):
        """
        Opens and updates the JavaScript files 'itemsCharts.js' and 'plantilla-metric-of-stundets.js' with the new JSON list `jsonList`.
        Then, opens the 'plantilla-metric-of-stundets.html' file in a web browser to display the data.
        After 5 seconds, the data is replaced with empty lists in the JavaScript files.

        Parameters:
        jsonList (list): New JSON list to update the JavaScript files with.

        Returns:
        None
        """  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        itemsRanking = os.path.join(parent_dir, r"assets/template-metrics-students", "itemsCharts.js")
        with open(itemsRanking, 'r') as archivo:
            contenido = archivo.read()

        templateMetrics = os.path.join(parent_dir, r"assets/template-metrics-students", "plantilla-metric-of-stundets.js")
        with open(templateMetrics, 'r') as archivo2:
            contenido2 = archivo2.read()

        # Modificar la lista en el contenido
        nueva_lista = jsonList # Nueva lista que deseas usar
        nuevo_contenido = contenido.replace('const Data = [];', f'const Data = {nueva_lista};')
        nuevo_contenido2 = contenido2.replace('const Data1 = [];', f'const Data1 = {nueva_lista};')
        # Escribir el contenido actualizado en el archivo JavaScript
        with open(itemsRanking, 'w') as archivo:
            archivo.write(nuevo_contenido)
        with open(templateMetrics, 'w') as archivo2:
            archivo2.write(nuevo_contenido2)
        htmlItems = os.path.join(parent_dir, r"assets/template-metrics-students", "plantilla-metric-of-stundets.html")
        webbrowser.open_new_tab(htmlItems)
        time.sleep(5)
        nuevo_contenido = contenido.replace(f'const Data = {nueva_lista};', 'const Data = [];')
        nuevo_contenido2 = contenido2.replace(f'const Data1 = {nueva_lista};', 'const Data1 = [];')
        
        with open(itemsRanking, 'w') as archivo:
            archivo.write(nuevo_contenido)
        with open(templateMetrics, 'w') as archivo2:
            archivo2.write(nuevo_contenido2)

    def generatorSummaryWeek(self, stdMetrics, attedancePercent, parent):
            """
            Generates a weekly summary message for a student based on their attendance percentage and metrics.

            Parameters:
            stdMetrics (list): A list of student metrics.
            attedancePercent (int): The student's attendance percentage.
            parent (QWidget): The parent widget.

            Returns:
            None
            """
            attendance_thresholds = [95, 80, 70, 60, 40]
            attendance_levels = ["Perfecta", "Alta", "Buena", "Media", "Regular", "Baja"]

            for threshold, level in zip(attendance_thresholds, attendance_levels):
                if attedancePercent >= threshold:
                    level_attendance = level
                    break
            else:
                level_attendance = "Baja"
            if stdMetrics[5]==0:
                messageWA = f"*Resumen%20Semanal%20de%20{stdMetrics[1]}*%20%F0%9F%98%8A%0A%0AActualmente%20tienes%20**{stdMetrics[3]+stdMetrics[4]}%20Tareas%20entregadas*%20|%20*{stdMetrics[5]}%20Tareas%20por%20entregar*%0A%0A*Tu%20asistencia%20es%20{level_attendance},%20has%20asistido%20hasta%20el%20momento%20al%20{attedancePercent}%%20de%20las%20clases.*%0A%0A*_Si%20desea%20mi%20ayuda,%20no%20olvide%20escribirme%20a%20este%20número.%20Estaré%20atento%20a%20cualquier%20inquietud_.%20:D"
            else:
                strTotalNoAttendActivity = ''
                for l in stdMetrics[20].keys():
                    textKeys = f'*Lección {l[1:]}*'
                    textTask = ''
                    for no_a in stdMetrics[20][l][1]:
                        task = no_a.split("/")
                        textTask += f'\n-https://platform.kodland.org/es/{task[-1]}'
                    strTotalNoAttendActivity += f'{textKeys}:{textTask}\n'    
                message = textTemplate["ESP"]["sumaryWeek"].replace("#nameStudent#", str(stdMetrics[1])).replace('#taskSub#', str(stdMetrics[4] + stdMetrics[3])).replace("#taskNoSub#", str(stdMetrics[5])).replace('#AttendPercent#', (str(attedancePercent)+"%")).replace('#attendaceLevel#', level_attendance).replace("#taskHerf#", strTotalNoAttendActivity)
                messageToWa = message.replace("\n", "%0A").replace(" ", "%20")
                if len(messageToWa) <  1000:
                    link = "https://api.whatsapp.com/send/?phone="+stdMetrics[18]+"&text="+messageToWa+"&type=phone_number&app_absent=0"
                    webbrowser.open_new(str(link))
                else:
                    messageToWa = textTemplate["ESP"]["WaLimitUp"].replace("\n", "%0A").replace(" ", "%20").replace(":", "%3A").replace("/", "%2F")
                    link = "https://api.whatsapp.com/send/?phone="+stdMetrics[18]+"&text="+messageToWa+"&type=phone_number&app_absent=0"
                    webbrowser.open_new(str(link))
                    self.openPopup(message)

    def openPopup(self, text):
            """
            Opens a popup window with the given text.

            Parameters:
                text (str): The text to be displayed in the popup window.
            """
            popup = PopupWindow(text)
            popup.exec_()                   
                     
    def open_external_link(self, url):
            """
            Opens an external link in the default web browser.

            Parameters:
                url (str): The URL of the external link to be opened.
            """
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
    
    def openTaskNoSummit(self, event, TasksNotReviewed):
        """
        Opens a web browser for each task not reviewed.

        Parameters:
            event: Event object.
            TasksNotReviewed (dict): Dictionary containing tasks not reviewed.
        """
        for href in TasksNotReviewed:
                webbrowser.open_new(str(href))
            
    def updateGridLayout(self, listID, ListLabel, listStd, layoutDChart, WidgetLoading, widgetMetrics, labelTextLoading, frame, boxHLayoudParent, typeCommand, nameGroup, stakeWdiget, MetricsGroupContainer):
            """
            Updates the grid layout with student data and displays spider chart.

            Parameters:
                listID (list): List of student IDs.
                ListLabel (list): List of labels for displaying student data.
                listStd (list): List of student data.
                layoutDChart: Layout for displaying the spider chart.
                WidgetLoading: Loading widget.
                widgetMetrics: Metrics widget.
                labelTextLoading: Label for loading status.
                frame: Frame object.
                boxHLayoudParent: Horizontal layout box.
            """
            
            if typeCommand == 'readyMetric': 
                attend_percent_general = 0
                percentTask_general = 0
                pointGeneral = 0
                course = listStd[0][23]
                id_course = id_couse_latamByTotalName[course]
                n_class = listStd[0][24]
                pointTotal = sum(points_total_course_latam[id_course][0:n_class+1])
                totalStd = len(listStd)
                labelTextLoading.setText("Put Data...")
                for i, id in enumerate(listStd):   
                    pointGeneral += int(id[9])
                    for ind, l in  enumerate(ListLabel[i]):
                        if ind == 0:
                            l.setText(f"{id[0]}")
                        elif ind == 1:
                            l.setText(f"<a href='https://backoffice.kodland.org/en/student_{id[0]}/'>{id[1]}<a>")
                            l.setOpenExternalLinks(True)
                            l.linkActivated.connect(self.open_external_link)
                        elif ind == 2:
                            percentTask = ((id[4]+id[3])/id[21])*100
                            textLabelStatus = self.textStatusStudent(percentTask)
                            l.setText(f"<b>{textLabelStatus[0]}</b>")
                            l.setStyleSheet(textLabelStatus[1])
                        elif ind == 3:
                            percentTask = int(((id[4]+id[3])/id[21])*100)
                            percentTask_general += percentTask
                            l.setText(f'<span>{id[4]+id[3]}/{id[21]}</span>\n<span><b>{percentTask}%</b></span>')
                        elif ind == 4:
                            l.setText(f"{id[3]}")
                            l.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                            l.setStyleSheet("color:blue;")
                            l.mousePressEvent = partial(self.openTaskNoSummit, TasksNotReviewed=id[26])
                        elif ind == 5:
                            attedancePercent= int((id[13]/id[14]) * 100) 
                            attend_percent_general += attedancePercent
                            l.setText(f'<span>{id[13]}/{id[14]}</span>\n<span><b>{attedancePercent}%</b></span>')
                            
                        elif ind == 6:
                            attedancePercent= int((id[13]/id[14]) * 100) 
                            ButtonTaskSummary = QtWidgets.QPushButton()
                            ButtonTaskSummary.setContentsMargins(0,0,0,0)
                            ButtonTaskSummary.setObjectName("ButtonMetrics")
                            icon = QtGui.QIcon(bs4Process(imageBS64["wa"]))
                            ButtonTaskSummary.setIcon(icon)
                            ButtonTaskSummary.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                            ButtonTaskSummary.clicked.connect(partial(self.generatorSummaryWeek,id, attedancePercent,boxHLayoudParent.parent().parent()))
                            l.addWidget(ButtonTaskSummary)
                        elif ind == 7:
                            ButtonSummaryGeneral = QtWidgets.QPushButton()
                            ButtonSummaryGeneral.setContentsMargins(0,0,0,0)
                            ButtonSummaryGeneral.setObjectName("ButtonMetrics")
                            icon = QtGui.QIcon(bs4Process(imageBS64["money"]))
                            ButtonSummaryGeneral.setIcon(icon)
                            ButtonSummaryGeneral.clicked.connect(partial(self.OpenTemplateMetric,id,))
                            ButtonSummaryGeneral.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                            l.addWidget(ButtonSummaryGeneral)
                asisGlobal = int((attend_percent_general/totalStd)/10)
                attendTaskGlobal = int((percentTask_general/totalStd)/10)
                pointGlobal = int((pointGeneral/ (pointTotal*totalStd))*10)
                data = [asisGlobal, attendTaskGlobal, pointGlobal]        
                categories = [f"Attendance\n{asisGlobal*10}%",f"Engagenment\n{attendTaskGlobal*10}%", f"Score\n{pointGlobal*10}%"]
                spider_chart = SpiderChartWidget(data, categories)
                layoutDChart.addWidget(spider_chart)
                WidgetLoading.setVisible(False)
                widgetMetrics.setVisible(True)
            elif typeCommand == "ErrorToTakeMetrics":
                # Eliminar todos los widgets dentro del contenedor boxLoadingLabel
                for i in reversed(range(WidgetLoading.layout().count())):
                    widgetToRemove = WidgetLoading.layout().itemAt(i).widget()
                    if widgetToRemove is not None:
                        widgetToRemove.setParent(None)
                        
                verticalLayouMetricLoading = WidgetLoading.layout()
                loadingMetricInfo = QtWidgets.QLabel()
                loadingMetricInfo.setText(f"Something went wrong, these are the possible reasons, \ninternet disconnection or low latency, or something has changed on the kodland page.\n\nExit and try again, if it occurs again report the error.\n\n{listID}")
                loadingMetricInfo.setAlignment(QtCore.Qt.AlignJustify)
                ButtonExit = QtWidgets.QPushButton()
                ButtonExit.setContentsMargins(0,0,0,0)
                icon = QtGui.QIcon("assets/images/exit-full-screen.png")
                ButtonExit.setIcon(icon)
                ButtonExit.setText('Exit')
                ButtonExit.setObjectName("ButtonMetrics")
                ButtonExit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                ButtonExit.setFixedSize(100,30)
                ButtonExit.clicked.connect(partial(self.exitFrame, frame, stakeWdiget, nameGroup, MetricsGroupContainer))
                verticalLayouMetricLoading.addWidget(loadingMetricInfo)
                verticalLayouMetricLoading.addWidget(ButtonExit)
                verticalLayouMetricLoading.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)

                WidgetLoading.update()


                 
            
    def textStatusStudent(self, percentTask):
        """
        Determines the text status of a student based on the percentage of completed tasks.

        Parameters:
            percentTask (float): The percentage of completed tasks.

        Returns:
            list: A list containing the status text and color code.
        """
        if percentTask < 20:
            text = "Bad"
            color = "color:#ff2b2a"
        elif percentTask < 40:
            text = "Low"
            color = "color:#ff8901"
        elif percentTask < 60:
            text = "Regular"
            color = "color: #ffc547"
        elif percentTask < 80:
            text = "Good"
            color = "color:#25d654"
        elif percentTask < 95:
            text = "High"
            color = "color:#14a33a"
        else:
            text = "Perfect"
            color = "color:#4314a3"
        return [text, color]

    def runMetric(self,id_group, 
                    name_group, 
                    n_student, 
                    curso, 
                    last_class,
                    next_class,
                    listLabel,
                    layoutChart, labelGif, widgetMetrics, labelText, frame, BoxLayout, stakeWdiget, MetricsGroupContainer):
            """
            Runs metric calculations for a group of students and updates the grid layout with the metrics.
            Parameters:
                id_group (int): The ID of the student group.
                name_group (str): The name of the student group.
                n_student (int): The number of students in the group.
                curso (str): The course of the group.
                last_class (str): The last class of the group.
                next_class (str): The next class of the group.
                listLabel (list): List of labels for displaying student data.
                layoutChart: Layout for displaying the spider chart.
                labelGif: GIF label.
                widgetMetrics: Metrics widget.
                labelText: Label for displaying text.
                frame: Frame object.
                BoxLayout: Widget object.
            """
            dataLoggin = intDB.findPassAndUserCache()
            self.metrics = instSele.takeMetricGroup(id_group = id_group, 
                    name_group = name_group, 
                    n_student = n_student, 
                    curso = curso, 
                    last_class = last_class,
                    next_class = next_class,
                    user=UserName,
                    passw=UserPass)
            listSd = self.metrics[name_group]
            listSdID = list(listSd.keys())
            listSdMetrics = list(listSd.values())
            self.signals.updateGridLayoutSignal.emit(listSdID, listLabel, listSdMetrics, layoutChart, labelGif, widgetMetrics, labelText, frame, BoxLayout, 'readyMetric', name_group, stakeWdiget, MetricsGroupContainer)
            totalPoints = sum(int(cache[9]) for cache in self.metrics[name_group].values())
            intDB.updateScoreByGroup(id_group, totalPoints)
            self.signals.updateGridLayoutSignal.emit([], listLabel, [], layoutChart, labelGif, widgetMetrics, labelText, frame, BoxLayout, 'ErrorToTakeMetrics', name_group, stakeWdiget, MetricsGroupContainer)

                
                
            
            
    def AddButtonFrameGroup(self, parent, nameGroup,stackedWidget, id_group, n_student,  curso, last_class, next_class):
        """
        Adds a button for a new group to the frame and sets up corresponding widgets for metrics display.

        Parameters:
            parent: Parent widget.
            nameGroup (str): Name of the group.
            stackedWidget: Stacked widget for managing multiple screens.
            id_group (int): ID of the group.
            n_student (str): Number of students in the group.
            curso (str): Course of the group.
            last_class (str): Last class of the group.
            next_class (str): Next class of the group.
        """
        def SwitchGroup(nameGroup):
                """Switches between group screens."""
                ind = self.screenID[nameGroup]
                stackedWidget.setCurrentIndex(ind)  

        if nameGroup not in self.screenID.keys():
            self.stackedWidget = stackedWidget
            name = nameGroup
            buttonNewGroup = QtWidgets.QPushButton()
            buttonNewGroup.setMinimumSize(80,20)
            buttonNewGroup.setStyleSheet("border-radius: 0px;") 
            buttonNewGroup.setText(nameGroup)
            buttonNewGroup.setObjectName("HomeON")
            buttonNewGroup.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.frame += 1
            frame = self.frame 
            buttonNewGroup.clicked.connect(partial(SwitchGroup, nameGroup))
            stacked_widget_now= stackedWidget.widget(frame)
            self.verticalButton.addWidget(buttonNewGroup)
            MetricsGroupContainer = QtWidgets.QWidget()
            MetricsGroupContainer.setGeometry(0,30, stackedWidget.width(), stackedWidget.height()-50)
            MetricsGroupContainer.setContentsMargins(0,0,0,0)

            containerBox_H = QtWidgets.QHBoxLayout(MetricsGroupContainer)
            containerBox_H.setContentsMargins(0,0,0,0)
            containerBoxHParentWidget = QtWidgets.QWidget()
            containerBoxHParentWidget.setVisible(False)
            containerBoxHParentWidget.setGeometry(0,0, MetricsGroupContainer.width(), MetricsGroupContainer.height())
            containerBoxHParentWidget.setContentsMargins(8,8,8,8)
            containerBoxHParent = QtWidgets.QHBoxLayout(containerBoxHParentWidget)

            containerBox_H.addWidget(containerBoxHParentWidget)

            wcontainerBoxVinfoGroup = QtWidgets.QWidget()
            wcontainerBoxVinfoGroup.setObjectName("wcontainerBoxVinfoGroup")
            containerBoxVinfoGroup = QtWidgets.QVBoxLayout(wcontainerBoxVinfoGroup)
            containerBoxVinfoGroup.setSpacing(4)
            containerBoxVinfoGroup.setContentsMargins(0,0,0,0)
            containerBoxVinfoGroup.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
            labeNameGroup = QtWidgets.QLabel()
            labeNameGroup.setContentsMargins(8,8,8,8)
            labeNameGroup.setText(nameGroup)
            labeNameGroup.setObjectName("labeNameGroup")
            labeNameGroup.setAlignment(QtCore.Qt.AlignCenter)
            widgetChart = QtWidgets.QWidget()
            widgetChart.setContentsMargins(0,0,0,0)
            layoutDChart = QtWidgets.QVBoxLayout(widgetChart)
            layoutDChart.setContentsMargins(-40,0,0,0)

            
            containerDescription = QtWidgets.QWidget()
            containerDescription.setObjectName("containerDescriptionGroup")
            layoutDescription = QtWidgets.QVBoxLayout(containerDescription)
            labelTitle = QtWidgets.QLabel()
            labelTitle.setText("Description")
            labelTitle.setObjectName("labelTitleDescriptionGroup")
            labelInfoDes = QtWidgets.QLabel()
            labelInfoDes.setObjectName("labelInfoDesDescriptionGroup")
            layoutDescription.addWidget(labelTitle)
            layoutDescription.addWidget(labelInfoDes)
            
            containerBoxVinfoGroup.addWidget(labeNameGroup)
            containerBoxVinfoGroup.addWidget(widgetChart)
            containerBoxVinfoGroup.addWidget(containerDescription)
            containerBoxHParent.addWidget(wcontainerBoxVinfoGroup)
    
            wcontainerBoxVinfoStundents = QtWidgets.QWidget()
            containerBoxVinfoStundents = QtWidgets.QVBoxLayout(wcontainerBoxVinfoStundents)

            headerGroupContainer  = QtWidgets.QWidget()
            headerGroupContainer.setContentsMargins(0,0,0,0)
            headerGroupContainer.setObjectName("headerGroupContainer")
            horizaontalLayoutheaderHome = QtWidgets.QHBoxLayout(headerGroupContainer)
            horizaontalLayoutheaderHome.setContentsMargins(0,0,0,0)
            buttonMetricsLayout = QtWidgets.QHBoxLayout()
            buttonMetricsLayout.setSpacing(2)
            buttonMetricsLayout.setContentsMargins(0,0,0,0)
            buttonMetricsLayout.setSizeConstraint(0)

            ButtonRecord = QtWidgets.QPushButton()
            ButtonRecord.setContentsMargins(0,0,0,0)
            ButtonRecord.setObjectName("ButtonMetrics")
            icon = QtGui.QIcon(bs4Process(imageBS64["record"]))
            ButtonRecord.setIcon(icon)
            ButtonRecord.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            buttonMetricsLayout.addWidget(ButtonRecord)
            
            ButtonUpdate = QtWidgets.QPushButton()
            ButtonUpdate.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon(bs4Process(imageBS64["update"]))
            ButtonUpdate.setIcon(icon)
            ButtonUpdate.setObjectName("ButtonMetrics")
            buttonMetricsLayout.addWidget(ButtonUpdate)
            ButtonUpdate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
            
            ButtonPoduin = QtWidgets.QPushButton()
            ButtonPoduin.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon(bs4Process(imageBS64["poduim2"]))
            ButtonPoduin.setIcon(icon)
            ButtonPoduin.setObjectName("ButtonMetrics")
            ButtonPoduin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            buttonMetricsLayout.addWidget(ButtonPoduin)

            ButtonExit = QtWidgets.QPushButton()
            ButtonExit.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon("assets/images/exit-full-screen.png")
            ButtonExit.setIcon(icon)
            ButtonExit.setObjectName("ButtonMetrics")
            ButtonExit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            buttonMetricsLayout.addWidget(ButtonExit)

            horizaontalLayoutheaderHome.addLayout(buttonMetricsLayout)
            horizaontalLayoutheaderHome.setAlignment(QtCore.Qt.AlignLeft)
            

            containerBoxVinfoStundents.addWidget(headerGroupContainer)

            self.tableContainer  = QtWidgets.QWidget()
            self.tableContainer.setContentsMargins(0,0,0,0)
            self.tableContainer.setObjectName("self.tableContainer")
            gridLayout = QtWidgets.QGridLayout(self.tableContainer)
            gridLayout.setContentsMargins(0, 0, 0, 0)
            gridLayout.setObjectName("gridLayout")
            gridLayout.setHorizontalSpacing(0)
            gridLayout.setVerticalSpacing(0)
            gridLayout.setColumnStretch(0, 1)
            gridLayout.setColumnStretch(1, 1)
            gridLayout.setColumnStretch(2, 1)
            gridLayout.setColumnStretch(3, 1)
            gridLayout.setColumnStretch(4, 1)
            gridLayout.setColumnStretch(5, 1)
            gridLayout.setColumnStretch(6, 1)



            labeIDHeader = QtWidgets.QLabel()        
            labeIDHeader.setText("ID")
            labeIDHeader.setObjectName("labelHeader")
            labeIDHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeNameHeader = QtWidgets.QLabel()        
            labeNameHeader.setText("Name")
            labeNameHeader.setObjectName("labelHeader")
            labeNameHeader.setAlignment(QtCore.Qt.AlignCenter)

            labeStatus = QtWidgets.QLabel()        
            labeStatus.setText("Engagement")
            labeStatus.setObjectName("labelHeader")
            labeStatus.setAlignment(QtCore.Qt.AlignCenter)

            labelTaskAttend = QtWidgets.QLabel()        
            labelTaskAttend.setText("Task Attend")
            labelTaskAttend.setObjectName("labelHeader")
            labelTaskAttend.setAlignment(QtCore.Qt.AlignCenter)

            labelTaskNoAttend = QtWidgets.QLabel()        
            labelTaskNoAttend.setText("Unreviewed\ntasks")
            labelTaskNoAttend.setObjectName("labelHeader")
            labelTaskNoAttend.setAlignment(QtCore.Qt.AlignCenter)

            labelAsis = QtWidgets.QLabel()        
            labelAsis.setText("Attendance")
            labelAsis.setObjectName("labelHeader")
            labelAsis.setAlignment(QtCore.Qt.AlignCenter)

           
            gridLayout.addWidget(labeIDHeader, 0,0)
            gridLayout.addWidget(labeNameHeader, 0,1)
            gridLayout.addWidget(labeStatus, 0,2)
            gridLayout.addWidget(labelTaskAttend, 0,3)
            gridLayout.addWidget(labelTaskNoAttend, 0,4)
            gridLayout.addWidget(labelAsis, 0,5)

            containerBoxVinfoStundents.addWidget(self.tableContainer)
            containerBoxVinfoStundents.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

            containerBoxHParent.addWidget(wcontainerBoxVinfoStundents)
            containerBoxHParent.setStretch(0, 3) 
            containerBoxHParent.setStretch(1, 7)
            

            
            self.ScreensGroup.append(MetricsGroupContainer)
            self.buttonHomeStatus = False
            self.OnOffHome()
            self.screenID[nameGroup] = self.frame
            boxLoadingLabel = QtWidgets.QWidget()           
            verticalLayouMetricLoading = QtWidgets.QVBoxLayout(boxLoadingLabel)
            verticalLayouMetricLoading.setAlignment(QtCore.Qt.AlignCenter)
            ruta_gif = os.path.join(os.path.dirname(__file__), '..', 'rolling.gif')
            movie = QtGui.QMovie(ruta_gif)
            labelGif = QtWidgets.QLabel()
            labelGif.setMinimumSize(30,30)
            labelGif.setMovie(movie)
            labelGif.setAlignment(QtCore.Qt.AlignCenter)
            movie.start()
            loadingMetricInfo = QtWidgets.QLabel()
            verticalLayouMetricLoading.addWidget(labelGif)
            verticalLayouMetricLoading.addWidget(loadingMetricInfo)
            
            ButtonExit.clicked.connect(partial(self.exitFrame, frame, stacked_widget_now, name, MetricsGroupContainer))

            loadingMetricInfo.setText(f"Loading metrics for {nameGroup} ...")
            stackedWidget.addWidget(MetricsGroupContainer)
            containerBox_H.addWidget(boxLoadingLabel)
            stackedWidget.setCurrentIndex(frame)
            n = n_student.split("/")
            n = int(n[0])
            self.listLabelStds = []
            for i in range(1,n+1):
                self.addRowEmpty(i, gridLayout)
                thread1 = th.Thread(target=partial(self.runMetric, id_group, nameGroup, n_student, curso, last_class, next_class, self.listLabelStds, layoutDChart, boxLoadingLabel, containerBoxHParentWidget, loadingMetricInfo, frame, containerBox_H, stacked_widget_now, MetricsGroupContainer))
            try:
                thread1.start()
            except Exception as e:
                loadingMetricInfo.setText("Error", str(e))



            def updateMetricsGroup():
                self.exitFrame(frame, stacked_widget_now, name, MetricsGroupContainer, True)
                self.AddButtonFrameGroup(parent, nameGroup,stackedWidget, id_group, n_student,  curso, last_class, next_class)
            ButtonUpdate.clicked.connect(updateMetricsGroup)
                 
        else:
            stackedWidget.setCurrentIndex(self.screenID[nameGroup])

    def exitFrame(self,ind, frame, NAME, widgetMetric, update=False):
        """
        Removes a group frame and associated widgets from the interface.

        Parameters:
            ind (int): Index of the frame.
            frame: The frame to be removed.
            NAME (str): Name of the group.
            widgetMetric: Widget containing metrics information.
            name: Name of the group.
            update (bool, optional): Flag indicating whether to update metrics. Defaults to False.
        """
        
        widgetMetric.deleteLater()
        self.stackedWidget.removeWidget(widgetMetric)
        if len(self.screenID) > 0:
            self.stackedWidget.setCurrentIndex(list(self.screenID.values())[-1])
        else:
            self.stackedWidget.setCurrentIndex(0)
        if frame is not None:
            frame.currentChanged.disconnect()

        
        indx = self.screenID[NAME]
        button_to_delete = self.verticalButton.itemAt(indx).widget()
        button_to_delete.deleteLater()
        if update:
            del self.screenID[NAME]
        else:
            thread = th.Thread(target=partial(instSele.quitDriver, NAME))
            thread.start()  
            del self.screenID[NAME]
            
        for ind in list(self.screenID.keys()):
            if self.screenID[ind] > indx:
                self.screenID[ind] = self.screenID[ind] - 1
        self.frame -= 1

    def addRowEmpty(self, i, gridLayout):
        """
        Adds an empty row to the grid layout.

        Parameters:
            i (int): Row index.
            gridLayout: Grid layout to add the row to.
        """
        objeNameRow = f"LabelContend{str(i%2)}"
        labeID = QtWidgets.QLabel()        
        labeID.setText("---")
        labeID.setObjectName(objeNameRow)
        labeID.setAlignment(QtCore.Qt.AlignCenter)

        labeName = QtWidgets.QLabel()        
        labeName.setText("<a href='http://www.ejemplo.com'>Name</a>")
        labeName.setObjectName(objeNameRow)
        labeName.setAlignment(QtCore.Qt.AlignCenter)

        labeStd = QtWidgets.QLabel()        
        labeStd.setText("---")
        labeStd.setObjectName(objeNameRow)
        labeStd.setAlignment(QtCore.Qt.AlignCenter)

        labelTaskAttend = QtWidgets.QLabel()        
        labelTaskAttend.setText("<a href='http://www.ejemplo.com'>---</a>")
        labelTaskAttend.setObjectName(objeNameRow)
        labelTaskAttend.setAlignment(QtCore.Qt.AlignCenter)

        labelTaskNoAttend = QtWidgets.QLabel()        
        labelTaskNoAttend.setText("<a href='http://www.ejemplo.com'>NextLesson</a>")
        labelTaskNoAttend.setObjectName(objeNameRow)
        labelTaskNoAttend.setAlignment(QtCore.Qt.AlignCenter)

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

        labelAsis = QtWidgets.QLabel()
        labelAsis.setText("----")
        labelAsis.setObjectName(objeNameRow)
        labelAsis.setAlignment(QtCore.Qt.AlignCenter)

        buttonMetricsWidget = QtWidgets.QWidget()
        buttonMetricsLayout = QtWidgets.QHBoxLayout(buttonMetricsWidget)
        buttonMetricsLayout.setSpacing(2)
        buttonMetricsLayout.setContentsMargins(4,0,0,4)
        buttonMetricsLayout.setSizeConstraint(0)
        

        gridLayout.addWidget(labeID, i, 0, )
        gridLayout.addWidget(labeName, i, 1)
        gridLayout.addWidget(labeStd, i,2)
        gridLayout.addWidget(labelTaskAttend, i,3 )
        gridLayout.addWidget(labelTaskNoAttend, i,4,)
        gridLayout.addWidget(labelAsis, i,5)
        gridLayout.addWidget(buttonMetricsWidget, i,6)

        listLabelStd = [labeID, labeName, labeStd, labelTaskAttend, labelTaskNoAttend, labelAsis, buttonMetricsLayout, buttonMetricsLayout]
        self.listLabelStds.append(listLabelStd)

    def CreateBottomWidgetFooter(self, hLayoutMain, MainWindow):
        """
        Creates the bottom widget footer for the interface.

        Parameters:
            hLayoutMain: Main layout.
            MainWindow: Main window object.
        """
        self.Theme = Theme
        self.MainWindow = MainWindow
        self.label = QtWidgets.QGroupBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.label.setMaximumHeight(20)
        self.label.setContentsMargins(0,0,0,0)
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        hLayoutMain.addWidget(self.label)
        self.label.setObjectName("BarBottom")
        #Button Max, min, exit


        self.verticalButton = QtWidgets.QHBoxLayout(self.label)
        self.verticalButton.setContentsMargins(0, 0,0, 0)
        self.verticalButton.setSpacing(2)
        self.verticalButton.setAlignment(QtCore.Qt.AlignLeft)
        
        self.buttonHome = QtWidgets.QPushButton()
        self.buttonHome.setMinimumSize(80,20)
        self.buttonHomeStatus = True
        self.buttonHome.setStyleSheet("border-radius: 0px;")
        self.buttonHome.setText("Home")
        self.buttonHome.setObjectName("HomeON")
        self.verticalButton.addWidget(self.buttonHome)
        self.buttonHome.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonHome.clicked.connect(self.OnOffHome)

    def OnOffHome(self):
        """
        Toggles the home button status and switches to the home screen.
        """
        if self.buttonHomeStatus:
            self.buttonHome.setObjectName("HomeON")
        else:
            self.buttonHome.setObjectName("HomeOff")
            if  self.frame != 0:
                self.stackedWidget.setCurrentIndex(0)
            
    def ReturnTheme(self):
        """
        Returns the current theme of the interface.
        """
        return self.Theme

class PopupWindow(QtWidgets.QDialog):
    def __init__(self, text=None):
        super().__init__()
        self.setWindowTitle("Message")
        self.setGeometry(200, 200, 400, 200)
        self.setObjectName("MainWindow")

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Crear un QTextEdit para mostrar el texto
        template_text = QtWidgets.QTextEdit()
        template_text.setPlainText(text)
        template_text.setReadOnly(True)
        layout.addWidget(template_text)

        # Botón para copiar el texto
        copy_button = QtWidgets.QPushButton("Copiar")
        copy_button.clicked.connect(partial(self.copyText, text))
        layout.addWidget(copy_button)

    def copyText(self, text):
        QtWidgets.QApplication.clipboard().setText(text)  # Copiar el texto al portapapeles
