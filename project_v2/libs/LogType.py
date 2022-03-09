from enum import Enum


class LogType(Enum):
    INFO = 1 # Вывод в визуальную форму
    ERROR = 2 # Ошибка для вывода в визуальную форму
    DEBUG = 3 # Вывод только в файл
    WARNING = 4 # Для отображения желтым :D