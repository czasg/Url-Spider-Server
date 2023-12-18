# coding: utf-8
import signal


class Closing:
    closes = []
    closed = False

    @classmethod
    def add_close(cls, close: callable):
        cls.closes.append(close)

    @classmethod
    def close(cls):
        cls.closed = True
        for close in cls.closes:
            try:
                close()
            except:
                pass


signal.signal(signal.SIGTERM, lambda *args: Closing.close())
signal.signal(signal.SIGINT, lambda *args: Closing.close())
signal.signal(signal.SIGILL, lambda *args: Closing.close())
