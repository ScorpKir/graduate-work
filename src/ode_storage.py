"""Хранилище дифференциальных уравнений"""

__author__ = 'Kirill Petryashev'

import numpy as np


def equation(x0: np.ndarray, t: np.ndarray, **kwargs) -> np.ndarray:
    """
    Функция задает дифференциальное уравнение

    x'' - mu * x' + x + a1 * x^2 + a2 * x * x' + a3 * x'^2 = 0

    В виде системы

    x' = y
    y' = mu * y - x - a1 * x^2 - a2 * x * y + a3 * y^2

    :param x0: Массив начальных условий x(0) и x'(0)
    :param t: Массив значений t
    :param args: Значения дифференциального уравнения

    :returns: Значения x' и x'' при заданных начальных условиях
    """
    x, y = x0
    mu = kwargs['mu']
    a1 = kwargs['a1']
    a2 = kwargs['a2']
    a3 = kwargs['a3']

    return np.array([
        y,
        mu * y - x - a1 * x ** 2 - a2 * x * y + a3 * y ** 2
    ])
