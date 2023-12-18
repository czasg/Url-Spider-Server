# coding: utf-8
import unittest

from spider.basics_spider import get, is_valid


class TestBase(unittest.TestCase):

    def test_basics_spider(self):
        self.assertEqual(
            get("https://abcdefg.666").dict(),
            {
                'domain': 'abcdefg.666',
                'host': 'abcdefg.666',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://abcdefg.666'
            }
        )
        self.assertEqual(
            get("https://abcdefg.666:8080").dict(),
            {
                'domain': 'abcdefg.666',
                'host': 'abcdefg.666:8080',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://abcdefg.666:8080'
            }
        )
        self.assertEqual(
            get("https://www.baidu.com").dict(),
            {
                'domain': 'baidu.com',
                'host': 'www.baidu.com',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://www.baidu.com'
            }
        )
        self.assertEqual(
            get("https://www.baidu.com:8080/test").dict(),
            {
                'domain': 'baidu.com',
                'host': 'www.baidu.com:8080',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://www.baidu.com:8080/test'
            }
        )
        self.assertEqual(
            get("https://10.251.11.16/test").dict(),
            {
                'domain': '10.251.11.16',
                'host': '10.251.11.16',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://10.251.11.16/test'
            }
        )
        self.assertEqual(
            get("https://10.251.11.16:8888/test").dict(),
            {
                'domain': '10.251.11.16',
                'host': '10.251.11.16:8888',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://10.251.11.16:8888/test'
            }
        )

    def test_basics_spider_cases(self):
        self.assertEqual(
            get("http://df.bytes.used.percent/fstype=ext4,mount=/").dict(),
            {
                'domain': 'used.percent',
                'host': 'df.bytes.used.percent',
                'is_valid': True,
                'scheme': 'http',
                'url': 'http://df.bytes.used.percent/fstype=ext4,mount=/'
            }
        )
        self.assertEqual(
            get("https://gov.ybsjyyn.com」").dict(),
            {
                'domain': 'ybsjyyn.com',
                'host': 'gov.ybsjyyn.com',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://gov.ybsjyyn.com」'
            }
        )
        self.assertEqual(
            get(
                "https://220.160.53.29:7066/LHSoft/AlarmAddress/dXNlcmlkPTYyZDUyNzExLWI4MWItNDQ5Zi1hYjg2LTdjMTQ4Y2E0MDhhYSZkYXRhdHlwZT0yJmRhdGF0aW1lPTIwMjMtMTAtMDUgMjA6MDA6MDA=").dict(),
            {
                'domain': '220.160.53.29',
                'host': '220.160.53.29:7066',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://220.160.53.29:7066/LHSoft/AlarmAddress/dXNlcmlkPTYyZDUyNzExLWI4MWItNDQ5Zi1hYjg2LTdjMTQ4Y2E0MDhhYSZkYXRhdHlwZT0yJmRhdGF0aW1lPTIwMjMtMTAtMDUgMjA6MDA6MDA='
            }
        )
        self.assertEqual(
            get("http://11185.cn、").dict(),
            {
                'domain': '11185.cn',
                'host': '11185.cn',
                'is_valid': True,
                'scheme': 'http',
                'url': 'http://11185.cn、'
            }
        )
        self.assertEqual(
            get("https://ebl.com.bd/min_due").dict(),
            {
                'domain': 'ebl.com',
                'host': 'ebl.com.bd',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://ebl.com.bd/min_due'
            }
        )
        self.assertEqual(
            get("http://jn.sdyouma.com:86/pj.do?id=580145823141990401").dict(),
            {
                'domain': 'sdyouma.com',
                'host': 'jn.sdyouma.com:86',
                'is_valid': True,
                'scheme': 'http',
                'url': 'http://jn.sdyouma.com:86/pj.do?id=580145823141990401'
            }
        )
        self.assertEqual(
            get("http://《www.jj.cn》").dict(),
            {
                'domain': 'jj.cn',
                'host': 'www.jj.cn',
                'is_valid': True,
                'scheme': 'http',
                'url': 'http://《www.jj.cn》'
            }
        )
        self.assertEqual(
            get("https://m.yqg.mobi/y1").dict(),
            {
                'domain': 'yqg.mobi',
                'host': 'm.yqg.mobi',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://m.yqg.mobi/y1'
            }
        )

    def test_basics_spider_country(self):
        self.assertEqual(
            get("https://m.yqg.mobi.cn").dict(),
            {
                'domain': 'yqg.mobi',
                'host': 'm.yqg.mobi.cn',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://m.yqg.mobi.cn'
            }
        )
        self.assertEqual(
            get("https://miclaro.com.gt").dict(),
            {
                'domain': 'miclaro.com',
                'host': 'miclaro.com.gt',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://miclaro.com.gt'
            }
        )
        self.assertEqual(
            get("https://miclaro.com.gt").dict(),
            {
                'domain': 'miclaro.com',
                'host': 'miclaro.com.gt',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://miclaro.com.gt'
            }
        )
        self.assertEqual(
            get("https://com.gt").dict(),
            {
                'domain': 'com.gt',
                'host': 'com.gt',
                'is_valid': True,
                'scheme': 'https',
                'url': 'https://com.gt'
            }
        )
        self.assertEqual(
            get("https://com.gt.").dict(),
            {
                'domain': '',
                'host': '',
                'is_valid': False,
                'scheme': '',
                'url': 'https://com.gt.'
            }
        )
        self.assertEqual(
            get("https://.com.gt").dict(),
            {
                'domain': '',
                'host': '',
                'is_valid': False,
                'scheme': '',
                'url': 'https://.com.gt'
            }
        )

    def test_basics_spider_valid(self):
        self.assertEqual(
            is_valid("com.gt"),
            True,
        )
        self.assertEqual(
            is_valid(".com.gt"),
            False,
        )
        self.assertEqual(
            is_valid("com.gt."),
            False,
        )


if __name__ == '__main__':
    unittest.main()
