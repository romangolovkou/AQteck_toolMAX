from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QPushButton


class AqTimeCellWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_state = 0
        self.label = None
        self.pic_0 = QPixmap('UI/icons/nixie_0.png').scaled(105, 164)
        self.pic_1 = QPixmap('UI/icons/nixie_1.png').scaled(105, 164)
        self.pic_2 = QPixmap('UI/icons/nixie_2.png').scaled(105, 164)
        self.pic_3 = QPixmap('UI/icons/nixie_3.png').scaled(105, 164)
        self.pic_4 = QPixmap('UI/icons/nixie_4.png').scaled(105, 164)
        self.pic_5 = QPixmap('UI/icons/nixie_5.png').scaled(105, 164)
        self.pic_6 = QPixmap('UI/icons/nixie_6.png').scaled(105, 164)
        self.pic_7 = QPixmap('UI/icons/nixie_7.png').scaled(105, 164)
        self.pic_8 = QPixmap('UI/icons/nixie_8.png').scaled(105, 164)
        self.pic_9 = QPixmap('UI/icons/nixie_9.png').scaled(105, 164)
        self.plusBtn = None
        self.minusBtn = None

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, number: int):
        self._current_state = number
        pic = getattr(self, f'pic_{number}')
        self.label.setPixmap(pic)

    def prepare_ui(self):
        self.label = self.findChildren(QLabel)[0]
        self.label.setPixmap(self.pic_0)
        buttons = self.findChildren(QPushButton)
        for btn in buttons:
            name = btn.objectName()
            if 'plus' in name:
                self.plusBtn = btn
                continue

            if 'minus' in name:
                self.minusBtn = btn
                continue

    def set_state(self, number: int):
        self.current_state = number
