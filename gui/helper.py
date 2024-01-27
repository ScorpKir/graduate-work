"""Вспомогательные модули для использования на интерфейсе"""

__author__ = 'Kirill Petryashev'

from enum import Enum


class EquationParameters(Enum):
    """
    Параметры дифференциального уравнения по умолчанию

    TODO: Подумать куда лучше положить это перечисление
    """
    DEFAULT_X_VALUE: float = 0.0
    DEFAULT_X_PRIME_VALUE: float = 0.01
    DEFAULT_MU_VALUE: float = 0.5
    DEFAULT_A1_VALUE: float = 0.0
    DEFAULT_A2_VALUE: float = 0.0
    DEFAULT_A3_VALUE: float = 0.0

def validate_float_input(value: str) -> bool:
    """
        Функция проверяет возможность конвертирования
        строки в число с плавающей точкой

        :param val: Текстовое значение для валидации
        :return: Логическое значение, обозначающее валидность строки
    """
    if not value in (None, '', '-'):
        try:
            float(value)
        except ValueError:
            return False
    return True
