from dataclasses import dataclass

from AqCalibSession import AqCalibSession
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
        if 'outputs' in data:
            self.Outputs = AqSubCalibrator(data['outputs'], loc_data)

        self.calib_session = None
        self.device = None

    def set_calib_device(self, device):
        self.device = device

    def check_pin_type_by_name(self, name):
        if hasattr(self, 'Inputs'):
            if self.Inputs.name == name:
                return 'inputs'

        if hasattr(self, 'Outputs'):
            if self.Outputs.name == name:
                return 'outputs'

    def get_ui_settings(self):
        ui_settings = dict()
        ui_settings['pinTypes'] = list()

        if hasattr(self, 'Inputs'):
            ui_settings['pinTypes'].append(self.Inputs.name)
            ui_settings[self.Inputs.name] = self.Inputs.get_ui_settings()
        if hasattr(self, 'Outputs'):
            ui_settings['pinTypes'].append(self.Outputs.name)
            ui_settings[self.Outputs.name] = self.Outputs.get_ui_settings()

        return ui_settings

    def create_calib_session(self, user_settings):
        if user_settings['_pinType'] == 'inputs':
            pins = self.Inputs
        elif user_settings['_pinType'] == 'outputs':
            pins = self.Outputs
        else:
            raise Exception('Cant create calib session')

        self.calib_session = AqCalibSession(user_settings, pins)
        return self.calib_session

    # def make_calib_cur_step(self):


    def pre_calib_func(self, user_settings):
        if user_settings['_pinType'] == 'outputs':
            cur_step = self.calib_session.get_cur_step()
            cur_channel = self.calib_session.get_cur_channel()
            if cur_step['cur_point_num'] == 0:
                self.save_channel_coeffs(cur_channel)
                self.set_ch_def_coeffs(cur_channel)
                point_value = cur_step['point_list'][cur_step['cur_point_num']]['point']
                self.set_ch_out_value(cur_channel, point_value)


    def save_channel_coeffs(self, channel):
        coeffs = channel.coeffs
        # збереження поточних коєфіцієнтів
        for coeff in coeffs:
            access_code = coeff.get_access_code()
            cur_coefficient = self.device.read_calib_coeff(access_code.param1,
                                                           access_code.param2,
                                                           access_code.param3)
            self.calib_session.saved_coeffs[channel] = {coeff.name: cur_coefficient}

    def set_ch_def_coeffs(self, channel):
        coeffs = channel.coeffs
        for coeff in coeffs:
            access_code = coeff.get_access_code()
            result = self.device.write_calib_coeff(access_code.param1,
                                                   access_code.param2,
                                                   access_code.param3,
                                                   coeff.def_value)

    def set_ch_out_value(self, channel, value):
        calib_param_type = channel.calib_param_type
        calib_param_value = channel.calib_param_value
        result = self.device.write_calib_param(calib_param_type.register, calib_param_type.point_value)
        result = self.device.write_calib_param(calib_param_value.register, value)

    def accept_measured_point(self, value):
        channel = self.calib_session.get_cur_channel()
        if channel.calib_param_value.value_type == 'UInteger':
            value = int(value)

        cur_step = self.calib_session.get_cur_step()
        cur_step['point_list'][cur_step['cur_point_num']]['measured_value'] = value


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




