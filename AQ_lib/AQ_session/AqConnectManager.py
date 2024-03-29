import asyncio
import threading
import time
from asyncio import CancelledError
from random import random
from codetiming import Timer

from AqConnect import AqOfflineConnect, AqModbusConnect, AqConnect, AqOfflineConnectSettings
from AqConnect import AqIpConnectSettings, AqComConnectSettings


class AqConnectManager(object):

    event_manager = None
    core_cv = None
    core_thread = None
    connect_list = []
    connect_mutex = dict()

    work_queue = asyncio.Queue()

    requested_connect = set()

    @classmethod
    def init(cls):
        cls.core_cv = asyncio.Event()
        cls.core_thread = threading.Thread(target=cls.run)
        cls.core_thread.daemon = True
        cls.core_thread.start()

    @classmethod
    def deinit(cls):
        for connect in cls.connect_list:
            connect.close()

    @classmethod
    def run(cls):
        asyncio.run(cls.core())

    @classmethod
    async def core(cls):
        tasks = [
            asyncio.create_task(cls.proceed()),
            asyncio.create_task(cls.proceedParamRequest("One")),
            asyncio.create_task(cls.proceedParamRequest("Two")),
            asyncio.create_task(cls.proceedParamRequest("Three")),
            asyncio.create_task(cls.proceedParamRequest("Four")),
        ]
        try:
            await asyncio.gather(*tasks)
        except CancelledError:
            return None

    @classmethod
    async def proceed(cls):
        while True:
            await asyncio.sleep(0.1)
            if cls.core_cv.is_set():
                for i in range(len(cls.requested_connect)):
                    await cls.work_queue.put(cls.requested_connect.pop())
                cls.requested_connect.clear()
                cls.core_cv.clear()

    @classmethod
    def notify(cls, connect_obj):
        cls.requested_connect.add(connect_obj)
        cls.core_cv.set()

    @classmethod
    def create_connect(cls, connect_settings, device_id=None) -> AqConnect:
        connect = None

        if isinstance(connect_settings, AqOfflineConnectSettings):
            connect = AqOfflineConnect(cls.notify)
        elif isinstance(connect_settings, (AqIpConnectSettings, AqComConnectSettings)):
            locker = cls.connect_mutex.get(connect_settings.addr, None)
            if locker is None:
                locker = asyncio.Lock()
                cls.connect_mutex[connect_settings.addr] = locker
            connect_settings.mutex = locker
            if device_id is None:
                device_id = 1
            connect = AqModbusConnect(connect_settings, device_id, cls.notify)
        else:
            print('AqConnectManagerError: unknown settings instance')
            return None

        if connect is not None:
            cls.connect_list.append(connect)

        return connect

    @classmethod
    def deleteConnect(cls, connect):
        cls.connect_list.remove(connect)

    @classmethod
    async def proceedParamRequest(cls, name):
        print(f"Created task {name}")

        timer = Timer(text=f"Task {name} elapsed time: {{:.4f}}")
        while True:
            connect = await cls.work_queue.get()
            timer.start()
            await connect.proceedOneRequestGroup()
            timer.stop()
