import os, json
import time, datetime

import random

# 定义自身类【Page类、Tool类】
class main:
    # 传入参数、订单号
    def __init__(self, IDcard = None, *args, **kwargs):
        self.ScriptDirname = os.path.dirname(os.path.abspath(__file__))  # 当前工作目录
        self.IDcard = IDcard
        self.youxiao = "是"

    def main(self):
        if "身份证" in self.data:
            dir = {"身份证位数":len(self.IDcard)}
            if len(self.IDcard) != 18:
                self.youxiao = "否"
            dir = dict(dir, **self.sqssq())
            dir = dict(dir, **self.sr())
            dir = dict(dir, **self.xb())
            dir = dict(dir, **self.zuihou())
            dir["证件是否正确"] = self.youxiao
            return dict(self.data, **dir)
        else:
            if "区" in self.data:
                qu = self.data["区"]
            else:
                with open(f"{self.ScriptDirname}/区.txt", encoding="utf-8") as f:
                    qu = f.readlines()
                qu = qu[random.randint(0, len(qu))].split("|")[0]
            if "时间" in self.data:
                t = self.data["时间"]
            else:
                t = random.randint(0, int(time.time()))
                t = time.strftime("%Y%m%d", time.localtime(t))
            if "派出所" in self.data:
                num = self.data["派出所"]
            else:
                num = random.randint(0, 99)
                if num < 10 :
                    num = f"0{str(num)}"
            if "性别" in self.data:
                sex = self.data["性别"]
            else:
                sex = random.randint(0, 9)
            key = f"{qu}{t}{num}{sex}"
            return {"生成身份证": key + self.zuihou(key)["最后一位"]}


    # 省市区
    def sqssq(self):
        num = self.IDcard[:6]
        if len(num) >= 6:
            with open(f"{self.ScriptDirname}/区.txt", encoding="utf-8") as f:
                qu = f.readlines()
            for i in qu:
                if num in i:
                    req = i.split("|")
                    if "\n" in req[-1]:
                        req[-1] = req[-1][:-1]
                    return {"省":req[1],"市":req[2],"区":req[3]}
        if len(num) >= 4:
            with open(f"{self.ScriptDirname}/市.txt", encoding="utf-8") as f:
                shi = f.readlines()
            for i in shi:
                if num[:4] in i:
                    req = i.split("|")
                    if "\n" in req[-1]:
                        req[-1] = req[-1][:-1]
                    return {"省":req[1],"市":req[2],"区":"未知"}
        if len(num) >= 2:
            with open(f"{self.ScriptDirname}/省.txt", encoding="utf-8") as f:
                sheng = f.readlines()
            for i in sheng:
                if num[:2] in i:
                    req = i.split("|")
                    if "\n" in req[-1]:
                        req[-1] = req[-1][:-1]
                    return {"省":req[1],"市":"未知","区":"未知"}
        self.youxiao = "否"
        return {"省":"未知","市":"未知","区":"未知"}

    # 生日
    def sr(self):
        dir = {"年":"未知", "月":"未知", "日":"未知"}
        try:
            dir["年"], dir["月"], dir["日"] = datetime.datetime.strptime(self.IDcard[6:10] + self.IDcard[10:12] + self.IDcard[12:14], '%Y%m%d').strftime('%Y-%m-%d').split("-")
            return dir
        except:
            self.youxiao = "否"
            return dir


    # 性别
    def xb(self):
        if len(self.IDcard) >= 16:
            num = self.IDcard[16]
            if (int(num) % 2) == 0:
                return {"性别":"女"}
            return {"性别": "男"}
        self.youxiao = "否"
        return {"性别": "未知"}

    # 最后一位
    def zuihou(self, num = None):
        if not num:
            num = self.IDcard
        if len(num) >= 17:
            list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            newlist = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
            add = 0
            for i in range(17):
                add += list[i] * int(num[i])
            last = newlist[add - add // 11 * 11]
            if num[-1] == last:
                return {"最后一位":last}
            self.youxiao = "否"
            return {"最后一位":last}
        else:
            self.youxiao = "否"
            return {"最后一位": "未知"}


if __name__ == '__main__':
    ident = "无"
    from json import dumps

    s = [
        "352601197304301527",
        "440181199608173636",
        "445202199601140641",
        "362522198412085035",
        "440781199804181337"
    ]
    for i in s:
        print(dumps(main(i).main(), ensure_ascii=False))