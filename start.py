import http_server
import dns_server
import threading
import http_proxy
from config import METHOD


if __name__ == '__main__':
    th1 = threading.Thread(target=dns_server.run, args=(), kwargs={})
    th2 = threading.Thread(target=http_server.run, args=(), kwargs={})
    th3 = threading.Thread(target=http_proxy.run, args=(), kwargs={})
    if METHOD == 'DNS':
        th1.start()
    else:
        th3.start()
    th2.start()

    print('ready')
