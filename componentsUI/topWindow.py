from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from utils import stylesheetUI
Theme = "Dark"

class TopWidget():
      
    def CreateTopWidgetTitle(self, hLayoutMain, MainWindow):
        self.Theme = Theme
        self.MainWindow = MainWindow
        self.label = QtWidgets.QGroupBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.label.setMaximumHeight(30)
        self.label.setContentsMargins(0,0,0,0)
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseMoveEvent = self.mouseMoveEvent
        hLayoutMain.addWidget(self.label)
        self.label.setObjectName("BarTitle")
        #Button Max, min, exit


        self.verticalButton = QtWidgets.QHBoxLayout(self.label)
        self.verticalButton.setContentsMargins(0, 0,0, 0)
        self.verticalButton.setSpacing(2)
        self.verticalButton.setAlignment(QtCore.Qt.AlignRight)
        
        buttoThemeWidget = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        buttoThemeWidget.setSizePolicy(sizePolicy)
        buttoThemeWidget.setContentsMargins(0, 0,0, 0)
        buttoThemeWidget.setMinimumSize(51,28)
        buttoThemeWidget.setObjectName("buttoThemeWidget")

        
        buttoTheme = QtWidgets.QPushButton(buttoThemeWidget)
        icon = QtGui.QIcon("assets/images/soleado.png")
        buttoTheme.setIcon(icon)
        buttoTheme.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        buttoTheme.setSizePolicy(sizePolicy)
        buttoTheme.setMaximumSize(48,24)
        buttoTheme.setObjectName("ButtonWindowTheme")
        buttoTheme.clicked.connect(self.ChangeTheme)
        self.verticalButton.addWidget(buttoThemeWidget)

        buttoMin = QtWidgets.QPushButton()
        buttoMin.setText("-")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        buttoMin.setSizePolicy(sizePolicy)
        buttoMin.setMinimumSize(30,30)
        buttoMin.setObjectName("ButtonWindow")
        buttoMin.clicked.connect(self.minimizeWindow)
        self.verticalButton.addWidget(buttoMin)


        buttoMax = QtWidgets.QPushButton()
        buttoMax.setMinimumSize(30,30)
        buttoMax.setText("O")
        buttoMax.setSizePolicy(sizePolicy)
        buttoMax.setObjectName("ButtonWindow")
        buttoMax.clicked.connect(self.maximizeWindow)
        self.verticalButton.addWidget(buttoMax)
        
        buttoExit = QtWidgets.QPushButton()
        buttoExit.setMinimumSize(30,30)
        buttoExit.setText("x")
        buttoExit.setSizePolicy(sizePolicy)
        buttoExit.setObjectName("ButtonWindow")
        buttoExit.clicked.connect(self.exitApplication)
        self.verticalButton.addWidget(buttoExit)

    def mousePressEvent(self, event): 
        if event.button() == QtCore.Qt.LeftButton and event.y() <= 40 and event.x()<= int(self.MainWindow.width()) - 100:
            self.dragPos = event.globalPos() - self.MainWindow.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton :
                self.MainWindow.move(event.globalPos() - self.dragPos)

    def minimizeWindow(self):
        self.MainWindow.showMinimized()

    def exitApplication(self):
        sys.exit()

    def maximizeWindow(self, *arg):
        print(self.MainWindow.width())
        if self.MainWindow.width()> 1000:
            self.MainWindow.resize(900, 550)
        else:
            desktop = QtWidgets.QDesktopWidget()
            screen_rect = desktop.screenGeometry(desktop.primaryScreen())
            self.MainWindow.setGeometry(screen_rect)

    def ChangeTheme(self):
        if self.Theme == "Dark":
            self.Theme = "Light"
            self.MainWindow.setStyleSheet(stylesheetUI.strStyleSheetsLight)
        elif self.Theme == "Light":
            self.Theme = "Dark"
            self.MainWindow.setStyleSheet(stylesheetUI.strStyleSheetsBlack)

    def ReturnTheme(self):
        return self.Theme


