# -*- coding: utf-8 -*-

import socket

host = socket.gethostname()
port = 19830

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)

response = ("HTTP/1.0 200 OK\r\n" +
            "Content-Length: 20\r\n" +
            "Content-Type: text/html\r\n" +
            "\r\n" +
            "HELLO\r\n")

print "(host, port) is (%s, %d)" % (host, port)
while True:
    c, addr = s.accept()
    msg = c.recv(1024)
    print msg
    c.send(response)
    c.close()

s.close()
