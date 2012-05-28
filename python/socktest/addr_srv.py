# -*- coding: utf-8 -*-

import socket

host = socket.gethostname()
port = 19830

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    print "Request from (%s, %d)" % addr
    c.send("Hello from %s" % host)
    c.close()
    
s.shutdown(socket.SHUT_RDWR)
s.close()
