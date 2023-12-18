# coding: utf-8
import json
import time
import loggus
import spider
import requests
import threading

from utils.env import Env
from utils.closing import Closing
from pika.exceptions import AMQPConnectionError
from utils.constant import SpiderPayload, HttpResponse
from service.rabbitmq import new_connection as new_rabbitmq_connection
from service.redis_service import new_connection  as new_redis_connection


class CallbackHandler:

    def __init__(self):
        self.rds = new_redis_connection()

    def callback(self, ch, frame, properties, body):
        start = time.time()
        try:
            payload = SpiderPayload(**json.loads(body))
            payload.url = str(payload.url)
        except:
            loggus.error("请求解析异常")
            ch.basic_ack(delivery_tag=frame.delivery_tag)
            return
        cacheKey = f"UID:{payload.uid}"
        log = loggus.update(uid=payload.uid)
        resp = HttpResponse(
            uid=payload.uid,
            ctx=payload.ctx,
        )
        try:
            log.info("开始爬虫任务")
            if self.rds.exists(cacheKey):
                resp.code = 99999
                resp.message = "爬虫任务多次重试均异常"
                log.warning(resp.message)
            else:
                self.rds.setex(cacheKey, 3600, payload.url)
                resp.data = spider.get(payload, log)
                resp.message = "爬虫获取成功"
                log.info(resp.message)
        except Exception as e:
            resp.code = 99999
            resp.message = "爬虫获取异常"
            log.update(err=e).error(resp.message)
            log.traceback()
        finally:
            resp.cost = int(time.time() - start)
            log.update(cost=resp.cost, url=payload.url).info("爬虫任务完成")
        retries = 5
        log = log.update(callback=payload.callback)
        while retries > 0:
            try:
                http_response = requests.post(
                    payload.callback,
                    json=resp.dict(),
                )
                if http_response.status_code < 300:
                    log.info("回调成功")
                    break
                log.error(f"回调状态码[{http_response.status_code}]异常[{http_response.text}]")
            except Exception as e:
                log.error(f"回调响应异常：{e}")
            retries -= 1
            time.sleep(3)
        ch.basic_ack(delivery_tag=frame.delivery_tag)


def heartbeat(connection, channel):
    try:
        while not Closing.closed and connection.is_open and channel.is_open:
            time.sleep(5)
    except:
        loggus.error("rmq connect heartbeat error")
    try:
        connection.close()
    except:
        pass


def main():
    ch = CallbackHandler()
    Closing.add_close(lambda: print("server closed"))
    retries = 5
    while not Closing.closed and retries > 0:
        try:
            # 建立连接
            connection, channel = new_rabbitmq_connection()
            Closing.add_close(lambda: connection.close())
            channel.basic_qos(prefetch_count=1)
            # 设置消息处理回调
            channel.basic_consume(queue=Env.RMQ_QUEUE, on_message_callback=ch.callback, auto_ack=False)
            loggus.info("starting consuming")
            threading.Thread(target=heartbeat, args=(connection, channel), daemon=True).start()
            channel.start_consuming()
        except AMQPConnectionError:
            loggus.warning("rmq reconnect")
        except:
            loggus.update(event="rmq connect close").traceback()
        finally:
            try:
                connection.close()
                Closing.closes.pop(None)
            except:
                pass
        time.sleep(10)
        retries -= 1
        loggus.info(f"当前重试次数[{retries}]")
    loggus.update(retries=retries).warning("爬虫消费者退出")


if __name__ == '__main__':
    main()
