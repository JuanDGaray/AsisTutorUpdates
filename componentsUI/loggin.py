from PyQt5 import QtCore, QtGui, QtWidgets
import os, time
import sys
import threading as th
sys.path.append('../utils/stylesheetUI.py')


from utils import stylesheetUI
from componentsUI import loading, topWindow
from src import selenuimManager

UserIsLogged = False
UserInput = None

#Instancias
class Loggin(QtWidgets.QWidget):
    def __init__(self, parent, error):
        super().__init__(parent)
        self.WindowLoggin(parent, error)
        self.label = QtWidgets.QLabel(self.logginContainer)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)

    def WindowLoggin(self, parent, error):      
        self.MainWindow = parent 
        #CentralWidget
        self.setObjectName("centralwidget")

        #LayoutWindow 
        self.verticalLayoutMain = QtWidgets.QVBoxLayout(self)
        self.verticalLayoutMain.setContentsMargins(0, 0,0, 0)
        self.verticalLayoutMain.setSpacing(0)
        self.verticalLayoutMain.setObjectName("verticalLayout")

        #TopWindow
        inst = topWindow.TopWidget()
        inst.CreateTopWidgetTitle(self.verticalLayoutMain, self.MainWindow)


       

        #LayoutMain
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(14, 14,14, 14)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayoutMain.addLayout(self.verticalLayout)

        #HeaderCotainer
        self.header = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setMaximumHeight(40)
        self.header.setAutoFillBackground(False)
        self.header.setObjectName("header")

        #Button Header Container (Bug and Collaborate)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout_2.setContentsMargins(-1, 4, 18, 4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.HelpCotainer = QtWidgets.QFrame(self.header)
        self.HelpCotainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.HelpCotainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.HelpCotainer.setObjectName("HelpCotainer")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.HelpCotainer)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.versionILabel = QtWidgets.QLabel(self.HelpCotainer)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setBold(True)
        font.setWeight(75)

        #Version Label
        self.versionILabel.setFont(font)
        self.versionILabel.setObjectName("versionILabel")
        self.horizontalLayout_5.addWidget(self.versionILabel)
        
        self.horizontalLayout_2.addWidget(self.HelpCotainer)
        self.BugCotainer = QtWidgets.QFrame(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BugCotainer.sizePolicy().hasHeightForWidth())


        self.BugCotainer.setSizePolicy(sizePolicy)
        self.BugCotainer.setMaximumSize(QtCore.QSize(16777215, 40))
        self.BugCotainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BugCotainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BugCotainer.setObjectName("BugCotainer")


        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.BugCotainer)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")


        self.ButtonColab = QtWidgets.QFrame(self.BugCotainer)
        self.ButtonColab.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ButtonColab.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonColab.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonColab.setObjectName("ButtonColab")


        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.ButtonColab)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")


        self.gitIcon = QtWidgets.QLabel(self.ButtonColab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gitIcon.sizePolicy().hasHeightForWidth())
        self.gitIcon.setSizePolicy(sizePolicy)
        self.gitIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.gitIcon.setAutoFillBackground(False)
        self.gitIcon.setTextFormat(QtCore.Qt.RichText)
        self.gitIcon.setScaledContents(True)
        self.gitIcon.setAlignment(QtCore.Qt.AlignCenter)
        self.gitIcon.setWordWrap(False)
        self.gitIcon.setIndent(-14)
        self.gitIcon.setOpenExternalLinks(False)
        self.gitIcon.setObjectName("gitIcon")


        self.horizontalLayout_6.addWidget(self.gitIcon, 0, QtCore.Qt.AlignTop)
        self.colaborateButton = QtWidgets.QPushButton(self.ButtonColab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colaborateButton.sizePolicy().hasHeightForWidth())
        self.colaborateButton.setSizePolicy(sizePolicy)
        self.colaborateButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.colaborateButton.setFont(font)
        self.colaborateButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.colaborateButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.colaborateButton.setAutoFillBackground(False)
        self.colaborateButton.setIconSize(QtCore.QSize(0, 0))
        self.colaborateButton.setAutoExclusive(False)
        self.colaborateButton.setAutoDefault(False)
        self.colaborateButton.setObjectName("colaborateButton")
        self.horizontalLayout_6.addWidget(self.colaborateButton, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.ButtonColab, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.ButtonBug = QtWidgets.QFrame(self.BugCotainer)
        self.ButtonBug.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ButtonBug.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonBug.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonBug.setObjectName("ButtonBug")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.ButtonBug)
        self.hboxlayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName("hboxlayout")
        self.bugIcon = QtWidgets.QLabel(self.ButtonBug)
        self.bugIcon.setMaximumSize(QtCore.QSize(32, 32))
        self.bugIcon.setObjectName("bugIcon")
        self.hboxlayout.addWidget(self.bugIcon)
        self.bugButton = QtWidgets.QPushButton(self.ButtonBug)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bugButton.sizePolicy().hasHeightForWidth())
        self.bugButton.setSizePolicy(sizePolicy)
        self.bugButton.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.bugButton.setFont(font)
        self.bugButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bugButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.bugButton.setAutoFillBackground(False)
        self.bugButton.setIconSize(QtCore.QSize(0, 0))
        self.bugButton.setAutoRepeat(False)
        self.bugButton.setAutoExclusive(False)
        self.bugButton.setAutoDefault(False)
        self.bugButton.setFlat(False)
        self.bugButton.setObjectName("bugButton")
        self.hboxlayout.addWidget(self.bugButton)
        self.horizontalLayout_3.addWidget(self.ButtonBug, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_2.addWidget(self.BugCotainer)
        self.verticalLayout.addWidget(self.header)


        """BODY"""
        self.body = QtWidgets.QWidget(self)
        self.body.setObjectName("body")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")


        self.groupBox = QtWidgets.QGroupBox(self.body)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(500, 500))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        #LOGGIN CONTAINER
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.logginContainer = QtWidgets.QFrame(self.groupBox)
        self.logginContainer.setMaximumSize(QtCore.QSize(400, 100))
        self.logginContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logginContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logginContainer.setObjectName("logginContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.logginContainer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.logginContainer)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.logginContainer)
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.label_4 = QtWidgets.QLabel(self.logginContainer)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.logginContainer)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout_5.addWidget(self.logginContainer, 0, QtCore.Qt.AlignVCenter)
        self.logginButton = QtWidgets.QFrame(self.groupBox)
        self.logginButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.logginButton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logginButton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logginButton.setObjectName("logginButton")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.logginButton)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.logginPush = QtWidgets.QPushButton(self.logginButton)
        self.logginPush.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.logginPush.setObjectName("logginPush")
        self.checkboxLayout = QtWidgets.QHBoxLayout()
        self.checkbox = QtWidgets.QCheckBox("Remember")
        self.checkboxLayout.addWidget(self.checkbox)
        self.checkboxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.checkbox.setObjectName("Remember")
        

        
        self.verticalLayout_4.addWidget(self.logginPush)
        self.verticalLayout_5.addLayout(self.checkboxLayout)
        self.verticalLayout_5.addWidget(self.logginButton)
        self.labeError = QtWidgets.QLabel()
        if error == "bad_credential": 
            self.labeError.setObjectName("labelError")
            self.labeError.setText("Password or user bad!\nTry again")
            self.verticalLayout_4.addWidget(self.labeError)
        
        self.logginPush.clicked.connect(lambda: self.switchtoLoading(user=self.lineEdit.text(), passw=self.lineEdit_2.text()))

        #INFO APP CONTAINER
        self.horizontalLayout_4.addWidget(self.groupBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.InfoContainer = QtWidgets.QGroupBox(self.body)
        self.InfoContainer.setMaximumSize(QtCore.QSize(300, 16777215))
        self.InfoContainer.setTitle("")
        self.InfoContainer.setObjectName("InfoContainer")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.InfoContainer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.InfoContainer)
        self.label_6.setFont(font)
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setScaledContents(True)
        self.label_6.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.InfoContainer)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.horizontalLayout_4.addWidget(self.InfoContainer)
        self.verticalLayout.addWidget(self.body)
        self.MainWindow.setCentralWidget(self)

        self.retranslateUi(MainWindow = parent)
        QtCore.QMetaObject.connectSlotsByName(parent)

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.versionILabel.setText(_translate("MainWindow", "Versión 2.0.18.15 | by Juan Garay"))
            self.gitIcon.setText(_translate("MainWindow", "<html><head/><body><p><img src=\"assets/images/github.png\"/></p></body></html>"))
            self.colaborateButton.setText(_translate("MainWindow", "Cooperate"))
            self.bugIcon.setText(_translate("MainWindow", "<html><head/><body><p><img src=\"assets/images/insect.png\"/></p></body></html>"))
            self.bugButton.setText(_translate("MainWindow", "Report Bug"))
            self.label.setText(_translate("MainWindow", "User:"))
            self.label_4.setText(_translate("MainWindow", "Password:"))
            self.logginPush.setText(_translate("MainWindow", "Loggin"))
            self.label_6.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">"
                                                "p, li { white-space: pre-wrap; }"
                                                "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Tutor Assistant is a web scraping-based program designed to efficiently scan tutor data and facilitate the organization and management of student information.</p></body></html>"))
            self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><img src=\"assets/images/tutoring.png\"/></p></body></html>"))
    def update_text(self, text):
        self.label.setText(text)

    def switchtoLoading(self, passw=None, user=None):
            if  len(passw) > 0 and len(user)>0:
                if self.checkbox.isChecked():
                     checkBox = True
                else:
                     checkBox = False
                self.loading = loading.LoadingScreen(self.MainWindow, "loggin", passw= passw, user=user, check=checkBox)
                self.MainWindow.setCentralWidget(self.loading)
                self.loading.show()
            else:
                self.labeError.setObjectName("labelError")
                self.labeError.setText("Write your password or user")
                self.verticalLayout_4.addWidget(self.labeError)
                 

        


        



    






    