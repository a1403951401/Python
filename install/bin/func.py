import subprocess


cleanlist = [
    "\n",
    "\r",
    " "
]

yuan = {
    "阿里云":"https://mirrors.aliyun.com/pypi/simple/",
    "清华大学":"https://pypi.tuna.tsinghua.edu.cn/simple",
    "豆瓣":"https://pypi.douban.com/simple/",
    "中国科技大学":"https://pypi.mirrors.ustc.edu.cn/simple/",
    "华中理工大学":"https://pypi.hustunique.com/",
    "山东理工大学":"https://pypi.sdutlinux.org/",
}


def sh(command, print_msg=True):
    p = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('gbk')
    if print_msg:
        print(result)
    return result

def clean(text):
    for i in cleanlist:
        text = text.replace(i, "")
    return text