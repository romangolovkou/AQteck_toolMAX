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
