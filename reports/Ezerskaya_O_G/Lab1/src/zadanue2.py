"""Модуль для проверки правильности скобочной последовательности."""


def is_valid(s):
    """
    Проверяет, является ли скобочная последовательность правильной.

    Аргументы:
        s (str): Строка, содержащая скобки '(', ')', '{', '}', '[', ']'

    Возвращает:
        bool: True если последовательность правильная, иначе False
    """
    stack = []
    brackets = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in brackets.values():
            stack.append(char)
        elif char in brackets:
            if not stack or stack.pop() != brackets[char]:
                return False

    return len(stack) == 0


test_cases = ["()", "()[]{}", "(]", "([])"]

for test in test_cases:
    print(f'Input: s = "{test}"')
    print(f"Output: {str(is_valid(test)).lower()}")
    print()
