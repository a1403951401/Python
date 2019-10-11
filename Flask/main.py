import sys, os, time
import json
import shutil
from threading import Thread
from flask import Flask, request, send_from_directory, make_response, render_template


app = Flask(
    __name__,
    static_folder="file"
)

def log(txt, now = None, file = False):
    if not now:
        now = str(int(time.time()))
    if file:
        filename = f"{sys.path[0]}/log/file/{now}.log"
    else:
        filename = f"{sys.path[0]}/log/req/{now}.log"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'a') as l:
        l.write(str(txt) + "\r")

@app.route('/', methods=['Get', 'POST'])
def index():
    # 获取 raw
    if request.is_json:
        raw = request.get_json()
    else:
        raw = {}
    # 获取文件
    now = str(int(time.time()))
    path = f"{sys.path[0]}/file/{now}"
    f = []
    file = dict(request.files)
    if len(file):
        os.makedirs(path)
    for k, v in file.items():
        v.save(os.path.join(path, f"{k}_{v.filename}"))
        f.append(
            {
                "url" : f"{now}/{k}_{v.filename}",
                "path" : f"{path}/{k}_{v.filename}",
                "key" : k,
                "filename" : v.filename
            }
        )
    # 获取请求头
    headers = {}
    for i in request.headers.to_wsgi_list():
        headers[i[0]] = i[1]
    dir = {
        "request_IP": request.remote_addr,
        "path": sys.path[0],
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "method": request.method,
        "headers": headers,
        "values": {
            "args": request.args.to_dict(),
            "form": request.form.to_dict(),
            "json": raw,
            "file": f,
            "values": request.values.to_dict(),
        }
    }
    if f:
        log(json.dumps(dir, ensure_ascii=False), file = True)
    else:
        log(json.dumps(dir, ensure_ascii=False))
    return render_template("index.html", url = request.host_url, file = f)

@app.route('/download/<time>/<file_name>/', methods=["GET"])
def download(time, file_name):
    try:
        print(f"{sys.path[0]}/file/{file_name}")
        response = make_response(
            send_from_directory(f"{sys.path[0]}/file/{time}/", file_name, as_attachment=True))
        return response
    except Exception as e:
        log(e)
        return "文件不存在"


def Clean(t, kill):
    path = sys.path[0] + "/file/"
    if not os.path.exists(path):
        os.makedirs(path)
    while True:
        time.sleep(t)
        for i in os.listdir(path):
            if os.stat(f"{path}{i}").st_mtime + kill * 60 * 60 * 24 < time.time():
                shutil.rmtree(f"{path}{i}")
                log(f"文件于 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 删除", i, file = True)



if __name__ == '__main__':
    t = 1
    kill = 30
    Thread(target = Clean, args=(t, kill, )).start()

    app.run(
        host = "0.0.0.0",
        port = "80",
        debug = False
    )