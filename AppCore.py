from AQ_EventManager import AQ_EventManager
from AQ_Session import AQ_CurrentSession
from AqConnectManager import AqConnectManager
from AqDeviceFabrica import DeviceCreator
from AqMessageManager import AqMessageManager
from AqWatchListCore import AqWatchListCore


class Core(object):
    event_manager = None
    session = None
    @classmethod
    def init(cls):
        cls.event_manager = AQ_EventManager.get_global_event_manager()
        cls.message_manager = AqMessageManager.get_global_message_manager()
        cls.session = AQ_CurrentSession(cls.event_manager, cls)
        AqConnectManager.init()
        DeviceCreator.init(cls.event_manager)
        AqWatchListCore.init()

    @classmethod
    def de_init(cls):
        AqConnectManager.deinit()
        AqWatchListCore.deinit()
        print('AppCore is deinit')
