import time
from datetime import datetime


class Time:

    @staticmethod
    def milliseconds():
        return round(time.time() * 1000)

    @staticmethod
    def seconds():
        return round(time.time())

    @staticmethod
    def datetime(formatter='%Y-%m-%d %H:%M:%S'):
        return datetime.now().strftime(formatter)
