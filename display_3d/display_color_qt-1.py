import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QCursor

from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D

# https://ja.stackoverflow.com/questions/45087/pyqt5%E3%81%A7%E6%8F%8F%E3%81%84%E3%81%9F3%E6%AC%A1%E5%85%83%E3%82%B0%E3%83%A9%E3%83%95%E3%81%AE%E8%A6%96%E7%82%B9%E3%82%92%E3%83%9E%E3%82%A6%E3%82%B9%E3%81%A7%E5%8B%95%E3%81%8B%E3%81%97%E3%81%9F%E3%81%84


class Main(QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        x = np.arange(-3, 3, 0.25)
        y = np.arange(-3, 3, 0.25)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) + np.cos(Y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        self.figure1 = plt.figure()
        #self.axes1 = self.figure1.add_subplot(111, projection='3d')
        self.axes1 = self.figure1.gca(projection="3d")
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setFixedSize(600, 450)
        self.toolbar1 = NavigationToolbar(self.canvas1, self)

        self.axes1.plot_surface(X, Y, Z, cmap='jet')

        layout1 = QVBoxLayout()
        layout1.addWidget(self.toolbar1)
        layout1.addWidget(self.canvas1)
        self.setLayout(layout1)

        self.canvas1.mpl_connect('button_press_event', self.mousePressEvent)
        self.canvas1.mpl_connect(
            'button_release_event', self.mouseReleaseEvent)

        self.startCursorPos = QPoint(0, 0)
        self.isDragging = False
        self.elev = 0
        self.azim = 0

        self.show()

    def mousePressEvent(self, event):
        if event.button == Qt.LeftButton:
            self.startCursorPos = QCursor.pos()
            self.isDragging = True

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            diff = QCursor.pos() - self.startCursorPos
            self.elev += diff.y()
            self.azim -= diff.x()
            self.update()
            self.isDragging = False

    def paintEvent(self, event):
        if self.isDragging:
            diff = QCursor.pos() - self.startCursorPos
            self.axes1.view_init(self.elev + diff.y(), self.azim - diff.x())
            self.canvas1.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())
