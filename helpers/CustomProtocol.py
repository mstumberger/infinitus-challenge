import json
import re


def encode(message: dict):
    parsed_message = json.dumps(message, ensure_ascii=True)
    length = len(parsed_message)
    return padhexa(length)+parsed_message


def decode(message: str):
    array = re.findall(r'([a-f0-9]{4})({[^}]+})', message)
    return array


def padhexa(length: int):
    return str(hex(length)[2:].zfill(4))


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
    # payload_1 = len(json.dumps({"foo": "bar", "bar": "baz", "baz": 12345}, ensure_ascii=True))
    # print(payload_1, padhexa(payload_1))
    # payload_1 = len(json.dumps({"command": "MAKE", "instructions": var}))
    # print(payload_1, str(padhexa(payload_1)).lower())
    # print(decode(encode({"foo": "bar", "bar": "baz", "baz": 12345})))
    string = '005c{"command": "PUT", "name": "Ruthe", "surname": "Van der Beken", "phone": "+60-293-920-4517"}0055{"command": "PUT", "name": "Lynn", "surname": "Blacket", "phone": "+62-746-315-8965"}0052{"command": "PUT", "name": "Duky", "surname": "Batch", "phone": "+7-812-344-9366"}0056{"command": "PUT", "name": "Linet", "surname": "Holson", "phone": "+420-310-583-5311"}0055{"command": "PUT", "name": "Tobit", "surname": "Arrigo", "phone": "+55-998-548-8754"}0056{"command": "PUT", "name": "Nick", "surname": "Buttrick", "phone": "+66-402-232-7380"}0057{"command": "PUT", "name": "Sheela", "surname": "Messier", "phone": "+93-208-735-9619"}0055{"command": "PUT", "name": "Catlee", "surname": "Cream", "phone": "+27-206-370-3889"}0055{"command": "PUT", "name": "Codi", "surname": "Portch", "phone": "+251-699-931-9665"}005a{"command": "PUT", "name": "Kamillah", "surname": "Enderson", "phone": "+63-521-684-4803"}'
    search_pattern = r"([a-f0-9]{4})({[^}]+})"
    array1 = re.findall(search_pattern, string)
    print(array1)
    for item in array1:
        print(item)

    """
    output should be:
        42 002a
        1045 0415
        ('0415', 'marko')
42 b'002a'
1045 b'0415'
(b'002a', b'{"foo": "bar", "bar": "baz", "baz": 12345}')
    """

