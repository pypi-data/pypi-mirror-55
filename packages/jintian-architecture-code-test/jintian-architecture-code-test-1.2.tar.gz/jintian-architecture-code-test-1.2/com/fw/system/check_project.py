import os
import time
from enum import Enum
from requests import exceptions

import requests


class DateEnum(Enum):
    YMD = "%Y-%m-%d"
    YMDHMS = "%Y-%m-%d %H:%M:%S"


class DateType(Enum):
    DAY = "days"
    HOUR = "hours"
    MINUTE = "minutes"
    SECONDS = "seconds"


def getCurrentDateTime(date_enum=DateEnum.YMDHMS):
    '''
            获取当前日期：2013-09-10这样的日期字符串
    '''
    return time.strftime(date_enum.value, time.localtime(time.time()))

def restartService():
    url = "http://{}:{}/test/hello".format("172.31.236.138", "8000")

    print("【自检】{}:准备自检{}....".format(getCurrentDateTime(), url))

    try:
        response = requests.get(url, timeout=5)
    except exceptions.Timeout as e:
        print("测试请求超时，准备执行重启脚本...")
        os.popen("docker stop file && docker start file")
    else:
        if response.status_code != 200:
            print("请求失败code :{}，准备执行重启脚本...".format(response.status_code))
            os.popen("docker stop file && docker start file")

if __name__ == '__main__':
    while True:
        try:
            restartService()
        except Exception as e:
            print("重启线程执行错误")
        finally:
            time.sleep(10 *60)