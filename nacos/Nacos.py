from nacos.func import *

# 构造请求的类
class Nacos:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # 获取配置
    def Get(self, data_id:str, group:str, tenant:str = "", timeout:int = 5):
        html = requests.get(
            url = getUrl(self.ip, self.port, "/nacos/v1/cs/configs"),
            params = {
                "tenant":tenant,
                "dataId":data_id,
                "group":group
            },
            timeout = timeout)
        return check(html)

    # 监听配置表，如果改变了则立即返回 True 否则会阻塞直到 timeout 返回 False
    def Listener(self, data_id:str, group:str, contentMD5:str = "", timeout:int = 30, tenant:str = ""):
        data = f"""{data_id}{u2}{group}{u2}{contentMD5}{u2}{tenant}{u1}"""
        html = requests.post(
            url = getUrl(self.ip, self.port, "/nacos/v1/cs/configs/listener"),
            data = {"Listening-Configs":data},
            headers = {"Long-Pulling-Timeout":str(timeout * 1000)}
        )
        if check(html):
            return True
        return False

    # 发布配置  成功 True 失败 Flase
    def Put(self, data_id:str, group:str, content:str, tenant:str = "", type:str = ""):
        html = requests.post(
            url = getUrl(self.ip, self.port, "/nacos/v1/cs/configs"),
            data={
                "tenant": tenant,
                "dataId":data_id,
                "group":group,
                "content":content,
                "type":type,
            },
        )
        return bool(check(html))

    # 删除配置  成功 True 失败 Flase
    def Delete(self, data_id:str, group:str, tenant:str = ""):
        html = requests.delete(
            url = getUrl(self.ip, self.port, "/nacos/v1/cs/configs"),
            params={
                "tenant": tenant,
                "dataId": data_id,
                "group": group,
            }
        )
        return bool(check(html))