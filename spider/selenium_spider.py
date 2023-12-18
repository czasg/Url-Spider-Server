# coding: utf-8
import re
import time
import loggus

from utils.env import Env
from selenium import webdriver
from selenium.webdriver.common.by import By
from spider.basics_spider import BasicsPayload

_META_REFRESH_RE = re.compile('<meta\s*http-equiv="refresh".*?url=(.*?)"\s*/>', re.S)


# _SCRIPT_REDIRECT_RE = re.compile(
#     r'<script(.*)>(.*?)((document\.)?)location((\.href)?)([ |\t ]?)=([ |\t]?)(["|\'])(?P<url>.*?)(["|\'])(;?).*',
#     re.I | re.S)
# _SHORT_REDIRECT_RE = re.compile(
#     r'[(location)|(href)]([ |\t ]?)=([ |\t]?)(["|\'])(?P<url>.*?)(["|\'])(;?).*', re.I | re.S)
# _FRAME_REDIRECT_RE = re.compile(
#     r'<[(frame)|(frameset)|(iframe)].*src([ |\t  ]?)=([ |\t]?)(["|\'])(?P<url>.*?)(["|\'])(;?).*', re.I | re.S)
# _UAE_REDIRECT_RE = re.compile(
#     r'<script(.*)\>(.*?)uaredirect\((["\']?)(?P<url>.*?)(["\']?)\);.*', re.I | re.S)


def get(payload: BasicsPayload, log=loggus):
    start = time.time()
    resp = {
        "title": "",
        "elements": 0,
        "screenshot": "",
        "page_source": {
            "meta_refresh": [],
            "script_redirect": [],
            "short_redirect": [],
            "frame_redirect": [],
            "uae_redirect": [],
        },
    }
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        options.add_experimental_option('prefs', {
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            'safebrowsing.disable_download_protection': True,
        })
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Remote(
            command_executor=Env.SELENIUM_REMOTE_SERVER,
            options=options,
        )
        driver.maximize_window()
        driver.set_page_load_timeout(30)  # 设置页面加载超时时间为30秒
        driver.get(payload.url)
        resp["title"] = driver.title
        resp["elements"] = len(driver.find_elements(By.XPATH, "//*"))
        resp["screenshot"] = driver.get_screenshot_as_base64()
        resp["page_source"].update({
            "meta_refresh": _META_REFRESH_RE.findall(driver.page_source),
            # "script_redirect": _SCRIPT_REDIRECT_RE.findall(driver.page_source),
            # "short_redirect": _SHORT_REDIRECT_RE.findall(driver.page_source),
            # "frame_redirect": _FRAME_REDIRECT_RE.findall(driver.page_source),
            # "uae_redirect": _UAE_REDIRECT_RE.findall(driver.page_source),
        })
        log.update(cost=int(time.time() - start)).info("获取selenium数据成功")
    except Exception as e:
        err_message = str(e)
        if err_message.startswith("Message: timeout: Timed out receiving message from renderer"):
            log.update(cost=int(time.time() - start)).error(f"获取selenium数据异常:请求超时")
        elif err_message.startswith("Message: unknown error: net::ERR_NAME_NOT_RESOLVED"):
            log.update(cost=int(time.time() - start)).error(f"获取selenium数据异常:域名解析失败")
        else:
            log.update(cost=int(time.time() - start)).error(f"获取selenium数据异常:{err_message}")
    finally:
        try:
            driver.quit()
        except:
            pass
    return resp


if __name__ == '__main__':
    print(get(BasicsPayload(
        url="https://www.baidu.com",
        scheme="https",
        host="www.baidu.com",
        domain="baidu.com",
        is_valid=True,
    )))
