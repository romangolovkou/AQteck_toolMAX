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
        DeviceInfoDialog.resize(420, 105)
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
"\n"
"#operatingInfoFrame, #generalInfoFrame {\n"
"	background-color: #1f232a;\n"
"	border: none;\n"
"}\n"
"\n"
"#frame_2 {\n"
"	border-top-left-radius: 10px;\n"
"	background-color: #000;\n"
"	border: none;\n"
"}\n"
"\n"
" #frame{\n"
"	border-top-right-radius: 10px;\n"
"	background-color: #1f232a;\n"
"	border: none;\n"
"}\n"
"\n"
"QLineEdit {\n"
"	min-width: 200px;\n"
"	min-height: 20 px;\n"
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
        self.ToolboxFrame = QFrame(DeviceInfoDialog)
        self.ToolboxFrame.setObjectName(u"ToolboxFrame")
        self.ToolboxFrame.setMinimumSize(QSize(0, 30))
        self.ToolboxFrame.setFrameShape(QFrame.StyledPanel)
        self.ToolboxFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.ToolboxFrame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.ToolboxFrame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMaximumSize(QSize(16777215, 30))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 0, 5, 0)
        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_3.addWidget(self.label_3, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.ToolboxFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(50, 30))

        self.horizontalLayout_2.addWidget(self.pushButton, 0, Qt.AlignHCenter)


        self.horizontalLayout.addWidget(self.frame, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.ToolboxFrame)

        self.generalInfoFrame = QFrame(DeviceInfoDialog)
        self.generalInfoFrame.setObjectName(u"generalInfoFrame")
        self.generalInfoFrame.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.generalInfoFrame.sizePolicy().hasHeightForWidth())
        self.generalInfoFrame.setSizePolicy(sizePolicy2)
        self.generalInfoFrame.setMinimumSize(QSize(0, 20))
        self.generalInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.generalInfoFrame.setFrameShadow(QFrame.Raised)
        self.generalInfoLayout = QFormLayout(self.generalInfoFrame)
        self.generalInfoLayout.setObjectName(u"generalInfoLayout")
        self.generalInfoLayout.setHorizontalSpacing(5)
        self.generalInfoLayout.setVerticalSpacing(5)
        self.generalInfoLayout.setContentsMargins(5, 0, 5, 5)
        self.label = QLabel(self.generalInfoFrame)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        self.label.setMinimumSize(QSize(100, 30))

        self.generalInfoLayout.setWidget(0, QFormLayout.SpanningRole, self.label)


        self.verticalLayout.addWidget(self.generalInfoFrame, 0, Qt.AlignTop)

        self.operatingInfoFrame = QFrame(DeviceInfoDialog)
        self.operatingInfoFrame.setObjectName(u"operatingInfoFrame")
        sizePolicy2.setHeightForWidth(self.operatingInfoFrame.sizePolicy().hasHeightForWidth())
        self.operatingInfoFrame.setSizePolicy(sizePolicy2)
        self.operatingInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.operatingInfoFrame.setFrameShadow(QFrame.Raised)
        self.operatingInfoLayout = QFormLayout(self.operatingInfoFrame)
        self.operatingInfoLayout.setObjectName(u"operatingInfoLayout")
        self.operatingInfoLayout.setHorizontalSpacing(5)
        self.operatingInfoLayout.setVerticalSpacing(5)
        self.operatingInfoLayout.setContentsMargins(5, 0, 5, 5)
        self.label_2 = QLabel(self.operatingInfoFrame)
        self.label_2.setObjectName(u"label_2")

        self.operatingInfoLayout.setWidget(0, QFormLayout.SpanningRole, self.label_2)


        self.verticalLayout.addWidget(self.operatingInfoFrame, 0, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(DeviceInfoDialog)

        QMetaObject.connectSlotsByName(DeviceInfoDialog)
    # setupUi

    def retranslateUi(self, DeviceInfoDialog):
        DeviceInfoDialog.setWindowTitle(QCoreApplication.translate("DeviceInfoDialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("DeviceInfoDialog", u"Device Information", None))
        self.pushButton.setText(QCoreApplication.translate("DeviceInfoDialog", u"Close", None))
        self.label.setText(QCoreApplication.translate("DeviceInfoDialog", u"General information", None))
        self.label_2.setText(QCoreApplication.translate("DeviceInfoDialog", u"Operating information", None))
    # retranslateUi

