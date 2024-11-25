from AqCalibAlg import AqCalibAlg
from AqCalibParamSetting import AqCalibParamSetting, AqCalibParamSignal


class AqCalibChannel(object):
    def __init__(self, data, loc_data):
        self._name = loc_data[data['name']['name'][4:]]
        if not isinstance(self._name, str):
            raise TypeError('CalibChannel.name is not str')

        self._ch_number = data['name']['value']
        if not isinstance(self._ch_number, int):
            raise TypeError('CalibChannel.ch_number is not int')

        settings_data = data['settings']
        for setting in settings_data:
            if setting['type'] == 'SensorType':
                self._parameter_type = AqCalibParamSetting(setting)
            elif setting['type'] == 'AinL':
                self._parameter_min_limit = AqCalibParamSetting(setting)
            elif setting['type'] == 'AinH':
                self._parameter_max_limit = AqCalibParamSetting(setting)
            elif setting['type'] == 'Signal':
                self._parameter_value = AqCalibParamSetting(setting)

        if data.get('signal', False) and not hasattr(self, '_parameter_value'):
            self._parameter_value = AqCalibParamSignal(data['signal'])

        self.calAlg = AqCalibAlg(data['calAlg'])

    @property
    def name(self):
        return self._name + ' ' + str(self._ch_number)

    @property
    def points(self):
        return self.calAlg.points

    @property
    def formula(self):
        return self.calAlg.formula

    @property
    def access_code(self):
        return self.calAlg.access_code

    @property
    def coeffs(self):
        return self.calAlg.coeffs

    @property
    def calib_param_type(self):
        return self._parameter_type

    @property
    def calib_param_value(self):
        return self._parameter_value

