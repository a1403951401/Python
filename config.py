import redis
from Libs.config import Cookies_Config
from Libs.Robot.Tool.func import Try

__r = redis.StrictRedis(
    host="47.102.96.180",
    port=6379,
    db=0,
    password="1403951401",
    decode_responses=True
)
print(__r.hset(name="name", key="key", value="value"))
print(__r.hget(name = "name", key = "key"))