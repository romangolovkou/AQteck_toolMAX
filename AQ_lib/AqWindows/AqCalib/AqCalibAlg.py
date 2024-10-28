from AqCalibCoeff import AqCalibCoeff


class AqCalibAlg(object):
    def __init__(self, data):
        self.formula = data['formula']
        if not (0 <= self.formula <= 4):
            raise ValueError("CalibAlg.formula must be between 0 and 4")

        coeffs_data = data['coeffs']
        self.coeffs = list()
        for coeff in coeffs_data:
            self.coeffs.append(AqCalibCoeff(coeff))

        points_data = data['points']
        self.points = list()
        for point in points_data:
            if isinstance(point['value'], int) or isinstance(point['value'], float):
                self.coeffs.append(point['value'])
            else:
                raise TypeError('Point value is not int or float')

