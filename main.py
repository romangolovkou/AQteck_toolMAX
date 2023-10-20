import sys
import time
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen
from AQ_MainWindow import AQ_MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("Icons/Splash3.png"))
    splash.show()

    # Имитация загрузки (можно заменить на вашу реализацию)
    # time.sleep(2)  # Например, 2 секунды

    window = AQ_MainWindow()
    # window.showMaximized()
    window.show()
    splash.close()
    sys.exit(app.exec())
