from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from helpers.Enum import ACTION
from helpers.Contact import Contact
from helpers.Filter import filter_by_prefix
import helpers.CustomProtocol as cP
import json

class PozabljivImenik(Protocol):
    CONTACTS = [
        Contact("klic", "v sili", "112"),
        Contact("Klemen", "Klemen", "424242")
    ]

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

            if command == ACTION.PUT:
                # for contact in self.CONTACTS:
                #     if contact.phone != data['phone']:
                        self.CONTACTS.append(Contact(data['name'], data['surname'], data['phone']))
                        success = True

            elif command == ACTION.GET:
                for contact in self.CONTACTS:
                    if contact.phone == data['phone']:
                        result=contact.__dict__
                        success = True

            elif command == ACTION.DELETE:
                for contact in self.CONTACTS[:]:
                    if contact.phone == data['phone']:
                        self.CONTACTS.remove(contact)
                        success = True

            elif command == ACTION.FIND:
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
        encoded_string = cP.encode(data)
        print(encoded_string)
        self.transport.write(encoded_string)



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