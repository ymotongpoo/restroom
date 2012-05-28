# -*- coding: utf-8 -*-

import socket

host = socket.gethostname()
port = 19830

c = socket.socket()
c.connect((host, port))
print c.recv(1024)
c.close()


