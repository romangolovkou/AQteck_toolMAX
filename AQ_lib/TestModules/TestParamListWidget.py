from random import random

from AqDeviceParamListModel import AqDeviceParamListModel
from TestFuncs import getRandomString


def generateTestData() -> AqDeviceParamListModel:
    dev_test_model = AqDeviceParamListModel()
    dev_test_model.name = getRandomString(random.randint(1, 20))
    dev_test_model.serial = getRandomString(random.randint(16, 18))
    dev_test_model.network_info = []
    for i in range(random.randint(1, 10)):
        dev_test_model.network_info.append(getRandomString(random.randint(10, 18))
                                           + " : "
                                           + getRandomString(random.randint(10, 30)))

