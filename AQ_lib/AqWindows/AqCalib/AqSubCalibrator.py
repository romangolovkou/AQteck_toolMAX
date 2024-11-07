from AqSensors import AqSensors


class AqSubCalibrator(object):

    def __init__(self, data, loc_data):
        super().__init__()
        self._name = loc_data[data['name'][4:]]
        if not isinstance(self.name, str):
            raise TypeError('SubCalibrator.name is not str')

        self.Sensors = AqSensors(data['sensors'], loc_data)

    def get_ui_settings(self):
        return self.Sensors.get_ui_settings()

    @property
    def name(self):
        return self._name

