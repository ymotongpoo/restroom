# -*- coding: utf-8 -*-

import socket

host = socket.gethostname()
port = 19830

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
print "bind socket..."
s.listen(1)

print "Waining for connections..."
clientsock, clientaddr = s.accept()

print "loop...."
while True:
    rcvmsg = clientsock.recv(1024)
    print "%s" % rcvmsg
    if rcvmsg == "":
        break

clientsock.shutdown(socket.SHUT_RDWR)
clientsock.close()
