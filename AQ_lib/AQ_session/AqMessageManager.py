import threading

from PySide6.QtCore import QObject, QSize
from PySide6.QtWidgets import QStyle

from QCustomModals import QCustomModals


class AqMessageManager(QObject):

    _global_instance = None
    _subscribers = list()

    def __init__(self):
        super().__init__()

    def subscribe(self, subscriber):
        """
        Subscribe for all messages.
        :param subscriber: Must be callback-function for console mode or
        must be QObject as parent for GUI mode.
        :return:
        """
        self._subscribers.append(subscriber)

    def send_main_message(self, modal_type, descr_text: str):
        for subscriber in self._subscribers:
            subscriber(modal_type, descr_text)

    def show_message(self, parent, modal_type, descr_text: str):
        kwargs = {
            "title": modal_type,
            "description": descr_text,
            "position": 'bottom-center',
            "parent": parent,
            'closeIcon': "Icons/Close.png",
            'modalIcon': "UI/icons/AQico_silver.png",
            "isClosable": True,
            "animationDuration": 3000  # set to zero if you want you modal to not auto-close
        }

        if modal_type == "Information":
            modal = QCustomModals.InformationModal(**kwargs)
        elif modal_type == "Success":
            modal = QCustomModals.SuccessModal(**kwargs)
        elif modal_type == "Warning":
            modal = QCustomModals.WarningModal(**kwargs)
        elif modal_type == "Error":
            modal = QCustomModals.ErrorModal(**kwargs)
        elif modal_type == "Custom":
            # kwargs["modalIcon"] = self.style().standardIcon(QStyle.SP_MessageBoxQuestion).pixmap(
            #     QSize(32, 32))  # Change QSystemIcon.Warning to any desired system icon
            # kwargs[
            #     "description"] += "\n\nCustom modals need additional styling since they are transparent by default."
            modal = QCustomModals.CustomModal(**kwargs)

        # Apply CSS styling to the main window or modal parent to avoid painting over default modal style
        # set dynamic bg & icons color for custom modal to match app theme
        # if self.isDark():
        #     bg_color = "#0E1115"
        #     icons_color = "#F5F5F5"  # white
        # else:
        #     bg_color = "#F0F0F0"
        #     icons_color = "#000"  # black
        # self.setStyleSheet("""
        #     InformationModal, SuccessModal, ErrorModal, WarningModal, CustomModal{
        #         border-radius: 10px;
        #     }
        #     CustomModal{
        #         background-color: """ + bg_color + """; /* Light gray background color */
        #         color: """ + icons_color + """
        #     }
        #     CustomModal *{
        #         background-color: transparent;
        #     }
        # """)

        # Apply QGraphicsDropShadowEffect to create a shadow effect
        # shadow_effect = QGraphicsDropShadowEffect(modal)
        # shadow_effect.setBlurRadius(10)
        # shadow_effect.setColor(QColor(0, 0, 0, 150))
        # shadow_effect.setOffset(0, 0)
        # modal.setGraphicsEffect(shadow_effect)

        modal.show()

    @staticmethod
    def get_global_message_manager():
        # Статический метод для получения или создания единственного экземпляра класса
        if AqMessageManager._global_instance is None:
            AqMessageManager._global_instance = AqMessageManager()
        return AqMessageManager._global_instance
