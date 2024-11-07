from AqCalibChannel import AqCalibChannel


class AqSensors(object):
    def __init__(self, data, loc_data):
        super().__init__()
        for sensor_data in data:
            if sensor_data['name'] == 'U':
                self.VoltageSensor = AqSensor(sensor_data, loc_data)
            if sensor_data['name'] == 'I':
                self.CurrentSensor = AqSensor(sensor_data, loc_data)
            if sensor_data['name'] == 'R':
                self.ResistanceSensor = AqSensor(sensor_data, loc_data)
            if sensor_data['name'] == 'TCJ':
                self.ColdJunctionSensor = AqSensor(sensor_data, loc_data)

    def get_ui_settings(self):
        ui_settings = dict()
        ui_settings['sensors'] = list()

        if hasattr(self, 'VoltageSensor'):
            ui_settings['sensors'].append(self.VoltageSensor.fullName)
            ui_settings[self.VoltageSensor.fullName] = self.VoltageSensor.get_ui_settings()
        if hasattr(self, 'CurrentSensor'):
            ui_settings['sensors'].append(self.CurrentSensor.fullName)
            ui_settings[self.CurrentSensor.fullName] = self.CurrentSensor.get_ui_settings()
        if hasattr(self, 'ResistanceSensor'):
            ui_settings['sensors'].append(self.ResistanceSensor.fullName)
            ui_settings[self.ResistanceSensor.fullName] = self.ResistanceSensor.get_ui_settings()
        if hasattr(self, 'ColdJunctionSensor'):
            ui_settings['sensors'].append(self.ColdJunctionSensor.fullName)
            ui_settings[self.ColdJunctionSensor.fullName] = self.ColdJunctionSensor.get_ui_settings()

        return  ui_settings

class AqSensor(object):
    def __init__(self, data, loc_data):
        super().__init__()
        self.name = data['name']
        if not isinstance(self.name, str):
            raise TypeError('Sensor.name is not str')

        self.fullName = loc_data[data['fullName'][4:]]
        if not isinstance(self.fullName, str):
            raise TypeError('Sensor.fullName is not str')

        self.images = data['images']

        self.lowLimit = data.get('lowLimit', None)
        if self.lowLimit is not None and not isinstance(self.lowLimit, int):
            raise TypeError('Sensor.lowLimit is not int')

        self.maxLimit = data.get('maxLimit', None)
        if self.maxLimit is not None and not isinstance(self.maxLimit, int):
            raise TypeError('Sensor.maxLimit is not int')

        self.unit = loc_data[data['unit'][4:]]
        if not isinstance(self.unit, str):
            raise TypeError('Sensor.unit is not str')

        self.channels = list()
        channels_data = data['channels']
        for channel in channels_data:
            self.channels.append(AqCalibChannel(channel, loc_data))

    def get_ui_settings(self):
        ui_settings = list()

        for channel in self.channels:
            ch_name = channel.name + ' ' + str(channel.ch_number)
            ui_settings.append(ch_name)

        return ui_settings


