import getopt
import sys
import time

from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

import console_app
import console_help_functions
from AppCore import Core
from AqMainWindow import AqMainWindow
from AqTranslateManager import AqTranslateManager

cur_lang = 'UA'


import sys
import logging

logging.basicConfig(filename='/tmp/foobar.log')

def exception_hook(exc_type, exc_value, exc_traceback):
    logging.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

sys.excepthook = exception_hook

if __name__ == '__main__':
    sys.excepthook = exception_hook
    #x = 1/0

    # Program started without advanced command
    Core.init()
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        AqTranslateManager.init(app)
        # translator = QTranslator(app)
        # if translator.load('translate/ua.qm'):
        #     app.installTranslator(translator)
        splash = QSplashScreen(QPixmap("UI/icons/Splash3.png"))
        splash.show()

        # # Имитация загрузки (можно заменить на вашу реализацию)
        # time.sleep(2)  # Например, 2 секунды

        window = AqMainWindow()
        # window.showMaximized()
        window.show()
        splash.close()
        sys.exit(app.exec())
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hc", ["help", "console"])
        except getopt.GetoptError:
            print('Type -h or --help to see all available commands')
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                console_help_functions.print_app_help()
                sys.exit(0)
            elif opt in ("-c", "--console"):
                result_code = console_app.run()
                sys.exit(result_code)
