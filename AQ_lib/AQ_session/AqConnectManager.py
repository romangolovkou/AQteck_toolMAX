import asyncio
import threading
import time
from random import random

from AqConnect import AqOfflineConnect, AqModbusConnect, AqConnect, AqOfflineConnectSettings
from AqConnect import AqIpConnectSettings, AqComConnectSettings


class AqConnectManager(object):

    event_manager = None
    core_cv = None
    core_thread = None
    connect_list = []
    request_stack = []

    @classmethod
    def init(cls):
        cls.core_cv = threading.Condition()
        cls.core_thread = threading.Thread(target=cls.run)
        cls.core_thread.start()

    @classmethod
    def run(cls):
        asyncio.run(cls.proceed())

    @classmethod
    async def proceed(cls):
        with AqConnectManager.core_cv:
            while True:
                cls.core_cv.wait()
                for i in range(len(cls.connect_list)):
                    while len(cls.connect_list[i].param_request_stack) > 0:
                        await cls.proceedParamRequest(cls.connect_list[i])
                    while len(cls.connect_list[i].file_request_stack) > 0:
                        await cls.proceedFileRequest(cls.connect_list[i].param_request_stack.pop())

    @classmethod
    def create_connect(cls, connect_settings, device_id=None) -> AqConnect:
        connect = None
        if isinstance(connect_settings, AqOfflineConnectSettings):
            connect = AqOfflineConnect(cls.core_cv)
        elif isinstance(connect_settings, (AqIpConnectSettings, AqComConnectSettings)):
            try:
                if device_id is None:
                    device_id = 1
                connect = AqModbusConnect(connect_settings, device_id, cls.core_cv)
                if connect.open():
                    connect.close()
                else:
                    connect = None
                    # raise Exception('AqConnectManagerError: failed to open connect')
            except Exception as e:
                print(str(e))
        else:
            print('AqConnectManagerError: unknown settings instance')
            return None

        if connect is not None:
            cls.connect_list.append(connect)

        return connect

    @staticmethod
    async def proceedParamRequest(connect):
        for i in range(len(connect.param_request_stack)):
            request = connect.param_request_stack.pop()
            connect.proceed_request(request)

    @staticmethod
    async def proceedFileRequest(req_data):
        data_storage = req_data['data']
        time.sleep(random.uniform(0.1, 2.0))
        data_storage = random.randint(50, 100)










