from flask import Flask
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

clients =[]

@sockets.route('/chatroom')
def chatroom(ws):
    # anyone who visits this route will become a client
    clients.append(ws)

    while not ws.closed:
        message = ws.receive()

        for client in clients:
            client.send(message)
        
    clients.remove(ws)

    # gunicorn process that (connect) runs your flask code and lets you upgradge to websockets. (flask cannot run on websockets) 