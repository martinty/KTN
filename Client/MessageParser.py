import json


class MessageParser:

    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'history': self.parse_history,
            'message': self.parse_message,
        }

    def parse(self, payload):
        payload = json.loads(payload)
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print('Invalid response!')

    def parse_error(self, payload):
        print(payload['timestamp'] + '\t' + 'Error: ' + payload['content'])

    def parse_info(self, payload):
        print(payload['timestamp'] + '\t' + payload['response'] + ': ' + payload['content'])

    def parse_history(self, payload):
        print('Chat history:')
        for index in payload['content']:
            msg = json.loads(index)
            print(msg['timestamp'] + '\t\t' + msg['sender'] + ': ' + msg['content'])

    def parse_message(self, payload):
        print(payload['timestamp'] + '\t' + payload['sender'] + ': ' + payload['content'])