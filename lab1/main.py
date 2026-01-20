import random
from datetime import date

from lab1.constants import (
    FACULTIES, GROUPS, FIRST_NAMES, LAST_NAMES, 
    PATRONYMICS, ADDRESSES, PHONES, BIRTH_YEARS
)
from lab1.model import Student


def create_students_array(count: int = 15) -> list[Student]:
    """Создать массив объектов студентов"""
    students = []
    
    for i in range(count):
        birth_year = random.choice(BIRTH_YEARS)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        
        student = Student(
            id=i + 1,
            last_name=random.choice(LAST_NAMES),
            first_name=random.choice(FIRST_NAMES),
            patronymic=random.choice(PATRONYMICS),
            birth_date=date(birth_year, birth_month, birth_day),
            address=random.choice(ADDRESSES),
            phone=random.choice(PHONES),
            faculty=random.choice(FACULTIES),
            course=random.randint(1, 4),
            group=random.choice(GROUPS)
        )
        students.append(student)
    
    return students


def print_students_by_faculty(students: list[Student], faculty: str):
    """a) Вывести список студентов заданного факультета"""
    print(f"\n{'='*80}")
    print(f"Список студентов факультета '{faculty}':")
    print(f"{'='*80}")
    
    found = False
    for student in students:
        if student.getFaculty() == faculty:
            print(student)
            found = True
    
    if not found:
        print(f"Студенты факультета '{faculty}' не найдены.")


def print_students_by_faculty_and_course(students: list[Student]):
    """b) Вывести списки студентов для каждого факультета и курса"""
    print(f"\n{'='*80}")
    print("Списки студентов для каждого факультета и курса:")
    print(f"{'='*80}")
    
    # Группируем студентов по факультету и курсу
    grouped = {}
    for student in students:
        key = (student.getFaculty(), student.getCourse())
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(student)
    
    # Выводим отсортированные списки
    for (faculty, course) in sorted(grouped.keys()):
        print(f"\n--- Факультет: {faculty}, Курс: {course} ---")
        for student in grouped[(faculty, course)]:
            print(student)


def print_students_born_after_year(students: list[Student], year: int):
    """c) Вывести список студентов, родившихся после заданного года"""
    print(f"\n{'='*80}")
    print(f"Список студентов, родившихся после {year} года:")
    print(f"{'='*80}")
    
    found = False
    for student in students:
        if student.getBirth_date().year > year:
            print(student)
            found = True
    
    if not found:
        print(f"Студенты, родившиеся после {year} года, не найдены.")


def print_students_by_group(students: list[Student], group: str):
    """d) Вывести список учебной группы"""
    print(f"\n{'='*80}")
    print(f"Список студентов группы '{group}':")
    print(f"{'='*80}")
    
    found = False
    for student in students:
        if student.getGroup() == group:
            print(student)
            found = True
    
    if not found:
        print(f"Студенты группы '{group}' не найдены.")


def main():
    # Создать массив объектов студентов
    students = create_students_array(15)
    
    # Вывести всех студентов
    print("="*80)
    print("ВСЕ СТУДЕНТЫ:")
    print("="*80)
    for student in students:
        print(student)
    
    # a) Список студентов заданного факультета
    target_faculty = random.choice(FACULTIES)
    print_students_by_faculty(students, target_faculty)
    
    # b) Списки студентов для каждого факультета и курса
    print_students_by_faculty_and_course(students)
    
    # c) Список студентов, родившихся после заданного года
    target_year = 2002
    print_students_born_after_year(students, target_year)
    
    # d) Список учебной группы
    target_group = random.choice(GROUPS)
    print_students_by_group(students, target_group)


if __name__ == "__main__":
    main()
