import threading

from PySide6.QtCore import QObject


class AqMessageManager(QObject):

    _global_instance = None

    def __init__(self):
        super().__init__()
        self._address_handlers = {}
        self._lock = threading.RLock()

    def register_address_handler(self, address, handler, approve_duplicate=False):
        with self._lock:
            if address not in self._address_handlers:
                self._address_handlers[address] = set()

            if approve_duplicate is False:
                function_name = handler.__name__
                for existing_handler in self._address_handlers[address]:
                    if existing_handler.__name__ == function_name:
                        self._address_handlers[address].remove(existing_handler)
                        self._address_handlers[address].add(handler)
                        return False  # Обработчик с таким именем уже зарегистрирован

            self._address_handlers[address].add(handler)

    def unregister_address_handler(self, address, handler):
        with self._lock:
            handlers = self._address_handlers.get(address, set())
            if handler in handlers:
                handlers.remove(handler)

    def send_message(self, address, *args, **kwargs):
        with self._lock:
            handlers = self._address_handlers.get(address, set())
            for handler in handlers:
                handler(*args, **kwargs)

    @staticmethod
    def get_global_message_manager():
        # Статический метод для получения или создания единственного экземпляра класса
        if AqMessageManager._global_instance is None:
            AqMessageManager._global_instance = AqMessageManager()
        return AqMessageManager._global_instance
