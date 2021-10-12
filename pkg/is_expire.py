import time


def is_expire(expire_time):
    if expire_time == '--':
        return False
    expire_time = time.mktime(time.strptime(expire_time, "%Y-%m-%d %H:%M:%S"))
    if -15 * 24 * 60 * 60 < int(expire_time) - int(time.time()) < 15 * 24 * 60 * 60:
        return int(expire_time) - int(time.time())
    else:
        return False
