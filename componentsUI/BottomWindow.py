from PyQt5 import QtWidgets, QtCore, QtGui
import sys

from PyQt5.QtCore import QObject
from utils import stylesheetUI
import threading as th
from PyQt5.QtCore import QThread, pyqtSignal
from functools import partial
from PyQt5.QtCore import pyqtSlot
from src.selenuimManager import SelenuimThreadLoggin
from src.dataBaseManager import db_manager
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import webbrowser, time
from utils import constants

Theme = "Light"
frameDelete = 0

instSele= SelenuimThreadLoggin()
intDB = db_manager()

class SpiderChartWidget(QtWidgets.QWidget):
    def __init__(self, data, categories):
        super().__init__()
        self.categories = categories
        self.data = data
        self.initUI()
        

    def initUI(self):
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

    class BottomWidgetSignals(QtCore.QObject):
        updateGridLayoutSignal = QtCore.pyqtSignal(list, list, list, QtWidgets.QLayout, QtWidgets.QWidget, QtWidgets.QWidget, QtWidgets.QLabel, int, QtWidgets.QHBoxLayout)

    def __init__(self):
        self.frame = 0
        self.screenID = {}
        self.ScreensGroup = []
        self.signals = self.BottomWidgetSignals()
        self.signals.updateGridLayoutSignal.connect(self.updateGridLayout)

    def OpenTemplateMetric(self, jsonList):
                                with open('assets/template-metrics-students/itemsCharts.js', 'r') as archivo:
                                    contenido = archivo.read()

                                with open('assets/template-metrics-students/plantilla-metric-of-stundets.js', 'r') as archivo2:
                                    contenido2 = archivo2.read()

                                # Modificar la lista en el contenido
                                nueva_lista = jsonList # Nueva lista que deseas usar
                                nuevo_contenido = contenido.replace('const Data = [];', f'const Data = {nueva_lista};')
                                nuevo_contenido2 = contenido2.replace('const Data1 = [];', f'const Data1 = {nueva_lista};')
                                # Escribir el contenido actualizado en el archivo JavaScript
                                with open('assets/template-metrics-students/itemsCharts.js', 'w') as archivo:
                                    archivo.write(nuevo_contenido)
                                with open('assets/template-metrics-students/plantilla-metric-of-stundets.js', 'w') as archivo2:
                                    archivo2.write(nuevo_contenido2)
                                ruta_absoluta = os.path.abspath("assets/template-metrics-students/plantilla-metric-of-stundets.html/")
                                webbrowser.open_new_tab('file://'+ruta_absoluta)
                                time.sleep(5)
                                nuevo_contenido = contenido.replace(f'const Data = {nueva_lista};', 'const Data = [];')
                                nuevo_contenido2 = contenido2.replace(f'const Data1 = {nueva_lista};', 'const Data1 = [];')
                                
                                with open('assets/template-metrics-students/itemsCharts.js', 'w') as archivo:
                                    archivo.write(nuevo_contenido)
                                with open('assets/template-metrics-students/plantilla-metric-of-stundets.js', 'w') as archivo2:
                                    archivo2.write(nuevo_contenido2)
    def generatorSummaryWeek(self, stdMetrics, attedancePercent):
            if stdMetrics[5]==0:
                messageWA = f"*Resumen%20Semanal%20de%20{stdMetrics[1]}*%20%F0%9F%98%8A%0A%0AActualmente%20tienes%20**{stdMetrics[3]+stdMetrics[4]}%20Tareas%20entregadas*%20|%20*{stdMetrics[5]}%20Tareas%20por%20entregar*%0A%0A*Tu%20asistencia%20es%20{stdMetrics[2]},%20has%20asistido%20hasta%20el%20momento%20al%20{attedancePercent}%%20de%20las%20clases.*%0A%0A*_Si%20desea%20mi%20ayuda,%20no%20olvide%20escribirme%20a%20este%20número.%20Estaré%20atento%20a%20cualquier%20inquietud_.%20:D"
            else:
                strTotalNoAttendActivity = ''
                for l in stdMetrics[20].keys():
                    textKeys = f'*Lección%20{l[1:]}*'
                    textTask = ''
                    for no_a in stdMetrics[20][l][1]:
                        task = no_a.split("/")
                        textTask += f'%0A%20%20-%20https%3A%2F%2Fplatform.kodland.org/es/{task[-1]}'
                    strTotalNoAttendActivity += f'{textKeys}:{textTask}%0A'    

                messageWA = f"*Resumen%20Semanal%20de%20{stdMetrics[1]}*%20%F0%9F%98%8A%0A%0AActualmente%20tienes%20*{stdMetrics[4] + stdMetrics[3]}%20Tareas%20entregadas*%20|%20*{stdMetrics[5]}%20Tareas%20por%20entregar*%0A%0A*Tu%20asistencia%20es%20{stdMetrics[2]},%20has%20asistido%20hasta%20el%20momento%20al%20{attedancePercent}%%20de%20las%20clases.*%0A%0A*Estas%20son%20tus%20actividades%20sin%20enviar:*%0A{strTotalNoAttendActivity}_Si%20desea%20mi%20ayuda,%20no%20olvide%20escribirme%20a%20este%20número.%20Estaré%20atento%20a%20cualquier%20inquietud_.%20:D"
            link = "https://api.whatsapp.com/send/?phone="+stdMetrics[18]+"&text="+messageWA+"&type=phone_number&app_absent=0"
            webbrowser.open_new(str(link))

    def open_external_link(self, url):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def updateGridLayout(self, listID, ListLabel, listStd, layoutDChart, WidgetLoading, widgetMetrics, labelTextLoading, frame, boxHLayoudParent):
            
            attend_percent_general = 0
            percentTask_general = 0
            pointGeneral = 0
            course = listStd[0][23][0]
            id_course = constants.id_couse_latamByTotalName[course]
            n_class = listStd[0][24]
            pointTotal = sum(constants.points_total_course_latam[id_course][0:n_class+1])
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
                    elif ind == 5:
                        attedancePercent= int((id[13]/id[14]) * 100) 
                        attend_percent_general += attedancePercent
                        l.setText(f'<span>{id[13]}/{id[14]}</span>\n<span><b>{attedancePercent}%</b></span>')
                    elif ind == 6:
                        attedancePercent= int((id[13]/id[14]) * 100) 
                        ButtonTaskSummary = QtWidgets.QPushButton()
                        ButtonTaskSummary.setContentsMargins(0,0,0,0)
                        ButtonTaskSummary.setObjectName("ButtonMetrics")
                        icon = QtGui.QIcon("assets/images/whatsapp.png")
                        ButtonTaskSummary.setIcon(icon)
                        ButtonTaskSummary.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                        ButtonTaskSummary.clicked.connect(partial(self.generatorSummaryWeek,id, attedancePercent))
                        l.addWidget(ButtonTaskSummary)
                    elif ind == 7:
                        ButtonSummaryGeneral = QtWidgets.QPushButton()
                        ButtonSummaryGeneral.setContentsMargins(0,0,0,0)
                        ButtonSummaryGeneral.setObjectName("ButtonMetrics")
                        icon = QtGui.QIcon("assets/images/money-graph-with-up-arrow.png")
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
            



    def textStatusStudent(self, percentTask):
        if percentTask < 20:
            text = "Bad"
            color = "color:#ff2b2a"
        elif percentTask < 40:
            text = "Low"
            color = "color:#ff8901"
        elif percentTask < 60:
            text = "regular"
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
                    layoutChart, labelGif, widgetMetrics, labelText, frame, StakeWid):
            
            dataLoggin = intDB.findPassAndUserCache()
            self.metrics = instSele.takeMetricGroup(id_group = id_group, 
                    name_group = name_group, 
                    n_student = n_student, 
                    curso = curso, 
                    last_class = last_class,
                    next_class = next_class,
                    user=dataLoggin[1],
                    passw=dataLoggin[2])
            
            listSd = self.metrics[name_group]
            listSdID = list(listSd.keys())
            listSdMetrics = list(listSd.values())
            self.signals.updateGridLayoutSignal.emit(listSdID, listLabel, listSdMetrics, layoutChart, labelGif, widgetMetrics, labelText, frame, StakeWid)
            




    def AddButtonFrameGroup(self, parent, nameGroup,stackedWidget, id_group, n_student,  curso, last_class, next_class):
        def SwitchGroup(nameGroup):
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
            icon = QtGui.QIcon("assets/images/video-camera.png")
            ButtonRecord.setIcon(icon)
            ButtonRecord.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            buttonMetricsLayout.addWidget(ButtonRecord)
            
            ButtonUpdate = QtWidgets.QPushButton()
            ButtonUpdate.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon("assets/images/actualizar.png")
            ButtonUpdate.setIcon(icon)
            ButtonUpdate.setObjectName("ButtonMetrics")
            buttonMetricsLayout.addWidget(ButtonUpdate)
            ButtonUpdate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
            
            ButtonPoduin = QtWidgets.QPushButton()
            ButtonPoduin.setContentsMargins(0,0,0,0)
            icon = QtGui.QIcon("assets/images/podium (2).png")
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
            movie = QtGui.QMovie("assets\images\Rolling-1s-18px.gif")
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
            thread1 = th.Thread(target=partial(self.runMetric, id_group, nameGroup, n_student, curso, last_class, next_class, self.listLabelStds, layoutDChart, boxLoadingLabel, containerBoxHParentWidget, loadingMetricInfo, frame, containerBox_H))
            thread1.start()

            def updateMetricsGroup():
                self.exitFrame(frame, stacked_widget_now, name, MetricsGroupContainer)
                self.AddButtonFrameGroup(parent, nameGroup,stackedWidget, id_group, n_student,  curso, last_class, next_class)
            ButtonUpdate.clicked.connect(updateMetricsGroup)
                 
        else:
            stackedWidget.setCurrentIndex(self.screenID[nameGroup])

          

    def exitFrame(self,ind, frame, NAME, widgetMetric):
                
                widgetMetric.deleteLater()
                self.stackedWidget.removeWidget(widgetMetric)
                indx = self.screenID[NAME]
                for ind in list(self.screenID.keys()):
                    if self.screenID[ind] > indx:
                        self.screenID[ind] = self.screenID[ind] - 1
                del self.screenID[NAME]
                button_to_delete = self.verticalButton.itemAt(indx).widget()
                button_to_delete.deleteLater()
                self.frame -= 1

                if len(self.screenID) > 0:
                    self.stackedWidget.setCurrentIndex(list(self.screenID.values())[-1])
                else:
                    self.stackedWidget.setCurrentIndex(0)
                if frame is not None:
                    frame.currentChanged.disconnect()

    
         
         

    def addRowEmpty(self, i, gridLayout):
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
        if self.buttonHomeStatus:
            self.buttonHome.setObjectName("HomeON")
        else:
            self.buttonHome.setObjectName("HomeOff")
            if  self.frame != 0:
                self.stackedWidget.setCurrentIndex(0)
            
        

    def ReturnTheme(self):
        return self.Theme
