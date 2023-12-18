# coding: utf-8
import time
import loggus
import warnings
import requests
import requests.utils

from bs4 import BeautifulSoup
from utils.env import Env
from utils.proxy import proxy
from Wappalyzer import Wappalyzer, WebPage
from spider.basics_spider import BasicsPayload
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures.thread import ThreadPoolExecutor

warnings.filterwarnings("ignore", category=UserWarning)
w = Wappalyzer.latest()
user_agents = [
    ('desktop', Env.UA_PC),
    ('android', Env.UA_ANDROID),
    ('iphone', Env.UA_IPHONE),
    ('wechat', Env.UA_WECHAT),
    ('alipay', Env.UA_ALIPAY),
]


class Internal:

    def __init__(self, payload: BasicsPayload, log=loggus):
        self.start = time.time()
        self.log = log
        self.data = {
            "langs": [],
            "programs": [],
            "similar": {
                "desktop": 0,
                "android": 0,
                "iphone": 0,
                "wechat": 0,
                "alipay": 0,
            },
            "elements": 0,
        }
        self.payload = payload
        self.responses = [None, None, None, None, None]
        self.useable_response = None

        def ua_requests(index, key, user_agent):
            try:
                self.responses[index] = (key, requests.get(
                    self.payload.url,
                    headers={
                        'User-Agent': user_agent,
                    },
                    timeout=26,
                    proxies=proxy.get_http_proxy(),
                ))
            except:
                self.responses[index] = (key, None)

        with ThreadPoolExecutor(5) as executor:
            for index in range(len(user_agents)):
                key, user_agent = user_agents[index]
                executor.submit(ua_requests, index, key, user_agent)

        for _, response in self.responses:
            if response and response.status_code == 200:
                self.useable_response = response
                break
        self.parse()

    def parse(self):
        if not self.useable_response:
            self.log.update(cost=int(time.time() - self.start)).warning("获取internal数据异常")
            return
        self.parse_html()
        self.parse_programs()
        self.parse_similar()
        self.log.update(cost=int(time.time() - self.start)).info("获取internal数据成功")

    def parse_html(self):
        text = self.useable_response.text
        try:
            soup = BeautifulSoup(text, 'lxml')
            self.data["elements"] = len(soup.find_all())
            lang = soup.html.get('lang')
            if lang:
                self.data["langs"].append(lang)
                return
        except:
            pass
        if '"zh"' in text:
            self.data["langs"].append("zh")
        if '"en"' in text:
            self.data["langs"].append("en")

    def parse_programs(self):
        try:
            resp = self.useable_response
            webpage = WebPage.new_from_response(resp)
            technologies = w.analyze(webpage)
            self.data["programs"] += list(technologies)
        except:
            pass

    def parse_similar(self):
        try:
            for key, response in self.responses:
                html = (response and response.text) or ""
                ratio_total = 0.0
                for _key, _response in self.responses:
                    if _key == key:
                        continue
                    _html = (_response and _response.text) or ""
                    vectorizer = CountVectorizer()
                    corpus = [_html, html]
                    vectors = vectorizer.fit_transform(corpus)
                    similarity = cosine_similarity(vectors)
                    ratio_total += similarity[0][1]
                self.data["similar"][key] = ratio_total / (len(self.responses) - 1)
        except:
            pass


if __name__ == '__main__':
    print(Internal(BasicsPayload(
        url="https://wordpress.com/zh-cn/",
        scheme="https",
        host="wordpress.com",
        domain="wordpress.com",
        is_valid=True,
    )).data)
