# -*- coding: utf-8 -*-
import socket, json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


class Client:

    def __init__(self, host, server_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = server_port
        self.host = host
        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))
        MessageReceiver(self, self.connection)
        print('Welcome too our chat server. You need to login!')
        while True:
            msg = raw_input('> ').split()
            try:
                self.create_request(msg[0], ' '.join(msg[1:]))
            except:
                print("Invalid input!")

    def disconnect(self):
        self.connection.shutdown(2)
        self.connection.close()

    def receive_message(self, message):
        parser = MessageParser()
        parser.parse(message)

    def send_payload(self, data):
        self.connection.send(json.dumps(data))

    def create_request(self, request, content):
        payload = {'request': request, 'content': content,}
        self.send_payload(payload)


if __name__ == '__main__':
    client = Client('localhost', 9998)