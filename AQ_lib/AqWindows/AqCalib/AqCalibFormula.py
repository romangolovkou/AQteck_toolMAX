


class CalibFormulaBank(object):

    # @classmethod
    # def init(cls, _event_manager):
    #     cls.event_manager = _event_manager

    @classmethod
    def get_formula_funk(cls, formula_num):
        if formula_num == 2:
            return cls.func__Y_equ_AX_plus_B

        return False

    @classmethod
    def func__Y_equ_AX_plus_B(cls, x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_x2 = sum(xi ** 2 for xi in x)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))

        # Вычисление коэффициентов
        a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        b = (sum_y - a * sum_x) / n

        result = {'a': {'value': round(a, 3)}, 'b': {'value': round(b, 3)}}

        return result



