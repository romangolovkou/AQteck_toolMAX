import threading

from PySide2.QtCore import QObject


class AQ_EventManager(QObject):

    _global_instance = None

    def __init__(self):
        super().__init__()
        self._event_handlers = {}
        self._lock = threading.RLock()

    def register_event_handler(self, event_name, handler, approve_duplicate=False):
        with self._lock:
            if event_name not in self._event_handlers:
                self._event_handlers[event_name] = set()

            if approve_duplicate is False:
                function_name = handler.__name__
                for existing_handler in self._event_handlers[event_name]:
                    if existing_handler.__name__ == function_name:
                        self._event_handlers[event_name].remove(existing_handler)
                        self._event_handlers[event_name].add(handler)
                        return False  # Обработчик с таким именем уже зарегистрирован

            self._event_handlers[event_name].add(handler)

    def unregister_event_handler(self, event_name, handler):
        with self._lock:
            handlers = self._event_handlers.get(event_name, set())
            if handler in handlers:
                handlers.remove(handler)

    def emit_event(self, event_name, *args, **kwargs):
        with self._lock:
            handlers = self._event_handlers.get(event_name, set())
            for handler in handlers:
                handler(*args, **kwargs)

    @staticmethod
    def get_global_event_manager():
        # Статический метод для получения или создания единственного экземпляра класса
        if AQ_EventManager._global_instance is None:
            AQ_EventManager._global_instance = AQ_EventManager()
        return AQ_EventManager._global_instance
