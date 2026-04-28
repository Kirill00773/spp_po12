"""
Модуль для увеличения числа, представленного списком цифр, на 1.

Пользователь вводит цифры через пробел.
Программа прибавляет единицу к числу и выводит результат.
"""


def increment_digits(digits: list[int]) -> list[int]:
    """
    Прибавляет 1 к числу, представленному списком цифр.

    :param digits: Список цифр (0-9)
    :return: Новый список цифр после увеличения на 1
    """
    result = digits.copy()
    index = len(result) - 1

    while index >= 0 and result[index] == 9:
        result[index] = 0
        index -= 1

    if index < 0:
        result.insert(0, 1)
    else:
        result[index] += 1

    return result


def main() -> None:
    """
    Точка входа в программу.

    Считывает цифры пользователя и выводит число + 1.
    """
    digits = list(map(int, input("Введите цифры через пробел: ").split()))
    incremented = increment_digits(digits)
    print(*incremented)


if __name__ == "__main__":
    main()
