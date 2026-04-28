"""Модуль для вычисления суммы квадратов отрицательных чисел."""

N = int(input("Введите количество чисел: "))

sum_of_squares = 0

for i in range(N):
    num = int(input(f"Введите число {i+1}: "))
    if num < 0:
        sum_of_squares += num ** 2

print("Сумма квадратов отрицательных чисел:", sum_of_squares)
