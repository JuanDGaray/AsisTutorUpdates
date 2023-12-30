from PyQt6.QtWidgets import QLabel, QLineEdit, QFrame, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt6.QtCore import Qt
from utils import stylesheetUI as ss
import sys
import os

# Obtén la ruta completa de la carpeta que contiene "main.py"
current_dir = os.path.dirname(os.path.abspath(__file__))

# Agrega la ruta de "utils" al sys.path
utils_path = os.path.join(current_dir, 'utils')
sys.path.append(utils_path)

def LabelsFooter(WidgetMain, Status):

    footerLabelRight = QLabel("TutorAsistant             Versión 2.0.18 - by. Juan Garay")
    footerLabelRight.setFont(ss.fontInput)
   

    # Agregar el QLabel al pie de página
    SBar = WidgetMain.statusBar()
    SBar.addPermanentWidget(footerLabelRight)
    SBar.setStyleSheet(f"background-color: rgb({ss.StrBackground3}); color: white;")

    WidgetMain.show()