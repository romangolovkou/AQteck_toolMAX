from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel


class AqTimeCellWidget(QWidget):
    pic_0 = QPixmap('Icons/nixie_0.png')
    pic_1 = QPixmap('Icons/nixie_1.png')
    pic_2 = QPixmap('Icons/nixie_2.png')
    pic_3 = QPixmap('Icons/nixie_3.png')
    pic_4 = QPixmap('Icons/nixie_4.png')
    pic_5 = QPixmap('Icons/nixie_5.png')
    pic_6 = QPixmap('Icons/nixie_6.png')
    pic_7 = QPixmap('Icons/nixie_7.png')
    pic_8 = QPixmap('Icons/nixie_8.png')
    pic_9 = QPixmap('Icons/nixie_9.png')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_state = 0

    def prepare_ui(self):
        self.findChildren(QLabel)[0].setPixmap(self.pic_8)
