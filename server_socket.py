# script written w help from the following sources:
# https://ruslanspivak.com/lsbaws-part1/
# https://docs.python.org/2/howto/sockets.html

import socket
import sys

PORT = 8888
HOST = socket.gethostname()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.bind((HOST, PORT))

socket.listen(5)

print 'socket listening at port ' + str(PORT) + ' on host ' + HOST

while True:
    (clientsocket, address) = socket.accept()
    request = clientsocket.recv(1024)
    print request

    http_response = """\
    HTTP/1.1 200 OK

    Hello, world!
    """
    clientsocket.sendall(http_response)
    clientsocket.close()
