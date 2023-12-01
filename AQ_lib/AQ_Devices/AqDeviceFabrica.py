
class DeviceCreator(object):
    event_manager = None
    @classmethod
    def init(cls, _event_manager):
        cls.event_manager = _event_manager

    @classmethod
    def from_settings(cls, connect_settings, device_type):
