
import socket
import json


CONTACTS = [
    {"name": "Ruthe", "surname": "Van der Beken", "phone": "+60-293-920-4517"},
    {"name": "Lynn", "surname": "Blacket", "phone": "+62-746-315-8965"},
    {"name": "Duky", "surname": "Batch", "phone": "+7-812-344-9366"},
    {"name": "Linet", "surname": "Holson", "phone": "+420-310-583-5311"},
    {"name": "Tobit", "surname": "Arrigo", "phone": "+55-998-548-8754"},
    {"name": "Nick", "surname": "Buttrick", "phone": "+66-402-232-7380"},
    {"name": "Sheela", "surname": "Messier", "phone": "+93-208-735-9619"},
    {"name": "Catlee", "surname": "Cream", "phone": "+27-206-370-3889"},
    {"name": "Codi", "surname": "Portch", "phone": "+251-699-931-9665"},
    {"name": "Kamillah", "surname": "Enderson", "phone": "+63-521-684-4803"},
]


def main(address="127.0.0.1", port=4242):

    messages = []
    for contact in CONTACTS:
        command = dict(command="PUT", **contact)
        payload = json.dumps(command).encode("utf-8")
        length = b"%04x" % len(payload)
        message = length + payload
        messages.append(message)

    sock = socket.socket()
    sock.connect((address, port))
    sock.sendall(b"".join(messages))
    sock.close()


if __name__ == "__main__":
    main()

