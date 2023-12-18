# coding: utf-8
import os
import loggus


class AutoFillMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name == "Env":
            for attrName in attrs.keys():
                if attrName.startswith("_"):
                    continue
                envValue = os.environ.get(attrName, None)
                if envValue is None:
                    continue
                loggus.info(f"检测到环境变量[{attrName}]")
                attrs[attrName] = envValue
        return type.__new__(cls, name, bases, attrs)


class Env(metaclass=AutoFillMetaClass):
    RMQ_HOST = "rmq"
    RMQ_PORT = "5672"
    RMQ_VIRTUAL_HOST = "/"
    RMQ_QUEUE = "urls"
    RMQ_USER = "admin"
    RMQ_PASSWORD = "admin"

    RDS_HOST = "rds"
    RDS_PORT = "6379"
    RDS_DB = "0"
    RDS_PASSWORD = ""

    SELENIUM_REMOTE_SERVER = "http://chrome"
    THIRD_COMPARE_SERVER = ""

    PROXY_SERVER = ""
    PROXY_DEFAULT = ""
    PROXY_POOL = ""

    LOG_FORMAT = "text"

    URL_REPLACE = "《 》 」 、 【 】"

    UA_PC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    UA_ANDROID = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Mobile Safari/537.36'
    UA_IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) Version/10.0 Mobile/14A300 Safari/602.1'
    UA_WECHAT = 'mozilla/5.0 (linux; u; android 4.1.2; zh-cn; mi-one plus build/jzo54k) applewebkit/534.30 (khtml, like gecko) version/4.0 mobile safari/534.30 micromessenger/5.0.1.352'
    UA_ALIPAY = 'Mozilla/5.0 (Linux; U; Android 12; zh-CN; M2102J2SC Build/SKQ1.211006.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.22.2.43 Mobile Safari/537.36 UCBS/3.22.2.43_220223200704 ChannelId(0) NebulaSDK/1.8.100112 Nebula AlipayDefined(nt:4G,ws:393|0|2.75) AliApp(AP/10.2.76.8000) AlipayClient/10.2.76.8000 Language/zh-Hans useStatusBar/true isConcaveScreen/true Region/CNAriver/1.0.0'
    UA_DINGTALK = 'Mozilla/5.0 (Linux; Android 6.0.1; MI MAX Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36 AliApp(DingTalk/3.2.0) com.alibaba.android.rimet/0 Channel/10002068 language/zh-CN'
    UA_WECOM = 'Mozilla/5.0 (Linux; Android 7.1.2; g3ds Build/NJH47F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.2.0 MicroMessenger/6.3.22 NetType/WIFI Language/zh'
    UA_FEISHU = 'Mozilla/5.0 (Linux; Android 9; MI 6X Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.156 Mobile Safari/537.36 Lark/5.10.4 LarkLocale/zh_CN ChannelName/Feishu TTWebView/0751130016452'
    UA_TAOBAO = 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; MI MAX Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.19.0.12 Mobile Safari/537.36 AliApp(TB/8.8.0) UCBS/2.11.1.1 TTID/10003959@taobao_android_8.8.0 WindVane/8.5.0 1080X1920 UT4Aplus/0.2.16'
    UA_WEIBO = 'Mozilla/5.0 (Linux; Android 9; MI 9 SE Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 Weibo (Xiaomi-MI 9 SE__weibo__11.1.3__android__android9)'
    UA_DOUYIN = 'Mozilla/5.0 (Linux; Android 12; M2102J2SC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.156 Mobile Safari/537.36 aweme_210600 JsSdk/1.0 NetType/4G Channel/xiaomi_1128_64 AppName/aweme app_version/21.6.0 ByteLocale/zh-CN Region/CN AppSkin/black AppTheme/dark BytedanceWebview/d8a21c6 TTWebView/0751130025454'
    UA_TOUTIAO = 'Mozilla/5.0 (Linux; Android 12; M2102J2SC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.181 Mobile Safari/537.36 JsSdk/2 NewsArticle/8.8.5 NetType/4g TTWebView/0881130037409'
    UA_ZHIHU = 'Mozilla/5.0 (Linux; Android 12; M2102J2SC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.104 Mobile Safari/537.36 ZhihuHybrid'
    UA_QQ = 'Mozilla/5.0 (Linux; Android 12; M2102J2SC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046011 Mobile Safari/537.36 V1_AND_SQ_8.8.98_3002_YYB_D A_8089800 PA QQ/8.8.98.8410 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/90 SimpleUISwitch/1 QQTheme/2971 InMagicWin/0 StudyMode/0 CurrentMode/1 CurrentFontScale/1.0 GlobalDensityScale/0.9818182 AppId/537124039'

    GFW_BYPASS_PROXY = None

    ICP_API_APPID = ''
    ICP_API_SECRET = ''
