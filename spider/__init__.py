# coding: utf-8
import json
import loggus

from spider import basics_spider
from spider import external_spider
from spider import internal_spider
from spider import selenium_spider
from spider import compare_spider
from utils.constant import SpiderPayload


def safe_encoder(obj):
    try:
        return json.dumps(obj)
    except:
        return str(obj)


def get(payload: SpiderPayload, log=loggus):
    basics_payload = basics_spider.get(payload.url)
    resp = {
        "basics": basics_payload.dict(),
    }
    if not basics_payload.is_valid:
        log.warning("检测到非法url，终止爬虫")
        return resp
    typ = set(payload.typ)
    if typ & {"*", "external"}:
        resp["external"] = external_spider.get(basics_payload, log)
    if typ & {"*", "internal"}:
        resp["internal"] = internal_spider.Internal(basics_payload, log).data
    if typ & {"*", "selenium"}:
        resp["selenium"] = selenium_spider.get(basics_payload, log)
    if typ & {"*", "compare"}:
        resp["compare"] = compare_spider.get(basics_payload, log)
    return json.loads(json.dumps(resp, default=safe_encoder))


if __name__ == '__main__':
    from pprint import pprint

    pprint(get(SpiderPayload(
        typ=["*"],
        ctx={},
        url="https://www.baidu.com",
        callback="",
    )))
