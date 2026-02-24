"""
Модуль для реализации множества символов переменной мощности (Задание 1).
"""

from typing import List, Optional, Any


class CharSet:
    """Класс, реализующий множество символов на базе списка."""

    def __init__(self, initial_chars: Optional[List[str]] = None) -> None:
        """
        Инициализация множества.

        :param initial_chars: Список символов для начальной инициализации.
        """
        self._elements: List[str] = []
        if initial_chars is not None:
            for char in initial_chars:
                self.add(char)

    @property
    def elements(self) -> List[str]:
        """Свойство для получения копии списка элементов множества."""
        return self._elements.copy()

    @elements.setter
    def elements(self, new_elements: List[str]) -> None:
        """Сеттер для полной перезаписи элементов множества."""
        self._elements.clear()
        for char in new_elements:
            self.add(char)

    def add(self, char: str) -> None:
        """Добавляет символ в множество, если его там нет."""
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Элемент должен быть одиночным символом.")
        if char not in self._elements:
            self._elements.append(char)

    def remove(self, char: str) -> None:
        """Удаляет символ из множества. Ничего не делает, если его нет."""
        if char in self._elements:
            self._elements.remove(char)

    def contains(self, char: str) -> bool:
        """Проверяет, принадлежит ли символ множеству."""
        return char in self._elements

    def intersect(self, other: 'CharSet') -> 'CharSet':
        """
        Возвращает новое множество, пересечение текущего и другого.
        """
        result = CharSet()
        for char in self._elements:
            if other.contains(char):
                result.add(char)
        return result

    def display(self) -> None:
        """Выводит элементы множества на консоль."""
        print(f"Элементы множества: {self}")

    def __str__(self) -> str:
        """Строковое представление множества."""
        if not self._elements:
            return "{}"
        return f"{{{', '.join(self._elements)}}}"

    def __eq__(self, other: Any) -> bool:
        """Сравнивает два множества на равенство (порядок не важен)."""
        if not isinstance(other, CharSet):
            return NotImplemented
        # Множества равны, если их отсортированные списки равны
        return sorted(self._elements) == sorted(other.elements)


def main() -> None:
    """Главная функция для демонстрации Задания 1."""
    print("--- Задание 1 ---")
    set1 = CharSet(['a', 'b', 'c', 'd', 'a'])  # 'a' добавится один раз
    set2 = CharSet(['c', 'd', 'e', 'f'])

    print("Множество 1:")
    set1.display()
    print("Множество 2:")
    set2.display()

    print(f"Принадлежит ли 'b' множеству 1? {set1.contains('b')}")
    print(f"Принадлежит ли 'z' множеству 1? {set1.contains('z')}")

    set1.remove('b')
    print(f"Множество 1 после удаления 'b': {set1}")

    set3 = set1.intersect(set2)
    print(f"Пересечение множества 1 и 2: {set3}")

    set4 = CharSet(['d', 'c', 'a'])
    print(f"Равны ли set1 и set4? {set1 == set4}")


if __name__ == "__main__":
    main()
