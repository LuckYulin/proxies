import time
import requests
from redis import Redis
from config import REDIS_URL
print(*REDIS_URL)

REDIS_db = Redis(*REDIS_URL)
headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}


def save_to_redis(proxy):
    if proxy is not None:
        REDIS_db.lpush('proxy', proxy)


def filter_ip(proxy):
    if proxy is not None:
        api = 'http://lagou.com/'
        proxies = {"http": "http://" + proxy}
        try:
            if requests.get(api, proxies=proxies, timeout=1.5, headers=headers).status_code == 200:
                print('{} OK'.format(proxy))
                return proxy
            else:
                return None
        except Exception as e:
            print("{} NO OK!".format(proxy))


def check_proxy():
    print('IP检查中...')
    while True:
        n = REDIS_db.llen('proxy')//2
        for i in range(n):
            proxy = REDIS_db.rpop('proxy')
            proxy = filter_ip(proxy.decode())
            save_to_redis(proxy)
        print("## IP池剩余{}".format(REDIS_db.llen('proxy')))
        time.sleep(5)


def save_(x):
    while True:
        if REDIS_db.llen('pending'):
            proxy = REDIS_db.rpop('pending')
            proxy = filter_ip(proxy.decode())
            save_to_redis(proxy)
        else:
            time.sleep(3)

