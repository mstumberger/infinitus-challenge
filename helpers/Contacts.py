from helpers.Contact import Contact
from helpers.Filter import filter_by_prefix

class Contacts:
    def __init__(self):
        self.CONTACTS = [
            Contact("klic", "v sili", "112"),
            Contact("Klemen", "Klemen", "424242")
        ]

    def action_PUT(self, data: dict):
        result, success, exists = None, False, False
        if 'name' in data.keys() and 'surname' in data.keys() and 'phone' in data.keys():
            for contact in self.CONTACTS:
                if contact.phone == data['phone']:
                    contact.name = data['name']
                    contact.surname = data['surname']
                    success = True
            if not exists:
                self.CONTACTS.append(Contact(data['name'], data['surname'], data['phone']))
                success = True
        else:
            result = 'Prefix is missing!'
        return success, result

    def action_GET(self, data: dict):
        success, result = False, []
        if 'phone' in data:
            for contact in self.CONTACTS:
                if contact.phone == data['phone']:
                    result = contact.__dict__
                    success = True
        else:
            result = 'Prefix is missing!'
        return success, result

    def action_DELETE(self, data: dict):
        success, result = False, None
        if 'phone' in data:
            for contact in self.CONTACTS[:]:
                if contact.phone == data['phone']:
                    self.CONTACTS.remove(contact)
                    result = 'Contact was removed'
                    success = True
        else:
            result = 'Prefix is missing!'
        return success, result

    def action_FIND(self, data: dict):
        success, result = False, None
        if 'prefix' in data:
            result = [contact.__dict__ for contact in filter_by_prefix(data['prefix'], self.CONTACTS)]
            success = True
        else:
            result = 'Prefix is missing!'
        return success, result