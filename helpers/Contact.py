class Contact (object):
    def __init__(self, name: str, surname: str, phone:str):
        self.name = name
        self.surname = surname
        self.phone = phone

    def to_string(self):
        return "Name: {},\nSurname: {},\nPhone: {}".format(self.name, self.surname, self.phone)