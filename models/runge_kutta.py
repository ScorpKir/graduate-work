"""
    Реализация метода Рунге-Кутты для 
    численного решения дифференциального уравнения

    Автор: Петряшев К. С.
"""
from typing import Final

import numpy as np

# Шаг и допустимая погрешность для определения цикла.
HOP: Final = 0.001
TOLERANCE: Final = 0.0001


def runge_kutta(
    y0: np.ndarray,
    ode: callable,
    time_: np.array,
    **kwargs
) -> np.array:
    '''
    Функция численно находит решение для краевой задачи
    дифференциального уравнения методом Рунге Кутты

    :param y0: Массив начальных условий y(0) и y'(0).
    :param ode: Функция, задающая дифференциальное уравнение.
    :param time_: Массив значений переменной, задающей время.
    :param kwargs: Параметры дифференциального уравнения.

    :return: Массив, содержащий точки, определяющие траекторию.
    '''
    # Вычисляем количество точек
    n = len(time_)

    # Задаем массив, в котором будет храниться результат
    sol = np.zeros((n, len(y0)))

    # Кладем первые значения в массив результата
    sol[0] = y0

    # Запускаем основной цикл
    for i in range(n - 1):
        # Вычисляем шаг
        hop = time_[i + 1] - time_[i]

        with np.errstate(over='raise', invalid='raise'):
            try:
                # Вычисляем значения k1, k2, k3, k4
                k1 = ode(sol[i], time_[i], **kwargs)
                k2 = ode(sol[i] + k1 * hop / 2., time_[i] + hop / 2., **kwargs)
                k3 = ode(sol[i] + k2 * hop / 2., time_[i] + hop / 2., **kwargs)
                k4 = ode(sol[i] + k3 * hop, time_[i] + hop, **kwargs)
            except FloatingPointError:
                return sol

            # Находим значения y и y' на текущем шаге
            sol[i + 1] = sol[i] + (hop / 6.) * (k1 + 2 * k2 + 2 * k3 + k4)

        if sol[i + 1, 0] == np.nan or sol[i + 1, 1] == np.nan:
            return sol[:i + 1]
    return sol


def __is_vertical_axe_intersected(
    current_point: np.array,
    previous_point: np.array,
    start_point: np.array
) -> bool:
    """
    Функция определяет, пересекли ли мы вертикальную ось.

    :param current_point: Текущая точка фазовой траектории.
    :param previous_point: Предыдущая точка фазовой траектории.
    :param start_point: Точка начала фазовой траектории.
    """
    vertical_axes_intersection_criterios = [
        current_point[0] > start_point[0] \
            and previous_point[0] < start_point[0],
        current_point[0] < start_point[0] \
            and previous_point[0] > start_point[0],
    ]
    return any(vertical_axes_intersection_criterios)


def is_cycle(
    start_point: np.array,
    ode: callable,
    **kwargs
) -> dict:
    """
    Функция численно находит решение для краевой задачи
    дифференциального уравнения методом Рунге Кутты
    и определяет, является ли решение циклом.

    :param start_point: Точка, с которой необходимо начать
        построение траектории.
    :param ode: функция, задающая дифференциальное уравнение.
    :param kwargs: Параметры дифференциального уравнения.

    :return: Словарь вида:

    {
        # Результат, является ли траектория циклом
        'result': False,

        # Массив описывающий фазовую траекторию
        'trajectory': [
            [0, 0.01],
            [0, 0.02],
            [0, 0.03],
            ...
            [0, 1]
        ]
    }
    """
    # Задаём шаг и допустимую погрешность
    hop, tolerance = 1e-2, 4e-4

    # Инициализируем траекторию, начиная со стартовой точки
    current_point = np.copy(start_point)
    points = np.array([current_point])

    # Задаём переменную времени
    time_ = 0.0

    # Счётчик пересечений вертикальной оси
    count_x_intersections = 0

    # Переменные для вычисления погрешностей
    sum_differences = 0.0
    count_hops = 0

    # Основной цикл Рунге-Кутты
    while True:
        with np.errstate(over='raise', invalid='raise'):
            try:
                time_ += hop
                k1 = ode(current_point, time_, **kwargs)
                k2 = ode(
                    current_point + k1 * hop / 2.,
                    time_ + hop / 2.,
                    **kwargs
                )
                k3 = ode(
                    current_point + k2 * hop / 2.,
                    time_ + hop / 2.,
                    **kwargs
                )
                k4 = ode(current_point + k3 * hop, time_ + hop, **kwargs)
            except FloatingPointError:
                return {
                    'start_point': start_point,
                    'result': False,
                    'trajectory': points
                }

        # Находим разницу между предыдущей и текущей точки
        difference = (hop / 6.) * (k1 + 2 * k2 + 2 * k3 + k4)

        # Находим текущее значение погрешности
        # Исходя из среднего значения разницы по всем итерациям
        sum_differences += abs(difference[1])
        count_hops += 1
        tolerance = sum_differences / count_hops

        # Находим значения y и y' на текущем шаге
        current_point += difference
        points = np.vstack((points, np.array([current_point])))

        # Если мы пересекаем вертикальную ось - регистрируем это.
        if __is_vertical_axe_intersected(
            current_point,
            points[-2],
            start_point
        ):
            count_x_intersections += 1

        # Формируем условия для положительного выхода из цикла
        # 1) Вертикальная ось была пересечена
        positive_conditions = [
            count_x_intersections >= 1,
            abs(start_point[0] - current_point[0]) <= tolerance,
            abs(start_point[1] - current_point[1]) <= tolerance
        ]

        # Если соблюдены условия для положительного выхода
        #   Возвращаем положительный результат
        if all(positive_conditions):
            return {
                'start_point': start_point,
                'result': True,
                'trajectory': points
            }

        # Если мы пересекли вертикальную ось два или более раз
        # Находимся далеко от неё и до сих пор не вышли из цикла - выходим
        negative_conditions = (
            count_x_intersections >= 2,
            current_point[0] - start_point[0] >= tolerance
        )
        if all(negative_conditions):
            return {
                'start_point': start_point,
                'result': False,
                'trajectory': points
            }
