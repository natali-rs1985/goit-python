import re
import json
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
        if value.isdigit() and 9 <= len(value) <= 12:
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
        return f'{self.name.value}:{self.phones}'

    def __str__(self):
        return f'{self.name.value}:{self.phones}'

    def add_phone(self, phone):
        _phone = Phone(phone)
        if _phone.is_valid():
            if _phone not in self.phones:
                self.phones.append(_phone)
            else:
                return 'This number is already exist'
        else:
            del _phone

    def remove_phone(self, phone):
        for i in self.phones:
            if phone == i.value:
                self.phones.remove(i)
        else:
            return 'This number not in address book'

    def change_phone(self, phone1, phone2):
        self.remove_phone(phone1)
        self.add_phone(phone2)

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

    def search(self, data):
        if data.casefold() in self.name.value.casefold():
            return self
        for phone in self.phones:
            if data.casefold() in phone.value.casefold():
                return self
        return False

    def get_by_name(self, name):
        if name.casefold() == self.name.value.casefold():
            return self.name
        return False

    def get_by_phone(self, phone):
        for i in self.phones:
            if phone == i.value:
                return self.name
        return False


class AddressBook(UserDict):

    def add_record(self, record):
        if record.name not in self:
            self.data[record.name] = record
        else:
            return 'Record with this name is already exist'

    def __repr__(self):
        return "\n".join([str(v) for v in self.data.values()])

    def iterator(self, n):
        # print(n, type(n))
        # n = int(n)
        k = 0
        key_list = list(self)
        key_list_max = len(key_list)
        while k < key_list_max:
            result = AddressBook()
            max_iter = key_list_max if len(key_list[k:]) < n else k + n
            for i in range(k, max_iter):
                result.add_record(self[key_list[i]])
                k += 1
            yield result

    def search_data(self, data):
        result = AddressBook()
        for record in self.data.values():
            search_record = record.search(data)
            if search_record:
                result.add_record(search_record)
        return result

    def get_record_by_name(self, name):
        for record in self.data.values():
            name = record.get_by_name(name)
            if name:
                return name
        return False

    def name_exists(self, name):
        names = set([x.value for x in self.data.keys()])
        return name in names

    def change_phone(self, phone_old, phone_new):
        for record in self.data.values():
            name = record.get_by_phone(phone_old)
            if name:
                self.data[name].change_phone(phone_old, phone_new)
                return True
        return False

    def add_phone(self, name, phone):
        name_obj = self.get_record_by_name(name)
        if name_obj:
            self.data[name_obj].add_phone(phone)
            return True
        return False


if __name__ == '__main__':
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
    print(isinstance(ad.data, dict))

    print(ad.__dict__)

    for item in ad:
        print(item)

