import asyncio
import dataclasses
import os
import threading
import time
from typing import Union

from PySide6.QtCore import Signal, QObject

from AqBaseTreeItems import AqParamItem
from AqWatchedItem import WatchedItem


class AqWatchListCore(QObject):

    core_cv = None
    stop_flag = None
    core_thread = None
    watched_items = list()
    poll_period = None
    signals = None

    @classmethod
    def init(cls):
        # At ms
        cls.poll_period = 5000
        cls.core_cv = threading.Condition()
        cls.stop_flag = threading.Event()
        cls.core_thread = threading.Thread(target=cls.run)
        cls.core_thread.start()
        cls.signals = AqWatchCoreSignals()

    @classmethod
    def deinit(cls):
        cls.stop_flag.set()

    @classmethod
    def addItem(cls, device, items: Union[AqParamItem, list]):
        watchedItem = cls.getWatchedItemByDevice(device)
        if watchedItem is None:
            # Create new device
            watchedItem = WatchedItem(device)
            # Add device to list
            cls.watched_items.append(watchedItem)
        # Add new item to watching list
        if isinstance(items, AqParamItem):
            watchedItem.addItemToWatch(items)
        elif isinstance(items, list):
            for item in items:
                watchedItem.addItemToWatch(item)

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
            while not cls.stop_flag.is_set():
                # print('\n')
                # print('AqWatchListCore: started making read request')
                for watched_item in cls.watched_items:
                    items_to_read = list()
                    for item in watched_item.items:
                        # if item.get_status() != 'changed':
                        if not item.is_blocked and item.get_status() != 'changed':
                            items_to_read.append(item)
                    cls.readWatchedItemParam(watched_item, items_to_read)
                await asyncio.sleep(0.5)

            print('AqWatchListCore is finished')

    @classmethod
    def writeWatchedItemParam(cls, items_to_write):
        watchedItem = cls.getWatchedItemByParamItem(items_to_write)
        watchedItem.device.write_parameters(items_to_write)

    @classmethod
    def readWatchedItemParam(cls, watchedItem, items_to_read):
        watchedItem.device.read_parameters(items_to_read)

class AqWatchCoreSignals(QObject):
    watch_item_change = Signal(WatchedItem)
    watch_item_remove = Signal(WatchedItem)
    def __init__(self):
        super().__init__()
