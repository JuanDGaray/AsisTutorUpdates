import sys
from PyQt5 import  QtCore, QtGui, QtWidgets
from componentsUI import loggin, loadingUpdates
from utils import stylesheetUI

window = "loggin"
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):

        event.accept()


class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        #Main Window
        #MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)    
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 200)
        MainWindow.setWindowIcon(QtGui.QIcon('bot.ico'))
        MainWindow.setWindowOpacity(1)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(stylesheetUI.strStyleSheetsLight)
        self.loading = loadingUpdates.LoadingScreen(MainWindow, loggin.Loggin(MainWindow, error=False))
        MainWindow.setCentralWidget(self.loading)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
 