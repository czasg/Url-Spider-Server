# coding: utf-8
import unittest

from utils.transform import any2str, any2list
from utils.proxy import Proxy
from utils.constant import SpiderPayload


class TestBase(unittest.TestCase):

    def test_any2str(self):
        self.assertEqual(
            any2str("test"),
            "test"
        )
        self.assertEqual(
            any2str(["test"]),
            "test"
        )

    def test_any2list(self):
        self.assertEqual(
            any2list("test"),
            ["test"]
        )

    def test_proxy(self):
        proxy = Proxy()
        self.assertEqual(
            proxy.get_http_proxy(),
            None
        )
        self.assertEqual(
            proxy.http_proxy(None),
            None
        )
        self.assertEqual(
            proxy.http_proxy("localhost:8080"),
            {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080"
            }
        )
        proxy = Proxy(default="localhost:8080")
        self.assertEqual(
            proxy.get_http_proxy(),
            {
                "http": "http://localhost:8080",
                "https": "http://localhost:8080"
            }
        )

    def test_spider_payload(self):
        SpiderPayload(url="http://www.baidu.com")
        SpiderPayload(url="http://www.baidu.com", callback="")
        SpiderPayload(url="http://www.baidu.com", callback="http://www")
        try:
            SpiderPayload(url="www.baidu.com")
            self.assertTrue(False)
        except:
            pass
        try:
            SpiderPayload(url="http://www.baidu.com", callback="www")
            self.assertTrue(False)
        except:
            pass


if __name__ == '__main__':
    unittest.main()
