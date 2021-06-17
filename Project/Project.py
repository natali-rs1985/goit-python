################################################################################
#         Note book classes                                                    #
################################################################################

from collections import UserDict
from datetime import datetime
from datetime import date
from pathlib import Path
import math
import re
import json

from Sort_files import sort_files



class Notebook(UserDict):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 3

    def add_note(self, note):
        self.data[note.id] = note

    # dump to json file###################################
    def dump(self, file):
        with open(file, 'w+') as write_file:
            dump_dict = {self.name: {}}
            for id in self.data.keys():
                dump_dict[self.name][str(id)] = {}
                dump_dict[self.name][str(id)]["keyword"] = [x for x in self.data[id].keyword]
                dump_dict[self.name][str(id)]["note"] = self.data[id].note
            json.dump(dump_dict, write_file)
            print("Note book '" + self.name + "' exported to the file")

    # restore from json file #############################
    def load(self, file):
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            print("Starting download from json")
            self.name = list(data.keys())[0]
            print("The name of note book ", self.name)
            for id in list(data[self.name].keys()):
                note_ = Note(data[self.name][id]["note"])
                if "keyword" in data[self.name][id].keys():
                    for k in data[self.name][id]["keyword"]:
                        if k not in note_.keyword:
                            note_.keyword.append(k)
                self.add_note(note_)
            print("Notes have been loaded from file")

    def delete(self, id):
        if id in self.data.keys():
            self.data.pop(id)

    def __iter__(self):
        return self

    def __next__(self):
        print("Len of note book dictionary ", len(list(self.data.keys())))
        if self.current_page < int(math.ceil(len(list(self.data.keys())) / self.records_on_the_page)):
            keys = list(self.data.keys())
            r_list = []
            for i in range(self.current_page * self.records_on_the_page,
                           min([(self.current_page + 1) * self.records_on_the_page, len(self.data)])):
                a_dict = {}
                a_dict["ID"] = keys[i]
                print(i)
                a_dict["Keyword"] = [x for x in self.data[keys[i]].keyword]
                a_dict["Note"] = self.data[keys[i]].note
                r_list.append(a_dict)
            self.current_page += 1
            return r_list
        else:
            self.current_page = 0
        raise StopIteration

    def find(self, request_lst):
        if type(request_lst) == type(" "):
            request_lst = list(request_lst.split(" "))
        res_lst = []
        for teg in request_lst:
            teg = (
                teg.replace("+", "\+")
                    .replace("*", "\*")
                    .replace("{", "\{")
                    .replace("}", "\}")
                    .replace("[", "\[")
                    .replace("]", "\]")
                    .replace("?", "\?")
                    .replace("$", "\$")
                    .replace("'\'", "\\")
                    .lower()
            )
            for id in self.data:
                if re.search(teg, " ".join(self.data[id].keyword).lower()) != None or re.search(teg, self.data[
                    id].note.lower()) != None:
                    if self.data[id] not in res_lst:
                        res_lst.append(self.data[id])
        return res_lst


class Note():
    id = 0

    def __init__(self, note):
        Note.id += 1
        self.id = Note.id
        self.keyword = []
        self.keyword = self.get_keywords(note)
        self.note = note

    def get_keywords(self, note):
        result_lst = []
        result = re.finditer("#[a-zA-Zа-яА-Я_\-\в]+", note)
        for group in result:
            result_lst.append(group.group(0)[1:])
        return result_lst

    def __str__(self):
        wide_str = len("###########################################################")
        str_res = "      ID: " + str(self.id) + "\n" + "      Keywords:"
        kw_str = ""
        str_count = 0
        for k in self.keyword:
            if str_count == wide_str:
                kw_str = kw_str + "\n"
                str_count = 0
            kw_str = kw_str + " #" + k
            str_count += len(" #" + k)
        str_res = str_res + kw_str
        str_res = str_res + "\n"
        str_count = 0
        for i in range(len(self.note)):
            if str_count == wide_str:
                str_res = str_res + "\n"
                str_count = 0
            str_res = str_res + self.note[i]
            str_count += 1
        return str_res

    ################################################################################


#         Adress book classes                                                    #
################################################################################


class AddressBook(UserDict):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 40

    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_page < int(math.ceil(len(self.data) / self.records_on_the_page)):
            keys = list(self.data.keys())
            r_list = []
            for i in range(self.current_page * self.records_on_the_page,
                           min([(self.current_page + 1) * self.records_on_the_page, len(self.data)])):
                a_dict = {}
                a_dict["Name"] = keys[i]
                a_dict["Phones"] = [x.value for x in self.data[keys[i]].phones]
                if type(self.data[keys[i]].birthday) != type(""):
                    a_dict["Birthday"] = str(self.data[keys[i]].birthday.value)
                if type(self.data[keys[i]].address) != type(""):
                    a_dict["Address"] = self.data[keys[i]].address.value
                if type(self.data[keys[i]].email) != type(""):
                    a_dict["Email"] = str(self.data[keys[i]].email.value)
                r_list.append(a_dict)
            self.current_page += 1
            return r_list
        else:
            self.current_page = 0
        raise StopIteration

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)

    def dump(self, file):
        with open(file, 'w+') as write_file:
            dump_dict = {self.name: {}}
            store_records_on_the_page = self.records_on_the_page
            self.records_on_the_page = 1
            id = 1
            for page in self:
                dump_dict[self.name]["RecID" + str(id)] = page[0]
                id += 1
            json.dump(dump_dict, write_file)
            self.records_on_the_page = store_records_on_the_page
            print("Adress book " + self.name + " exported to the file")

    def load(self, file):
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            self.name = list(data.keys())[0]
            for name in list(data[self.name].keys()):
                record = data[self.name][name]
                rec = Record(record["Name"])
                if "Phones" in record.keys():
                    for phone in record["Phones"]:
                        rec.add_phone(Phone(phone))
                if "Birthday" in record.keys():
                    lst = record["Birthday"].split("-")
                    birthday = Birthday(lst[2] + "." + lst[1] + "." + lst[0])
                    rec.add_birthday(birthday)
                if "Address" in record.keys():
                    rec.add_address(Address(record["Address"]))
                if "Email" in record.keys():
                    rec.add_email(Email(record["Email"]))

                self.add_record(rec)
            print("Data have been loaded from file")

    def find(self, request):
        result_lst = []
        for name in self.data.keys():
            search_list = [name]
            search_list.extend([phone.value for phone in self.data[name].phones])
            for field in search_list:
                if request[0] == '+':
                    request = request[1:]
                if re.search(request.upper(), field.upper()) != None:
                    result_lst.append(name)
                    break
        return result_lst


class Record:
    def __init__(self, name):
        self.phones = list()
        self.birthday = ""
        self.email = ""
        self.address = ""
        self.name = Name(name)

    def add_keywords(self, keywords):
        self.keywords = keywords

    def add_notes(self, notes):
        self.notes = notes

    def add_phone(self, phone):
        if phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(phone)

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address

    def del_phone(self, phone):
        self.phones = list(filter(lambda x: x.value != phone, self.phones))

    def edit_phone(self, phone, new_phone):
        if phone in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(Phone(new_phone))

    def add_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if type(self.birthday) != type(""):
            date1 = datetime(datetime.now().timetuple().tm_yday, self.birthday.value.timetuple().tm_mon,
                             self.birthday.value.timetuple().tm_mday)
            delta = date1.timetuple().tm_yday - datetime.now().timetuple().tm_yday
            if delta > 0:
                return str(delta)
            else:
                date1 = datetime(datetime.now().timetuple().tm_year + 1, self.birthday.value.timetuple().tm_mon,
                                 self.birthday.value.timetuple().tm_mday)
                date2 = datetime(datetime.now().timetuple().tm_year, datetime.now().timetuple().tm_mon,
                                 datetime.now().timetuple().tm_mday)
                delta = date1 - date2
            return str(delta.days)
        return str(1000)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(f"{self.__dict__}")

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value_):
        if len(value_) > 0:
            self.__value = value_


class Name(Field):
    def __init__(self, name):
        self.__value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def set_value(self, value):
        if len(value) > 0:
            self.__value = value


class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if re.search('\+\d{12}', phone) != None:
            self.__value = phone
        else:
            raise ValueError("Phone should be in the next format: '+XXXXXXXXXXXX' (12 digits)")


class Email(Field):
    def __init__(self, email):
        self.value = email

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, email):
        if re.search('[a-zA-Z0-9\.\-\_]+@[a-zA-Z\.]+.[a-z]{2,4}', email) != None:
            self.__value = email
        else:
            raise ValueError("Email should be in the next format: 'name@[domains].high_level_domain'")


class Address(Field):
    def __init__(self, address):
        self.value = address

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, address):
        self.__value = address


class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday):
        if re.search('\d{2}\.\d{2}\.\d{4}', birthday) != None:
            self.__value = datetime.strptime(birthday, '%d.%m.%Y').date()
        else:
            return False


################################################################################
#         CLI BOT section                                                      #
################################################################################

exit_command = ["good bye", "close", "exit"]


def format_phone_number(func):
    def inner(phone):
        result = func(phone)
        if len(result) == 12:
            result = '+' + result
        else:
            result = '+38' + result
        return result

    return inner


@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone


def hello_(data):
    return "How can I help You?"


def add_phone(name):
    while True:
        phone = choose_phone()
        if phone == 'exit':
            return 0
        if phone not in [ph.value for ph in a.data[name].phones]:
            a.data[name].add_phone(Phone(phone))
            print("Phone number succesfully added")
            return 1
        else:
            print("This number already belonged to contact " + name + ", please try again")


def add_email(name):
    while True:
        print("Input email for the contact " + name)
        email = input()
        if email == 'exit':
            return 0
        else:
            try:
                a.data[name].add_email(Email(email))
                print("Email succesfully added")
            except:
                print("incorrect email format. Try again")
                continue
            return 1


def add_address(name):
    address_dict = {}
    print("Input address for the contact " + name)
    address_dict["country"] = input("Input country: ")
    address_dict["zip"] = input("Input ZIP code: ")
    address_dict["region"] = input("Input region: ")
    address_dict["city"] = input("Input city: ")
    address_dict["street"] = input("Input street: ")
    address_dict["building"] = input("Input building: ")
    address_dict["apartment"] = input("Input apartment: ")
    a.data[name].add_address(Address(address_dict))
    print("Address succesfully added")


def add_birthday(name):
    birthday = choose_date()
    if birthday == 'exit':
        print("Operation canselled")
    else:
        b = Birthday(birthday)
        a.data[name].add_birthday(b)
        print("Birthday setted successfully")
    return "Please choose command"


############################# add the record to address book ####################################################

def add_contact(data):
    while True:
        print("Input the name of a contact")
        name = input()
        if name not in a.data.keys():
            r = Record(name)
            a.add_record(r)
            break
        else:
            print("Contact with that name already exists. Try again")
    while True:
        print("Type 'P' to add phone number, 'O' skip to add other details")
        choose = input().lower()
        if choose == 'p':
            add_phone(name)
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Print 'E to enter e-mail or 'O' to add other details")
        choose = input().lower()
        if choose == 'e':
            add_email(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Print 'A to enter address or 'O' to add other details")
        choose = input().lower()
        if choose == 'a':
            add_address(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Print 'B' to enter birthday or 'F' to finish with contact details")
        choose = input().lower()
        if choose == 'b':
            add_birthday(name)
            break
        if choose == 'f':
            print("OK, let's finish with " + name)
            break
    print("Contact details saved")
    return "Please choose command"


############################# edit the record in address book ####################################################

def edit_contact(data):
    name = choose_record()
    if name == 'exit':
        print("Operation canselled")
        return "Please choose command"

    while True:
        print("Type 'N' to edit a name of a contact, 'O' to edit other details")
        choose = input().lower()
        if choose == 'n':
            print("Please give me a new name for a contact: " + name)
            name_new = input()
            a.data[name_new] = a.data[name]
            a.data.pop(name)
            name = name_new
            print("The name of a contact succesfully changed")
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Type 'P' to edit phone list, 'O' skip to edit other contact details")
        choose = input().lower()
        if choose == 'p':
            print("Existing phone numbers for the contact " + name)
            for ph in a.data[name].phones:
                print("      " + ph.value)
            while True:
                print(
                    "Type 'A' to add new phone, 'E' to edit phone, 'D' for delete existing one, 'O' skip to other details")
                choose_p = input().lower()
                if choose_p == 'a':
                    add_phone(name)
                elif choose_p == 'e':
                    while True:
                        print("I need the old number to change")
                        phone = choose_phone()
                        if phone == 'exit':
                            print("Operation canselled")
                            break
                        if phone in [ph.value for ph in a.data[name].phones]:
                            print("I need the new number to save")
                            phone_new = choose_phone()
                            a.data[name].edit_phone(phone, phone_new)
                            print("Phone changed succesfully")
                        else:
                            print("This number doesn't belong to the " + name)
                            continue
                        break
                elif choose_p == 'd':
                    while True:
                        print("input the phone number you would like to delete")
                        phone = choose_phone()
                        if phone == 'exit':
                            print("Operation canselled")
                            break
                        elif phone in [ph.value for ph in a.data[name].phones]:
                            a.data[name].del_phone(phone)
                            print("Phone deleted succesfully")
                            break
                        else:
                            print("This number doesn't belong to the " + name + " Try again")
                elif choose_p == 'o':
                    print("OK, let's go ahead")
                    break
                break
        elif choose == "o":
            print("OK, let's go ahead")
            break
    while True:
        print("Print 'E to edit the e-mail or 'O' to edit other details")
        choose = input().lower()
        if choose == 'e':
            if type(a.data[name].email) != type(""):
                print("Current email for the record " + name + " is:" + a.data[name].email.value)
            add_email(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Print 'A to edit the address or 'O' to skip for other details")
        choose = input().lower()
        if choose == 'a':
            if type(a.data[name].address) != type(""):
                print("Current saved address for record " + name + " is:")
                for key in record["address"].keys():
                    print("            " + key + " " * (len("apartment") - len(key)) + ": " + record["address"][key])

            add_address(name)
            break
        if choose == 'o':
            print("OK, let's go ahead")
            break
    while True:
        print("Print 'B' to edit birthday or 'F' to finish with contact details")
        choose = input().lower()
        if choose == 'b':
            if type(a.data[name].address) != type(""):
                print("Current saved birthday for record " + name + " is: " + a.data[name].birthday.value)
            add_birthday(name)
            break
        if choose == 'f':
            print("OK, let's finish with " + name)
            break
    print("Contact details saved")
    return "Please choose command"


def find_contacts(data):
    res_lst = []
    print("Please input info to search. It could be the name, phone number or even a part of them")
    search_str = input().rstrip()
    search_str = (
        search_str.strip()
            .replace("+", "\+")
            .replace("*", "\*")
            .replace("{", "\{")
            .replace("}", "\}")
            .replace("[", "\[")
            .replace("]", "\]")
            .replace("?", "\?")
            .replace("$", "\$")
            .replace("'\'", "\\")

    )

    res_lst = a.find(search_str)
    if res_lst == []:
        print("Couldn't find records in the phone book")
    else:
        print("Found next contacts:")
        for contact in res_lst:
            print(contact)
            for ph in a.data[contact].phones:
                print("       " + ph.value)
    return "Please choose command"


def show_all(data):
    print("test of show all")
    adress_book = a
    for page in adress_book:
        for record in page:
            print("Name:", record["Name"])
            print("      Phone list:")
            for phone in record["Phones"]:
                print("      " + phone)
            if "Email" in record.keys():
                print("      Email: ", record["Email"])
            if "Address" in record.keys():
                print("      Address: ")
                str_address = record["Address"].replace("{", "").replace("}", "").replace("'", "")
                for pair in str_address.split(","):
                    print("            " + pair.split(":")[0].strip().capitalize() + " " * (
                                len("apartment:") - len(pair.split(":")[0].strip())) + ": " + pair.split(":")[1])
            if "Birthday" in record.keys():
                print("      Birthday: ", record["Birthday"])
        input("Press enter to continue")
    return "Please choose command"


def help_(command):
    print("List of available commands: ")
    for key in exec_command.keys():
        print(exec_command[key][1])
    print("exit:      Exit program ('good by', 'close' also works)")
    return "Please choose command"


def choose_record():
    print("Please enter the name of a contact")
    while True:
        name = input().lower
        if name in a.data.keys().lower():
            break
        elif name.lower() == 'exit':
            break
        else:
            print("Couldn`t find exactly this name in adress book.")
            print("Here are the list of the contacts with similar spelling:")
            for c in a.find(name):
                print("     " + c)
            print("Please try to choose the name again or type 'Exit' to come back to main menu")
    return name


def choose_phone():
    print("Please enter the phone number")
    while True:
        phone = input().lower()
        if phone == 'exit':
            break
        is_correct_format = re.search("\+?[\ \d\-\(\)]+$", phone)
        phone = sanitize_phone_number(phone)
        if is_correct_format != None and len(phone) == 13:
            break
        else:
            print("Phone number is incorrect format, please try again or type 'Exit' to come back to main menu")
    return phone


def choose_date():
    print("Please enter the date of birthday in format dd.mm.yyyy")
    while True:
        birthday = input().lower()
        is_correct_format = re.search("\d{2}[\/\.\:]\d{2}[\/\.\:]\d{4}", birthday)
        if is_correct_format != None:
            birthday = birthday.replace("/", ".")
            birthday = birthday.replace(":", ".")
            b_array = birthday.split(".")
            try:
                datetime.strptime(birthday, '%d.%m.%Y').date()
            except ValueError:
                print("You gave me incorrect date, be carefull nex time")
            else:
                break
        elif birthday == 'exit':
            break
        print("Date has incorrect format, please try again or type 'Exit' to come back to main menu")
    return birthday


def delete_contact(command):
    choose = ""
    while True:
        name = choose_record()
        if name == 'exit':
            print("Operation canselled")
            return "Please choose command"
        while True:
            print("Find a contact " + name + ", are you sure to delete it? Please type Y/N?")
            choose_d = input().lower()
            if choose_d == 'y':
                a.delete(name)
                print("Contact " + name + " deleted")
                return "Please choose command"
            elif choose_d == 'n':
                print("Operation canselled")
                return "Please choose command"
            else:
                print("Make a correct choise, please")
        return "Please choose command"

    ############################# add the note to note book ####################################################


def add_note(command):
    while True:
        print("Input the text of your note here. Use a hashtags # for key_words. Allowed to use copy/paste to speed up")
        note = Note(input())
        if len(note.keyword) == 0:
            print("You forgot to add a keywords, please let me them, using # and separate them by spaces")
            input_str = input("#Key words: ")
            lst = input_str.split(" ")
            for kw in lst:
                note.keyword.append(kw[1:])
        n.add_note(note)
        break

    return "Please choose command"


############################# edit the note  ####################################################
def edit_note(command):
    while True:
        res_lst = []
        print(
            "Input the keywords for the note you would like to edit (You could input a couple of keywords separated by spaces)")
        input_str = input()
        res_lst = n.find(input_str)
        if res_lst != []:
            print("I found some notes connected to your request:")
            for result in res_lst:
                print(result)
                print("###########################################################")
            break
        elif input_str.lower() == 'exit':
            print("Operation canselled")
            return 0
        else:
            print("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    while True:
        choose = input("Input ID of note you would like to edit: ")
        if choose in [str(x.id) for x in res_lst]:
            print("Keywords: ", ["# " + k for k in n.data[int(choose)].keyword])
            print("----------------- you could copy here ------------------------")
            print(n.data[int(choose)].note)
            print("------------------ avoid new line character when copy --------")
            print("You could use copy/paste to speed up. Use # to mark up keywords")
            new_text = input()
            note_temp = Note(new_text)
            print("Please add a keywords for a note, separated by space.")
            kw_lst = input("Keywords: ").split(" ")
            print(kw_lst)
            note_temp.keyword.extend(kw_lst)
            n.data[int(choose)] = note_temp
            print("Note succesfully changed")
            break
        elif choose.lower() == 'exit':
            print("Operation cancelled")
            break
        else:
            print("Make a correct choice")
            continue
        break

    return "Please choose command"


############################# delete the note ####################################################
def delete_note(command):
    while True:
        res_lst = []
        print("Input the keyword for the note you would like to delete")
        input_str = input("You could input a couple of keywords separated by spaces: ")
        res_lst = n.find(input_str)
        if len(res_lst) != 0:
            print("I found some notes connected to your request:")
            for result in res_lst:
                print(result)
                print("###########################################################")
            while True:
                choose = input("Input ID of note you would like to delete: ")
                if choose in [str(x.id) for x in res_lst]:
                    n.delete(int(choose))
                    print("Note succesfully deleted")
                    break
                elif choose.lower() == 'exit':
                    print("Operation cancelled")
                    break
                else:
                    print("Make a correct choice")
                    continue
            break

        elif input_str.lower() == 'exit':
            print("Operation cancelled")
            break

        else:
            print("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    return "Please choose command"


def find_notes(command):
    while True:
        res_lst = []
        print("Input the keyword for the note you would like to find")
        input_str = input("Allowed input of multiply keywords separated by spaces: ")
        res_lst = n.find(input_str)
        if len(res_lst) != 0:
            print("I found some notes connected to your request:")
            for result in res_lst:
                print(result)
            break
        elif input_str.lower() == 'exit':
            print("Operation cancelled")
            break
        else:
            print("Couldn't find notes with specified keywords, try again or type 'exit'")
            continue
    return "Please choose command"


############################# show all the notes ####################################################
def show_notes(command):
    for page in n:
        for record in page:
            print("      ID:", record["ID"])
            print("      Keywords: ", ["#" + kw for kw in record["Keyword"]])
            print("      Text of note: ")
            print(record["Note"])
            print("###########################################################")
        input("Press enter to continue")
    return "Please choose command"


############################# sorting the notes by keywords list ####################################################
def sort_notes(command):
    sort_notebook = Notebook("temp")
    sort_notebook.data = dict(sorted(n.data.items(), key=lambda item: sorted(item[1].keyword, key=lambda x: x.upper())))
    n.data = sort_notebook.data
    for item in n.data.keys():
        n.data[item].keyword = sorted(n.data[item].keyword, key=lambda x: x.upper())
        print(n.data[item])
        print("###########################################################")
    print("Sorting completed")
    return "Please choose command"


def sort_folder(command):
    src_path = Path(input('Enter folder to sort in format Disc:\\\Folder\\\Folder to sort :\n'))
    sort_files(src_path)
    print("Sorting completed")
    return "Please choose command"


def next_birthday(command):
    res_lst = []
    while True:
        print("Please let me know how many days in the period that we are looking for birthdays")
        days = input()
        try:
            period = int(days)
            if period > 365 or period <= 0:
                print("Incorrect period, should be between 0 and 365 days")
                continue
            else:
                for name in a.data.keys():
                    if int(a.data[name].days_to_birthday()) < period:
                        res_lst.append(a.data[name])
                if len(res_lst) > 0:
                    print("List of contacts that have birthday in ", days, " days:")
                    for res in res_lst:
                        print("Name ", res.name.value, ", birthday ", str(res.birthday.value))
                else:
                    print("I'm sorry, couldn't find any")
                break
        except:
            print("Incorrect input, should be numeric between 0 and 365 days")
            continue
    return "Please choose command"


def save_(data):
    a.dump("Work telephones.json")
    n.dump("Work notes.json")
    return "Please choose command"


exec_command = {
    "hello": [hello_, "hello:     Greetings", 0],
    "add contact": [add_contact, "add contact:        Add a new contact", 2],  # adopted to the project needs
    "edit contact": [edit_contact, "edit contact:       Edit the contact detail", 2],  # adopted to the project needs
    "find contact": [find_contacts, "find contact:       Find the records by phone or name", 1],
    # adopted to the project needs
    "find notes": [find_notes, "find notes:         Find the notes by text or keywords", 1],
    # adopted to the project needs
    "show all contacts": [show_all, "show all contacts:  Print all the records of adress book, page by page", 0],
    # adopted to the project needs
    "show all notes": [show_notes, "show all notes:     Print all the records of adress book, page by page", 0],
    # adopted to the project needs
    "help": [help_, "help:               Print a list of the available commands", 0],  # adopted to the project needs,
    "add note": [add_note, "add note:           Add new text note ", 0],  # adopted to the project needs
    "edit note": [edit_note, "edit note:          Edit existing text note ", 0],  # adopted to the project needs
    "delete contact": [delete_contact, "delete contact:     Delete contact", 2],  # adopted to the project needs,
    "delete note": [delete_note, "delete note:        Delete text note", 2],  # adopted to the project needs,
    "sort notes": [sort_notes, "sort note:          Sort of the notes by keywords", 2],  # adopted to the project needs
    "sort folder": [sort_folder, "sort folder:          Sort selected folder by file types", 2],
    # adopted to the project needs
    "next birthday": [next_birthday, "next birthday:      Let you the contats with birthdays in specified period", 2],
    # adopted to the project needs
    "save": [save_, "save:               Save the current state of data to disk", 0]  # adopted to the project needs,

}


def handler(command, data):
    return exec_command[command][0](data.replace(command + " ", ""))


def parser(input_str):
    for token in exec_command.keys():
        if token in input_str:
            return handler(token, input_str.replace(token + " ", ""))
    return "Input error, please type 'help' for commands description"


def listener():
    command = ""
    communication_str = "CLI phone book bot looking for command"
    while (command) not in exit_command:
        print(communication_str + ": ")
        command = input().lower()
        communication_str = parser(command)


a = AddressBook("Work telephones")
n = Notebook("Work notes")
try:
    a.load("Work telephones.json")
except:
    print("Couldn't find file, starting with empty adress book")

try:
    n.load("Work notes.json")
except:
    print("Couldn't load file, starting with empty note book")

listener()
try:
    a.dump("Work telephones.json")
except:
    print("Couldn't save file, all the changes could be loose")