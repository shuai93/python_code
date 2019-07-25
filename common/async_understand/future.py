import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stopped = False
urls_todo = set(range(10))

class Future():
    
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)



class Crawler():

    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass

        f = Future()
        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        get = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
        sock.send(get.encode('ascii'))
        global stopped
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break

class Task():
    
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)

def loop():

    while not stopped:

        events = selector.select()

        for event_key, _ in events:
            callback = event_key.data
            callback()

if __name__ == "__main__":
    import time
    stime = time.time()
    for url in urls_todo:
        c = Crawler(url)
        Task(c.fetch())
    loop()

    print(time.time() - stime)
