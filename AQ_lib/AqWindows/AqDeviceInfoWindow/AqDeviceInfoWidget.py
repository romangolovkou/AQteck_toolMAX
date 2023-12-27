import random
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QLineEdit, QFormLayout

from AqWindowTemplate import AqDialogTemplate
from DeviceModels import AqDeviceInfoModel
from AqCustomDialogWindow import QDialog, loadDialogJsonStyle


class AqDeviceInfoWidget(AqDialogTemplate):
    """
    Widget require ui.generalInfoFrame and ui.operatingInfoFrame for work
    Check names at your generated Ui
    """

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Device info'
        # loadDialogJsonStyle(self, self.ui)
        self.generalTextEditors = list()
        self.operatingTextEditors = list()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.generalInfoWidgets = list()
        # getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())

        if not hasattr(self.ui, 'generalInfoLayout') or \
                not hasattr(self.ui, 'operatingInfoLayout'):
            raise Exception('AqDeviceInfoWidgetError: no frames to show info')

    def set_device_info_model(self, model: AqDeviceInfoModel):
        i = 1
        for item in model.general_info:
            line_edit = QLineEdit(self.ui.generalInfoFrame)
            line_edit.isReadOnly = True
            line_edit.setText(item['info_str'])
            self.ui.generalInfoLayout.setWidget(i, QFormLayout.LabelRole, line_edit)
            line_edit = QLineEdit(self.ui.generalInfoFrame)
            line_edit.isReadOnly = True
            line_edit.setText(item['info_value'])
            self.ui.generalInfoLayout.setWidget(i, QFormLayout.FieldRole, line_edit)
            i += 1

    def set_device_info_model(self):
        rowCnt1 = random.randint(2, 10)
        rowCnt2 = random.randint(2, 10)

        for i in range(1, rowCnt1):
            line_edit = QLineEdit(self.ui.operatingInfoFrame)
            line_edit.isReadOnly = True
            line_edit.setText("Generated string "+str(i))
            self.ui.generalInfoLayout.setWidget(i, QFormLayout.LabelRole, line_edit)
            line_edit = QLineEdit(self.ui.generalInfoFrame)
            line_edit.isReadOnly = True
            line_edit.setText("Generated string "+str(i))
            self.ui.generalInfoLayout.setWidget(i, QFormLayout.FieldRole, line_edit)

        for i in range(1, rowCnt2):
            line_edit = QLineEdit(self.ui.operatingInfoFrame)
            line_edit.isReadOnly = True
            line_edit.setText("Generated string "+str(i))
            self.ui.operatingInfoLayout.setWidget(i, QFormLayout.LabelRole, line_edit)
            line_edit = QLineEdit(self.ui.operatingInfoFrame)
            line_edit.isReadOnly = True
            line_edit.setText("Generated string "+str(i))
            self.ui.operatingInfoLayout.setWidget(i, QFormLayout.FieldRole, line_edit)

        self.ui.generalInfoLayout.parent().adjustSize()
        self.ui.operatingInfoLayout.parent().adjustSize()
        self.adjustSize()




# class AqDeviceInfoDialog(QDialog, AqDeviceInfoWidget):
#
#     def __init__(self, _ui, parent=None):
#         # AqDeviceInfoWidget.__init__(self, _ui)
#         QDialog.__init__(self, _ui)
