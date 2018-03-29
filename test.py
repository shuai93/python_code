
from functools import  partial, wraps

class A(object):

    def __init__(self):
        print(self.meta.a)
        print(self.__module__)
        print(super())

    class meta:
        a = 1

# def attach_wrapper(obj, func=None):
#     if func is None:
#         print("partial")
#         return partial(attach_wrapper, obj)
#     setattr(obj, func.__name__, func)
#     return func

def ll(func=None, level="aa"):
    if func is None:
        print("aaaaaaaa")
        return partial(ll, level=level)
    @wraps(func)
    def wrapper():
        print("func______")
        return  func()
    return wrapper


@ll
def func():
     n = 1
     return n



if __name__ == "__main__":
    print(func.__module__)
    # print(func.__name__)
    # attach_wrapper(f1)
    func()
    print(ll())