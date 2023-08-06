import datetime
import time


def get_timestamp(human: bool = None) -> str:
    if human:
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return str(int(time.time()))
