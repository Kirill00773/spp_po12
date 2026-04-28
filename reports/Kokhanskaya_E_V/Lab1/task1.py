n = int(input("Введите количество чисел (N): "))
numbers = []

print(f"Введите {n} чисел:")
for _ in range(n):
    num = int(input())
    numbers.append(num)

unique_numbers = set(numbers)
print("Результат:", *unique_numbers)
