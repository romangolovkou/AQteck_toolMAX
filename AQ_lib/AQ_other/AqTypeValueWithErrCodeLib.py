import struct

from AqTranslateManager import AqTranslateManager

UA_ERR_BANK = {
    0xF6000000: 'Немає даних',
    0xF7000000: 'Датчик вимкнений',
    0xF8000000: 'Занадто висока температура холодного спаю',
    0xF9000000: 'Занадто низька температура холодного спаю',
    0xFA000000: 'Обчислене значення занадто велике',
    0xFB000000: 'Обчислене значення занадто мале',
    0xFC000000: 'Коротке замикання',
    0xFD000000: 'Обрив датчика',
    0xFE000000: 'Відсутній зв’язок з АЦП',
    0xFF000000: 'Некоректний калібрувальний коефіцієнт',

    # Коди помилок обчислення float-величин
    # Більшість із них притаманні лише модулю обчислювачів, однак деякі можуть виникати
    # і в інших модулях (наприклад, у модулі виконавчих механізмів)

    0xF5000000: 'Невірна кількість входів',
    0xF5000001: 'Вхід обчислювача вимкнено',
    0xF5000002: 'Датчик, що використовується обчислювачем, вимкнений',
    0xF5000003: 'Невідповідність між датчиком і обчислювачем',
    0xF5000004: 'Фільтр, що використовується обчислювачем, вимкнений',
    0xF5000005: 'Неприпустимий формат даних фільтра RS485',
    0xF5000006: 'Низька температура сухого термометра (вологість)',
    0xF5000007: 'Висока температура сухого термометра',
    0xF5000008: 'Низька температура вологого термометра',
    0xF5000009: 'Висока температура вологого термометра',
    0xF500000A: 'Обчислювач вимкнено',
    0xF500000B: 'На вході обчислювача корінь із від’ємного числа',
    0xF500000C: 'Невірно задано індекс датчика',
    0xF500000D: 'Невірно задано індекс мережевого фільтра',
}

EN_ERR_BANK = {
    0xF6000000: 'No data',
    0xF7000000: 'Sensor is disabled',
    0xF8000000: 'High cold junction temperature',
    0xF9000000: 'Low cold junction temperature',
    0xFA000000: 'Calculated value is too high',
    0xFB000000: 'Calculated value is too low',
    0xFC000000: 'Short circuit',
    0xFD000000: 'Sensor break',
    0xFE000000: 'No connection with ADC',
    0xFF000000: 'Invalid calibration coefficient',

    # Float calculation error codes
    # Most of them are specific to the calculation module,
    # but some may also occur in other modules (e.g., actuator module)

    0xF5000000: 'Incorrect number of inputs',
    0xF5000001: 'Calculator input is disabled',
    0xF5000002: 'Sensor used by the calculator is disabled',
    0xF5000003: 'Mismatch between sensor and calculator',
    0xF5000004: 'Filter used by the calculator is disabled',
    0xF5000005: 'Invalid RS485 filter data format',
    0xF5000006: 'Low dry thermometer temperature (humidity)',
    0xF5000007: 'High dry thermometer temperature',
    0xF5000008: 'Low wet thermometer temperature',
    0xF5000009: 'High wet thermometer temperature',
    0xF500000A: 'Calculator is disabled',
    0xF500000B: 'Negative value at the square root calculator input',
    0xF500000C: 'Invalid sensor index',
    0xF500000D: 'Invalid network filter index',
}

ERR_BANK = {
    'EN': EN_ERR_BANK,
    'UA': UA_ERR_BANK
}


def check_err_code_in_value(value):
    if isinstance(value, float):
        # Преобразуем float в байты, затем в hex
        hex_repr = struct.unpack('<I', struct.pack('<f', value))[0]
        err_code = hex(hex_repr)
        err_code = int(err_code, 16)
        # err_code = hex(err_code).upper()
        cur_lang = AqTranslateManager.get_current_lang()
        if cur_lang not in ERR_BANK.keys():
            cur_lang = 'UA'

        if err_code in ERR_BANK[cur_lang].keys():
            value = ERR_BANK[cur_lang][err_code]

    return value
