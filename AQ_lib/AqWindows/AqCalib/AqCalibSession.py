


class AqCalibSession(object):

    def __init__(self, user_settings, pins):
        super().__init__()

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
        else:
            if num < len(self.session_channels):
                self._current_ch = self.session_channels[num]

    def get_cur_channel(self):
        return self._current_ch

    def get_step_ui_settings(self):
        cur_ch_steps = self._ch_steps[self._current_ch]
        return cur_ch_steps['point_list'][cur_ch_steps['cur_point_num']]
