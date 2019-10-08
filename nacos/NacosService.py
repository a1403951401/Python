from nacos.func import *

class NacosService:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # 创建服务【当创建失败的时候，请求会抛出异常，请自行进行捕获】
    def Add(self, serviceName, groupName = "", namespaceId = "", protectThreshold = 0, metadata = "", selector = ""):
        html = requests.post(
            url=getUrl(self.ip, self.port, "/nacos/v1/ns/service"),
            data = {
                "serviceName" : serviceName,
                "groupName" : groupName,
                "namespaceId" : namespaceId,
                "protectThreshold" : protectThreshold,
                "metadata" : metadata,
                "selector" : selector,
            }
        )
        return check(html)

    def Delete(self):
        pass



if __name__ == '__main__':
    import time
    n = NacosService("47.102.96.180", 8848)
    print(n.Add("444"))