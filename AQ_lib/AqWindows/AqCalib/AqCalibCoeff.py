from dataclasses import dataclass

from AqParamCalibCom import Com


@dataclass
class CalibAccessCode:
    param1: int
    param2: int
    param3: int

    def __post_init__(self):
        # Проверка диапазона
        if not (0 <= self.param1 <= 32):  # Замените диапазон на нужный
            raise ValueError("AccessCode.param1 must be between 0 and 32")

        # Проверка диапазона
        if not (0 <= self.param2 <= 32):  # Замените диапазон на нужный
            raise ValueError("AccessCode.param2 must be between 0 and 32")

        # Проверка диапазона
        if not (0 <= self.param3 <= 32):  # Замените диапазон на нужный
            raise ValueError("AccessCode.param3 must be between 0 and 32")


class AqCalibCoeffRuleParam(object):
    def __init__(self, data):
        if isinstance(data['valueType'], str):
            self.valueType = data['valueType']
        else:
            raise TypeError('CalibCoeffRuleParam.valueType is not str')

        self.Com = Com(isLittleEndianWords=data['com']['isLittleEndianWords'],
                       length=data['com']['length'],
                       register=data['com']['register'],
                       writeCommand=data['com']['writeCommand'])


class AqCalibCoeffAccessRule(object):
    def __init__(self, data):
        if isinstance(data['type'], str):
            self.rule_type = data['type']
        else:
            raise TypeError('CalibCoeffAccessRule.rule_type is not str')

        if isinstance(data['valueType'], str):
            self.valueType = data['valueType']
        else:
            raise TypeError('CalibCoeffAccessRule.valueType is not str')

        self.Com = Com(isLittleEndianWords=data['com']['isLittleEndianWords'],
                       length=data['com']['length'],
                       register=data['com']['register'],
                       writeCommand=data['com']['writeCommand'])


class AqCalibCoeff(object):
    def __init__(self, data):
        if data['name'] == 'a' or data['name'] == 'b' or\
                data['name'] == 'c' or data['name'] == 'k':
            self._name = data['name']
        else:
            raise ValueError("Coeff name must be a or b or c or k")

        try:
            defValue = float(data['defValue'])
            minValue = float(data['minValue'])
            maxValue = float(data['maxValue'])
        except:
            raise Exception('CalibCoeff defValue or minValue or maxValue is not float')

        if not (minValue < defValue < maxValue):
            raise ValueError("Coeff min max def somethink wrong")

        self._defValue = defValue
        self._minValue = minValue
        self._maxValue = maxValue
        #TODO: error - допустипая погрешность в процентах сделать потом,
        # как будет понятно для чего это
        self.error = data['error']

        self.accessRule = AqCalibCoeffAccessRule(data['accessRule'])
        self.accessParam = AqCalibCoeffRuleParam(data['accessRule']['accessParam'])
        self.accessCode = CalibAccessCode(data['accessRule']['accessParam']['accessCode']['param1'],
                                          data['accessRule']['accessParam']['accessCode']['param2'],
                                          data['accessRule']['accessParam']['accessCode']['param3'])

    def get_access_code(self):
        return self.accessCode

    @property
    def name(self):
        return self._name

    @property
    def def_value(self):
        return self._defValue

    @property
    def min_value(self):
        return self._minValue

    @property
    def max_value(self):
        return self._maxValue

