from dataclasses import dataclass

from AqParamCalibCom import Com
from AqSubCalibrator import AqSubCalibrator


class AqCalibrator(object):

    def __init__(self, data, loc_data):
        super().__init__()
        self.protocol = data['protocol']
        if not isinstance(self.protocol, str):
            raise TypeError('Calibrator.protocol is not str')

        data_dev_name = data['devName']
        loc_key = data['devName']['value'][4:]
        self.DevName = DevName(loc_data[loc_key],
                               data_dev_name['valueType'],
                               Com(isLittleEndianWords=data_dev_name['com']['isLittleEndianWords'],
                                   length=data_dev_name['com']['length'],
                                   register=data_dev_name['com']['register'],
                                   readCommand=data_dev_name['com']['readCommand']
                                   ))

        self.timeout = data['timeout']['value']
        if not isinstance(self.timeout, int):
            raise TypeError('Calibrator.timeout is not int')

        if 'inputs' in data:
            self.Inputs = AqSubCalibrator(data['inputs'], loc_data)

        x = list()





@dataclass
class DevName:
    value: str
    valueType: str
    com: Com

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError('Calibrator.protocol is not str')

        if not isinstance(self.valueType, str):
            raise TypeError('Calibrator.protocol is not str')




