import sys, importlib, time
from PyQt5.QtWidgets import QProgressBar,QLabel, QVBoxLayout, QWidget, QStackedWidget, QDialog, QApplication
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from componentsUI import loggin
from  src import loadUpdates



class WorkerThread(QThread):
    update_text_signal = pyqtSignal(str)
    finished = pyqtSignal(bool,str)

    def run(self):
        taskStr = ["Checking for updates...(1/3)", "Updating drivers...(2/3)", "Opening drivers...(3/3)"]

        for i in range(3):
            self.update_text_signal.emit(taskStr[i])
            if i == 0:
                UpdateApp = loadUpdates.UpdateApp()
                self.update = UpdateApp.is_update_available()
                if self.update :
                    self.href = UpdateApp.takeHref()
                    self.finished.emit(self.update, self.href)
                    return
            if i == 1:
                loadUpdates.UpdateDriver()
        self.finished.emit(False, 'None')

class LoadingScreen(QWidget):
    def __init__(self, parent, finishhWiget):
        super().__init__()
        self.MainWindow = parent
        self.setObjectName("centralwidget")

        self.verticalLayoutMain = QVBoxLayout(self)
        self.verticalLayoutMain.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutMain.setSpacing(0)
        self.verticalLayoutMain.setObjectName("verticalLayout")

        self.layoutText = QVBoxLayout()

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setRange(0, 0)
        self.progressBar.setFixedWidth(400)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.progressBar.setObjectName("Progressbar")

        self.layoutText.addWidget(self.label)
        self.layoutText.addWidget(self.progressBar)
        self.layoutText.setAlignment(Qt.AlignCenter)

        self.verticalLayoutMain.addLayout(self.layoutText)
        self.startTask()

    def startTask(self):
        self.worker_thread = WorkerThread()
        self.worker_thread.finished.connect(self.finish_task)
        self.worker_thread.update_text_signal.connect(self.update_text)
        self.worker_thread.start()

    def update_timer(self):
        self.time_out -= 1  # Actualizar el tiempo restante

        if self.time_out <= 0:
            self.timer.stop()
            QApplication.quit()
            sys.exit()
    def finish_task(self, update=None, href=None):
        
        self.progressBar.deleteLater()
        if update:
            self.time_out = 15
            text_with_link = f"""
                                New updates to the application modules have been uploaded.<br>
                                To find out more, go to: <br><a href="{href}">{href}</a>
                                <br>This program will close in {self.time_out } seconds. Please reopen it.
                                """
            self.label.setText(text_with_link)

            self.timer = QTimer(self)
            
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(1000) 
        else:
            self.MainWindow.resize(900, 500)
            loggin.Loggin(self.MainWindow, error=False)

    def update_text(self, text):
        self.label.setText(text)


        
        
