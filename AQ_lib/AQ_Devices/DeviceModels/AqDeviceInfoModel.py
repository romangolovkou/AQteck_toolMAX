class AqDeviceInfoModel:

    def __init__(self):
        super().__init__()
        self.general_info = []
        self.operating_params_info = []

    def add_general_info(self, info_str, info_value):
        self.general_info.append({'info_str': info_str, 'info_value': info_value})

    def add_operating_info(self, info_str, info_value, editor):
        self.operating_params_info.append({'info_str': info_str, 'info_value': info_value, 'item': editor})

    def clear(self):
        self.general_info.clear()
        self.operating_params_info.clear()

