import time
from datetime import datetime

from scrapy import cmdline


def doSth():
    cmdline.execute('scrapy crawl yinghua'.split())


def time_ti(h=17, m=3):
    while True:
        now = datetime.now()
        if now.hour == h and now.minute == m:
            doSth()
        # 每隔60秒检测一次
        time.sleep(60)


if __name__ == "__main__":
    time_ti()
