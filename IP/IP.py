import requests



def IP(ip):
    url = "http://wq.apnic.net/query?searchtext=" + ip
    return requests.get(url).text


if __name__ == '__main__':
    req = IP("113.119.8.69")
    print(req)