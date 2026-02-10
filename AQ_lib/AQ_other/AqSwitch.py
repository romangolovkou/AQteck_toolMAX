from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, Property, QPropertyAnimation, Signal
from PySide6.QtGui import QPainter, QColor


class AqSwitchBtn(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._width = 30#50
        self._height = 15#28
        self.setFixedSize(self._width, self._height)

        self._checked = False
        self._offset = 2

        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(150)

    # ===== Property for animation =====
    def getOffset(self):
        return self._offset

    def setOffset(self, value):
        self._offset = value
        self.update()

    offset = Property(float, getOffset, setOffset)

    # ===== Logic =====
    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)

        start = self._offset
        end = self.width() - self.height() + 2 if self._checked else 2

        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def isChecked(self):
        return self._checked

    def setChecked(self, state: bool):
        self._checked = state
        self._offset = self.width() - self.height() + 2 if state else 2
        self.update()

    # ===== Painting =====
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # background
        bg_color = QColor("#4cd964") if self._checked else QColor("#ccc")
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self._height/2, self._height/2)

        # knob
        knob_rect = QRectF(self._offset, 2, self._height - 4, self._height - 4)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(knob_rect)
