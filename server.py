from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from helpers.Enum import enum
from helpers.Contact import Contact
from helpers.Filter import filter_by_prefix
import json

class PozabljivImenik(Protocol):
    actions = enum(PUT='PUT', GET='GET', DELETE='DELETE', FIND='FIND')
    CONTACTS = []

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("Connection made")

    def connectionLost(self, reason):
        print("Connection lost")

    def dataReceived(self, data):
        data = data.decode('utf-8')
        if data == '\x03':
            self.transport.loseConnection()
            return
        if '\r\n\r\n' in data:
            data = data.split('\r\n\r\n')[1]
            print(data)
            print(type(data))
            data = json.loads(data)
            print(type(data))
            self.action(data)

    def action(self, data):
        success = False
        result = None

        if 'command' in data:
            command = data['command']

            if command == self.actions.PUT:
                # for contact in self.CONTACTS:
                #     if contact.phone != data['phone']:
                        self.CONTACTS.append(Contact(data['name'], data['surname'], data['phone']))
                        success = True

            elif command == self.actions.GET:
                for contact in self.CONTACTS:
                    if contact.phone == data['phone']:
                        result=contact.__dict__
                        success = True

            elif command == self.actions.DELETE:
                for contact in self.CONTACTS[:]:
                    if contact.phone == data['phone']:
                        self.CONTACTS.remove(contact)
                        success = True

            elif command == self.actions.FIND:
                if 'prefix' in data:
                    result = json.dumps([contact.__dict__ for contact in filter_by_prefix(data['prefix'], self.CONTACTS)])
                    success = True
                else:
                    self.response({"success": success, 'result': result, 'reason': 'Prefix is missing!'})

            else:
                self.response({"success": success, 'result': result, 'reason': 'Command not found.'})

            self.response({ "success": success, 'result': result })
        else:
            self.response({"success": success, 'result': result, 'reason': 'Command is missing!'})

    def response(self, data):
        print("response = ", data)
        self.transport.write(bytes(json.dumps(data), 'utf-8'))



class PozabljivImenikFactory(Factory):
    def buildProtocol(self, addr):
        return PozabljivImenik(self)


def main():
    # endpoint = TCP4ServerEndpoint(reactor, 4242)
    # endpoint.listen(PozabljivImenikFactory())
    # reactor.run()
    reactor.listenTCP(4242, PozabljivImenikFactory())
    reactor.run()


if __name__ == "__main__":
    main()