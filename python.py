import nacos, time

config = "随机文本"





def AAA(txt):
    global config
    config = txt

n = nacos.CreatNewNacos("47.102.96.180", 8848)
n.HoldConifg.Start("111", "1", AAA)
while True:
    time.sleep(1)
    print(config)