import time
import functools

print(__file__)
print('hello')


class Test(object):
    pass


def run_time(name='python'):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            print(' {} run time = {}'.format(name, time.time() - start_time))
            return res
        return wrapper
    return decorate


@run_time(name='java')
def test(a: str) -> None:
    print(a)
    time.sleep(2)


if __name__ == "__main__":
    test(1)
