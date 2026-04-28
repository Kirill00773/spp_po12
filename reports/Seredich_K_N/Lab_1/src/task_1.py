"""
Модуль для вычисления медианы списка чисел.

Запрашивает у пользователя количество чисел и сами числа,
после чего выводит медиану.
"""


def median(numbers: list[int]) -> float:
    """
    Возвращает медиану списка чисел.

    :param numbers: Список целых чисел
    :return: Медиана списка
    """
    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)
    mid = length // 2

    if length % 2 == 1:
        return float(sorted_numbers[mid])

    return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2


def main() -> None:
    """
    Точка входа в программу.

    Считывает данные пользователя и выводит медиану.
    """
    count = int(input("Введите количество чисел: "))
    nums = list(map(int, input("Введите числа через пробел: ").split()))

    if len(nums) != count:
        print("Предупреждение: количество введённых чисел не совпадает.")

    result = median(nums)
    print(f"Медиана: {result}")


if __name__ == "__main__":
    main()
