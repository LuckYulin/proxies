# utf8
from pyquery import PyQuery as pq
from multiprocessing import Pool
from bs4 import BeautifulSoup
from check_save_proxy import check_proxy, save_, REDIS_db
from multiprocessing import Process
from app import app_start
import time
import requests


headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}


def iphai_proxy(x):    # ip海代理 https 代理
    url_suffixs = ['ng', 'wp', 'wg']
    time.sleep(3)
    url = 'http://www.iphai.com/free/{}'.format(url_suffixs[x])
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf8'
        html = pq(response.text)
        items = html('table tr').items()
        for item in items:
            proxy = "{}:{}".format(item('td').eq(0).text(), item('td').eq(1).text())
            if not proxy == ':':
                print("hai", proxy)
                REDIS_db.lpush('pending', proxy)
    except Exception as e:
        # print(1, e)
        pass


def xici_proxy(n):   # 西刺代理
    try:
        url = 'https://www.xicidaili.com/wt/{}'.format(n)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf8'
        soup = BeautifulSoup(response.text, 'lxml')
        ips = soup.select('.odd')
        for i in ips:
            proxy = "{}:{}".format(i.select('td')[1].text, i.select('td')[2].text)
            print("xici", proxy)
            REDIS_db.lpush('pending', proxy)
    except Exception as e:
        # print(1, e)
        pass


def kuai_proxy(n):    # 快代理
    try:
        url = 'https://www.kuaidaili.com/free/inha/{}/'.format(n)
        print(url)
        response = requests.get(url, headers=headers)   # 当除第一次循环可以执行外,其它后面的循环返回的是空,
        response.encoding = 'utf8'
        # 状态码是503,此时循环慢一点即可,用time.sleep(2)即可
        html = pq(response.text)
        items = html('table tbody tr').items()
        for item in items:
            proxy = "{}:{}".format(item('td').eq(0).text(), item('td').eq(1).text())
            print("kuai", proxy)
            REDIS_db.lpush('pending', proxy)
    except Exception as e:
        # print(1, e)
        pass


def get_proxy(x):    # 89 代理
    try:
        url = 'http://www.89ip.cn/index_{}.html'.format(x)
        response = requests.get(url, headers=headers)   # 当除第一次循环可以执行外,其它后面的循环返回的是空,
        response.encoding = 'utf8'                      # 状态码是503,此时循环慢一点即可,用time.sleep(2)即可
        html = pq(response.text)
        items = html('tbody tr').items()
        for item in items:
            proxy = "{}:{}".format(item('td').eq(0).text(), item('td').eq(1).text())
            print("89代理", proxy)
            REDIS_db.lpush('pending', proxy)
    except Exception as e:
        # print(1, e)
        pass


def proxy_66(i):    # 66代理
    try:
        url = 'http://www.66ip.cn/areaindex_{}/1.html'.format(i)
        response = requests.get(url, headers=headers)   # 当除第一次循环可以执行外,其它后面的循环返回的是空,
        response.encoding = 'gbk'                      # 状态码是503,此时循环慢一点即可,用time.sleep(2)即可
        html = pq(response.text)
        items = html('#footer table tr').items()
        for item in items:
            ip = item('td').eq(0).text()
            port = item('td').eq(1).text()
            if ip != 'ip' and port != '端口号':
                proxy = "{}:{}".format(item('td').eq(0).text(), item('td').eq(1).text())
                print("66代理", proxy)
                REDIS_db.lpush('pending', proxy)
    except Exception as e:
        # print(1, e)
        pass


def main(page):
    try:
        pool = Pool()
        pool.map(iphai_proxy, [i for i in range(3)])     # https 代理
        pool.map(proxy_66, [i for i in range(1, 35)])
        pool.map(xici_proxy, [i for i in range(1, page)])
        pool.map(kuai_proxy, [i for i in range(1, page)])
        pool.map(get_proxy, [i for i in range(1, page)])
        pool.map(save_, [i for i in range(3)])

    except Exception as e:
        print(8, e)


def proxy_run():
    print('程序运行中...')
    Process(target=app_start).start()
    Process(target=check_proxy).start()
    while True:
        if REDIS_db.llen('proxy') >= 50:
            print('获取ip睡眠中...')
            time.sleep(25)
        elif REDIS_db.llen('proxy') < 20:
            print('正在获取ip...')
            main(10)
        else:
            print('休眠中...')
            time.sleep(25)


if __name__ == '__main__':
    proxy_run()