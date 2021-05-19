users = {}


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
        else:
            return result
    return inner


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


@exception_handler
def data_parser(user_input):
    data = user_input.split(' ')[1:]

    return data


def hello_func(*args):
    return 'How can I help you?'


@exception_handler
def add_func(data):
    if not users.get(data[0]):
        users.update({data[0]: data[1]})
    else:
        return 'User is already exists'


@exception_handler
def change_func(data):
    if users.get(data[0]):
        users.update({data[0]: data[1]})
    else:
        return 'No user found'


@exception_handler
def phone_func(data):
    if users.get(data[0]):
        return users.get(data[0])
    else:
        return 'No user found'


def show_all_func(*args):
    return users


def exit_func(*args):
    return 'Good bye!'


COMMANDS = {'hello': hello_func,
            'add': add_func,
            'change': change_func,
            'phone': phone_func,
            'show all': show_all_func,
            'exit': exit_func,
            'good bye': exit_func,
            'close': exit_func}


@exception_handler
def get_command_handler(command):
    return COMMANDS[command]


def main():
    while True:
        user_input = input()

        command = command_parser(user_input)
        data = data_parser(user_input)

        operation_handler = get_command_handler(command)
        if operation_handler:
            res = operation_handler(data)
        else:
            continue
        if res:
            print(res)

        if command == 'exit' or command == 'close' or command == 'good bye':
            break


if __name__ == "__main__":
    main()
