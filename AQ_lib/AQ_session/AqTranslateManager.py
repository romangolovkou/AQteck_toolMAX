from PySide6.QtCore import QObject, QTranslator, Signal, QCoreApplication


class AqTranslateManager(QObject):

    _current_lang = 'EN'

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
        if retrans_method not in cls._retranslate_subscribers:
            cls._retranslate_subscribers.append(retrans_method)

    @classmethod
    def de_subscribe(cls, retrans_method):
        if retrans_method in cls._retranslate_subscribers:
            cls._retranslate_subscribers.remove(retrans_method)

    @classmethod
    def tr(cls, origin_text):
        translate_text = QCoreApplication.translate('Custom context', origin_text, None)
        return translate_text
