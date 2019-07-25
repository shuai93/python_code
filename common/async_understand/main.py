'''

'''


import socket
import time

from concurrent import futures

def blocking_way():
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
    return response

def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    return len([fut.result() for fut in futs])


if __name__ == "__main__":
    stime = time.time()
    # print(process_way())
    print(blocking_way())

    print(time.time() - stime)