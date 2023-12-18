# coding: utf-8
import re
import time
import loggus
import base64
import whois
import requests
import dns.resolver
import requests.utils

from utils.env import Env
from bs4 import BeautifulSoup
from utils.proxy import proxy
from utils.transform import any2str, any2list
from spider.basics_spider import BasicsPayload
from concurrent.futures.thread import ThreadPoolExecutor


def cdn(host):
    try:
        resolver = dns.resolver.Resolver()
        result = resolver.resolve(host, dns.rdatatype.CNAME)
        if not result:
            return "", 0
        for answer in result.response.answer:
            for key in answer.items.keys():
                return key.to_text().strip("."), answer.ttl
    except:
        return "", 0


def icp(domain) -> dict:
    try:
        return requests.get(
            "https://www.mxnzp.com/api/beian/search",
            params={
                "domain": base64.b64encode(domain.encode("utf-8")),
                "app_id": Env.ICP_API_APPID,
                "app_secret": Env.ICP_API_SECRET,
            },
            proxies=proxy.get_http_proxy(),
            timeout=10,
        ).json()["data"] or {}
    except:
        return {}


def has_sitemap(meta: BasicsPayload) -> bool:
    try:
        return requests.get(
            f"{meta.scheme}://{meta.host}/sitemap.xml",
            headers={
                "User-Agent": Env.UA_PC,
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
            },
            timeout=10,
            proxies=proxy.get_http_proxy(),
        ).status_code < 400
    except:
        return False


def bing(url):
    try:
        search_url = f"https://www.bing.com/search?q=site:{url}"
        headers = {
            "User-Agent": Env.UA_PC,
            'Accept': '*/*',
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
        }
        response = requests.get(search_url, headers=headers, proxies=proxy.get_http_proxy(), timeout=10)
        if '没有与此相关的结果:' in response.text:
            return 0
        soup = BeautifulSoup(response.text, 'html.parser')
        result_stats = soup.find(class_='sb_count')
        if result_stats is not None:
            count = re.search(r'\d{1,}', result_stats.text.replace(',', '')).group(0)
            return int(count)
    except:
        pass
    return 0


def google(url):
    try:
        search_url = f"https://www.google.com/search?q=site:{url}"
        headers = {
            "User-Agent": Env.UA_PC,
            'Accept': '*/*',
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
        }
        response = requests.get(search_url, headers=headers, timeout=4, proxies=proxy.get_http_proxy())
        soup = BeautifulSoup(response.text, 'html.parser')
        result_stats = soup.find(id='result-stats')
        if result_stats is not None:
            count = re.search('\d{1,}', result_stats.text.replace(',', '')).group(0)
            return int(count)
    except:
        pass
    return 0


def baidu(url):
    try:
        search_url = f"https://www.baidu.com/s?wd=site:{url}"
        headers = {
            "User-Agent": Env.UA_PC,
            'Accept': '*/*',
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
        }
        response = requests.get(search_url, headers=headers, proxies=proxy.get_http_proxy(), timeout=10)
        if '抱歉没有找到与' in response.text:
            return 0
        stats = re.search("找到相关结果数约(.*?)个", response.text)
        if stats:
            return int(stats.group(0).replace(",", ""))
    except:
        pass
    return 0


def get(payload: BasicsPayload, log=loggus):
    start = time.time()
    resp = {
        "org": "",
        "creation_date": [],
        "expiration_date": [],
        "country": "",
        "state": "",
        "whois_server": "",
        "emails": [],
        "name_servers": [],
        "registrar": "",
        "cdn_name": "",
        "domain_ttl": 0,
        "icp": {},
        "has_sitemap": False,
        "search_engine": {
            "bing": 0,
            "google": 0,
            "baidu": 0,
        }
    }

    def update_whois():
        try:
            who = whois.whois(payload.url)
            resp.update({
                "org": any2str(who.org),
                "creation_date": any2list(who.creation_date),
                "expiration_date": any2list(who.expiration_date),
                "country": any2str(who.country),
                "state": any2str(who.state),
                "whois_server": any2str(who.whois_server),
                "emails": any2list(who.emails),
                "name_servers": any2list(who.name_servers),
                "registrar": any2str(who.registrar),
            })
        except:
            pass

    def update_cdn():
        try:
            cname, ttl = cdn(payload.host)
            resp.update({
                "cdn_name": any2str(cname),
                "domain_ttl": ttl,
            })
        except:
            pass

    def update_icp():
        try:
            resp["icp"] = icp(payload.domain)
        except:
            pass

    def update_sitemap():
        try:
            resp["has_sitemap"] = has_sitemap(payload)
        except:
            pass

    def update_bing():
        try:
            resp["search_engine"]["bing"] = bing(payload.domain)
        except:
            pass

    def update_google():
        try:
            resp["search_engine"]["google"] = google(payload.domain)
        except:
            pass

    def update_baidu():
        try:
            resp["search_engine"]["baidu"] = baidu(payload.domain)
        except:
            pass

    try:
        with ThreadPoolExecutor(7) as executor:
            executor.submit(update_whois)
            executor.submit(update_cdn)
            executor.submit(update_icp)
            executor.submit(update_sitemap)
            executor.submit(update_bing)
            executor.submit(update_google)
            executor.submit(update_baidu)
        log.update(cost=int(time.time() - start)).info("获取external数据成功")
    except Exception as e:
        log.update(cost=int(time.time() - start)).error(f"获取external数据异常:{e}")
    return resp


if __name__ == '__main__':
    print(get(BasicsPayload(
        url="https://www.baidu.com",
        scheme="https",
        host="www.baidu.com",
        domain="baidu.com",
        is_valid=True,
    )))
