# coding: utf-8
import time
import loggus
import requests

from utils.env import Env
from spider.basics_spider import BasicsPayload


def get(payload: BasicsPayload, log=loggus):
    start = time.time()
    try:
        if Env.THIRD_COMPARE_SERVER:
            resp = requests.post(
                Env.THIRD_COMPARE_SERVER,
                json={
                    "url": payload.url,
                },
                timeout=12,
            ).json()
            if resp["code"] == 0:
                log.update(cost=int(time.time() - start)).info("获取compare数据成功")
                return {
                    "tencent": resp["data"]["securityLevel"],
                    "360": 0,
                }
        log.update(cost=int(time.time() - start)).warning("未获取compare数据")
    except Exception as e:
        log.update(cost=int(time.time() - start)).error(f"获取compare数据异常:{e}")
    return {
        "tencent": 0,
        "360": 0,
    }


if __name__ == '__main__':
    print(get(BasicsPayload(
        url="https://wordpress.com/zh-cn/",
        scheme="https",
        host="wordpress.com",
        domain="wordpress.com",
        is_valid=True,
    )))
