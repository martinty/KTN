# -*- coding: utf-8 -*-
import SocketServer, json, time, datetime

connectedClients = {}
clientNames = []
history = []

class ClientHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.loginFlag = False
        self.client = ''

        while True:
            received_string = self.connection.recv(4096)
            jsonObject = json.loads(received_string)
            request = jsonObject['request']
            content = jsonObject['content']

            if not self.loginFlag and request == 'login':
                self.loginReq(content)
            elif request == 'help':
                self.helpReq()
            elif self.loginFlag:
                if request == 'msg':
                    self.msgReq('message', content)
                elif request == 'names':
                    self.namesReq()
                elif request == 'history':
                    self.historyReq()
                elif request == 'logout':
                    self.logoutReq()
                else:
                    self.reqResponder('error', 'Invalid request, type "help" for info')
            else:
                self.reqResponder('error', 'Invalid request, type "help" for info')

    def validUsername(self, username):
        validChar = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        for char in username:
            if char not in validChar:
                return False
        return True

    def isUsernameFree(self, username):
        if username in clientNames:
            return False
        else:
            return True

    def namesReq(self):
        userList = clientNames
        userList = ', '.join(userList)
        self.reqResponder('info', userList)

    def logoutReq(self):
        del connectedClients[self.connection]
        self.loginFlag = False
        clientNames.remove(self.client)
        self.reqResponder('info', 'You are now logged out')

    def historyReq(self):
        self.reqResponder('history', history)

    def loginReq(self, username):
        if self.validUsername(username) and self.isUsernameFree(username):
            self.client = username
            connectedClients[self.connection] = self.client
            clientNames.append(self.client)
            self.loginFlag = True
            self.reqResponder('info', 'Login successfull')
            self.historyReq()
        else:
            self.reqResponder('error', 'Invalid username or username already in use')

    def helpReq(self):
        if self.loginFlag:
            self.reqResponder('info', 'Available requests are: msg, history, names and logout')
        else:
            self.reqResponder('info', 'Available request is login')

    def msgReq(self, response, message):
        data = self.jsonMsgGenerator(response, message)
        for client in connectedClients:
            client.send(data)
        history.append(data)

    def jsonMsgGenerator(self, response, message):
        return json.dumps(
            {
                'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'sender': self.client,
                'response': response,
                'content': message,
            }
        )

    def reqResponder(self, response, content):
        data = json.dumps(
            {
                'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'sender': self.client,
                'response': response,
                'content': content,
                }
        )
        if response == 'message':
            history.append(data)

        self.connection.send(data)
        print('--> [', self.ip, ']:', data)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    allow_reuse_address = True

if __name__ == "__main__":

    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
