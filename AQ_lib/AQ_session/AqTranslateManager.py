from PySide6.QtCore import QObject, QTranslator, Signal

from AqMessageManager import AqMessageManager


class AqTranslateManager(QObject):

    _current_lang = 'UA'

    _available_langs = {'EN', 'UA'}

    _translator = None
    _app = None

    _retranslate_subscribers = list()

    @classmethod
    def init(cls, app):
        cls._app = app
        cls._translator = QTranslator(app)
        if cls._translator.load(f'translate/{cls._current_lang.lower()}.qm'):
            app.installTranslator(cls._translator)

    @classmethod
    def set_current_lang(cls, lang='EN'):
        if lang in cls._available_langs:
            cls._current_lang = lang
            if cls._translator.load(f'translate/{cls._current_lang.lower()}.qm'):
                cls._app.installTranslator(cls._translator)

            for subcriber in cls._retranslate_subscribers:
                subcriber()

    @classmethod
    def subscribe(cls, retrans_method):
        cls._retranslate_subscribers.append(retrans_method)
