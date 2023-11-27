# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DeviceInfoDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DeviceInfoDialog(object):
    def setupUi(self, DeviceInfoDialog):
        if not DeviceInfoDialog.objectName():
            DeviceInfoDialog.setObjectName(u"DeviceInfoDialog")
        DeviceInfoDialog.setWindowModality(Qt.WindowModal)
        DeviceInfoDialog.resize(416, 134)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeviceInfoDialog.sizePolicy().hasHeightForWidth())
        DeviceInfoDialog.setSizePolicy(sizePolicy)
        DeviceInfoDialog.setStyleSheet(u"* {\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	background: transparent;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"\n"
"#mainFrame {\n"
"	background-color: #2c313c;\n"
"}\n"
"\n"
"#windowNameFrame {\n"
"	border-top-left-radius: 10px;\n"
"	background-color: #2F4858;\n"
"	border: none;\n"
"}\n"
"\n"
" #btnFrame {\n"
"	border-top-right-radius: 10px;\n"
"	background-color: #2c313c;\n"
"	border: none;\n"
"}\n"
"\n"
"#generalInfoFrame, #operatingInfoFrame {\n"
"	border-top: 1px solid;\n"
"	border-left: 1px solid;\n"
"	border-color: #637A7B\n"
"}\n"
"\n"
"QLineEdit {\n"
"	min-width: 200px;\n"
"	min-height: 20 px;\n"
"	border-right: 1px solid;\n"
"	border-bottom: 1px solid;\n"
"	border-color: #637A7B\n"
"}\n"
"\n"
"QLabel {\n"
"	min-height: 30px;\n"
"	font-size: 12pt;\n"
"}")
        self.verticalLayout = QVBoxLayout(DeviceInfoDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.toolboxFrame = QFrame(DeviceInfoDialog)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.windowNameFrame.sizePolicy().hasHeightForWidth())
        self.windowNameFrame.setSizePolicy(sizePolicy1)
        self.windowNameFrame.setMaximumSize(QSize(16777215, 30))
        self.windowNameFrame.setFrameShape(QFrame.StyledPanel)
        self.windowNameFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.windowNameFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.windowNameLabel = QLabel(self.windowNameFrame)
        self.windowNameLabel.setObjectName(u"windowNameLabel")
        sizePolicy1.setHeightForWidth(self.windowNameLabel.sizePolicy().hasHeightForWidth())
        self.windowNameLabel.setSizePolicy(sizePolicy1)
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


        self.horizontalLayout.addWidget(self.btnFrame, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.toolboxFrame)

        self.mainFrame = QFrame(DeviceInfoDialog)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy2)
        self.mainFrame.setMinimumSize(QSize(0, 0))
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.giLabel = QLabel(self.mainFrame)
        self.giLabel.setObjectName(u"giLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.giLabel.sizePolicy().hasHeightForWidth())
        self.giLabel.setSizePolicy(sizePolicy3)
        self.giLabel.setMinimumSize(QSize(100, 30))

        self.verticalLayout_2.addWidget(self.giLabel)

        self.generalInfoFrame = QFrame(self.mainFrame)
        self.generalInfoFrame.setObjectName(u"generalInfoFrame")
        self.generalInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.generalInfoFrame.setFrameShadow(QFrame.Raised)
        self.generalInfoLayout = QFormLayout(self.generalInfoFrame)
        self.generalInfoLayout.setObjectName(u"generalInfoLayout")
        self.generalInfoLayout.setHorizontalSpacing(0)
        self.generalInfoLayout.setVerticalSpacing(0)
        self.generalInfoLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.generalInfoFrame, 0, Qt.AlignTop)

        self.oiLabel = QLabel(self.mainFrame)
        self.oiLabel.setObjectName(u"oiLabel")

        self.verticalLayout_2.addWidget(self.oiLabel)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.operatingInfoFrame = QFrame(self.mainFrame)
        self.operatingInfoFrame.setObjectName(u"operatingInfoFrame")
        sizePolicy2.setHeightForWidth(self.operatingInfoFrame.sizePolicy().hasHeightForWidth())
        self.operatingInfoFrame.setSizePolicy(sizePolicy2)
        self.operatingInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.operatingInfoFrame.setFrameShadow(QFrame.Raised)
        self.operatingInfoLayout = QFormLayout(self.operatingInfoFrame)
        self.operatingInfoLayout.setObjectName(u"operatingInfoLayout")
        self.operatingInfoLayout.setHorizontalSpacing(0)
        self.operatingInfoLayout.setVerticalSpacing(0)
        self.operatingInfoLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.operatingInfoFrame, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.mainFrame, 0, Qt.AlignTop)


        self.retranslateUi(DeviceInfoDialog)

        QMetaObject.connectSlotsByName(DeviceInfoDialog)
    # setupUi

    def retranslateUi(self, DeviceInfoDialog):
        DeviceInfoDialog.setWindowTitle(QCoreApplication.translate("DeviceInfoDialog", u"Dialog", None))
        self.windowNameLabel.setText(QCoreApplication.translate("DeviceInfoDialog", u"Device Information", None))
        self.closeBtn.setText(QCoreApplication.translate("DeviceInfoDialog", u"Close", None))
        self.giLabel.setText(QCoreApplication.translate("DeviceInfoDialog", u"General information", None))
        self.oiLabel.setText(QCoreApplication.translate("DeviceInfoDialog", u"Operating information", None))
    # retranslateUi

