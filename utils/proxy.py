# coding: utf-8
import requests

from utils.env import Env


def _iterator(items):
    while True:
        for item in items:
            yield item


class Proxy:

    def __init__(self, server="", default=""):
        self.server = server
        self.default = default
        self.default_proxies = _iterator(default.split(","))

    def http_proxy(self, proxy):
        if not proxy:
            return None
        if not proxy.startswith("http"):
            proxy = f"http://{proxy}"
        return {
            "http": proxy,
            "https": proxy
        }

    def get_http_proxy(self):
        if self.server:
            try:
                return self.http_proxy(requests.get(self.server, timeout=4).text)
            except:
                pass
        if self.default:
            proxy = next(self.default_proxies)
            if not proxy.startswith("http"):
                proxy = f"http://{proxy}"
            return {
                "http": proxy,
                "https": proxy
            }
        return None

    def get_default_http_proxy(self):
        return None


proxy = Proxy(Env.PROXY_SERVER, Env.PROXY_DEFAULT)
