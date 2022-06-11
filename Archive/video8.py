import cv2
import sys

from PyQt5.QtCore import QTimer, QRect, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget


class Example:
    def __init__(self):
        self.centralwidget = None
        self.gridLayout = None
        self.lblVid = None
        self.timer = None
        self.cap = None

    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.lblVid = QLabel(self.centralwidget)
        self.lblVid.setGeometry(QRect(4, 5, 791, 561))
        self.lblVid = QLabel(self.centralwidget)
        self.lblVid.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.gridLayout.addWidget(self.lblVid, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.startVideo()

    def startVideo(self):
        self.cap = cv2.VideoCapture('3.mp4')
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.timer = QTimer()
        millisecs = int(1000.0 / fps)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(millisecs)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            pix = pix.scaled(self.lblVid.width(), self.lblVid.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lblVid.setPixmap(pix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Example()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
