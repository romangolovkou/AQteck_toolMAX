from AqParamCalibCom import Com


class AqCalibParamSetting(object):
    def __init__(self, data):
        self.param_type = data['type']
        if not isinstance(self.param_type, str):
            raise TypeError("CalibParamSetting.param_type is not str")

        self.defValue = data['defValue']
        if not isinstance(self.defValue, int):
            raise TypeError("CalibParamSetting.defValue is not int")

        self.valueType = data['valueType']
        if not isinstance(self.valueType, str):
            raise TypeError("CalibParamSetting.valueType is not str")

        self.Com = Com(isLittleEndianWords=data['com']['isLittleEndianWords'],
                       length=data['com']['length'],
                       register=data['com']['register'],
                       readCommand=data['com']['readCommand'])


class AqCalibParamSignal(object):
    def __init__(self, data):
        self.valueType = data['valueType']
        if not isinstance(self.valueType, str):
            raise TypeError("CalibParamSignal.valueType is not str")

        self.Com = Com(isLittleEndianWords=data['com']['isLittleEndianWords'],
                       length=data['com']['length'],
                       register=data['com']['register'],
                       readCommand=data['com']['readCommand'])



