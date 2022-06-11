"""
label
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    '''
    win.setGeometry(x, y, a, b)
              x
             ____
          a |    | b
            |____|
              y

    '''
    win.setWindowTitle("Rafael")

    label = QtWidgets.QLabel(win)
    label.setText("my first labeladadada adad asd ad")
    label.move(10, 50)
    '''
    label.move(x, y)
             x->
             ____
          y |    | 
            |____|
              

   '''

    win.show()
    sys.exit(app.exec_())


window()
