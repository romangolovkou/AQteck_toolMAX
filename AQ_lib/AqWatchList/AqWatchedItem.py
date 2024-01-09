import dataclasses

from AqBaseTreeItems import AqParamItem
from AqBaseDevice import AqBaseDevice

class WatchedItem:

    def __init__(self, device):
        self.items = list()
        self.device: AqBaseDevice = device

    def addItemToWatch(self, item):
        if item not in self.items:
            self.items.append(item)

    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)

    def check_param_in_self(self, item):
        if item in self.items:
            return True
        else:
            return False

