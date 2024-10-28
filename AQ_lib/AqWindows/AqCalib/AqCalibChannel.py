from AqCalibAlg import AqCalibAlg
from AqCalibParamSetting import AqCalibParamSetting, AqCalibParamSignal


class AqCalibChannel(object):
    def __init__(self, data, loc_data):
        self.name = loc_data[data['name']['name'][4:]]
        if not isinstance(self.name, str):
            raise TypeError('CalibChannel.name is not str')

        self.ch_number = data['name']['value']
        if not isinstance(self.ch_number, int):
            raise TypeError('CalibChannel.ch_number is not int')

        settings_data = data['settings']
        for setting in settings_data:
            if setting['type'] == 'SensorType':
                self.parameter_type = AqCalibParamSetting(setting)
            elif setting['type'] == 'AinL':
                self.parameter_min_limit = AqCalibParamSetting(setting)
            elif setting['type'] == 'AinH':
                self.parameter_max_limit = AqCalibParamSetting(setting)

        self.parameter_value = AqCalibParamSignal(data['signal'])
        self.calAlg = AqCalibAlg(data['calAlg'])


