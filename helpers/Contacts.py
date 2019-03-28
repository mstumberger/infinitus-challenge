from helpers.Contact import Contact
from helpers.Filter import filter_by_prefix
import time
from datetime import timedelta


class Contacts:
    CONTACTS = [
        Contact("klic", "v sili", "112"),
        Contact("Klemen", "Klemen", "424242")
    ]

    def action_PUT(self, data: dict):
        start = time.clock()
        result, success = None, False
        if 'name' in data.keys() and 'surname' in data.keys() and 'phone' in data.keys():
            for contact in self.CONTACTS:
                if contact.phone == data['phone']:
                    contact.name = data['name']
                    contact.surname = data['surname']
                    success = True
            if not success:
                self.CONTACTS.append(Contact(data['name'], data['surname'], data['phone']))
                success = True
        else:
            result = 'Prefix is missing!'
        end = time.clock()
        execution_time = str(timedelta(seconds=end-start)).split(":")[2]
        return success, result, execution_time

    def action_GET(self, data: dict):
        start = time.clock()
        success, result = False, []
        if 'phone' in data:
            for contact in self.CONTACTS:
                if contact.phone == data['phone']:
                    result = contact.__dict__
                    success = True
        else:
            result = 'Prefix is missing!'

        end = time.clock()
        execution_time = str(timedelta(seconds=end-start)).split(":")[2]
        return success, result, execution_time

    def action_DELETE(self, data: dict):
        start = time.clock()
        success, result = False, 'Contact was not found'
        if 'phone' in data:
            for contact in self.CONTACTS[:]:
                if contact.phone == data['phone']:
                    self.CONTACTS.remove(contact)
                    result = 'Contact was removed'
                    success = True
        else:
            result = 'Prefix is missing!'

        end = time.clock()
        execution_time = str(timedelta(seconds=end-start)).split(":")[2]
        return success, result, execution_time

    def action_FIND(self, data: dict):
        start = time.clock()
        success, result = False, None
        if 'prefix' in data:
            result = [contact.__dict__ for contact in filter_by_prefix(data['prefix'], self.CONTACTS)]
            success = True
        else:
            result = 'Prefix is missing!'
        end = time.clock()
        execution_time = str(timedelta(seconds=end-start)).split(":")[2]
        return success, result, execution_time
