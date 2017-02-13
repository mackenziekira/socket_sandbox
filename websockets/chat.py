# built based off the heroku tutorial: https://devcenter.heroku.com/articles/python-websockets

import os
import logging
import redis
import gevent
from flask import Flask, render_template
from flask_sockets import flask_sockets
from chat_class import ChatBackend

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

chats = ChatBackend()
chats.start()

@app.route('/')
def hello():
    return render_template('index.html')