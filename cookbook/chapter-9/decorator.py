from functools import wraps
import logging

def decorator(func):

    @wraps(func)
    def wraps(*args, **kwargs):
        print("decorator")
        return func(*args, **kwargs)



def logged(level, name=None, message=None):
    """
    logging function
    """

    def decorate(func):
        logname= name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrappers(*args, **kwargs):
            print("level = {}, logmsg = {}, logname = {}".format(level, logmsg, logname))
            log.log(level, logmsg)
            return func(*args, **kwargs)

        return wrappers

    return decorate

@logged(logging.DEBUG)
def add(x, y):
    return x + y


def sub(x, y):
    return x - y


if __name__ == "__main__":
    # print(logging.DEBUG)
    print(add(3, 2))