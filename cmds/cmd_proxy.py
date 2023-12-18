# coding: utf-8
import pywss
import random

from utils.env import Env


def proxy_iter(proxies):
    while True:
        for proxy in proxies:
            yield proxy


class ProxyView:

    def __init__(self):
        proxy_pool = Env.PROXY_POOL.split(",")
        random.shuffle(proxy_pool)  # 随机打乱
        self.proxy_pool = proxy_iter(proxy_pool)

    def http_get(self, ctx: pywss.Context):
        try:
            prob = int(ctx.url_params.get("prob", 100))  # 获取代理的概率
        except:
            ctx.set_status_code(pywss.StatusBadRequest)
            return
        if prob >= 100 or random.randint(0, 100) <= prob:
            proxy_ip = next(self.proxy_pool)
        else:
            proxy_ip = None
        if proxy_ip:
            ctx.write(proxy_ip)
        else:
            ctx.set_status_code(pywss.StatusNoContent)


def main():
    app = pywss.App()
    app.openapi()
    app.view("/", ProxyView)
    app.run()
