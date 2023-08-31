from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton


class AQ_addButton(QPushButton):
    def __init__(self, event_manager, text, parent=None):
        super().__init__(text, parent)
        self.event_manager = event_manager
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setFixedSize(100, 35)
        self.clicked.connect(lambda: self.event_manager.emit_event('Add_device'))
        self.setStyleSheet("""
                            QPushButton {
                                border-left: 1px solid #9ef1d3;
                                border-top: 1px solid #9ef1d3;
                                border-bottom: 1px solid #5bb192;
                                border-right: 1px solid #5bb192;
                                color: #D0D0D0;
                                background-color: #2b2d30;
                                border-radius: 4px;
                            }
                            QPushButton:hover {
                                background-color: #3c3e41;
                            }
                            QPushButton:pressed {
                                background-color: #429061;
                            }
                        """)

        self.show()
