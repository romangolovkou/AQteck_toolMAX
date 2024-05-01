from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QCheckBox, QLabel, QLineEdit, QWidget

from AqTranslateManager import AqTranslateManager


class AqScanCheckBoxFrame(QFrame):
    clicked_signal = Signal()
    def __init__(self, parent):
        super().__init__(parent)
        self.child_buttons = None
        self.warning_label = QLabel(AqTranslateManager.tr('Check something!'), self.parent())
        self.warning_label.setStyleSheet("color: #fe2d2d; \n")
        self.warning_label.setFixedSize(100, 20)
        self.warning_label.hide()

    def prepare_ui(self):
        self.child_buttons = self.findChildren(QCheckBox)

        for child_btn in self.child_buttons:
            child_btn.clicked.connect(self.check_buttons_selected)

    @property
    def checkedCount(self):
        checked_count = 0
        for child_btn in self.child_buttons:
            if child_btn.isChecked():
                checked_count += 1

        return checked_count

    def check_buttons_selected(self):
        have_checked = False
        if self.checkedCount > 0:
            have_checked = True

        if have_checked is False:
            self.show_warning()
        else:
            self.hide_warning()

        self.clicked_signal.emit()

    def show_warning(self):
        rect = self.geometry()
        pos = self.mapTo(self, rect.topRight())
        self.warning_label.move(pos.x() - 105, pos.y())
        self.warning_label.show()

    def hide_warning(self):
        self.warning_label.hide()

class AqScanSlaveIDFrame(QFrame):
    changed_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.startLineEdit = None
        self.endLineEdit = None
        self.slaveIdWarningMsgLabel = None
        self.warning_label = QLabel(AqTranslateManager.tr('End address cannot be less than start address!'), self)
        self.warning_label.setStyleSheet("color: #fe2d2d; \n")
        self.warning_label.setFont(QFont('Segoe UI', 10))
        self.warning_label.setFixedSize(250, 20)
        self.warning_label.move(10, 55)
        self.warning_label.hide()

    def prepare_ui(self):
        self.startLineEdit = self.findChildren(QLineEdit, 'startLineEdit')[0]
        self.endLineEdit = self.findChildren(QLineEdit, 'endLineEdit')[0]

        self.startLineEdit.textChanged.connect(self.line_edit_changed)
        self.endLineEdit.textChanged.connect(self.line_edit_changed)

    @property
    def addressRange(self):
        start = self.startLineEdit.text()
        end = self.endLineEdit.text()
        if start != '' and end != '':
            address_range = (int(end) + 1) - int(start)
            if address_range < 1:
                address_range = 0
        else:
            address_range = 0
        return address_range

    def line_edit_changed(self):
        start = self.startLineEdit.text()
        end = self.endLineEdit.text()
        if start != '' and end != '':
            if int(start) > int(end):
                self.show_warning()
            else:
                self.hide_warning()

        self.changed_signal.emit()

    def show_warning(self):
        self.warning_label.show()

    def hide_warning(self):
        self.warning_label.hide()


class AqScanNetworkSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def prepare_ui(self):
        self.boudrate_frame = self.findChildren(AqScanCheckBoxFrame, 'boudrateFrame')[0]
        self.parity_frame = self.findChildren(AqScanCheckBoxFrame, 'parityFrame')[0]
        self.stopbits_frame = self.findChildren(AqScanCheckBoxFrame, 'stopbitsFrame')[0]
        self.slave_id_frame = self.findChildren(AqScanSlaveIDFrame, 'slaveIdFrame')[0]

        self.boudrate_frame.prepare_ui()
        self.parity_frame.prepare_ui()
        self.stopbits_frame.prepare_ui()
        self.slave_id_frame.prepare_ui()

        self.boudrate_frame.clicked_signal.connect(self.setting_changed)
        self.parity_frame.clicked_signal.connect(self.setting_changed)
        self.stopbits_frame.clicked_signal.connect(self.setting_changed)
        self.slave_id_frame.changed_signal.connect(self.setting_changed)

        self.user_message_label = QLabel('', self.slave_id_frame)
        self.user_message_label.setStyleSheet("color: #D0D0D0; \n")
        self.user_message_label.setFont(QFont('Segoe UI', 10))
        self.user_message_label.setFixedSize(300, 20)
        self.user_message_label.move(10, 55)

    def setting_changed(self):
        # Тимчасовий хардкод у 3 секунди отриманий фактичним заміром часі
        second_per_range = 3
        boudrate_range = self.boudrate_frame.checkedCount
        parity_range = self.parity_frame.checkedCount
        stopbits_range = self.stopbits_frame.checkedCount
        address_range = self.slave_id_frame.addressRange

        total_range = boudrate_range * parity_range * \
                      stopbits_range * address_range

        expected_time = total_range * second_per_range

        if expected_time > 0:
            hours = expected_time // 3600
            remaining_seconds = expected_time % 3600
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            if hours > 0:
                self.user_message_label.setText(AqTranslateManager.tr("Possible search time") +
                                                f' {hours} ' + AqTranslateManager.tr("hours") +
                                                f' {minutes} ' + AqTranslateManager.tr('minutes') +
                                                f' {seconds} ' + AqTranslateManager.tr('seconds'))
            elif minutes > 0:
                self.user_message_label.setText(AqTranslateManager.tr("Possible search time") +
                                                f' {minutes} ' + AqTranslateManager.tr('minutes') +
                                                f' {seconds} ' + AqTranslateManager.tr('seconds'))
            elif seconds > 0:
                self.user_message_label.setText(AqTranslateManager.tr("Possible search time") +
                                                f' {seconds} ' + AqTranslateManager.tr('seconds'))

            self.user_message_label.setStyleSheet("color: #D0D0D0; \n")
            self.user_message_label.show()
        else:
            self.user_message_label.hide()

    def show_not_found_error(self):
        self.user_message_label.setStyleSheet("color: #fe2d2d; \n")
        self.user_message_label.setText(AqTranslateManager.tr("Not match anything"))
