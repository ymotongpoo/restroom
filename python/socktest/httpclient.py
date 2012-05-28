# -*- coding: utf-8 -*-

import socket

host = socket.gethostbyname("q.ymotongpoo.com")
port = socket.getservbyname('http', 'tcp')

in_addr = socket.inet_aton(host)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((in_addr, port))
s.send("GET /index.html HTTP/1.0\r\n\r\n")

while True:
    msg = s.recv(1024)
    print(msg)

    if len(msg) == 0:
        break

s.close()
