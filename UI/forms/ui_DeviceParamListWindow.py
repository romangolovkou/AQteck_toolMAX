# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DeviceParamListWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidgetItem,
    QVBoxLayout, QWidget)

from AqDeviceParamWindow.AqParamListWidget import (AqParamListInfoFrame, AqParamListTableWidget)

class Ui_DeviceParamListWidget(object):
    def setupUi(self, DeviceParamListWidget):
        if not DeviceParamListWidget.objectName():
            DeviceParamListWidget.setObjectName(u"DeviceParamListWidget")
        DeviceParamListWidget.resize(979, 396)
        DeviceParamListWidget.setStyleSheet(u"* {\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	background: transparent;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"\n"
"#toolboxFrame {\n"
"	border-top-left-radius: 10px;\n"
"	background-color: #2c313c;\n"
"	border-top-right-radius: 10px;\n"
"}\n"
"\n"
"#windowNameFrame {\n"
"	border-top-left-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
"	background-color: #2F4858;\n"
"}\n"
"\n"
"#mainFrame {\n"
"	background-color: #2c313c;\n"
"}\n"
"\n"
"#tableFrame {\n"
"	border-left: 1px solid #637A7B;\n"
"}\n"
"\n"
"QLabel {\n"
"	min-height: 30px;\n"
"	font-size: 12pt;\n"
"}\n"
"\n"
"QTableWidget {\n"
"	background-color: transparent;\n"
"	gridline-color: #637A7B;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"	background-color: transparent;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"	background-color: #A5ADA8;\n"
"}\n"
"\n"
"QHeaderView {\n"
"	background-color: #637A7B;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"	background-color: #637A7B;\n"
"\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(DeviceParamListWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.toolboxFrame = QFrame(DeviceParamListWidget)
        self.toolboxFrame.setObjectName(u"toolboxFrame")
        self.toolboxFrame.setMinimumSize(QSize(0, 30))
        self.toolboxFrame.setFrameShape(QFrame.StyledPanel)
        self.toolboxFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.toolboxFrame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.windowNameFrame = QFrame(self.toolboxFrame)
        self.windowNameFrame.setObjectName(u"windowNameFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.windowNameFrame.sizePolicy().hasHeightForWidth())
        self.windowNameFrame.setSizePolicy(sizePolicy)
        self.windowNameFrame.setMaximumSize(QSize(16777215, 30))
        self.windowNameFrame.setFrameShape(QFrame.StyledPanel)
        self.windowNameFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.windowNameFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.windowNameLabel = QLabel(self.windowNameFrame)
        self.windowNameLabel.setObjectName(u"windowNameLabel")
        sizePolicy.setHeightForWidth(self.windowNameLabel.sizePolicy().hasHeightForWidth())
        self.windowNameLabel.setSizePolicy(sizePolicy)
        self.windowNameLabel.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_3.addWidget(self.windowNameLabel, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.windowNameFrame)

        self.btnFrame = QFrame(self.toolboxFrame)
        self.btnFrame.setObjectName(u"btnFrame")
        self.btnFrame.setFrameShape(QFrame.StyledPanel)
        self.btnFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.btnFrame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.closeBtn = QPushButton(self.btnFrame)
        self.closeBtn.setObjectName(u"closeBtn")
        self.closeBtn.setMaximumSize(QSize(50, 30))

        self.horizontalLayout_2.addWidget(self.closeBtn, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.btnFrame)


        self.verticalLayout.addWidget(self.toolboxFrame)

        self.mainFrame = QFrame(DeviceParamListWidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.deviceInfoLabel = QLabel(self.mainFrame)
        self.deviceInfoLabel.setObjectName(u"deviceInfoLabel")

        self.verticalLayout_4.addWidget(self.deviceInfoLabel)

        self.infoFrame = AqParamListInfoFrame(self.mainFrame)
        self.infoFrame.setObjectName(u"infoFrame")
        self.infoFrame.setFrameShape(QFrame.StyledPanel)
        self.infoFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.infoFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEdit_6 = QLineEdit(self.infoFrame)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.verticalLayout_2.addWidget(self.lineEdit_6)

        self.lineEdit_4 = QLineEdit(self.infoFrame)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout_2.addWidget(self.lineEdit_4)

        self.lineEdit = QLineEdit(self.infoFrame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_2.addWidget(self.lineEdit)


        self.verticalLayout_4.addWidget(self.infoFrame)

        self.tableFrame = QFrame(self.mainFrame)
        self.tableFrame.setObjectName(u"tableFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableFrame.sizePolicy().hasHeightForWidth())
        self.tableFrame.setSizePolicy(sizePolicy1)
        self.tableFrame.setFrameShape(QFrame.StyledPanel)
        self.tableFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.tableFrame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tableView = AqParamListTableWidget(self.tableFrame)
        if (self.tableView.columnCount() < 8):
            self.tableView.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.tableView.rowCount() < 5):
            self.tableView.setRowCount(5)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableView.setVerticalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableView.setVerticalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableView.setVerticalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableView.setVerticalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableView.setVerticalHeaderItem(4, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableView.setItem(0, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableView.setItem(0, 1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableView.setItem(0, 2, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableView.setItem(0, 3, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableView.setItem(0, 4, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableView.setItem(0, 5, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableView.setItem(0, 6, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableView.setItem(0, 7, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableView.setItem(1, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableView.setItem(1, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableView.setItem(1, 2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableView.setItem(1, 3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableView.setItem(1, 4, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableView.setItem(1, 5, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableView.setItem(1, 6, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableView.setItem(1, 7, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableView.setItem(2, 0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableView.setItem(2, 1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableView.setItem(2, 2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableView.setItem(2, 3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableView.setItem(2, 4, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableView.setItem(2, 5, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableView.setItem(2, 6, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableView.setItem(2, 7, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableView.setItem(3, 0, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableView.setItem(3, 1, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableView.setItem(3, 2, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableView.setItem(3, 3, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableView.setItem(3, 4, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableView.setItem(3, 5, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableView.setItem(3, 6, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableView.setItem(3, 7, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tableView.setItem(4, 0, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tableView.setItem(4, 1, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.tableView.setItem(4, 2, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tableView.setItem(4, 3, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tableView.setItem(4, 4, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tableView.setItem(4, 5, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tableView.setItem(4, 6, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.tableView.setItem(4, 7, __qtablewidgetitem52)
        self.tableView.setObjectName(u"tableView")
        sizePolicy1.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy1)
        self.tableView.setMinimumSize(QSize(0, 0))
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setGridStyle(Qt.SolidLine)
        self.tableView.horizontalHeader().setVisible(True)
        self.tableView.horizontalHeader().setMinimumSectionSize(120)
        self.tableView.horizontalHeader().setDefaultSectionSize(120)
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setMinimumSectionSize(25)
        self.tableView.verticalHeader().setDefaultSectionSize(25)
        self.tableView.verticalHeader().setHighlightSections(False)

        self.verticalLayout_3.addWidget(self.tableView, 0, Qt.AlignTop)


        self.verticalLayout_4.addWidget(self.tableFrame, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.mainFrame)


        self.retranslateUi(DeviceParamListWidget)

        QMetaObject.connectSlotsByName(DeviceParamListWidget)
    # setupUi

    def retranslateUi(self, DeviceParamListWidget):
        DeviceParamListWidget.setWindowTitle(QCoreApplication.translate("DeviceParamListWidget", u"Form", None))
        self.windowNameLabel.setText(QCoreApplication.translate("DeviceParamListWidget", u"Device Information", None))
        self.closeBtn.setText(QCoreApplication.translate("DeviceParamListWidget", u"Close", None))
        self.deviceInfoLabel.setText(QCoreApplication.translate("DeviceParamListWidget", u"\u041c\u0423210-402 S/N 5012398139128371", None))
        self.lineEdit_6.setText(QCoreApplication.translate("DeviceParamListWidget", u"Current IP: 102.15.13.23", None))
        self.lineEdit_4.setText(QCoreApplication.translate("DeviceParamListWidget", u"Protocol: Modbus TCP", None))
        self.lineEdit.setText(QCoreApplication.translate("DeviceParamListWidget", u"Byte order: Least significant register first", None))
        ___qtablewidgetitem = self.tableView.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DeviceParamListWidget", u"Parameter", None));
        ___qtablewidgetitem1 = self.tableView.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DeviceParamListWidget", u"Group", None));
        ___qtablewidgetitem2 = self.tableView.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DeviceParamListWidget", u"Address (dec)", None));
        ___qtablewidgetitem3 = self.tableView.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DeviceParamListWidget", u"Address (hex)", None));
        ___qtablewidgetitem4 = self.tableView.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("DeviceParamListWidget", u"Number of registers", None));
        ___qtablewidgetitem5 = self.tableView.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("DeviceParamListWidget", u"Read function", None));
        ___qtablewidgetitem6 = self.tableView.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("DeviceParamListWidget", u"Write function", None));
        ___qtablewidgetitem7 = self.tableView.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("DeviceParamListWidget", u"Data type", None));
        ___qtablewidgetitem8 = self.tableView.verticalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("DeviceParamListWidget", u"\u041d\u043e\u0432\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430", None));
        ___qtablewidgetitem9 = self.tableView.verticalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("DeviceParamListWidget", u"\u041d\u043e\u0432\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430", None));
        ___qtablewidgetitem10 = self.tableView.verticalHeaderItem(3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("DeviceParamListWidget", u"\u041d\u043e\u0432\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430", None));
        ___qtablewidgetitem11 = self.tableView.verticalHeaderItem(4)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("DeviceParamListWidget", u"\u041d\u043e\u0432\u0430\u044f \u0441\u0442\u0440\u043e\u043a\u0430", None));

        __sortingEnabled = self.tableView.isSortingEnabled()
        self.tableView.setSortingEnabled(False)
        ___qtablewidgetitem12 = self.tableView.item(0, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("DeviceParamListWidget", u"1", None));
        ___qtablewidgetitem13 = self.tableView.item(0, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("DeviceParamListWidget", u"2", None));
        ___qtablewidgetitem14 = self.tableView.item(0, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("DeviceParamListWidget", u"3", None));
        ___qtablewidgetitem15 = self.tableView.item(0, 3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("DeviceParamListWidget", u"4", None));
        ___qtablewidgetitem16 = self.tableView.item(0, 4)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("DeviceParamListWidget", u"fgh", None));
        ___qtablewidgetitem17 = self.tableView.item(0, 5)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("DeviceParamListWidget", u"gfh", None));
        ___qtablewidgetitem18 = self.tableView.item(0, 6)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("DeviceParamListWidget", u"gfhfg", None));
        ___qtablewidgetitem19 = self.tableView.item(0, 7)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("DeviceParamListWidget", u"gfhg", None));
        ___qtablewidgetitem20 = self.tableView.item(1, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("DeviceParamListWidget", u"2", None));
        ___qtablewidgetitem21 = self.tableView.item(1, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("DeviceParamListWidget", u"3", None));
        ___qtablewidgetitem22 = self.tableView.item(1, 2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("DeviceParamListWidget", u"4", None));
        ___qtablewidgetitem23 = self.tableView.item(1, 3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("DeviceParamListWidget", u"5", None));
        ___qtablewidgetitem24 = self.tableView.item(1, 4)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("DeviceParamListWidget", u"gf", None));
        ___qtablewidgetitem25 = self.tableView.item(1, 5)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("DeviceParamListWidget", u"hfgh", None));
        ___qtablewidgetitem26 = self.tableView.item(1, 6)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("DeviceParamListWidget", u"hgf", None));
        ___qtablewidgetitem27 = self.tableView.item(1, 7)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("DeviceParamListWidget", u"hgfh", None));
        ___qtablewidgetitem28 = self.tableView.item(2, 0)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("DeviceParamListWidget", u"23", None));
        ___qtablewidgetitem29 = self.tableView.item(2, 1)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("DeviceParamListWidget", u"4", None));
        ___qtablewidgetitem30 = self.tableView.item(2, 2)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("DeviceParamListWidget", u"5", None));
        ___qtablewidgetitem31 = self.tableView.item(2, 3)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("DeviceParamListWidget", u"6", None));
        ___qtablewidgetitem32 = self.tableView.item(2, 4)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("DeviceParamListWidget", u"hfghf", None));
        ___qtablewidgetitem33 = self.tableView.item(2, 5)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("DeviceParamListWidget", u"dsfg", None));
        ___qtablewidgetitem34 = self.tableView.item(2, 6)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("DeviceParamListWidget", u"sdfg", None));
        ___qtablewidgetitem35 = self.tableView.item(2, 7)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("DeviceParamListWidget", u"fhgfh", None));
        ___qtablewidgetitem36 = self.tableView.item(3, 0)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("DeviceParamListWidget", u"123", None));
        ___qtablewidgetitem37 = self.tableView.item(3, 1)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("DeviceParamListWidget", u"123", None));
        ___qtablewidgetitem38 = self.tableView.item(3, 2)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("DeviceParamListWidget", u"312", None));
        ___qtablewidgetitem39 = self.tableView.item(3, 3)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("DeviceParamListWidget", u"132", None));
        ___qtablewidgetitem40 = self.tableView.item(3, 4)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("DeviceParamListWidget", u"ghfgh", None));
        ___qtablewidgetitem41 = self.tableView.item(3, 5)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("DeviceParamListWidget", u"sdgfsd", None));
        ___qtablewidgetitem42 = self.tableView.item(3, 6)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("DeviceParamListWidget", u"sdgf", None));
        ___qtablewidgetitem43 = self.tableView.item(3, 7)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("DeviceParamListWidget", u"gfh", None));
        ___qtablewidgetitem44 = self.tableView.item(4, 0)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("DeviceParamListWidget", u"1323", None));
        ___qtablewidgetitem45 = self.tableView.item(4, 1)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("DeviceParamListWidget", u"123", None));
        ___qtablewidgetitem46 = self.tableView.item(4, 2)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("DeviceParamListWidget", u"1243", None));
        ___qtablewidgetitem47 = self.tableView.item(4, 3)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("DeviceParamListWidget", u"123", None));
        ___qtablewidgetitem48 = self.tableView.item(4, 4)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("DeviceParamListWidget", u"hg", None));
        ___qtablewidgetitem49 = self.tableView.item(4, 5)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("DeviceParamListWidget", u"fg", None));
        ___qtablewidgetitem50 = self.tableView.item(4, 6)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("DeviceParamListWidget", u"hfgh", None));
        ___qtablewidgetitem51 = self.tableView.item(4, 7)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("DeviceParamListWidget", u"gfhfg", None));
        self.tableView.setSortingEnabled(__sortingEnabled)

    # retranslateUi

