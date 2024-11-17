


class AqCalibSession(object):

    def __init__(self, user_settings, pins):
        super().__init__()

        self.session_channels = pins.get_channels_by_settings(user_settings)

        self._current_ch_num = 0
        self._current_ch = self.session_channels[self._current_ch_num]
        self.image = pins.get_image(user_settings)

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
