from AqCalibCoeff import AqCalibCoeff
from AqCalibFormula import CalibFormulaBank


class AqCalibAlg(object):
    def __init__(self, data):
        self._formula_func = CalibFormulaBank.get_formula_funk(data['formula'])
        if not self._formula_func:
            raise ValueError("CalibAlg.formula incorrect")

        coeffs_data = data['coeffs']
        self._coeffs = list()
        for coeff in coeffs_data:
            self._coeffs.append(AqCalibCoeff(coeff))

        points_data = data['points']
        self._points = list()
        for point in points_data:
            if isinstance(point['value'], int) or isinstance(point['value'], float):
                self._points.append(point['value'])
            else:
                raise TypeError('Point value is not int or float')

    @property
    def points(self):
        return self._points

    @property
    def access_code(self):
        return self.coeffs.get_access_code()

    @property
    def coeffs(self):
        return self._coeffs

    @property
    def formula_func(self):
        return self._formula_func


