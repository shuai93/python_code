import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stopped = False
urls_todo = set(range(10))

class Crawler():

    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass

        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped

        chunk = self.sock.recv(1024)
        if chunk:
            self.response += chunk
            
        else:
            selector.unregister(key.fd)
            urls_todo.remove(self.url)

            if not urls_todo:
                stopped = True
def loop():

    while not stopped:

        events = selector.select()

        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)

if __name__ == "__main__":
    import time
    stime = time.time()
    for url in urls_todo:
        c = Crawler(url)
        c.fetch()
    loop()

    print(time.time() - stime)
