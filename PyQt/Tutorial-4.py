"""
OOP Based App
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class RafaelWindow(QMainWindow):
    def __init__(self):
        super(RafaelWindow, self).__init__()
        "Arguments"
        self.label = None
        self.b1 = None

        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Title")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)             # QtWidgets.QLabel(win) -> QtWidgets.QLabel(self)
        self.label.setText("My Label")
        self.label.move(30, 30)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Button 1")
        self.b1.clicked.connect(self.click_b1)

    def click_b1(self):
        self.label.setText("Pressed the button")
        self.update()

    def update(self):
        self.label.adjustSize()


def run():
    app = QApplication(sys.argv)
    win = RafaelWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
