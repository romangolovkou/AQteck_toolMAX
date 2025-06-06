from dataclasses import dataclass

from AqCalibParamSetting import AqCalibParamSetting
from AqCalibSession import AqCalibSession
from AqParamCalibCom import Com
from AqSubCalibrator import AqSubCalibrator


class AqCalibrator(object):

    def __init__(self, data, loc_data, dev_mode):
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

        if 'init_cfg' in data:
            self.init_cfg_params = list()
            for setting in data['init_cfg']:
                self.init_cfg_params.append(AqCalibParamSetting(setting))

        if 'inputs' in data:
            self.Inputs = AqSubCalibrator(data['inputs'], loc_data, dev_mode)
        if 'outputs' in data:
            self.Outputs = AqSubCalibrator(data['outputs'], loc_data, dev_mode)

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

    def init_calib_device_config(self):
        result = True
        if hasattr(self, 'init_cfg_params'):
            for param in self.init_cfg_params:
                result &= self.device.write_calib_param(param.register, param.value)

        return result

    def pre_ch_calib_func(self, user_settings):
        cur_step = self.calib_session.get_cur_step()
        cur_channel = self.calib_session.get_cur_channel()
        if cur_step['cur_point_num'] == 0:
            if not self.save_channel_coeffs(cur_channel):
                return False
            if not self.set_ch_def_coeffs(cur_channel):
                return False

        if user_settings['_pinType'] == 'outputs':
            point_value = cur_step['point_list'][cur_step['cur_point_num']]['point']
            if not self.set_ch_out_value(cur_channel, point_value):
                return False
        elif user_settings['_pinType'] == 'inputs':
            if not self.set_ch_cfg(cur_channel):
                return False

        return True

    def post_ch_calib_func(self):
        cur_channel = self.calib_session.get_cur_channel()
        return self.set_saved_cur_ch_cfg(cur_channel)

    def save_channel_coeffs(self, channel):
        coeffs = channel.coeffs
        ch_dict = dict()
        # збереження поточних коєфіцієнтів
        for coeff in coeffs:
            access_code = coeff.get_access_code()
            cur_coefficient = self.device.read_calib_coeff(access_code.param1,
                                                           access_code.param2,
                                                           access_code.param3)

            if cur_coefficient is False:
                return False

            ch_dict[coeff.name] = cur_coefficient

        self.calib_session.saved_coeffs[channel] = ch_dict
        return True

    def set_ch_def_coeffs(self, channel):
        result = False
        coeffs = channel.coeffs
        for coeff in coeffs:
            access_code = coeff.get_access_code()
            result = self.device.write_calib_coeff(access_code.param1,
                                                   access_code.param2,
                                                   access_code.param3,
                                                   coeff.def_value)
            if result is False:
                return False

        return result

    def set_ch_cfg(self, channel):
        result = True
        self.calib_session.saved_cfg_params_values = dict()
        channel_cfg_params = channel.get_all_ch_cfg_params
        for param in channel_cfg_params:
            self.calib_session.saved_cfg_params_values[param] = self.device.read_calib_param(param.register)
            result &= self.device.write_calib_param(param.register, param.value)

        return result

    def set_saved_cur_ch_cfg(self, channel):
        result = True
        channel_cfg_params = channel.get_all_ch_cfg_params
        for param in channel_cfg_params:
            value = self.calib_session.saved_cfg_params_values[param]
            result &= self.device.write_calib_param(param.register, value)

        return result

    def set_ch_out_value(self, channel, value):
        result = True
        self.set_ch_cfg(channel)
        calib_param_value = channel.calib_param_value
        result &= self.device.write_calib_param(calib_param_value.register, value)

        return result

    def get_cur_ch_value(self):
        cur_channel = self.calib_session.get_cur_channel()
        calib_param_value = cur_channel.calib_param_value
        value = self.device.read_calib_param(calib_param_value.register)
        if isinstance(value, (int, float)):
            return value
        else:
            return False

    def set_ch_saved_coeffs(self, channel):
        result = False
        coeffs = channel.coeffs
        for coeff in coeffs:
            try:
                value = self.calib_session.saved_coeffs[channel][coeff.name]
                access_code = coeff.get_access_code()
                result = self.device.write_calib_coeff(access_code.param1,
                                                       access_code.param2,
                                                       access_code.param3,
                                                       value)
                if result is False:
                    return False
            except:
                print('not have saved value for channel')

        return result

    def write_new_coeffs(self):
        wr_channels = self.calib_session.get_available_to_write_channels()

        for channel in wr_channels:
            coeffs = channel['channel'].coeffs
            for coeff in coeffs:
                access_code = coeff.get_access_code()
                result = self.device.write_calib_coeff(access_code.param1,
                                                       access_code.param2,
                                                       access_code.param3,
                                                       channel['new_value'][coeff.name]['value'])
                if result is False:
                    return False

        return True

    def accept_measured_value(self, value):
        return self.calib_session.accept_measured_value(value)

    def accept_measured_point(self, value):
        self.calib_session.accept_measured_point(value)

    def make_calculation(self):
        self.calib_session.make_calculation()

    def return_saved_coeffs(self):
        for channel in self.calib_session.session_channels:
            self.set_ch_saved_coeffs(channel)

    def clear_session_cash(self):
        self.calib_session.clear_calib_cash()


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




