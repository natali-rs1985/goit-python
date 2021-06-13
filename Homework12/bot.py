from addbook import AddressBook, Phone, Name, Record
import pickle


# декоратор ошибок
def exception_handler(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            print('Please try again')
        except IndexError:
            print('Give all data')
        except ValueError:
            print('Give me correct data')
        except FileNotFoundError:
            print('File not found')
        else:
            return result
    return inner


# из ввода юзера выделяем команды
@exception_handler
def command_parser(user_input):
    user_input = user_input.casefold()
    if user_input == 'show all':
        command = 'show all'
    elif user_input == 'good bye':
        command = 'good bye'
    else:
        command = user_input.split(' ')[0]

    return command


# из ввода юзера выделяем данные для записи в адресную книгу
@exception_handler
def data_parser(user_input):
    data = user_input.split(' ')[1:]

    return data


# функция приветствия
def hello_func(users, data, *args):
    return 'How can I help you?'


# добавляем запись в адресную книгу
@exception_handler
def add_func(users, data):
    name = data[0]
    phone = data[1]
    if not users.name_exists(name):
        record = Record(name)
        if phone:
            record.add_phone(phone)
            users.add_record(record)
    else:
        return 'User is already exist'


# изменяем телефон в адресной книге
@exception_handler
def change_func(users, data):
    phone1 = data[0]
    phone2 = data[1]
    res = users.change_phone(phone1, phone2)
    if not res:
        return 'No user found'


# выводим на экран телефон по имени
@exception_handler
def phone_func(users, data):
    name = data[0]
    if users.name_exists(name):
        name_obj = users.get_record_by_name(name)
        record = users.data[name_obj]
        return record.phones
    else:
        return 'No user found'


# нахождение записи по имени или телефону
def find_func(users, data):
    return users.search_data(data[0])


def add_phone_func(users, data):
    name = data[0]
    phone = data[1]
    if users.name_exists(name):
        users.add_phone(name, phone)
    else:
        return 'No user found'


# выводим на экран всю адресную книгу по несколько записей за раз
def show_all_func(users, data, n=10, *args):
    # n = int(n) if n else 10
    for block in users.iterator(n):
        print(block)
        input('Нажмите  Enter')
    return 'End'


# выход из программы
def exit_func(users, data, *args):
    return 'Good bye!'


COMMANDS = {'hello': hello_func,
            'add': add_func,
            'change': change_func,
            'phone': phone_func,
            'find': find_func,
            'add_phone': add_phone_func,
            'show all': show_all_func,
            'exit': exit_func,
            'good bye': exit_func,
            'close': exit_func}


# функция сохранения записей в файл
def save_result(users, file):
    with open(file, 'wb') as fh:
        pickle.dump(users, fh)


@exception_handler
def get_command_handler(command):
    return COMMANDS[command]


def main():
    file = 'saved_data.bin'
    try:
        with open(file, 'rb') as fh:
            users = pickle.load(fh)
    except Exception as err:
        users = AddressBook()

    while True:

        user_input = input()

        command = command_parser(user_input)
        data = data_parser(user_input)

        operation_handler = get_command_handler(command)
        if operation_handler:
            res = operation_handler(users, data=data)
            save_result(users, file)
        else:
            continue
        if res:
            print(res)

        if command == 'exit' or command == 'close' or command == 'good bye':
            with open(file, 'wb') as fh:
                pickle.dump(users, fh)
            break


if __name__ == "__main__":
    main()
