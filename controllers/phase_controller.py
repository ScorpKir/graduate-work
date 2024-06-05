"""
Контроллер получения фазовой траектории дифференциального уравнения
в зависимости от параметра.

Автор: Петряшев К. С.
"""

from typing import Final

import numpy as np
from models.ode_storage import equation
from models.runge_kutta import runge_kutta, is_cycle


# Константы для поиска циклов
STEP: Final = 0.004
COUNT_BATCHES: Final = 4


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
        np.linspace(0, 4, 100),
        **kwargs
    )


def __process_one_batch(batch: list, start_x: float, **kwargs: dict) -> list:
    results = []
    for coordinate in batch:
        result = is_cycle([start_x, coordinate], equation, **kwargs)
        if result['result']:
            result.pop('result')
            results.append(result)
    return results


def find_cycles_in_phase_field(
    x0: float,
    y_min: float, 
    y_max: float,
    **kwargs
) -> list[dict]:
    """
    Поиск циклов в фазовом поле для дифференциального уравнения
    по коэффициентам и начальной точке.

    :param x0: Начальное значение x(0).
    :param y_min: Минимальное значение для x'(0).
    :param y_max: Максимальное значение для x'(0).
    :param kwargs: Коэффициенты уравнения.

    :return: Массив из объектов вида:
    
    {
        # Массив описывающий фазовую траекторию
        'trajectory': [
            [0, 0.01],
            [0, 0.02],
            [0, 0.03],
            ...
            [0, 1]
        ],
        # Начальные условия порождающие цикл
        'start_point': [0, 0]
    }
    """
    # Создаём набор значений x'(0) в рамках переданного диопазона с
    # шагом, заданным в константе.
    y0 = np.arange(
        y_min,
        y_max,
        STEP
    )

    # Здесь будут храниться начальные условия, порождающие цикл
    # а также сами траектории, являющиеся циклом
    results = []
    for value in y0:
        result = is_cycle(np.array([x0, value]), equation, **kwargs)
        if result['result']:
            result.pop('result')
            results.append(result)
    return results
