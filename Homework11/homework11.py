import re
from collections import UserDict
from datetime import datetime


class Field:

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):

    def __init__(self, value):
        super().__init__(self)
        self.value = value

    def __repr__(self):
        return self.value


class Phone(Field):

    def __init__(self, value):
        super().__init__(self)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) >= 10:
            self.__value = value
        else:
            print('Phone is not correct')

    def is_valid(self):
        return True if self.value else False

    def __repr__(self):
        return self.value


class Birthday(Field):

    def __init__(self, value=None):
        super().__init__(self)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        regex = r'\d{2}.\d{2}.\d{4}'
        if re.search(regex, value):
            self.__value = value
        else:
            print('Not correct date of birth. Must be in format dd.mm.yyyy')

    def is_valid(self):
        return True if self.value else False

    def __repr__(self):
        return self.value


class Record:
    __slots__ = ["name", "phones", "birthday"]

    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = self.add_birthday(birthday)

    def __repr__(self):
        return f'{self.phones}'

    def add_phone(self, phone):
        _phone = Phone(phone)
        if _phone.is_valid():
            self.phones.append(_phone)
        else:
            del _phone

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone1, phone2):
        self.phones.remove(phone1)
        self.phones.append(phone2)

    @staticmethod
    def add_birthday(birthday):
        if birthday:
            _birthday = Birthday(birthday)
            if _birthday.is_valid():
                return _birthday

    def days_to_birthday(self):
        current_date = datetime.now().date()
        if self.birthday.is_valid():
            birthday_date = datetime.strptime(self.birthday.value, '%d.%m.%Y').date().replace(year=current_date.year)
            delta = birthday_date - current_date
            if delta.days < 0:
                new_birthday_date = birthday_date.replace(year=birthday_date.year+1)
                delta = new_birthday_date - current_date
                return delta.days
            else:
                delta = birthday_date - current_date
                return delta.days


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name] = record

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        keys = tuple(self.data.keys())
        if self.index == len(keys):
            self.index = 0
            raise StopIteration

        key = keys[self.index]
        self.index += 1
        item = self.data[key]

        return item.name, item.phones


ad = AddressBook()

tart = Record("alex", '01.08.1985')
tart.add_phone("380674459366")
tart.add_phone("38050")
ad.add_record(tart)

tart2 = Record('Nata')
tart2.add_phone('0972254578')
tart2.add_phone('380504578899')
ad.add_record(tart2)

tart3 = Record('Gosha', '05.07.2004')
tart3.add_phone('80674458965')
ad.add_record(tart3)

print(*tart.phones)
print(tart3.name, tart3.birthday)
print(tart.days_to_birthday())

print(ad)

for item in ad:
    print(item)