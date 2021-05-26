from collections import UserDict


class Field:
    pass


class Name(Field):
    __slots__ = ["name"]

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Phone(Field):
    __slots__ = ["phone"]

    def __init__(self, phone):
        self.phone = phone

    def __repr__(self):
        return self.phone


class Record:
    __slots__ = ["name", "phones"]

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __repr__(self):
        return "{0}".format(self.phones)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone1, phone2):
        self.phones.remove(phone1)
        self.phones.append(phone2)


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name] = record


ad = AddressBook()
tart = Record("alex")
tart.add_phone("38067")
tart.add_phone("38050")
ad.add_record(tart)

print(tart.phones[1])
print(ad)
