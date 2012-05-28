# -*- coding: utf-8 -*-

import socket

host = "localhost"
port = 19830

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    msg = raw_input("type message:")
    s.sendall(msg)
    if msg == "":
        s.close()
        break
