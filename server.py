from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from helpers.Enum import ACTION
from helpers.Contact import Contact
from helpers.Filter import filter_by_prefix
import helpers.CustomProtocol as cP
import json
import sys

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

        try:
            data = json.loads(data)
            print(type(data))
            self.action(data)
        except json.decoder.JSONDecodeError as e:
            print('JSONDecodeError: {}, line number: {}'.format(e, sys.exc_info()[2].tb_lineno))
            self.response(False, None, 'JSONDecodeError: {}'.format(e))

    def action(self, data):
        success = False
        result = None

        if 'command' in data:
            command = data['command']

            if command == ACTION.PUT:
                    exists = False
                    for contact in self.CONTACTS:
                        if contact.phone == data['phone']:
                            exists = True
                            break
                    if not exists:
                        self.CONTACTS.append(Contact(data['name'], data['surname'], data['phone']))
                        success = True
                    else:
                        self.response(success, result, 'Number exists')
                        return

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
                    self.response(success, result, 'Prefix is missing!')
                    return

            else:
                self.response(success, result, 'Command not found.')
                return

            self.response(success, result)
            return
        else:
            self.response(success, result, 'Command is missing!')
            return

    def response(self, success, result, reason=None):
        data = dict()
        data['success'] = success
        data['result'] = result
        if reason is not None:
            data[reason] = reason

        encoded_string = cP.encode(data)
        print(encoded_string)
        self.transport.write(encoded_string)



class PozabljivImenikFactory(Factory):
    def buildProtocol(self, addr):
        return PozabljivImenik(self)


def main():
    reactor.listenTCP(4242, PozabljivImenikFactory())
    reactor.run()


if __name__ == "__main__":
    main()