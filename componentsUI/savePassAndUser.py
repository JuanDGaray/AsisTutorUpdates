import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QDialog

class ConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(200, 200, 200, 100)

        layout = QVBoxLayout()

        Textlabel = QLabel("¿Desea guardar las credenciales para la próxima sesión?")
        layout.addWidget(Textlabel)

        btn_si = QPushButton("yes")
        btn_si.clicked.connect(self.accept)
        layout.addWidget(btn_si)

        btn_no = QPushButton("no")
        btn_no.clicked.connect(self.reject)
        layout.addWidget(btn_no)

        self.setLayout(layout)


def showDialog(QWidget):
    dialog = ConfirmationDialog(QWidget)

    result = dialog.exec_()

    if result == QDialog.Accepted:
        return True
