import os, sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{path}/bin")

from bin.DownloadPackages import download, line
from bin.InstallPackages import install

do = {
    "在线安装" : line,
    "下载离线包" : download,
    "安装离线包" : install,
}

for i in range(len(do)):
    print(f"{i} : {list(do.keys())[i]}")

req = input("请输入你的选择【默认在线安装】：")

try:
    func = list(do.values())[int(req)]
except:
    func = line
func(path)