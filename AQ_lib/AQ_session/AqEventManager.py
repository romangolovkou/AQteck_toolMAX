from PySide6.QtCore import QObject


class AqEventManager(object):

    _event_handlers = {}

    @classmethod
    def register_event_handler(cls, event_name, handler, approve_duplicate=False):
        if event_name not in cls._event_handlers:
            cls._event_handlers[event_name] = set()

        if approve_duplicate is False:
            function_name = handler.__name__
            for existing_handler in cls._event_handlers[event_name]:
                if existing_handler.__name__ == function_name:
                    cls._event_handlers[event_name].remove(existing_handler)
                    cls._event_handlers[event_name].add(handler)
                    return False  # Обработчик с таким именем уже зарегистрирован

        cls._event_handlers[event_name].add(handler)

    @classmethod
    def unregister_event_handler(cls, event_name, handler):
        handlers = cls._event_handlers.get(event_name, set())
        if handler in handlers:
            handlers.remove(handler)

    @classmethod
    def emit_event(cls, event_name, *args, **kwargs):
        handlers = cls._event_handlers.get(event_name, set())
        for handler in handlers:
            handler(*args, **kwargs)
