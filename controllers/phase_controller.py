"""
Контроллер получения фазовой траектории дифференциального уравнения
в зависимости от параметра.

Автор: Петряшев К. С.
"""

import numpy as np
from models.ode_storage import equation
from models.runge_kutta import runge_kutta


def get_solution_by_initial_conditions(x0: np.ndarray, **kwargs) -> np.ndarray:
    """
        Получение решение дифференциального уравнения по начальным условиям
        и коэффициентам.

        :param x0: Начальные условия задачи.
        :param kwargs: Коэффициенты уравнения.

        :return: Массив значений x и x' решения уравнения.
    """
    return runge_kutta(
        x0,
        equation,
        np.linspace(0, 1, 100),
        **kwargs
    )
