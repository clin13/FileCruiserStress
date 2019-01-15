import time
from functools import wraps

def retry_auth(ExceptionToCheck, tries=3, delay=1):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try:
                return f(reauth = False, *args, **kwargs)
            except ExceptionToCheck as e:
                msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                #print msg
            time.sleep(mdelay)
            mtries -= 1
            return f(reauth = True, *args, **kwargs)
        return f_retry  # true decorator
    return deco_retry

def normal_retry(tries=3, delay=1):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try:
                return f(*args, **kwargs)
            except Exception as e:
                msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                print(msg)
            time.sleep(mdelay)
            mtries -= 1
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry
