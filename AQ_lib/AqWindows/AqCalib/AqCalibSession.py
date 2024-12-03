


class AqCalibSession(object):

    def __init__(self, user_settings, pins):
        super().__init__()
        self.saved_coeffs = dict()
        self.new_coeffs = dict()
        self.error_coeffs = dict()

        self.user_settings = user_settings

        self.session_channels = pins.get_channels_by_settings(user_settings)

        self._current_ch_num = 0
        self._current_ch = self.session_channels[self._current_ch_num]
        self.image = pins.get_image(user_settings)
        self._ch_steps = dict()

        for channel in self.session_channels:
            ch_steps = list()
            for i in range(len(channel.points)):
                step_point_settings = dict()
                step_point_settings['step'] = i + 1
                step_point_settings['steps_count'] = len(channel.points)
                step_point_settings['name'] = channel.name
                step_point_settings['point'] = channel.points[i]
                step_point_settings['unit'] = pins.get_unit(user_settings)
                ch_steps.append(step_point_settings)


            sub_dict = {'cur_point_num': 0, 'point_list': ch_steps}
            self._ch_steps[channel] = sub_dict

    def update_cur_ch(self, num=None):
        if num is None:
            if (self._current_ch_num + 1) < len(self.session_channels):
                self._current_ch_num += 1
                self._current_ch = self.session_channels[self._current_ch_num]
                return True
            else:
                self._current_ch_num = 0
                self._current_ch = self.session_channels[self._current_ch_num]
                return False
        else:
            if 0 <= num < len(self.session_channels):
                self._current_ch = self.session_channels[num]
                return True
            else:
                return False

    def get_cur_channel(self):
        return self._current_ch

    def update_cur_step(self):
        cur_ch_steps = self._ch_steps[self._current_ch]
        if (cur_ch_steps['cur_point_num'] + 1) < len(cur_ch_steps['point_list']):
            cur_ch_steps['cur_point_num'] += 1
            return True
        else:
            cur_ch_steps['cur_point_num'] = 0
            return False

    def get_cur_step(self):
        return self._ch_steps[self._current_ch]

    def get_step_ui_settings(self):
        cur_ch_steps = self._ch_steps[self._current_ch]
        return cur_ch_steps['point_list'][cur_ch_steps['cur_point_num']]

    def activate_next_step(self):
        result = True
        if not self.update_cur_step():
            result = self.update_cur_ch()

        return result

    def accept_measured_point(self, value):
        channel = self.get_cur_channel()
        if channel.calib_param_value.value_type == 'UInteger':
            value = int(value)

        cur_step = self.get_cur_step()
        cur_step['point_list'][cur_step['cur_point_num']]['measured_value'] = value

    def make_calculation(self):
        x_list = list()
        y_list = list()
        for channel in self.session_channels:
            formula_func = channel.formula_func
            ch_step = self._ch_steps[channel]
            x_list.clear()
            y_list.clear()
            for i in range(len(ch_step['point_list'])):
                if self.user_settings['_pinType'] == 'outputs':
                    y_list.append(ch_step['point_list'][i]['point'])
                    x_list.append(ch_step['point_list'][i]['measured_value'])

            self.new_coeffs[channel] = formula_func(x_list, y_list)
            keys = self.new_coeffs[channel].keys()
            err_dict = dict()
            for key in keys:
                ch_coeff = None
                for coeff in channel.coeffs:
                    if coeff.name == key:
                        ch_coeff = coeff
                        break

                if ch_coeff.min_value <\
                        self.new_coeffs[channel][ch_coeff.name]['value']\
                        < ch_coeff.max_value:
                    err_dict[ch_coeff.name] = False
                else:
                    err_dict[ch_coeff.name] = True

            self.error_coeffs[channel] = err_dict

    def get_calib_result(self):
        ch_list = list()

        for channel in self.session_channels:
            ch_dict = dict()
            ch_dict['name'] = channel.name
            ch_dict['coeff'] = self.new_coeffs[channel]

            keys = ch_dict['coeff'].keys()

            for key in keys:
                coeff_dict = ch_dict['coeff'][key]
                coeff_dict['coeff_error'] = self.error_coeffs[channel][key]

            ch_list.append(ch_dict)

        return ch_list

    def get_available_to_write_coeffs(self):
        available_channels = list()
        for s_channel in self.session_channels:
            coeffs = s_channel.coeffs
            err_flag = False
            for coeff in coeffs:
                err_flag = err_flag or self.error_coeffs[s_channel][coeff.name]

            if err_flag is False:
                available_channels.append({'channel': s_channel, 'new_value': self.new_coeffs[s_channel]})

        return available_channels


