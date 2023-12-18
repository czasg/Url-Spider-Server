# coding: utf-8
import pika
import time
import loggus
import threading

from utils.env import Env

heartbeat = 600


def new_connection():
    credentials = pika.PlainCredentials(Env.RMQ_USER, Env.RMQ_PASSWORD)
    parameters = pika.ConnectionParameters(credentials=credentials, **{
        "host": Env.RMQ_HOST,
        "port": int(Env.RMQ_PORT),
        "virtual_host": Env.RMQ_VIRTUAL_HOST,
        "heartbeat": heartbeat,
    })
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=Env.RMQ_QUEUE, durable=True, arguments={
        "x-max-priority": 100,
    })
    return (connection, channel)


class Pool:

    def __init__(self, expire=heartbeat - 10):
        self.lock = threading.Lock()
        self.expire = expire
        self.connection = None
        self.channel = None
        self.init()

    def init(self):
        with self.lock:
            loggus.info("初始化RMQ")
            try:
                self.channel.close()
            except:
                pass
            try:
                self.connection.close()
            except:
                pass
            self.connection, self.channel = new_connection()
            self.next_expire = int(time.time()) + self.expire

    def is_expire(self) -> bool:
        return int(time.time()) > self.next_expire

    def get_connection(self):
        if self.is_expire():
            self.init()
        return self.connection

    def get_channel(self):
        if self.is_expire():
            self.init()
        with self.lock:
            return self.channel
