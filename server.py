from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from helpers.Enum import ACTION
from helpers.Contacts import Contacts
import helpers.CustomProtocol as cP
import json
import sys


class PozabljivImenik(Protocol):
    CONTACTS = Contacts()

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("Connection made")

    def connectionLost(self, reason):
        print("Connection lost", reason)

    def dataReceived(self, data):
        data = data.decode('utf-8')
        if data == '\x03':
            self.transport.loseConnection()
            return
        if '\r\n\r\n' in data:
            data = data.split('\r\n\r\n')[1]

        try:
            array_of_commands = cP.decode(data)
            for command in array_of_commands:
                self.action(json.loads(command[1]))
        except json.decoder.JSONDecodeError as e:
            print('JSONDecodeError: {}, line number: {}'.format(e, sys.exc_info()[2].tb_lineno))
            self.response(False, 'JSONDecodeError: {}'.format(e))

    def action(self, data):
        try:
            if 'command' in data:
                command = data['command'].upper()
                if command == ACTION.PUT:
                    success, result = self.CONTACTS.action_PUT(data)

                elif command == ACTION.GET:
                    success, result = self.CONTACTS.action_GET(data)

                elif command == ACTION.DELETE:
                    success, result = self.CONTACTS.action_DELETE(data)

                elif command == ACTION.FIND:
                    success, result = self.CONTACTS.action_FIND(data)

                else:
                    result = 'Command not found or missing a value'
                    success = False
            else:
                result = 'Command is missing!'
                success = False

            self.response(success, result)
        except Exception as e:
            print('Error: {}, line number: {}'.format(e, sys.exc_info()[2].tb_lineno))
            self.response(False, 'ActionError: {}'.format(e))

    def response(self, success, result):
        encoded_string = cP.encode({'success': success, 'result': result})
        print(encoded_string)
        self.transport.write(encoded_string.encode('utf-8'))


class PozabljivImenikFactory(Factory):
    def buildProtocol(self, addr):
        return PozabljivImenik(self)


def main():
    reactor.listenTCP(4242, PozabljivImenikFactory())
    reactor.run()


if __name__ == "__main__":
    main()
