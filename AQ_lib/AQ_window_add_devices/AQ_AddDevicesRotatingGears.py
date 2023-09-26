from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QWidget, QGraphicsView, QFrame, QGraphicsScene
PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'

class AQ_RotatingGearsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем QGraphicsPixmapItem и добавляем его в сцену
        self.gear_big = RotatingGear(QPixmap(PROJ_DIR + 'Icons/gear182.png'), 40, 1)
        # Создаем виджет QGraphicsView и устанавливаем его для окна
        self.gear_big_view = QGraphicsView(self)
        self.gear_big_view.setStyleSheet("background: transparent;")
        self.gear_big_view.setFrameStyle(QFrame.NoFrame)  # Убираем рамку
        self.gear_big_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gear_big_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Создаем сцену и устанавливаем ее для виджета
        self.gear_big_scene = QGraphicsScene(self)
        self.gear_big_scene.addItem(self.gear_big)
        self.gear_big_view.setScene(self.gear_big_scene)
        self.gear_big_view.setGeometry(90, 0, 182, 182)

        # Создаем QGraphicsPixmapItem и добавляем его в сцену
        self.gear_small = RotatingGear(QPixmap(PROJ_DIR + 'Icons/gear127.png'), 40, 4)
        # Создаем виджет QGraphicsView и устанавливаем его для окна
        self.gear_small_view = QGraphicsView(self)
        self.gear_small_view.setStyleSheet("background: transparent;")
        self.gear_small_view.setFrameStyle(QFrame.NoFrame)  # Убираем рамку
        self.gear_small_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gear_small_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Создаем сцену и устанавливаем ее для виджета
        self.gear_small_scene = QGraphicsScene(self)
        self.gear_small_scene.addItem(self.gear_small)
        self.gear_small_view.setScene(self.gear_small_scene)
        self.gear_small_view.setGeometry(0, 40, 127, 127)

    def start(self):
        self.gear_small.start()
        self.gear_big.start()

    def stop(self):
        self.gear_small.stop()
        self.gear_big.stop()


class RotatingGear(QGraphicsPixmapItem):
    def __init__(self, pixmap, interval, angle_degree):
        super().__init__()
        self.setPixmap(pixmap)
        self.setTransformOriginPoint(self.boundingRect().center())
        self.angle = 0
        self.angle_rotate = angle_degree
        self.interval = interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_gear)

    def rotate_gear(self):
        self.angle += self.angle_rotate  # Угол поворота в градусах
        self.setRotation(self.angle)

    def start(self):
        self.timer.start(self.interval)  # Установите интервал вращения в миллисекундах

    def stop(self):
        self.timer.stop()
