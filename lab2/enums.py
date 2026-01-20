from enum import StrEnum, auto


class TulipTypeEnum(StrEnum):
    SINGLE_EARLY = "Простые ранние"
    DOUBLE_LATE = "Махровые поздние"
    FRINGED = "Бахромчатые"
    PARROT = "Попугайные"

class FlowerColorEnum(StrEnum):
    RED = "Красный"
    BLUE = "Синий"
    YELLOW = "Желтый"
    GREEN = "Зеленый"
    PURPLE = "Фиолетовый"
    ORANGE = "Оранжевый"