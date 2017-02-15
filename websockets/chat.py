# built based off the heroku tutorial: https://devcenter.heroku.com/articles/python-websockets

import os
import logging
import redis
import gevent
from flask import Flask, render_template
from flask_sockets import Sockets
from chat_class import ChatBackend

REDIS_URL = 'redis://localhost:6379'
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

class ChatBackend(object):
    """registers and updates websocket clients"""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        print 'im at iterdata'
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'sending message: {}'.format(data))
                yield data

    def register(self, client):
        """register a client websocket connection for redis updates"""
        print 'registered ', client
        self.clients.append(client)

    def send(self, client, data):
        """send data to client, or removes client from clients list if no longer a valid connection"""
        try:
            print 'sending ', data, ' to ', client
            client.send(data)
        except Exception:
            print 'removing ', client, data
            self.clients.remove(client)

    def run(self):
        """listen for new messages in redis, sends them to clients"""
        print 'im at run'
        for data in self.__iter_data():
            for client in self.clients:
                print 'running ', client, data
                gevent.spawn(self.send, client, data)

    def start(self):
        """maintain redis subscription in background"""
        print 'started chat backend'
        gevent.spawn(self.run)

chats = ChatBackend()
chats.start()

@app.route('/')
def hello():
    return render_template('index.html')

@sockets.route('/submit')
def inbox(ws):
    """receive incoming chat messages, insert them in redis"""
    while not ws.closed:
        gevent.sleep(0.1)
        message = ws.receive()
        print 'inbox route got', message

        if message:
            app.logger.info(u'Inserting message: {}'.format(message))
            redis.publish(REDIS_CHAN, message)

@sockets.route('/receive')
def outbox(ws):
    """send outgoing chat messages via chatbackend instance"""
    print 'outbox registered this ws client ', ws
    chats.register(ws)

    while not ws.closed:
        gevent.sleep(0.1)

