from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QScrollArea, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QTextEdit(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)

        # Establecer la política de la barra de desplazamiento
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Personalizar la apariencia con hojas de estilo
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                border-radius: 5px;
            }

            QScrollBar:vertical {
                width: 10px;
                background-color: #ccc;
            }

            QScrollBar::handle:vertical {
                background-color: #666;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
