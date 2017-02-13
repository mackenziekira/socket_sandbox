class ChatBackend(object):
    """registers and updates websocket clients"""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'sending message: {}'.format(data))
                yield data

    def register(self, client):
        """register a client websocket connection for redis updates"""
        self.clients.append(client)

    def send(self, client, data):
        """send data to client, or removes client from clients list if no longer a valid connection"""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """listen for new messages in redis, sends them to clients"""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """maintain redis subscription in background"""
        gevent.spawn(self.run)