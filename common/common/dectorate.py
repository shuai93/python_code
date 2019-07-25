#!/usr/bin/env python3  
# @Time    : 18-1-19 上午11:48
# @Author  : ys
# @Email   : youngs@yeah.net
import tornado.gen


class mylocker:
    def __init__(self):
        print("mylocker.__init__() called.")

    @staticmethod
    def acquire():
        print("mylocker.acquire() called.")

    @staticmethod
    def unlock():
        print("  mylocker.unlock() called.")


class lockerex(mylocker):
    @staticmethod
    def acquire():
        print("lockerex.acquire() called.")

    @staticmethod
    def unlock():
        print("  lockerex.unlock() called.")


def lockhelper(cls):
    """
    cls 必须实现acquire和release静态方法
    :param cls: 
    :return: 
    """
    def _deco(func):
        def __deco(*args, **kwargs):
            print("before %s called." % func.__name__)
            cls.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                cls.unlock()

        return __deco

    return _deco


class Example(object):
    @lockhelper(mylocker)
    def myfunc(self):
        print(" myfunc() called.")

    @lockhelper(mylocker)
    @lockhelper(lockerex)
    def myfunc2(self, a, b):
        print(" myfunc2() called.")
        return a + b


# 实现 add(1)(2) 闭包的实现
def add(a):
    def fun(b):
        return a + b
    return fun


# 简单的类装饰器
def Tracer(aClass):
    class Wrapper:
        def __init__(self, *args, **kargs):
            self.fetches = 0
            self.wrapped = aClass(*args, **kargs)

        def __getattr__(self, attrname):
            print('Trace: ' + attrname)
            self.fetches += 1
            print(self.fetches)
            return getattr(self.wrapped, attrname)

    return Wrapper

@Tracer
class Person:
    def __init__(self,name,hours,rate):
        self.name = name
        self.hours = hours
        self.rate = rate
    def pay(self):
        return self.hours * self.rate


@Tracer
class Spam:

    def display(self):
        print('Spam!' * 8)


if __name__ == "__main__":
    print(add(1)(2))
    spam = Spam()
    spam.display()


    # a = Example()
    # a.myfunc()
    # print(a.myfunc())
    # print(a.myfunc2(1, 2))
    # print(a.myfunc2(3, 4))
