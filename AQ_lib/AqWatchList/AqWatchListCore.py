import asyncio
import dataclasses
import os
import threading
import time
from PySide6.QtCore import Signal, QObject

from AqBaseTreeItems import AqParamItem
from AqWatchedItem import WatchedItem


class AqWatchListCore(QObject):

    core_cv = None
    core_thread = None
    watched_items = list()
    poll_period = None
    signals = None

    @classmethod
    def init(cls):
        # At ms
        cls.poll_period = 5000
        cls.core_cv = threading.Condition()
        cls.core_thread = threading.Thread(target=cls.run)
        cls.core_thread.start()
        cls.signals = AqWatchCoreSignals()

    @classmethod
    def addItem(cls, device, items):
        watchedItem = cls.getWatchedItemByDevice(device)
        if watchedItem is None:
            # Create new device
            watchedItem = WatchedItem(device)
            # Add device to list
            cls.watched_items.append(watchedItem)
        # Add new item to watching list
        watchedItem.addItemToWatch(items)
        cls.signals.watch_item_change.emit(watchedItem)

    @classmethod
    def getWatchedItemByDevice(cls, device):
        watchedItem = [i for i in cls.watched_items if i.device is device]
        if len(watchedItem) > 0:
            return watchedItem[0]
        else:
            return None

    @classmethod
    def getWatchedItemByParamItem(cls, item: AqParamItem):
        for w_item in cls.watched_items:
            if w_item.check_param_in_self(item) is True:
                return w_item

        return None

    @classmethod
    def removeItem(cls, item):
        if isinstance(item, WatchedItem):
            cls.watched_items.remove(item)
            cls.signals.watch_item_remove.emit(item)
        elif isinstance(item, AqParamItem):
            watchedItem = cls.getWatchedItemByParamItem(item)
            if watchedItem is not None:
                watchedItem.removeItem(item)
                cls.signals.watch_item_change.emit(watchedItem)
        else:
            pass

    def removeItemByDevice(self, device):
        pass

    def setPollingPeriod(cls, period):
        cls.poll_period = period

    @classmethod
    def run(cls):
        asyncio.run(cls.proceed())


    @classmethod
    async def proceed(cls):
        with cls.core_cv:
            while True:
                # print('\n')
                # print('AqWatchListCore: started making read request')
                for watched_item in cls.watched_items:
                    watched_item.device.read_parameters(watched_item.items)
                time.sleep(0.5)


class AqWatchCoreSignals(QObject):
    watch_item_change = Signal(WatchedItem)
    watch_item_remove = Signal(WatchedItem)
    def __init__(self):
        super().__init__()
