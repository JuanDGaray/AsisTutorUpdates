import time
import sys
from PyQt5.QtWidgets import QProgressBar, QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from componentsUI import topWindow, home, loggin
from src.selenuimManager import SelenuimThreadLoggin
from src.dataBaseManager import db_manager
import functools

processLoading = None
userText = None
passText = None



class updateTextExternalSignal(QObject):
    update_text_signal = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    switchToLoggin = pyqtSignal()
    
    
    
    def update_progress(self, value, text):
        self.update_progress_signal.emit(value, text)

    def exitTextExternalSignal(self):
        self.finished.emit()

    def stopByException(self, exception, text):
        self.finished.emit(exception, text)

class LoadingScreen(QWidget):
    def __init__(self, parent, process, passw, user, check = False):
        global processLoading, passText, userText
        super().__init__()
        self.MainWindow = parent
        processLoading = process
        passText = passw
        userText = user
        self.checkBool = check
        self.setObjectName("centralwidget")

        self.verticalLayoutMain = QVBoxLayout(self)
        self.verticalLayoutMain.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutMain.setSpacing(0)
        self.verticalLayoutMain.setObjectName("verticalLayout")

        self.layout = QVBoxLayout()

        insTop = topWindow.TopWidget()
        insTop.CreateTopWidgetTitle(self.verticalLayoutMain, self.MainWindow)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setRange(0, 0)
        self.progressBar.setFixedWidth(500)
        self.progressBar.setObjectName("Progressbar")
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressBar)
        self.layout.setAlignment(Qt.AlignCenter)

        self.verticalLayoutMain.addLayout(self.layout)
       
        self.selenium_thread = SelenuimThreadLoggin()
        self.selenium_thread.finished_signal.connect(lambda exception, text, : self.finish_task(exception, text))
        self.selenium_thread.update_text_signal.connect(self.update_text)


        if process == "loggin":
            self.start_selenium(userText, passText, True)

    def start_selenium(self, UserName, UserPass, NewLogin):

        self.selenium_thread.set_credentials(UserName, UserPass, NewLogin)
        self.selenium_thread.start()

    def switchToLoggin(self, errorText):
        loggin.Loggin(self.MainWindow, error=errorText)

    def finish_task(self, exception, text):
        if  processLoading == "loggin":
            if exception:
                if len(text)==0:
                    self.switchToLoggin(errorText = "bad_credential")
                else:
                    self.progressBar.deleteLater()
                    self.label.setText(text)    
            else:
                home.Inithome(self.MainWindow)
                if self.checkBool:
                    db_manager().save_credential(userText, passText)
                    


    def update_text(self, text):
        self.label.setText(text)
