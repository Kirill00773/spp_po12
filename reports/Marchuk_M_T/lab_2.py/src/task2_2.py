"""
Модуль для моделирования системы 'Факультатив'.
Включает Студентов, Преподавателей, Курсы и Архив оценок.
"""


class Course:
    """Класс для представления учебного курса."""

    def __init__(self, title):
        """Инициализация курса."""
        self.title = title
        self.students = []

    def __str__(self):
        """Строковое представление курса."""
        return f"Курс: {self.title} (Записано студентов: {len(self.students)})"


class Student:
    """Класс для представления студента."""

    def __init__(self, name):
        """Инициализация студента."""
        self.name = name

    def __str__(self):
        """Строковое представление студента."""
        return f"Студент: {self.name}"


class Teacher:
    """Класс для представления преподавателя."""

    def __init__(self, name):
        """Инициализация преподавателя."""
        self.name = name

    def announce_course(self, title):
        """Объявляет о начале записи на курс."""
        print(f"[Преподаватель {self.name}]: Открыта запись на курс '{title}'")
        return Course(title)

    def set_grade(self, student, course, value, archive_obj):
        """Выставляет оценку студенту и сохраняет в архив."""
        print(f"[Преподаватель {self.name}]: Выставлена оценка {value} студенту {student.name}")
        archive_obj.save_record(student.name, course.title, value)


class Archive:
    """Класс для хранения истории оценок."""

    def __init__(self):
        """Инициализация пустого архива."""
        self.records = []

    def save_record(self, student_name, course_title, grade):
        """Сохраняет запись об оценке."""
        self.records.append({
            "student": student_name,
            "course": course_title,
            "grade": grade
        })

    def show_all(self):
        """Выводит все записи архива на экран."""
        print("\n--- АРХИВ ОЦЕНОК ---")
        if not self.records:
            print("Записей нет.")
        for record in self.records:
            print(f"Студент: {record['student']} | Курс: {record['course']} | Оценка: {record['grade']}")


def main():
    """Основная логика демонстрации системы."""
    print("--- Система Факультатив ---")
    my_archive = Archive()
    teacher_obj = Teacher("Иванов И.И.")
    stud1 = Student("Алексей Крощенко")
    stud2 = Student("Мария Петрова")

    course_python = teacher_obj.announce_course("Программирование на Python")

    while True:
        print("\nМеню системы:")
        print("1. Записать студента 1 на курс")
        print("2. Записать студента 2 на курс")
        print("3. Выставить оценку студенту 1")
        print("4. Выставить оценку студенту 2")
        print("5. Посмотреть архив")
        print("0. Выход")

        choice = input("Действие: ")

        if choice == "1":
            course_python.students.append(stud1)
            print(f"{stud1.name} записан.")
        elif choice == "2":
            course_python.students.append(stud2)
            print(f"{stud2.name} записан.")
        elif choice == "3":
            grade_val = input("Введите оценку для Алексея: ")
            teacher_obj.set_grade(stud1, course_python, grade_val, my_archive)
        elif choice == "4":
            grade_val = input("Введите оценку для Марии: ")
            teacher_obj.set_grade(stud2, course_python, grade_val, my_archive)
        elif choice == "5":
            my_archive.show_all()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
