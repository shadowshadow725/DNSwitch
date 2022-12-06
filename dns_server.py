#!/usr/bin/python3

import re
import sys
import socket
import traceback
from config import DNS_PORT, ADDRESS, IP


HOSTS_FILE = "hosts.txt"

SERVER_HOST = IP
SERVER_PORT = DNS_PORT


class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.domain = bytearray()
        tipo = (data[2] >> 3) & 15
        if tipo == 0:
            ini = 12
            lon = data[ini]
            while lon != 0:
                self.domain += data[ini + 1:ini + lon + 1] + bytes(".", "ascii")
                ini += lon + 1
                lon = data[ini]
        self.domain = str(self.domain, "utf8").rstrip(".")

    def response(self, ip):
        packet = bytearray()
        if self.domain:
            packet += self.data[:2] + bytearray([0x81, 0x80])
            packet += self.data[4:6] + self.data[4:6] + bytearray([0x00, 0x00, 0x00, 0x00])  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += bytearray([0xC0, 0x0C])  # Pointer to domain name
            packet += bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x3c, 0x00, 0x04])  # Response type, ttl and resource data length -> 4 bytes
            packet += bytearray([int(x) for x in ip.split(".")])  # 4 bytes of IP
        return packet


def parse_host_file_as_regex():
    host_list = []
    host_list.append([re.compile(ADDRESS), SERVER_HOST])
    return host_list


def run():
    host_data = parse_host_file_as_regex()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_HOST, SERVER_PORT))
    print("DNS Proxy server started on UDP port {}!".format(SERVER_PORT))
    while True:
        try:
            (data, addr) = sock.recvfrom(1024)
            p = DNSQuery(data)
            result = [ip_addr for (regex, ip_addr) in host_data if regex.search(p.domain)]
            if result:
                ip = result[0]
                print("Local:  {} -> {}".format(p.domain, ip))
                sock.sendto(p.response(ip), addr)
            else:
                ip = socket.gethostbyname(p.domain)
                print("Remote: {} -> {}".format(p.domain, ip))
                sock.sendto(p.response(ip), addr)
        except KeyboardInterrupt:
            print("Done!")
            sock.close()
            sys.exit(0)
        except:
            traceback.print_exc()
