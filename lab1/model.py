from datetime import datetime, date
from typing import Optional


class Student:
    def __init__(
        self,
        id: int,
        last_name: str,
        first_name: str,
        faculty: str,
        course: int,
        group: str,
        patronymic: Optional[str] = "",
        birth_date: Optional[date] = None,
        address: Optional[str] = "",
        phone: Optional[str] = "",
    ):
        """Основной конструктор с обязательными и опциональными параметрами"""
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic if patronymic else ""
        self.birth_date = birth_date if birth_date else date.today()
        self.address = address if address else ""
        self.phone = phone if phone else ""
        self.faculty = faculty
        self.course = course
        self.group = group

    @classmethod
    def create_minimal(
        cls,
        id: int,
        last_name: str,
        first_name: str,
        faculty: str,
        course: int,
        group: str,
    ):
        """Альтернативный конструктор с минимальными параметрами"""
        return cls(
            id=id,
            last_name=last_name,
            first_name=first_name,
            faculty=faculty,
            course=course,
            group=group
        )

    @classmethod
    def create_copy(cls, other: 'Student'):
        """Альтернативный конструктор копирования"""
        return cls(
            id=other.id,
            last_name=other.last_name,
            first_name=other.first_name,
            patronymic=other.patronymic,
            birth_date=other.birth_date,
            address=other.address,
            phone=other.phone,
            faculty=other.faculty,
            course=other.course,
            group=other.group
        )

    # Геттеры (getters)
    def getId(self) -> int:
        return self.id

    def getLast_name(self) -> str:
        return self.last_name

    def getFirst_name(self) -> str:
        return self.first_name

    def getPatronymic(self) -> str:
        return self.patronymic

    def getBirth_date(self) -> date:
        return self.birth_date

    def getAddress(self) -> str:
        return self.address

    def getPhone(self) -> str:
        return self.phone

    def getFaculty(self) -> str:
        return self.faculty

    def getCourse(self) -> int:
        return self.course

    def getGroup(self) -> str:
        return self.group

    # Сеттеры (setters)
    def setId(self, id: int):
        self.id = id

    def setLast_name(self, last_name: str):
        self.last_name = last_name

    def setFirst_name(self, first_name: str):
        self.first_name = first_name

    def setPatronymic(self, patronymic: str):
        self.patronymic = patronymic

    def setBirth_date(self, birth_date: date):
        self.birth_date = birth_date

    def setAddress(self, address: str):
        self.address = address

    def setPhone(self, phone: str):
        self.phone = phone

    def setFaculty(self, faculty: str):
        self.faculty = faculty

    def setCourse(self, course: int):
        self.course = course

    def setGroup(self, group: str):
        self.group = group

    # Переопределение toString()
    def __str__(self):
        return (
            f"Студент [ID: {self.id}, "
            f"ФИО: {self.last_name} {self.first_name} {self.patronymic}, "
            f"Дата рождения: {self.birth_date.strftime('%d.%m.%Y')}, "
            f"Адрес: {self.address}, "
            f"Телефон: {self.phone}, "
            f"Факультет: {self.faculty}, "
            f"Курс: {self.course}, "
            f"Группа: {self.group}]"
        )

    def __repr__(self):
        return self.__str__()

    # Переопределение hashCode()
    def __hash__(self):
        return hash((
            self.id,
            self.last_name,
            self.first_name,
            self.patronymic,
            self.birth_date,
            self.faculty,
            self.course,
            self.group
        ))

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return (
            self.id == other.id and
            self.last_name == other.last_name and
            self.first_name == other.first_name and
            self.patronymic == other.patronymic and
            self.birth_date == other.birth_date and
            self.faculty == other.faculty and
            self.course == other.course and
            self.group == other.group
        )
