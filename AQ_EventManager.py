from PyQt5.QtCore import QObject


class AQ_EventManager(QObject):
    def __init__(self):
        super().__init__()
        self._event_handlers = {}

    def register_handler(self, event_name, handler):
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    def emit_event(self, event_name, *args, **kwargs):
        handlers = self._event_handlers.get(event_name, [])
        for handler in handlers:
            handler(*args, **kwargs)
