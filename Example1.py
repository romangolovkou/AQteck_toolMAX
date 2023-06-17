from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 615)
        MainWindow.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_window_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_window_frame.setGeometry(QtCore.QRect(0, 0, 450, 600))
        self.main_window_frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.main_window_frame.setStyleSheet("background-color: rgb(52, 73, 94);\n"
"border-radius: 20px;\n"
"\n"
"")
        self.main_window_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_window_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_window_frame.setObjectName("main_window_frame")
        self.tab_menu_frame = QtWidgets.QFrame(self.main_window_frame)
        self.tab_menu_frame.setGeometry(QtCore.QRect(0, 0, 450, 30))
        self.tab_menu_frame.setStyleSheet("background-color: rgb(35, 50, 65);\n"
"border-top-left-radius: 0px;\n"
"border-top-right-radius: 0px;\n"
"border-bottom-left-radius: 0px;\n"
"border-bottom-right-radius: 0px;")
        self.tab_menu_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tab_menu_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_menu_frame.setObjectName("tab_menu_frame")
        self.button_exit = QtWidgets.QPushButton(self.tab_menu_frame)
        self.button_exit.setGeometry(QtCore.QRect(415, 8, 15, 15))
        self.button_exit.setStyleSheet("QPushButton {\n"
"    border-radius: 7px;\n"
"    background-color: rgb(231, 76, 60);\n"
"}\n"
"QPushButton:hover:hover{\n"
"    background-color: rgb(192, 57, 43);\n"
"}")
        self.button_exit.setText("")
        self.button_exit.setObjectName("button_exit")
        self.button_fullscrean = QtWidgets.QPushButton(self.tab_menu_frame)
        self.button_fullscrean.setGeometry(QtCore.QRect(395, 8, 15, 15))
        self.button_fullscrean.setStyleSheet("QPushButton {\n"
"    border-radius: 7px;\n"
"    background-color: rgb(46, 204, 113);\n"
"}\n"
"QPushButton:hover:hover{\n"
"    background-color: rgb(39, 174, 96);\n"
"}")
        self.button_fullscrean.setText("")
        self.button_fullscrean.setObjectName("button_fullscrean")
        self.label = QtWidgets.QLabel(self.tab_menu_frame)
        self.label.setGeometry(QtCore.QRect(200, 4, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(236, 240, 241);")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AC"))
        self.label.setText(_translate("MainWindow", "<strong>Name AC</strong>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())