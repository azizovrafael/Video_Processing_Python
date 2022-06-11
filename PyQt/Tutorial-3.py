"""
Button
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def mene_bas():
    print("Basdin.")

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)

    win.setWindowTitle("Rafael")

    label = QtWidgets.QLabel(win)
    label.setText("my first labeladadada adad asd ad")
    label.move(10, 50)

    b1 = QtWidgets.QPushButton(win)
    b1.setText("Mene Bas")
    b1.clicked.connect(mene_bas)

    win.show()
    sys.exit(app.exec_())


window()
