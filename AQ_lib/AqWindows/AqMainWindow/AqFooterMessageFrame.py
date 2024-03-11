from PySide6.QtCore import QPropertyAnimation, QSize, QTimer, QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QLabel, QGraphicsDropShadowEffect


class AqFooterMessageFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.footerMessageLabel = None
        self.animation = None

    def prepare_ui(self):
        self.footerMessageLabel = self.findChild(QLabel, 'footerMessageLabel')
        if self.footerMessageLabel is None:
            raise Exception(self.objectName() + ' : lost footerMessageLabel')

        effect = QGraphicsDropShadowEffect(self)
        effect.setColor(QColor('#000000'))
        effect.setBlurRadius(20)
        effect.setXOffset(0)
        effect.setYOffset(0)
        self.footerMessageLabel.setGraphicsEffect(effect)
        self.footerMessageLabel.hide()
        self.animation = QPropertyAnimation(self.footerMessageLabel, b'geometry')
        self.animation.setDuration(500)

    def expand_message(self):
        self.footerMessageLabel.show()
        self.animation.setStartValue(QRect(0, 0, 0, 30))
        self.animation.setEndValue(QRect(0, 0,
                                         self.footerMessageLabel.sizeHint().width(),
                                         30))
        self.animation.start()

    def collapse_message(self):
        self.animation.setStartValue(QRect(0, 0,
                                           self.footerMessageLabel.width(),
                                           30))
        self.animation.setEndValue(QRect(0, 0, 0, 30))
        self.animation.start()

    def show_message(self, msg: str):
        self.footerMessageLabel.setText(msg)
        self.expand_message()
        QTimer.singleShot(5000, self.collapse_message)


