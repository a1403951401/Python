from .func import sh, clean, yuan

def download(path, line = False):
    for i in range(len(yuan)):
        print(f"{i} : {list(yuan.keys())[i]} {list(yuan.values())[i]}")
    try:
        req = int(input("请输入你的选择【默认阿里云】："))
        if req > len(yuan) or req < 0:
            req = 0
    except:
        req = 0
    host = list(yuan.values())[req]
    print(f"已选择 {list(yuan.keys())[int(req)]} {host}")

    err = []
    with open(f"{path}/install.txt", "r") as f:
        packages = f.readlines()
    for i in packages:
        i = clean(i)
        print(f"下载 {i} 中")
        if line:
            req = sh(f"pip install {i} -i {host}")
        else:
            req = sh(f"pip download -d {path}/download {i} -i {host}")
        if "Successfully" in req:
            print(f"{i} 下载成功")
        else:
            err.append(i)
            print(f"{i} 下载失败，可能已经安装包")
    print(err)

def line(path):
    download(path, line = True)