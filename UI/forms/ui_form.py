# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 621)
        MainWindow.setWindowOpacity(1.000000000000000)
        MainWindow.setStyleSheet(u"*{\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	background: transparent;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"\n"
"#menuBtn {\n"
"	border-top-left-radius: 10px;\n"
"	border-top-right-radius: 10px;\n"
"	background-color: #000;\n"
"}\n"
"\n"
"#frame_3 QPushButton{\n"
"	border-top-left-radius: 10px;\n"
"	border-top-right-radius: 10px;\n"
"background-color: #1f232a;\n"
"}\n"
"\n"
"#frame_2{\n"
"	border-top-left-radius: 10px;\n"
"	border-top-right-radius: 10px;\n"
"	background-color: #16191d;\n"
"}\n"
"\n"
"#leftContainerMenu{\n"
"	background-color: #2c313c;\n"
"}\n"
"\n"
"#centerContainer {\n"
"	background-color: #16191d;\n"
"}\n"
"\n"
"#deviceWidget_1 {\n"
"	background-color: #16191d;\n"
"	border-top-left-radius: 5px;\n"
"	border-bottom-left-radius: 5px;\n"
"}\n"
"\n"
"#scrollDevListBtn{\n"
"	background-color: #1f232a;\n"
"}\n"
"\n"
"#addBtnWidget {\n"
"	background-color: #16191d;\n"
"	border-top-left-radius: 5px;\n"
"	border-bottom-left-radius: 5px;\n"
"} \n"
"\n"
"#rightMe"
                        "nuContainer {\n"
"	background-color: #16191d;\n"
"}\n"
"\n"
"#rightMenuSubContainer {\n"
"	background-color: #2c313c;\n"
"	border-top-left-radius: 10px;\n"
"	border-bottom-left-radius: 10px;\n"
"}\n"
"\n"
"#rightMenuSubContainer Line {\n"
"	border: 5px solid #16191d;\n"
"	border-style: solid;\n"
"	background-color: #16191d;\n"
"}\n"
"\n"
" #line_2 ,  #line_3, #line_4,  #line_5  {\n"
"	border: 2px solid #16191d;\n"
"	border-style: solid;\n"
"	background-color: #16191d;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.headerContainer = QWidget(self.centralwidget)
        self.headerContainer.setObjectName(u"headerContainer")
        self.verticalLayout_5 = QVBoxLayout(self.headerContainer)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.menuContainer = QWidget(self.headerContainer)
        self.menuContainer.setObjectName(u"menuContainer")
        self.menuContainer.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.menuContainer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.menuContainer)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.menuBtn = QPushButton(self.frame)
        self.menuBtn.setObjectName(u"menuBtn")
        self.menuBtn.setMaximumSize(QSize(45, 45))
        icon = QIcon()
        icon.addFile(u"../../../../AQico_translucent.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menuBtn.setIcon(icon)
        self.menuBtn.setIconSize(QSize(40, 40))

        self.verticalLayout_6.addWidget(self.menuBtn)


        self.horizontalLayout_3.addWidget(self.frame)

        self.frame_3 = QFrame(self.menuContainer)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(2, 0, 0, 0)
        self.devicesMenuBtn = QPushButton(self.frame_3)
        self.devicesMenuBtn.setObjectName(u"devicesMenuBtn")
        self.devicesMenuBtn.setMinimumSize(QSize(100, 35))

        self.horizontalLayout_10.addWidget(self.devicesMenuBtn, 0, Qt.AlignBottom)

        self.paramsMenuBtn = QPushButton(self.frame_3)
        self.paramsMenuBtn.setObjectName(u"paramsMenuBtn")
        self.paramsMenuBtn.setMinimumSize(QSize(100, 35))

        self.horizontalLayout_10.addWidget(self.paramsMenuBtn, 0, Qt.AlignBottom)

        self.loggingMenuBtn = QPushButton(self.frame_3)
        self.loggingMenuBtn.setObjectName(u"loggingMenuBtn")
        self.loggingMenuBtn.setMinimumSize(QSize(100, 35))

        self.horizontalLayout_10.addWidget(self.loggingMenuBtn, 0, Qt.AlignBottom)

        self.utilsMenuBtn = QPushButton(self.frame_3)
        self.utilsMenuBtn.setObjectName(u"utilsMenuBtn")
        self.utilsMenuBtn.setMinimumSize(QSize(100, 35))

        self.horizontalLayout_10.addWidget(self.utilsMenuBtn, 0, Qt.AlignBottom)


        self.horizontalLayout_3.addWidget(self.frame_3, 0, Qt.AlignLeft)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.frame_2 = QFrame(self.menuContainer)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_6.setSpacing(7)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(5, 0, 5, 0)
        self.minimizeBtn = QPushButton(self.frame_2)
        self.minimizeBtn.setObjectName(u"minimizeBtn")
        self.minimizeBtn.setMinimumSize(QSize(35, 25))
        icon1 = QIcon()
        icon1.addFile(u":/icon/E:/feather/minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeBtn.setIcon(icon1)
        self.minimizeBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.minimizeBtn)

        self.maximizeBtn = QPushButton(self.frame_2)
        self.maximizeBtn.setObjectName(u"maximizeBtn")
        self.maximizeBtn.setMinimumSize(QSize(35, 25))
        icon2 = QIcon()
        icon2.addFile(u":/icon/E:/feather/copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeBtn.setIcon(icon2)
        self.maximizeBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.maximizeBtn)

        self.closeBtn = QPushButton(self.frame_2)
        self.closeBtn.setObjectName(u"closeBtn")
        self.closeBtn.setMinimumSize(QSize(35, 25))
        icon3 = QIcon()
        icon3.addFile(u":/icon/E:/feather/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.closeBtn.setIcon(icon3)
        self.closeBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.closeBtn)


        self.horizontalLayout_3.addWidget(self.frame_2)


        self.verticalLayout_5.addWidget(self.menuContainer)

        self.popUpContainer = QWidget(self.headerContainer)
        self.popUpContainer.setObjectName(u"popUpContainer")
        self.popUpContainer.setMinimumSize(QSize(0, 0))
        self.popUpContainer.setMaximumSize(QSize(16777215, 0))
        self.horizontalLayout_4 = QHBoxLayout(self.popUpContainer)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(20, 0, 0, 0)
        self.mainMenuPopUpContainer = QWidget(self.popUpContainer)
        self.mainMenuPopUpContainer.setObjectName(u"mainMenuPopUpContainer")

        self.horizontalLayout_4.addWidget(self.mainMenuPopUpContainer)

        self.devicePopUpContainer = QWidget(self.popUpContainer)
        self.devicePopUpContainer.setObjectName(u"devicePopUpContainer")
        self.verticalLayout_10 = QVBoxLayout(self.devicePopUpContainer)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.addDeviceMenuBtn_2 = QToolButton(self.devicePopUpContainer)
        self.addDeviceMenuBtn_2.setObjectName(u"addDeviceMenuBtn_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.addDeviceMenuBtn_2.sizePolicy().hasHeightForWidth())
        self.addDeviceMenuBtn_2.setSizePolicy(sizePolicy2)
        self.addDeviceMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.addDeviceMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.addDeviceMenuBtn_2.setLayoutDirection(Qt.LeftToRight)
        self.addDeviceMenuBtn_2.setAutoFillBackground(False)
        self.addDeviceMenuBtn_2.setIcon(icon)
        self.addDeviceMenuBtn_2.setIconSize(QSize(20, 20))
        self.addDeviceMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_10.addWidget(self.addDeviceMenuBtn_2)

        self.deleteDeviceMenuBtn_2 = QToolButton(self.devicePopUpContainer)
        self.deleteDeviceMenuBtn_2.setObjectName(u"deleteDeviceMenuBtn_2")
        sizePolicy2.setHeightForWidth(self.deleteDeviceMenuBtn_2.sizePolicy().hasHeightForWidth())
        self.deleteDeviceMenuBtn_2.setSizePolicy(sizePolicy2)
        self.deleteDeviceMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.deleteDeviceMenuBtn_2.setMaximumSize(QSize(130, 25))
        font = QFont()
        font.setKerning(False)
        self.deleteDeviceMenuBtn_2.setFont(font)
        self.deleteDeviceMenuBtn_2.setFocusPolicy(Qt.TabFocus)
        self.deleteDeviceMenuBtn_2.setIcon(icon)
        self.deleteDeviceMenuBtn_2.setIconSize(QSize(20, 20))
        self.deleteDeviceMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_10.addWidget(self.deleteDeviceMenuBtn_2)

        self.ipAddrMenuBtn_2 = QToolButton(self.devicePopUpContainer)
        self.ipAddrMenuBtn_2.setObjectName(u"ipAddrMenuBtn_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ipAddrMenuBtn_2.sizePolicy().hasHeightForWidth())
        self.ipAddrMenuBtn_2.setSizePolicy(sizePolicy3)
        self.ipAddrMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.ipAddrMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.ipAddrMenuBtn_2.setIcon(icon)
        self.ipAddrMenuBtn_2.setIconSize(QSize(20, 20))
        self.ipAddrMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_10.addWidget(self.ipAddrMenuBtn_2)


        self.horizontalLayout_4.addWidget(self.devicePopUpContainer, 0, Qt.AlignTop)

        self.paramPopUpContainer = QWidget(self.popUpContainer)
        self.paramPopUpContainer.setObjectName(u"paramPopUpContainer")
        self.verticalLayout_9 = QVBoxLayout(self.paramPopUpContainer)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.readParamMenuBtn_2 = QToolButton(self.paramPopUpContainer)
        self.readParamMenuBtn_2.setObjectName(u"readParamMenuBtn_2")
        self.readParamMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.readParamMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.readParamMenuBtn_2.setIcon(icon)
        self.readParamMenuBtn_2.setIconSize(QSize(20, 20))
        self.readParamMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_9.addWidget(self.readParamMenuBtn_2)

        self.writeParamMenuBtn_2 = QToolButton(self.paramPopUpContainer)
        self.writeParamMenuBtn_2.setObjectName(u"writeParamMenuBtn_2")
        self.writeParamMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.writeParamMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.writeParamMenuBtn_2.setIcon(icon)
        self.writeParamMenuBtn_2.setIconSize(QSize(20, 20))
        self.writeParamMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_9.addWidget(self.writeParamMenuBtn_2)

        self.setDefaultMenuBtn_2 = QToolButton(self.paramPopUpContainer)
        self.setDefaultMenuBtn_2.setObjectName(u"setDefaultMenuBtn_2")
        self.setDefaultMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.setDefaultMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.setDefaultMenuBtn_2.setIcon(icon)
        self.setDefaultMenuBtn_2.setIconSize(QSize(20, 20))
        self.setDefaultMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_9.addWidget(self.setDefaultMenuBtn_2)

        self.poaramListMenuBtn = QToolButton(self.paramPopUpContainer)
        self.poaramListMenuBtn.setObjectName(u"poaramListMenuBtn")
        self.poaramListMenuBtn.setMaximumSize(QSize(130, 25))
        self.poaramListMenuBtn.setIcon(icon)
        self.poaramListMenuBtn.setIconSize(QSize(20, 20))
        self.poaramListMenuBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_9.addWidget(self.poaramListMenuBtn)


        self.horizontalLayout_4.addWidget(self.paramPopUpContainer, 0, Qt.AlignTop)

        self.logPopUpContainer = QWidget(self.popUpContainer)
        self.logPopUpContainer.setObjectName(u"logPopUpContainer")
        self.verticalLayout_7 = QVBoxLayout(self.logPopUpContainer)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.saveLogMenuBtn = QToolButton(self.logPopUpContainer)
        self.saveLogMenuBtn.setObjectName(u"saveLogMenuBtn")
        sizePolicy2.setHeightForWidth(self.saveLogMenuBtn.sizePolicy().hasHeightForWidth())
        self.saveLogMenuBtn.setSizePolicy(sizePolicy2)
        self.saveLogMenuBtn.setMinimumSize(QSize(25, 25))
        self.saveLogMenuBtn.setMaximumSize(QSize(130, 25))
        self.saveLogMenuBtn.setLayoutDirection(Qt.LeftToRight)
        self.saveLogMenuBtn.setAutoFillBackground(False)
        self.saveLogMenuBtn.setIcon(icon)
        self.saveLogMenuBtn.setIconSize(QSize(20, 20))
        self.saveLogMenuBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_7.addWidget(self.saveLogMenuBtn)

        self.dataLogCfgMenuBtn = QToolButton(self.logPopUpContainer)
        self.dataLogCfgMenuBtn.setObjectName(u"dataLogCfgMenuBtn")
        sizePolicy2.setHeightForWidth(self.dataLogCfgMenuBtn.sizePolicy().hasHeightForWidth())
        self.dataLogCfgMenuBtn.setSizePolicy(sizePolicy2)
        self.dataLogCfgMenuBtn.setMinimumSize(QSize(25, 25))
        self.dataLogCfgMenuBtn.setMaximumSize(QSize(130, 25))
        self.dataLogCfgMenuBtn.setFont(font)
        self.dataLogCfgMenuBtn.setFocusPolicy(Qt.TabFocus)
        self.dataLogCfgMenuBtn.setIcon(icon)
        self.dataLogCfgMenuBtn.setIconSize(QSize(20, 20))
        self.dataLogCfgMenuBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_7.addWidget(self.dataLogCfgMenuBtn)


        self.horizontalLayout_4.addWidget(self.logPopUpContainer, 0, Qt.AlignTop)

        self.utilsPopUpContainer = QWidget(self.popUpContainer)
        self.utilsPopUpContainer.setObjectName(u"utilsPopUpContainer")
        self.verticalLayout_11 = QVBoxLayout(self.utilsPopUpContainer)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.watchListMenuBtn = QToolButton(self.utilsPopUpContainer)
        self.watchListMenuBtn.setObjectName(u"watchListMenuBtn")
        self.watchListMenuBtn.setMinimumSize(QSize(25, 25))
        self.watchListMenuBtn.setMaximumSize(QSize(130, 25))
        self.watchListMenuBtn.setIcon(icon)
        self.watchListMenuBtn.setIconSize(QSize(20, 20))
        self.watchListMenuBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_11.addWidget(self.watchListMenuBtn)

        self.rtcMenuBtn_2 = QToolButton(self.utilsPopUpContainer)
        self.rtcMenuBtn_2.setObjectName(u"rtcMenuBtn_2")
        self.rtcMenuBtn_2.setMinimumSize(QSize(25, 25))
        self.rtcMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.rtcMenuBtn_2.setIcon(icon)
        self.rtcMenuBtn_2.setIconSize(QSize(20, 20))
        self.rtcMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_11.addWidget(self.rtcMenuBtn_2)

        self.passwordMenuBtn_2 = QToolButton(self.utilsPopUpContainer)
        self.passwordMenuBtn_2.setObjectName(u"passwordMenuBtn_2")
        self.passwordMenuBtn_2.setMaximumSize(QSize(130, 25))
        self.passwordMenuBtn_2.setLayoutDirection(Qt.LeftToRight)
        self.passwordMenuBtn_2.setIcon(icon)
        self.passwordMenuBtn_2.setIconSize(QSize(20, 20))
        self.passwordMenuBtn_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_11.addWidget(self.passwordMenuBtn_2)

        self.firmwareMenuBtn = QToolButton(self.utilsPopUpContainer)
        self.firmwareMenuBtn.setObjectName(u"firmwareMenuBtn")
        self.firmwareMenuBtn.setMaximumSize(QSize(130, 25))
        self.firmwareMenuBtn.setIcon(icon)
        self.firmwareMenuBtn.setIconSize(QSize(20, 20))
        self.firmwareMenuBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_11.addWidget(self.firmwareMenuBtn)

        self.calibrationMenuBtn = QToolButton(self.utilsPopUpContainer)
        self.calibrationMenuBtn.setObjectName(u"calibrationMenuBtn")
        self.calibrationMenuBtn.setMinimumSize(QSize(25, 25))
        self.calibrationMenuBtn.setMaximumSize(QSize(130, 25))
        self.calibrationMenuBtn.setIcon(icon)
        self.calibrationMenuBtn.setIconSize(QSize(20, 20))
        self.calibrationMenuBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_11.addWidget(self.calibrationMenuBtn)


        self.horizontalLayout_4.addWidget(self.utilsPopUpContainer, 0, Qt.AlignTop)


        self.verticalLayout_5.addWidget(self.popUpContainer)


        self.verticalLayout.addWidget(self.headerContainer)

        self.mainContainer = QWidget(self.centralwidget)
        self.mainContainer.setObjectName(u"mainContainer")
        self.horizontalLayout = QHBoxLayout(self.mainContainer)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.leftContainerMenu = QWidget(self.mainContainer)
        self.leftContainerMenu.setObjectName(u"leftContainerMenu")
        self.leftContainerMenu.setMinimumSize(QSize(150, 0))
        self.leftContainerMenu.setStyleSheet(u"")
        self.verticalLayout_12 = QVBoxLayout(self.leftContainerMenu)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 1, 0, 0)
        self.frame_6 = QFrame(self.leftContainerMenu)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(5, 0, 0, 0)
        self.projectLabel = QLabel(self.frame_6)
        self.projectLabel.setObjectName(u"projectLabel")
        font1 = QFont()
        font1.setPointSize(10)
        self.projectLabel.setFont(font1)

        self.horizontalLayout_16.addWidget(self.projectLabel)


        self.verticalLayout_12.addWidget(self.frame_6)

        self.deviceListContainer = QWidget(self.leftContainerMenu)
        self.deviceListContainer.setObjectName(u"deviceListContainer")
        self.deviceListContainer.setMinimumSize(QSize(0, 0))
        self.verticalLayout_16 = QVBoxLayout(self.deviceListContainer)
        self.verticalLayout_16.setSpacing(5)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(5, 5, 0, 1)
        self.deviceWidget_1 = QWidget(self.deviceListContainer)
        self.deviceWidget_1.setObjectName(u"deviceWidget_1")
        self.deviceWidget_1.setMaximumSize(QSize(200, 60))
        self.horizontalLayout_8 = QHBoxLayout(self.deviceWidget_1)
        self.horizontalLayout_8.setSpacing(2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.deviceImage = QFrame(self.deviceWidget_1)
        self.deviceImage.setObjectName(u"deviceImage")
        self.deviceImage.setMinimumSize(QSize(50, 50))
        self.deviceImage.setMaximumSize(QSize(50, 50))
        self.deviceImage.setFrameShape(QFrame.StyledPanel)
        self.deviceImage.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.deviceImage)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.devIcon = QLabel(self.deviceImage)
        self.devIcon.setObjectName(u"devIcon")
        self.devIcon.setMaximumSize(QSize(50, 50))
        self.devIcon.setTextFormat(Qt.AutoText)
        self.devIcon.setPixmap(QPixmap(u"../../../../AQico_translucent.png"))
        self.devIcon.setScaledContents(True)
        self.devIcon.setAlignment(Qt.AlignCenter)
        self.devIcon.setWordWrap(False)

        self.horizontalLayout_9.addWidget(self.devIcon)


        self.horizontalLayout_8.addWidget(self.deviceImage)

        self.deviceInfo = QFrame(self.deviceWidget_1)
        self.deviceInfo.setObjectName(u"deviceInfo")
        self.deviceInfo.setMinimumSize(QSize(0, 0))
        self.deviceInfo.setMaximumSize(QSize(145, 50))
        self.deviceInfo.setFrameShape(QFrame.StyledPanel)
        self.deviceInfo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.deviceInfo)
        self.verticalLayout_13.setSpacing(3)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.deviceName = QLabel(self.deviceInfo)
        self.deviceName.setObjectName(u"deviceName")
        font2 = QFont()
        font2.setBold(False)
        self.deviceName.setFont(font2)

        self.verticalLayout_13.addWidget(self.deviceName, 0, Qt.AlignLeft)

        self.label = QLabel(self.deviceInfo)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)

        self.verticalLayout_13.addWidget(self.label, 0, Qt.AlignLeft)

        self.label_2 = QLabel(self.deviceInfo)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.verticalLayout_13.addWidget(self.label_2)


        self.horizontalLayout_8.addWidget(self.deviceInfo)


        self.verticalLayout_16.addWidget(self.deviceWidget_1)

        self.deviceWidget_2 = QWidget(self.deviceListContainer)
        self.deviceWidget_2.setObjectName(u"deviceWidget_2")
        self.deviceWidget_2.setMaximumSize(QSize(200, 60))
        self.horizontalLayout_11 = QHBoxLayout(self.deviceWidget_2)
        self.horizontalLayout_11.setSpacing(2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.deviceImage_2 = QFrame(self.deviceWidget_2)
        self.deviceImage_2.setObjectName(u"deviceImage_2")
        self.deviceImage_2.setMinimumSize(QSize(50, 50))
        self.deviceImage_2.setMaximumSize(QSize(50, 50))
        self.deviceImage_2.setFrameShape(QFrame.StyledPanel)
        self.deviceImage_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.deviceImage_2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.devIcon_2 = QLabel(self.deviceImage_2)
        self.devIcon_2.setObjectName(u"devIcon_2")
        self.devIcon_2.setMaximumSize(QSize(50, 50))
        self.devIcon_2.setTextFormat(Qt.AutoText)
        self.devIcon_2.setPixmap(QPixmap(u"../../../../AQico_translucent.png"))
        self.devIcon_2.setScaledContents(True)
        self.devIcon_2.setAlignment(Qt.AlignCenter)
        self.devIcon_2.setWordWrap(False)

        self.horizontalLayout_12.addWidget(self.devIcon_2)


        self.horizontalLayout_11.addWidget(self.deviceImage_2)

        self.deviceInfo_2 = QFrame(self.deviceWidget_2)
        self.deviceInfo_2.setObjectName(u"deviceInfo_2")
        self.deviceInfo_2.setMinimumSize(QSize(0, 0))
        self.deviceInfo_2.setMaximumSize(QSize(145, 50))
        self.deviceInfo_2.setFrameShape(QFrame.StyledPanel)
        self.deviceInfo_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.deviceInfo_2)
        self.verticalLayout_14.setSpacing(3)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.deviceName_2 = QLabel(self.deviceInfo_2)
        self.deviceName_2.setObjectName(u"deviceName_2")
        self.deviceName_2.setFont(font2)

        self.verticalLayout_14.addWidget(self.deviceName_2, 0, Qt.AlignLeft)

        self.label_3 = QLabel(self.deviceInfo_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.verticalLayout_14.addWidget(self.label_3, 0, Qt.AlignLeft)

        self.label_4 = QLabel(self.deviceInfo_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.verticalLayout_14.addWidget(self.label_4)


        self.horizontalLayout_11.addWidget(self.deviceInfo_2)


        self.verticalLayout_16.addWidget(self.deviceWidget_2)

        self.deviceWidget_3 = QWidget(self.deviceListContainer)
        self.deviceWidget_3.setObjectName(u"deviceWidget_3")
        self.deviceWidget_3.setEnabled(True)
        self.deviceWidget_3.setMaximumSize(QSize(200, 60))
        self.horizontalLayout_13 = QHBoxLayout(self.deviceWidget_3)
        self.horizontalLayout_13.setSpacing(2)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(3, 3, 3, 3)
        self.deviceImage_3 = QFrame(self.deviceWidget_3)
        self.deviceImage_3.setObjectName(u"deviceImage_3")
        self.deviceImage_3.setMinimumSize(QSize(50, 50))
        self.deviceImage_3.setMaximumSize(QSize(50, 50))
        self.deviceImage_3.setFrameShape(QFrame.StyledPanel)
        self.deviceImage_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.deviceImage_3)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.devIcon_3 = QLabel(self.deviceImage_3)
        self.devIcon_3.setObjectName(u"devIcon_3")
        self.devIcon_3.setMaximumSize(QSize(50, 50))
        self.devIcon_3.setTextFormat(Qt.AutoText)
        self.devIcon_3.setPixmap(QPixmap(u"../../../../AQico_translucent.png"))
        self.devIcon_3.setScaledContents(True)
        self.devIcon_3.setAlignment(Qt.AlignCenter)
        self.devIcon_3.setWordWrap(False)

        self.horizontalLayout_14.addWidget(self.devIcon_3)


        self.horizontalLayout_13.addWidget(self.deviceImage_3)

        self.deviceInfo_3 = QFrame(self.deviceWidget_3)
        self.deviceInfo_3.setObjectName(u"deviceInfo_3")
        self.deviceInfo_3.setMinimumSize(QSize(0, 0))
        self.deviceInfo_3.setMaximumSize(QSize(145, 50))
        self.deviceInfo_3.setFrameShape(QFrame.StyledPanel)
        self.deviceInfo_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.deviceInfo_3)
        self.verticalLayout_15.setSpacing(3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.deviceName_3 = QLabel(self.deviceInfo_3)
        self.deviceName_3.setObjectName(u"deviceName_3")
        self.deviceName_3.setFont(font2)

        self.verticalLayout_15.addWidget(self.deviceName_3, 0, Qt.AlignLeft)

        self.label_5 = QLabel(self.deviceInfo_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.verticalLayout_15.addWidget(self.label_5, 0, Qt.AlignLeft)

        self.label_6 = QLabel(self.deviceInfo_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.verticalLayout_15.addWidget(self.label_6)


        self.horizontalLayout_13.addWidget(self.deviceInfo_3)


        self.verticalLayout_16.addWidget(self.deviceWidget_3)

        self.addBtnWidget = QWidget(self.deviceListContainer)
        self.addBtnWidget.setObjectName(u"addBtnWidget")
        self.addBtnWidget.setMaximumSize(QSize(200, 16777215))
        self.addBtnWidget.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.addBtnWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(20, 0, 20, 0)
        self.deviceImage_4 = QFrame(self.addBtnWidget)
        self.deviceImage_4.setObjectName(u"deviceImage_4")
        self.deviceImage_4.setMinimumSize(QSize(40, 50))
        self.deviceImage_4.setMaximumSize(QSize(50, 50))
        self.deviceImage_4.setFrameShape(QFrame.StyledPanel)
        self.deviceImage_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.deviceImage_4)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.devIcon_4 = QLabel(self.deviceImage_4)
        self.devIcon_4.setObjectName(u"devIcon_4")
        self.devIcon_4.setMaximumSize(QSize(40, 40))
        self.devIcon_4.setTextFormat(Qt.AutoText)
        self.devIcon_4.setPixmap(QPixmap(u"../../../../plus_2040520 \u043a\u043e\u043f\u0438\u044f.png"))
        self.devIcon_4.setScaledContents(True)
        self.devIcon_4.setAlignment(Qt.AlignCenter)
        self.devIcon_4.setWordWrap(False)

        self.horizontalLayout_15.addWidget(self.devIcon_4)


        self.horizontalLayout_2.addWidget(self.deviceImage_4, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.deviceInfo_4 = QFrame(self.addBtnWidget)
        self.deviceInfo_4.setObjectName(u"deviceInfo_4")
        self.deviceInfo_4.setMinimumSize(QSize(0, 0))
        self.deviceInfo_4.setMaximumSize(QSize(145, 30))
        self.deviceInfo_4.setFrameShape(QFrame.StyledPanel)
        self.deviceInfo_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.deviceInfo_4)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.deviceInfo_4)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setFont(font2)

        self.verticalLayout_17.addWidget(self.label_11, 0, Qt.AlignHCenter)

        self.label_12 = QLabel(self.deviceInfo_4)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setFont(font2)

        self.verticalLayout_17.addWidget(self.label_12, 0, Qt.AlignHCenter)


        self.horizontalLayout_2.addWidget(self.deviceInfo_4, 0, Qt.AlignLeft)


        self.verticalLayout_16.addWidget(self.addBtnWidget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer)


        self.verticalLayout_12.addWidget(self.deviceListContainer)

        self.scrollDevListBtn = QPushButton(self.leftContainerMenu)
        self.scrollDevListBtn.setObjectName(u"scrollDevListBtn")
        self.scrollDevListBtn.setMinimumSize(QSize(0, 0))
        self.scrollDevListBtn.setMaximumSize(QSize(16777215, 20))
        icon4 = QIcon()
        icon4.addFile(u":/icon/E:/feather/chevrons-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.scrollDevListBtn.setIcon(icon4)

        self.verticalLayout_12.addWidget(self.scrollDevListBtn)


        self.horizontalLayout.addWidget(self.leftContainerMenu)

        self.centerContainer = QWidget(self.mainContainer)
        self.centerContainer.setObjectName(u"centerContainer")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.centerContainer.sizePolicy().hasHeightForWidth())
        self.centerContainer.setSizePolicy(sizePolicy4)
        self.centerContainer.setStyleSheet(u"")
        self.horizontalLayout_5 = QHBoxLayout(self.centerContainer)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.treeViewContainer = QWidget(self.centerContainer)
        self.treeViewContainer.setObjectName(u"treeViewContainer")
        sizePolicy4.setHeightForWidth(self.treeViewContainer.sizePolicy().hasHeightForWidth())
        self.treeViewContainer.setSizePolicy(sizePolicy4)
        self.verticalLayout_8 = QVBoxLayout(self.treeViewContainer)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget_2 = QStackedWidget(self.treeViewContainer)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        sizePolicy4.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy4)
        self.NoDevicesPage = QWidget()
        self.NoDevicesPage.setObjectName(u"NoDevicesPage")
        sizePolicy4.setHeightForWidth(self.NoDevicesPage.sizePolicy().hasHeightForWidth())
        self.NoDevicesPage.setSizePolicy(sizePolicy4)
        self.verticalLayout_3 = QVBoxLayout(self.NoDevicesPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_5 = QFrame(self.NoDevicesPage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy5)
        self.frame_5.setMinimumSize(QSize(0, 300))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_5)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 40)
        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        font3 = QFont()
        font3.setPointSize(12)
        self.label_7.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_7, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_8, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setEnabled(True)
        self.label_9.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_9, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.factoryPic = QLabel(self.frame_5)
        self.factoryPic.setObjectName(u"factoryPic")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.factoryPic.sizePolicy().hasHeightForWidth())
        self.factoryPic.setSizePolicy(sizePolicy6)
        self.factoryPic.setMinimumSize(QSize(273, 151))
        self.factoryPic.setMaximumSize(QSize(273, 151))
        self.factoryPic.setSizeIncrement(QSize(0, 0))
        self.factoryPic.setPixmap(QPixmap(u"../../../../industrial_pic1.png"))
        self.factoryPic.setScaledContents(True)
        self.factoryPic.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.factoryPic, 0, Qt.AlignHCenter)


        self.verticalLayout_3.addWidget(self.frame_5, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.stackedWidget_2.addWidget(self.NoDevicesPage)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        sizePolicy4.setHeightForWidth(self.page_2.sizePolicy().hasHeightForWidth())
        self.page_2.setSizePolicy(sizePolicy4)
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget_2.addWidget(self.page_2)

        self.verticalLayout_8.addWidget(self.stackedWidget_2)

        self.frame_4 = QFrame(self.treeViewContainer)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setMinimumSize(QSize(0, 50))
        self.frame_4.setMaximumSize(QSize(16777215, 50))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.readParamMenuBtn_3 = QToolButton(self.frame_4)
        self.readParamMenuBtn_3.setObjectName(u"readParamMenuBtn_3")
        self.readParamMenuBtn_3.setMinimumSize(QSize(25, 25))
        self.readParamMenuBtn_3.setMaximumSize(QSize(130, 25))
        self.readParamMenuBtn_3.setIcon(icon)
        self.readParamMenuBtn_3.setIconSize(QSize(20, 20))
        self.readParamMenuBtn_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.readParamMenuBtn_3)

        self.writeParamMenuBtn_3 = QToolButton(self.frame_4)
        self.writeParamMenuBtn_3.setObjectName(u"writeParamMenuBtn_3")
        self.writeParamMenuBtn_3.setMinimumSize(QSize(25, 25))
        self.writeParamMenuBtn_3.setMaximumSize(QSize(130, 25))
        self.writeParamMenuBtn_3.setIcon(icon)
        self.writeParamMenuBtn_3.setIconSize(QSize(20, 20))
        self.writeParamMenuBtn_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.writeParamMenuBtn_3)

        self.toolButton = QToolButton(self.frame_4)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMinimumSize(QSize(0, 25))
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(20, 20))
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.toolButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.setDefaultMenuBtn_3 = QToolButton(self.frame_4)
        self.setDefaultMenuBtn_3.setObjectName(u"setDefaultMenuBtn_3")
        self.setDefaultMenuBtn_3.setMinimumSize(QSize(25, 25))
        self.setDefaultMenuBtn_3.setMaximumSize(QSize(130, 25))
        self.setDefaultMenuBtn_3.setIcon(icon)
        self.setDefaultMenuBtn_3.setIconSize(QSize(20, 20))
        self.setDefaultMenuBtn_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_7.addWidget(self.setDefaultMenuBtn_3)


        self.verticalLayout_8.addWidget(self.frame_4)


        self.horizontalLayout_5.addWidget(self.treeViewContainer)

        self.rightMenuContainer = QWidget(self.centerContainer)
        self.rightMenuContainer.setObjectName(u"rightMenuContainer")
        self.rightMenuContainer.setMinimumSize(QSize(0, 0))
        self.rightMenuContainer.setMaximumSize(QSize(45, 16777215))
        self.rightMenuContainer.setStyleSheet(u"")
        self.verticalLayout_18 = QVBoxLayout(self.rightMenuContainer)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 20, 0, 0)
        self.rightMenuSubContainer = QWidget(self.rightMenuContainer)
        self.rightMenuSubContainer.setObjectName(u"rightMenuSubContainer")
        self.rightMenuSubContainer.setMinimumSize(QSize(0, 400))
        self.rightMenuSubContainer.setMaximumSize(QSize(16777215, 500))
        self.verticalLayout_24 = QVBoxLayout(self.rightMenuSubContainer)
        self.verticalLayout_24.setSpacing(5)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(5, 0, 5, 0)
        self.deviceInfoFrame = QFrame(self.rightMenuSubContainer)
        self.deviceInfoFrame.setObjectName(u"deviceInfoFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.deviceInfoFrame.sizePolicy().hasHeightForWidth())
        self.deviceInfoFrame.setSizePolicy(sizePolicy7)
        self.deviceInfoFrame.setFrameShape(QFrame.StyledPanel)
        self.deviceInfoFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.deviceInfoFrame)
        self.verticalLayout_19.setSpacing(5)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.deviceInfoBtn = QToolButton(self.deviceInfoFrame)
        self.deviceInfoBtn.setObjectName(u"deviceInfoBtn")
        self.deviceInfoBtn.setMinimumSize(QSize(32, 32))
        self.deviceInfoBtn.setMaximumSize(QSize(195, 32))
        self.deviceInfoBtn.setLayoutDirection(Qt.RightToLeft)
        self.deviceInfoBtn.setIcon(icon)
        self.deviceInfoBtn.setIconSize(QSize(32, 32))
        self.deviceInfoBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_19.addWidget(self.deviceInfoBtn, 0, Qt.AlignLeft)

        self.paramListBtn = QToolButton(self.deviceInfoFrame)
        self.paramListBtn.setObjectName(u"paramListBtn")
        self.paramListBtn.setMinimumSize(QSize(32, 32))
        self.paramListBtn.setMaximumSize(QSize(195, 32))
        self.paramListBtn.setLayoutDirection(Qt.RightToLeft)
        self.paramListBtn.setIcon(icon)
        self.paramListBtn.setIconSize(QSize(32, 32))
        self.paramListBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_19.addWidget(self.paramListBtn, 0, Qt.AlignLeft)


        self.verticalLayout_24.addWidget(self.deviceInfoFrame, 0, Qt.AlignTop)

        self.line_4 = QFrame(self.rightMenuSubContainer)
        self.line_4.setObjectName(u"line_4")
        sizePolicy5.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy5)
        self.line_4.setMinimumSize(QSize(160, 2))
        self.line_4.setMaximumSize(QSize(16777215, 2))
        self.line_4.setAutoFillBackground(False)
        self.line_4.setStyleSheet(u"")
        self.line_4.setLineWidth(4)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_24.addWidget(self.line_4)

        self.deviceUtilsFrame = QFrame(self.rightMenuSubContainer)
        self.deviceUtilsFrame.setObjectName(u"deviceUtilsFrame")
        sizePolicy7.setHeightForWidth(self.deviceUtilsFrame.sizePolicy().hasHeightForWidth())
        self.deviceUtilsFrame.setSizePolicy(sizePolicy7)
        self.deviceUtilsFrame.setMinimumSize(QSize(0, 0))
        self.deviceUtilsFrame.setMaximumSize(QSize(16777215, 150))
        self.deviceUtilsFrame.setFrameShape(QFrame.StyledPanel)
        self.deviceUtilsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.deviceUtilsFrame)
        self.verticalLayout_21.setSpacing(5)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.setRtcBtn = QToolButton(self.deviceUtilsFrame)
        self.setRtcBtn.setObjectName(u"setRtcBtn")
        self.setRtcBtn.setMinimumSize(QSize(32, 32))
        self.setRtcBtn.setMaximumSize(QSize(195, 32))
        self.setRtcBtn.setLayoutDirection(Qt.RightToLeft)
        icon5 = QIcon()
        icon5.addFile(u"../../../../icon/clock_223404.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setRtcBtn.setIcon(icon5)
        self.setRtcBtn.setIconSize(QSize(32, 32))
        self.setRtcBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_21.addWidget(self.setRtcBtn, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.setPasswordBtn = QToolButton(self.deviceUtilsFrame)
        self.setPasswordBtn.setObjectName(u"setPasswordBtn")
        self.setPasswordBtn.setMinimumSize(QSize(32, 32))
        self.setPasswordBtn.setMaximumSize(QSize(195, 32))
        self.setPasswordBtn.setLayoutDirection(Qt.RightToLeft)
        icon6 = QIcon()
        icon6.addFile(u"../../../../icon/padlock_2889676.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setPasswordBtn.setIcon(icon6)
        self.setPasswordBtn.setIconSize(QSize(32, 32))
        self.setPasswordBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_21.addWidget(self.setPasswordBtn, 0, Qt.AlignLeft)

        self.calibDeviceBtn = QToolButton(self.deviceUtilsFrame)
        self.calibDeviceBtn.setObjectName(u"calibDeviceBtn")
        self.calibDeviceBtn.setMinimumSize(QSize(32, 32))
        self.calibDeviceBtn.setMaximumSize(QSize(195, 32))
        self.calibDeviceBtn.setLayoutDirection(Qt.RightToLeft)
        icon7 = QIcon()
        icon7.addFile(u"../../../../icon/setting_10035148.png", QSize(), QIcon.Normal, QIcon.Off)
        self.calibDeviceBtn.setIcon(icon7)
        self.calibDeviceBtn.setIconSize(QSize(32, 32))
        self.calibDeviceBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_21.addWidget(self.calibDeviceBtn, 0, Qt.AlignLeft|Qt.AlignVCenter)


        self.verticalLayout_24.addWidget(self.deviceUtilsFrame, 0, Qt.AlignTop)

        self.line_3 = QFrame(self.rightMenuSubContainer)
        self.line_3.setObjectName(u"line_3")
        sizePolicy5.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy5)
        self.line_3.setMinimumSize(QSize(0, 2))
        self.line_3.setMaximumSize(QSize(16777215, 2))
        self.line_3.setAutoFillBackground(False)
        self.line_3.setStyleSheet(u"")
        self.line_3.setLineWidth(4)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_24.addWidget(self.line_3)

        self.deviceLogFrame = QFrame(self.rightMenuSubContainer)
        self.deviceLogFrame.setObjectName(u"deviceLogFrame")
        sizePolicy7.setHeightForWidth(self.deviceLogFrame.sizePolicy().hasHeightForWidth())
        self.deviceLogFrame.setSizePolicy(sizePolicy7)
        self.deviceLogFrame.setMinimumSize(QSize(0, 0))
        self.deviceLogFrame.setMaximumSize(QSize(16777215, 200))
        self.deviceLogFrame.setFrameShape(QFrame.StyledPanel)
        self.deviceLogFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.deviceLogFrame)
        self.verticalLayout_20.setSpacing(5)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.saveLogBtn = QToolButton(self.deviceLogFrame)
        self.saveLogBtn.setObjectName(u"saveLogBtn")
        self.saveLogBtn.setMinimumSize(QSize(32, 32))
        self.saveLogBtn.setMaximumSize(QSize(195, 32))
        self.saveLogBtn.setLayoutDirection(Qt.RightToLeft)
        self.saveLogBtn.setIcon(icon)
        self.saveLogBtn.setIconSize(QSize(32, 32))
        self.saveLogBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_20.addWidget(self.saveLogBtn, 0, Qt.AlignLeft)

        self.configLogBtn = QToolButton(self.deviceLogFrame)
        self.configLogBtn.setObjectName(u"configLogBtn")
        self.configLogBtn.setMinimumSize(QSize(32, 32))
        self.configLogBtn.setMaximumSize(QSize(195, 32))
        self.configLogBtn.setLayoutDirection(Qt.RightToLeft)
        self.configLogBtn.setIcon(icon)
        self.configLogBtn.setIconSize(QSize(32, 32))
        self.configLogBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_20.addWidget(self.configLogBtn, 0, Qt.AlignLeft)


        self.verticalLayout_24.addWidget(self.deviceLogFrame, 0, Qt.AlignTop)

        self.line_2 = QFrame(self.rightMenuSubContainer)
        self.line_2.setObjectName(u"line_2")
        sizePolicy5.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy5)
        self.line_2.setMinimumSize(QSize(0, 2))
        self.line_2.setMaximumSize(QSize(16777215, 2))
        self.line_2.setAutoFillBackground(False)
        self.line_2.setStyleSheet(u"")
        self.line_2.setLineWidth(4)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_24.addWidget(self.line_2)

        self.firmwareFrame = QFrame(self.rightMenuSubContainer)
        self.firmwareFrame.setObjectName(u"firmwareFrame")
        self.firmwareFrame.setFrameShape(QFrame.StyledPanel)
        self.firmwareFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.firmwareFrame)
        self.verticalLayout_22.setSpacing(5)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.firmwareUpdBtn = QToolButton(self.firmwareFrame)
        self.firmwareUpdBtn.setObjectName(u"firmwareUpdBtn")
        self.firmwareUpdBtn.setMinimumSize(QSize(32, 32))
        self.firmwareUpdBtn.setMaximumSize(QSize(195, 32))
        self.firmwareUpdBtn.setLayoutDirection(Qt.RightToLeft)
        self.firmwareUpdBtn.setIcon(icon)
        self.firmwareUpdBtn.setIconSize(QSize(32, 32))
        self.firmwareUpdBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_22.addWidget(self.firmwareUpdBtn, 0, Qt.AlignLeft)

        self.rebootDeviceBtn = QToolButton(self.firmwareFrame)
        self.rebootDeviceBtn.setObjectName(u"rebootDeviceBtn")
        self.rebootDeviceBtn.setMinimumSize(QSize(32, 32))
        self.rebootDeviceBtn.setMaximumSize(QSize(195, 32))
        self.rebootDeviceBtn.setLayoutDirection(Qt.RightToLeft)
        self.rebootDeviceBtn.setIcon(icon)
        self.rebootDeviceBtn.setIconSize(QSize(32, 32))
        self.rebootDeviceBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_22.addWidget(self.rebootDeviceBtn, 0, Qt.AlignLeft)


        self.verticalLayout_24.addWidget(self.firmwareFrame)

        self.line_5 = QFrame(self.rightMenuSubContainer)
        self.line_5.setObjectName(u"line_5")
        sizePolicy5.setHeightForWidth(self.line_5.sizePolicy().hasHeightForWidth())
        self.line_5.setSizePolicy(sizePolicy5)
        self.line_5.setMinimumSize(QSize(0, 2))
        self.line_5.setMaximumSize(QSize(16777215, 2))
        self.line_5.setAutoFillBackground(False)
        self.line_5.setStyleSheet(u"")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setLineWidth(4)
        self.line_5.setFrameShape(QFrame.HLine)

        self.verticalLayout_24.addWidget(self.line_5)

        self.watcListFrame = QFrame(self.rightMenuSubContainer)
        self.watcListFrame.setObjectName(u"watcListFrame")
        self.watcListFrame.setFrameShape(QFrame.StyledPanel)
        self.watcListFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.watcListFrame)
        self.verticalLayout_23.setSpacing(5)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.watchListBtn = QToolButton(self.watcListFrame)
        self.watchListBtn.setObjectName(u"watchListBtn")
        self.watchListBtn.setMinimumSize(QSize(32, 32))
        self.watchListBtn.setMaximumSize(QSize(195, 32))
        self.watchListBtn.setLayoutDirection(Qt.RightToLeft)
        self.watchListBtn.setIcon(icon)
        self.watchListBtn.setIconSize(QSize(32, 32))
        self.watchListBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_23.addWidget(self.watchListBtn, 0, Qt.AlignLeft)


        self.verticalLayout_24.addWidget(self.watcListFrame, 0, Qt.AlignTop)


        self.verticalLayout_18.addWidget(self.rightMenuSubContainer, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout_5.addWidget(self.rightMenuContainer)


        self.horizontalLayout.addWidget(self.centerContainer)


        self.verticalLayout.addWidget(self.mainContainer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuBtn.setText("")
        self.devicesMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Devices", None))
        self.paramsMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.loggingMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Logging", None))
        self.utilsMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Utilits", None))
        self.minimizeBtn.setText("")
        self.maximizeBtn.setText("")
        self.closeBtn.setText("")
        self.addDeviceMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Add devices", None))
        self.deleteDeviceMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Delete devices", None))
        self.ipAddrMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"IP addresses", None))
        self.readParamMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Read parameters", None))
        self.writeParamMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Write parameters", None))
        self.setDefaultMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Factory settings", None))
        self.poaramListMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Parameters list", None))
        self.saveLogMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Save log data", None))
        self.dataLogCfgMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Data logging settings", None))
        self.watchListMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Watch list", None))
        self.rtcMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Set real-time clock", None))
        self.passwordMenuBtn_2.setText(QCoreApplication.translate("MainWindow", u"Set password", None))
        self.firmwareMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Firmware update", None))
        self.calibrationMenuBtn.setText(QCoreApplication.translate("MainWindow", u"Device calibration", None))
        self.projectLabel.setText(QCoreApplication.translate("MainWindow", u"Project: @ProjectName@", None))
        self.devIcon.setText("")
        self.deviceName.setText(QCoreApplication.translate("MainWindow", u"MY210-501", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ID: 88888888888888888", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"IP: 255.255.255.255", None))
        self.devIcon_2.setText("")
        self.deviceName_2.setText(QCoreApplication.translate("MainWindow", u"MY210-501", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ID: 88888888888888888", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"IP: 255.255.255.255", None))
        self.devIcon_3.setText("")
        self.deviceName_3.setText(QCoreApplication.translate("MainWindow", u"MY210-501", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"ID: 88888888888888888", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"IP: 255.255.255.255", None))
        self.devIcon_4.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Click here to add", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"new device", None))
        self.scrollDevListBtn.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Hello!!!", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Nothing to show here", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"To get started, click \"Add device\" in the device panel", None))
        self.factoryPic.setText("")
        self.readParamMenuBtn_3.setText(QCoreApplication.translate("MainWindow", u"Read all", None))
        self.writeParamMenuBtn_3.setText(QCoreApplication.translate("MainWindow", u"Write changed", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"Write all", None))
        self.setDefaultMenuBtn_3.setText(QCoreApplication.translate("MainWindow", u"Reset to default", None))
        self.deviceInfoBtn.setText(QCoreApplication.translate("MainWindow", u"Device Information", None))
        self.paramListBtn.setText(QCoreApplication.translate("MainWindow", u"Parameter list", None))
        self.setRtcBtn.setText(QCoreApplication.translate("MainWindow", u"Real-time clock", None))
        self.setPasswordBtn.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.calibDeviceBtn.setText(QCoreApplication.translate("MainWindow", u"Calibration", None))
        self.saveLogBtn.setText(QCoreApplication.translate("MainWindow", u"Save log data", None))
        self.configLogBtn.setText(QCoreApplication.translate("MainWindow", u"Logging configuration", None))
        self.firmwareUpdBtn.setText(QCoreApplication.translate("MainWindow", u"Firmware update", None))
        self.rebootDeviceBtn.setText(QCoreApplication.translate("MainWindow", u"Reboot device", None))
        self.watchListBtn.setText(QCoreApplication.translate("MainWindow", u"Watch list", None))
    # retranslateUi

