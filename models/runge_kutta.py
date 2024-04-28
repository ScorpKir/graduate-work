"""
    Реализация метода Рунге-Кутты для 
    численного решения дифференциального уравнения

    Автор: Петряшев К. С.
"""

import numpy as np


def runge_kutta(y0: np.ndarray, f: callable, t, **kwargs) -> np.ndarray:
    '''
        Функция численно находит решение для краевой задачи
        дифференциального уравнения методом Рунге Кутты

        :param y0: массив начальных условий y(0) и y'(0)
        :param f: функция, задающая дифференциальное уравнение
        :param t: массив значений переменной t
        :param args: параметры дифференциального уравнения

        :return: массив, содержащий значения y и y'
    '''
    # Вычисляем количество точек
    n = len(t)

    # Задаем массив, в котором будет храниться результат
    sol = np.zeros((n, len(y0)))

    # Кладем первые значения в массив результата
    sol[0] = y0

    # Запускаем основной цикл
    for i in range(n - 1):
        # Вычисляем шаг
        hop = t[i + 1] - t[i]

        with np.errstate(over='raise', invalid='raise'):
            try:
                # Вычисляем значения k1, k2, k3, k4
                k1 = f(sol[i], t[i], **kwargs)
                k2 = f(sol[i] + k1 * hop / 2., t[i] + hop / 2., **kwargs)
                k3 = f(sol[i] + k2 * hop / 2., t[i] + hop / 2., **kwargs)
                k4 = f(sol[i] + k3 * hop, t[i] + hop, **kwargs)
            except FloatingPointError as ex:
                raise ValueError(
                    'В процессе вычисления достигнута бесконечность'
                ) from ex

            # Находим значения y и y' на текущем шаге
            sol[i + 1] = sol[i] + (hop / 6.) * (k1 + 2 * k2 + 2 * k3 + k4)

        if sol[i + 1, 0] == np.nan or sol[i + 1, 1] == np.nan:
            return sol[:i + 1]
    return sol
