# working through python socket programming tutorial at http://www.binarytides.com/python-socket-programming-tutorial/

import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'failed to create socket. error code: ' + str(msg[0]) + ' error message: ' + msg[1]
    sys.exit()

print 'socket created'

host = 'www.google.com'
ports = range(0, 100) 

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    print 'hostname could not be resolved. exiting'
    sys.exit()

print 'ip address of ' + host + ' is ' + remote_ip


for port in ports:
    try:
        s.connect((remote_ip , port))

        print 'socket connected to ' + host + ' on ip ' + remote_ip
    except socket.error, msg:
        print 'failed to connect to server. error code: ' + str(msg[0]) + ' error message: ' + msg[1]
        