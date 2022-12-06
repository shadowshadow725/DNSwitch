import http_server
import dns_server
import threading


if __name__ == '__main__':
    th1 = threading.Thread(target=dns_server.run, args=(), kwargs={})
    th2 = threading.Thread(target=http_server.run, args=(), kwargs={})

    th1.start()
    th2.start()

    print('ready')
