import time, sys
from PyQt5.QtWidgets import QProgressBar, QApplication, QMainWindow, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget, QDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMovie
from componentsUI import loggin, home
from  src import loadUpdates
sys.path.append('../utils/stylesheetUI.py')

from utils import stylesheetUI


class WorkerThread(QThread):
    update_text_signal = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        taskStr = ["Checking for updates...(1/3)", "Updating drivers...(2/3)", "Opening drivers...(3/3)"]

        for i in range(3):
            self.update_text_signal.emit(taskStr[i])
            if i == 0:
                loadUpdates.UpdateApp()
            if i == 1:
                loadUpdates.UpdateDriver()
        self.finished.emit()

class LoadingScreen(QWidget):
    def __init__(self, parent, finishhWiget):
        super().__init__()
        self.MainWindow = parent
        self.setObjectName("centralwidget")

        self.verticalLayoutMain = QVBoxLayout(self)
        self.verticalLayoutMain.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutMain.setSpacing(0)
        self.verticalLayoutMain.setObjectName("verticalLayout")

        layout = QVBoxLayout()

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setRange(0, 0)
        self.progressBar.setFixedWidth(400)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.progressBar.setObjectName("Progressbar")

        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        layout.setAlignment(Qt.AlignCenter)

        self.verticalLayoutMain.addLayout(layout)
        self.startTask()

    def startTask(self):
        self.worker_thread = WorkerThread()
        self.worker_thread.finished.connect(self.finish_task)
        self.worker_thread.update_text_signal.connect(self.update_text)
        self.worker_thread.start()

    def finish_task(self):
        self.MainWindow.resize(900, 500)
        loggin.Loggin(self.MainWindow, error=False)

    def update_text(self, text):
        self.label.setText(text)


        
        
