import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QFrame, QPushButton, QWidget, QVBoxLayout

# Crea la aplicación
app = QApplication(sys.argv)

# Crea el widget que quieres mostrar
widget = QWidget()

# Crea un QFrame y establece su diseño principal como un QVBoxLayout
frame = QFrame()
frameLayout = QVBoxLayout(frame)

# Agrega un botón al diseño del QFrame
button = QPushButton("Botón")
frameLayout.addWidget(button)

# Crea una escena gráfica y un visor gráfico
scene = QGraphicsScene()
view = QGraphicsView(scene)

# Agrega el QFrame a la escena gráfica como un elemento gráfico
proxy = QGraphicsProxyWidget(scene)
proxy.setWidget(frame)
proxy.setPos(0, 0)
proxy.setZValue(1)

# Muestra el visor gráfico
view.show()

# Ejecuta la aplicación
sys.exit(app.exec_())