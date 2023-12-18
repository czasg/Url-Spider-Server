# coding: utf-8
import pika
import time
import pywss
import spider
import loggus

from utils.constant import SpiderPayload, HttpResponse
from service.rabbitmq import Pool as RabbitMQPool
from utils.env import Env
from utils.errs import UrlInvalidSchemaErr

_request_demo = {
    "typ": ["external", "internal", "selenium", "compare", "*"],
    "ctx": {"请求上下文": "请求上下文"},
    "url": "https://www.baidu.com",
    "callback": "",
}
_response_demp = {
    "basics": {"domain": "baidu.com",
               "host": "www.baidu.com",
               "is_valid": True,
               "scheme": "https",
               "url": "https://www.baidu.com"},
    "compare": {"360": 0, "tencent": 0},
    "external": {"cdn_name": "www.a.shifen.com",
                 "country": "CN",
                 "creation_date": ["1999-10-11 11:05:17"],
                 "domain_ttl": 193,
                 "emails": ["abusecomplaints@markmonitor.com",
                            "whoisrequest@markmonitor.com"],
                 "expiration_date": ["1999-10-11 11:05:17",
                                     "1999-10-11 11:05:17"],
                 "has_sitemap": False,
                 "icp": {"domain": "baidu.com",
                         "icpCode": "京ICP证030173号-1",
                         "name": "百度",
                         "passTime": "2022-10-11",
                         "type": "企业",
                         "unit": "北京百度网讯科技有限公司"},
                 "name_servers": ["NS1.BAIDU.COM",
                                  "NS2.BAIDU.COM",
                                  "NS3.BAIDU.COM",
                                  "NS4.BAIDU.COM",
                                  "NS7.BAIDU.COM",
                                  "ns3.baidu.com",
                                  "ns2.baidu.com",
                                  "ns1.baidu.com",
                                  "ns7.baidu.com",
                                  "ns4.baidu.com"],
                 "org": "Beijing Baidu Netcom Science Technology Co., Ltd.",
                 "registrar": "MarkMonitor, Inc.",
                 "search_engine": {"baidu": 0, "bing": 0, "google": 0},
                 "state": "Beijing",
                 "whois_server": "whois.markmonitor.com"},
    "internal": {"elements": 293,
                 "langs": ["en"],
                 "programs": [],
                 "similar": {"alipay": 0.9461244085197196,
                             "android": 0.9461936328375934,
                             "desktop": 0.7859096619383046,
                             "iphone": 0.9462730400217281,
                             "wechat": 0.9462400277967253}},
    "selenium": {
        "elements": 0,
        "screenshot": "base64",
    }
}


class UrlView:

    def __init__(self, rmq: RabbitMQPool):
        self.rmq = rmq

    @pywss.openapi.docs(
        request=_request_demo,
        response=_response_demp,
    )
    def http_post(self, ctx: pywss.Context):
        start = time.time()
        # 解析请求
        try:
            req = SpiderPayload(**ctx.json())
        except UrlInvalidSchemaErr as e:
            loggus.error(f"请求参数异常: {e}")
            ctx.write(HttpResponse(code=99999, message=f"{e}").dict())
            return
        except Exception as e:
            loggus.error(f"请求参数异常: {e}")
            ctx.write(HttpResponse(code=99999, message="请求参数异常").dict())
            return
        log = loggus.update(uid=req.uid)
        resp = HttpResponse(uid=req.uid, ctx=req.ctx)
        # 异步请求
        if req.callback:
            log = log.update(url=req.url)
            try:
                self.rmq.get_channel(). \
                    basic_publish(
                    exchange='',
                    routing_key=Env.RMQ_QUEUE,
                    body=req.json(),
                    properties=pika.BasicProperties(priority=req.priority),
                )
                resp.message = "异步请求成功"
                log.info(resp.message)
            except:
                try:
                    self.rmq.init()
                    self.rmq.get_channel(). \
                        basic_publish(
                        exchange='',
                        routing_key=Env.RMQ_QUEUE,
                        body=req.json(),
                        properties=pika.BasicProperties(priority=req.priority),
                    )
                    resp.message = "异步请求成功"
                    log.info(resp.message)
                except:
                    resp.code = 99999
                    resp.message = "异步请求异常"
                    log.error(resp.message)
                    log.traceback()
            resp.cost = int(time.time() - start)
            ctx.write(resp.dict())
            return
        # 同步请求
        log.info("开始爬虫任务")
        try:
            resp.data = spider.get(req, log)
        except:
            resp.code = 99999
            resp.message = "爬虫请求异常"
            loggus.update(uid=req.uid).traceback()
        finally:
            resp.cost = int(time.time() - start)
            log.update(cost=resp.cost, url=req.url).info("爬虫任务完成")
        ctx.write(resp.dict())


def main():
    app = pywss.App()
    app.openapi()
    app.get("/", lambda ctx: ctx.redirect("/docs"))
    app.view("/api/v1/url", UrlView)
    app.run()
