import json

def encode(message: dict):
    parsed_message = json.dumps(message).encode('utf8')
    length = len(parsed_message)
    return padhexa(length)+parsed_message

def decode(message: str):
    return message[:4], message[4:]

def padhexa(length: int):
    return str(hex(length)[2:].zfill(4)).encode('utf-8')

if __name__ == "__main__":
    var = """
    The commands are sent to the application using the following custom protocol:

    a)  Each command is sent as a “message”, whose first four bytes (octets), let’s call them “length”,
        specify the length, in bytes, of the remainder of that “message” (let’s call that remainder “payload”).

    b)  “length” is encoded as a zero padded hexadecimal ASCII [0-9a-f].
        Uppercase ASCII letters are not allowed.
        E.g., for a payload of length 42 bytes, the “length” part of the “message” should be “002a”,
        while for a payload of length 4242 bytes, it should be “1092”.

    c)  “payload” contains an utf-8 encoded JSON Object,
        containing at a minimum a key named “command”,
        whose value specifies which command “Pozabljivi imenik” should perform,
        as well as all parameters required by that specific command.
    """
    payload_1 = len(json.dumps({"foo": "bar", "bar": "baz", "baz": 12345}).encode('utf8'))
    print(payload_1, padhexa(payload_1))
    payload_1 = len(json.dumps({"command": "MAKE", "instructions": var}))
    print(payload_1, str(padhexa(payload_1)).lower())
    print(decode(encode({"foo": "bar", "bar": "baz", "baz": 12345})))

    """
    output should be:
        42 002a
        1045 0415
        ('0415', 'marko')
    """

