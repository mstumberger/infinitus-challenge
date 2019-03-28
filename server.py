from datetime import timedelta

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from helpers.Enum import ACTION
from helpers.Contacts import Contacts
import helpers.CustomProtocol as cP
import json
import sys
import uuid
import time


class PozabljivImenik(Protocol):
    CONTACTS = Contacts()
    REQUESTS = {}

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("Connection made")

    def connectionLost(self, reason):
        print("Connection lost", reason)

    def dataReceived(self, data):
        request_id = uuid.uuid4().hex
        self.REQUESTS[request_id] = {"in": time.clock(), "out": None,  "commands": {}}
        data = data.decode('utf-8')
        if data == '\x03':
            self.transport.loseConnection()
            return
        if '\r\n\r\n' in data:
            data = data.split('\r\n\r\n')[1]
        print(data)
        try:
            array_of_commands = cP.decode(data)
            for command in array_of_commands:
                command_id = uuid.uuid4().hex
                self.action(command, request_id, command_id)
            self.REQUESTS.pop(request_id, None)
        except Exception as e:
            print('Error: {}, line number: {}'.format(e, sys.exc_info()[2].tb_lineno))
            self.response(False, 'JSONDecodeError: {}'.format(e), request_id)

    def add_command(self, request_id, command_id, command, execution_time):
        command_information = {
            'command': command,
            'id': command_id,
            'execution_time': execution_time,
            'out': time.clock()}
        self.REQUESTS[request_id]['commands'][command_id] = command_information

    def action(self, command, request_id, command_id):
        try:
            length, data = command
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError as e:
                print('JSONDecodeError: {}, line number: {}'.format(e, sys.exc_info()[2].tb_lineno))
                self.response(False, 'JSONDecodeError: {}'.format(e), request_id, command_id)

            # if length validation is ok
            if cP.encode(data) == "".join(command):
                if 'command' in data:
                    parsed_command = data['command'].upper()
                    if parsed_command == ACTION.PUT:
                        success, result, execution_time = self.CONTACTS.action_PUT(data)
                        self.add_command(request_id, command_id, data, execution_time)

                    elif parsed_command == ACTION.GET:
                        success, result, execution_time = self.CONTACTS.action_GET(data)
                        self.add_command(request_id, command_id, data, execution_time)

                    elif parsed_command == ACTION.DELETE:
                        success, result, execution_time = self.CONTACTS.action_DELETE(data)
                        self.add_command(request_id, command_id, data, execution_time)

                    elif parsed_command == ACTION.FIND:
                        success, result, execution_time = self.CONTACTS.action_FIND(data)
                        self.add_command(request_id, command_id, data, execution_time)

                    else:
                        result = 'Command not found or missing a value'
                        success = False
                else:
                    result = 'Command is missing!'
                    success = False
            else:
                result = 'Command length mismatch'
                success = False

            self.response(success, result, request_id, command_id)
        except Exception as e:
            print('Error: {}, line number: {}'.format(e, sys.exc_info()[2].tb_lineno))
            self.response(False, 'ActionError: {}'.format(e), request_id, command_id)

    def response(self, success, result, request_id, command_id=None):
        encoded_string = cP.encode({'success': success, 'result': result})
        self.transport.write(encoded_string.encode('utf-8'))
        self.REQUESTS[request_id]["out"] = time.clock()
        self.how_long_it_took(encoded_string, request_id, command_id)

    def how_long_it_took(self, response, request_id, command_id):
        print("Request id: {},\ncommand id: {}".format(request_id, command_id))
        print("It took {} s to execute {} command"
              .format(self.REQUESTS[request_id]['commands'][command_id]['execution_time'],
                      self.REQUESTS[request_id]['commands'][command_id]["command"]["command"]))
        print("Response: {}".format(response))
        execution_time = str(timedelta(seconds=self.REQUESTS[request_id]['out'] -
                                               self.REQUESTS[request_id]['in'])).split(":")[2]
        print("It took {} s to execute command from request\n----".format(execution_time))
        self.REQUESTS[request_id].pop(command_id, None)


class PozabljivImenikFactory(Factory):
    def buildProtocol(self, addr):
        return PozabljivImenik(self)


def main():
    reactor.listenTCP(4242, PozabljivImenikFactory())
    reactor.run()


if __name__ == "__main__":
    main()
