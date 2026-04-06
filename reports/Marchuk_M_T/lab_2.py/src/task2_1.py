"""
Модуль для работы с классом IsoscelesTriangle.
Реализует расчет площади, периметра и проверку существования.
"""
import math


class IsoscelesTriangle:
    """Класс для представления равнобедренного треугольника."""

    def __init__(self, base, side):
        """Инициализация сторон треугольника."""
        self._base = float(base)
        self._side = float(side)

    @property
    def base(self):
        """Возвращает основание треугольника."""
        return self._base

    @base.setter
    def base(self, value):
        """Устанавливает основание треугольника."""
        if value <= 0:
            raise ValueError("Сторона должна быть положительной")
        self._base = value

    @property
    def side(self):
        """Возвращает боковую сторону треугольника."""
        return self._side

    @side.setter
    def side(self, value):
        """Устанавливает боковую сторону треугольника."""
        if value <= 0:
            raise ValueError("Сторона должна быть положительной")
        self._side = value

    def is_exists(self):
        """Проверка существования: сумма двух боковых сторон больше основания."""
        return 2 * self._side > self._base > 0 and self._side > 0

    def get_perimeter(self):
        """Возвращает периметр треугольника."""
        if not self.is_exists():
            return 0.0
        return self._base + 2 * self._side

    def get_area(self):
        """Возвращает площадь треугольника."""
        if not self.is_exists():
            return 0.0
        # h = sqrt(side^2 - (base/2)^2)
        height = math.sqrt(self._side**2 - (self._base / 2)**2)
        return 0.5 * self._base * height

    def __str__(self):
        """Строковое представление объекта."""
        if self.is_exists():
            return f"Равнобедренный треугольник (основание={self._base}, бедра={self._side})"
        return "Треугольник с такими сторонами не существует"

    def __eq__(self, other):
        """Сравнение двух треугольников."""
        if not isinstance(other, IsoscelesTriangle):
            return False
        return self._base == other.base and self._side == other.side


def main():
    """Интерактивная проверка класса."""
    print("--- Тестирование класса Треугольник ---")
    b_val1 = input("Введите основание треугольника 1: ")
    s_val1 = input("Введите боковую сторону треугольника 1: ")
    tri1 = IsoscelesTriangle(b_val1, s_val1)

    b_val2 = input("Введите основание треугольника 2: ")
    s_val2 = input("Введите боковую сторону треугольника 2: ")
    tri2 = IsoscelesTriangle(b_val2, s_val2)

    while True:
        print("\nМЕНЮ:")
        print(f"1. Показать данные (T1: {tri1})")
        print("2. Расчитать периметр и площадь T1")
        print("3. Проверить существование T1")
        print("4. Сравнить T1 и T2")
        print("0. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            print(f"T1: {tri1}")
            print(f"T2: {tri2}")
        elif choice == "2":
            print(f"Периметр T1: {tri1.get_perimeter()}")
            print(f"Площадь T1: {tri1.get_area():.2f}")
        elif choice == "3":
            msg = "Существует" if tri1.is_exists() else "Не существует"
            print(f"Результат: {msg}")
        elif choice == "4":
            print(f"Равны ли треугольники?: {tri1 == tri2}")
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
