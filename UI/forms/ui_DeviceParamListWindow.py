# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DeviceParamListWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidgetItem, QVBoxLayout,
    QWidget)

from AqDeviceParamWindow.AqParamListWidget import (AqParamListInfoFrame, AqParamListTableWidget)

class Ui_DeviceParamListWidget(object):
    def setupUi(self, DeviceParamListWidget):
        if not DeviceParamListWidget.objectName():
            DeviceParamListWidget.setObjectName(u"DeviceParamListWidget")
        DeviceParamListWidget.resize(979, 238)
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
"}\n"
"\n"
"QPushButton {\n"
"	border"
                        ": 1px solid #637A7B;\n"
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
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.deviceInfoLabel = QLabel(self.mainFrame)
        self.deviceInfoLabel.setObjectName(u"deviceInfoLabel")

        self.verticalLayout_4.addWidget(self.deviceInfoLabel)

        self.infoFrame = AqParamListInfoFrame(self.mainFrame)
        self.infoFrame.setObjectName(u"infoFrame")
        self.infoFrame.setFrameShape(QFrame.StyledPanel)
        self.infoFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.infoFrame)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 0, 0, 0)

        self.verticalLayout_4.addWidget(self.infoFrame)

        self.tableFrame = QFrame(self.mainFrame)
        self.tableFrame.setObjectName(u"tableFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableFrame.sizePolicy().hasHeightForWidth())
        self.tableFrame.setSizePolicy(sizePolicy1)
        self.tableFrame.setMaximumSize(QSize(16777215, 500))
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

        self.saveBtn = QPushButton(self.mainFrame)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setMinimumSize(QSize(100, 0))
        self.saveBtn.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_4.addWidget(self.saveBtn, 0, Qt.AlignLeft)

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
        self.deviceInfoLabel.setText("")
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
        self.saveBtn.setText(QCoreApplication.translate("DeviceParamListWidget", u"Save to file...", None))
    # retranslateUi

