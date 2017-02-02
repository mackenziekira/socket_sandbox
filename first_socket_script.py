# working through python socket programming tutorial at http://www.binarytides.com/python-socket-programming-tutorial/

import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'failed to create socket. error code: ' + str(msg[0]) + ' error message: ' + msg[1]
    sys.exit()

print 'socket created'

host = 'www.github.com'
port = 443

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    print 'hostname could not be resolved. exiting'
    sys.exit()

print 'ip address of ' + host + ' is ' + remote_ip

try:
    s.connect((remote_ip , port))
    print 'socket connected to ' + host + ' on ip ' + remote_ip + ' port ' + str(port)
except socket.error, msg:
    print 'failed to connect to server. error code: ' + str(msg[0]) + ' error message: ' + msg[1]

message = "GET / HTTP/1.1\r\n\r\n"

try:
    s.sendall(message)
except socket.error:
    print 'failed to send'
    sys.exit()

print 'message sent!'
