"""
nacos 官网
https://nacos.io/en-us/

本 SDK 基于 Open-API
https://nacos.io/en-us/docs/open-api.html
"""

class CreatNewNacos:
    def __init__(self, ip, port):
        from .NacosAdmin import NacosAdmin
        from .NacosConfig import NacosConfig
        from .NacosInstance import NacosInstance
        from .NacosService import NacosService

        self.NacosAdmin = NacosAdmin(ip, port)
        self.NacosConfig = NacosConfig(ip, port)
        self.NacosInstance = NacosInstance(ip, port)
        self.NacosService = NacosService(ip, port)

        self.HoldState = False

    # 持续监测某个配置文件，如果配置文件发生改变，则触发一个新的事件
    def __Hold(self, data_id : str, group : str, target,
                 timeout : int = 30, tenant : str = ""):

        from .func import getMD5
        contentMD5 = getMD5(
            self.NacosConfig.Get(data_id, group)
        )
        while True:
            if self.HoldState:
                req = self.NacosConfig.Listener(
                    data_id=data_id,
                    group=group,
                    contentMD5=contentMD5,
                    timeout=timeout,
                    tenant=tenant
                )
                if req:
                    newConfig = self.NacosConfig.Get(data_id, group)
                    contentMD5 = getMD5(
                        newConfig
                    )
                    target(newConfig)
            else:
                print("停止循环")
                break

    # 创建一个 Hold 线程，专门由于检测配置
    def Hold(self, data_id : str, group : str, target,
                 timeout : int = 30, tenant : str = ""):

        from threading import Thread
        self.HoldState = Thread(
            target = self.__Hold,
            args = (
                data_id,
                group,
                target
            ),
            kwargs = {
                "timeout":timeout,
                "tenant":tenant
            }
        )
        self.HoldState.start()
        return True
