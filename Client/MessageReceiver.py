# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):

    def __init__(self, client, connection):
        super(MessageReceiver, self).__init__()
        self.daemon = True
        self.client = client
        self.connection = connection
        self.start()

    def run(self):
        while True:
            self.client.receive_message(self.connection.recv(1024))