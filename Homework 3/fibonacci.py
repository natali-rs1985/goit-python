def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def main():
    n = int(input('Введите n: '))
    result = fibonacci(n)
    print(result)


if __name__ == '__main__':
    main()
